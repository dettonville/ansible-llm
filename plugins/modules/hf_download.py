#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: hf_download
version_added: "2.20.0"
author:
    - "Lee Johnson (@lj020326)"
short_description: >-
    Download files or repositories dynamically from Hugging Face Hub.
description:
    - >-
      Downloads models, datasets, or specific files from Hugging Face Hub
      using the huggingface_hub library. Features dynamic filename resolution,
      etag/hash checking for updates, authentication tokens, revisions,
      subfolders, force-download controls, file permission adjustments, and
      idempotent local cache management.
attributes:
    check_mode:
        support: full
        description: >-
            Supports check mode to predict changes without downloading files.
    diff_mode:
        support: none
        description: Does not support diff mode.
    platform:
        support: full
        platforms: posix
        description: Target system must be POSIX-compliant.
    safe_file_operations:
        support: full
        description: >-
            Uses Ansible's atomic file creation and attributes handlers.
    vault:
        support: none
        description: Does not directly decrypt vault-encrypted payload files.
options:
    repo_id:
        description:
            - >-
              The Hugging Face repository ID
              (e.g., 'unsloth/Qwen3.8-27B-GGUF').
        type: str
        required: true
    filename:
        description:
            - Name of the specific file to download. If omitted, the module can
              resolve filenames matching standard patterns or download all
              repo files.
        type: str
        required: false
    quant_preference:
        description:
            - Target quantization pattern (e.g., 'Q4_K_M', 'NVFP4') to
              automatically select a matching file if `filename` is omitted.
        type: str
        required: false
    local_dir:
        description:
            - Local folder where the file(s) should be downloaded.
        type: str
        required: true
    repo_type:
        description:
            - Type of repository ('model', 'dataset', 'space').
        type: str
        choices: ['model', 'dataset', 'space']
        default: 'model'
    subfolder:
        description:
            - Subfolder inside the repository where the file is located.
        type: str
    revision:
        description:
            - An optional revision ID (branch name, tag, or commit hash).
        type: str
    token:
        description:
            - Hugging Face API token for authenticating gated or private repos.
        type: str
    force_download:
        description:
            - Whether to force downloading files even if they already match
              remote checksums.
        type: bool
        default: false
    local_files_only:
        description:
            - Whether to only inspect local files without checking HF Hub
              for remote updates.
        type: bool
        default: false
    local_dir_use_symlinks:
        description:
            - Whether to use symlinks when downloading files locally.
            - Auto-detects based on system capabilities by default.
            - >-
                Option deprecated in recent huggingface_hub versions;
                kept for signature backward compatibility.
        type: raw
        default: 'auto'
extends_documentation_fragment:
    - ansible.builtin.files
'''

EXAMPLES = r'''
- name: Ensure LLM models are present and up to date
  dettonville.llm.hf_download:
    repo_id: "unsloth/Qwen3.8-27B-NVFP4"
    quant_preference: "UD-Q4_K_M"
    local_dir: "/opt/llm/models"
    token: "{{ lookup('env', 'HF_TOKEN') }}"
    owner: "vllm"
    group: "vllm"
  register: model_download_results

- name: Download a GGUF model file
  dettonville.llm.hf_download:
    repo_id: "TheBloke/Llama-2-7B-Chat-GGUF"
    filename: "llama-2-7b-chat.Q4_K_M.gguf"
    local_dir: "/opt/llm/models"
    owner: "vllm"
    group: "vllm"

- name: Download a gated model file using authentication token
  dettonville.llm.hf_download:
    repo_id: "meta-llama/Meta-Llama-3-8B-Instruct"
    filename: "model.safetensors"
    local_dir: "/opt/llm/models/llama3"
    token: "{{ lookup('env', 'HF_TOKEN') }}"

- name: Download a file from a specific revision/branch
  dettonville.llm.hf_download:
    repo_id: "mistralai/Mistral-7B-v0.1"
    filename: "config.json"
    local_dir: "/opt/llm/models/mistral"
    revision: "refs/pr/1"

- name: Download a file located within a repository subfolder
  dettonville.llm.hf_download:
    repo_id: "unsloth/llama-3-8b-Instruct-bnb-4bit"
    filename: "tokenizer.json"
    local_dir: "/opt/llm/models/unsloth"
    subfolder: "tokenizers"

- name: Force re-download a file ignoring local cache
  dettonville.llm.hf_download:
    repo_id: "TheBloke/Llama-2-7B-Chat-GGUF"
    filename: "llama-2-7b-chat.Q4_K_M.gguf"
    local_dir: "/opt/llm/models"
    force_download: true

- name: Restrict downloads to local cache only
  dettonville.llm.hf_download:
    repo_id: "TheBloke/Llama-2-7B-Chat-GGUF"
    filename: "llama-2-7b-chat.Q4_K_M.gguf"
    local_dir: "/opt/llm/models"
    local_files_only: true
'''

RETURN = r'''
downloaded_files:
    description: List of files downloaded or verified.
    returned: success
    type: list
resolved_filename:
    description: Primary resolved filename that was downloaded.
    returned: success
    type: str
changed:
    description: Whether any downloads or file updates took place.
    returned: always
    type: bool
'''

import os
import re

# noinspection PyPackageRequirements
from ansible.module_utils.basic import AnsibleModule

try:
    # noinspection PyPackageRequirements
    from huggingface_hub import HfApi, hf_hub_download

    HAS_HF_HUB = True
except ImportError:
    HfApi = None
    hf_hub_download = None
    HAS_HF_HUB = False


def resolve_target_file(
    api, repo_id, repo_type, revision, token, quant_preference=None
):
    """Dynamically find a matching file in the repo based on preferences or
    default patterns."""
    repo_files = api.list_repo_files(
        repo_id=repo_id, repo_type=repo_type, revision=revision, token=token
    )

    if quant_preference:
        pattern = re.compile(re.escape(quant_preference), re.IGNORECASE)
        matching_files = [f for f in repo_files if pattern.search(f)]
        if matching_files:
            return matching_files[0]

    # Fallback to first .gguf or standard main weight file if no spec given
    gguf_files = [f for f in repo_files if f.endswith('.gguf')]
    if gguf_files:
        return gguf_files[0]

    safetensor_files = [f for f in repo_files if f.endswith('.safetensors')]
    if safetensor_files:
        return safetensor_files[0]

    if repo_files:
        return repo_files[0]

    raise ValueError(f"No valid files found in repository '{repo_id}'")


def run_module():
    module_args = dict(
        repo_id=dict(type="str", required=True),
        filename=dict(type="str", required=False, default=None),
        quant_preference=dict(type="str", required=False, default=None),
        local_dir=dict(type="str", required=True),
        repo_type=dict(
            type="str", default="model", choices=["model", "dataset", "space"]
        ),
        subfolder=dict(type="str", required=False),
        revision=dict(type="str", required=False),
        token=dict(type="str", required=False, no_log=True),
        force_download=dict(type="bool", default=False),
        local_files_only=dict(type="bool", default=False),
        local_dir_use_symlinks=dict(
            type="raw", required=False, default="auto"
        ),
        owner=dict(type="str", required=False),
        group=dict(type="str", required=False),
        mode=dict(type="raw", required=False),
    )

    result = dict(changed=False, downloaded_files=[], resolved_filename="")

    module = AnsibleModule(
        argument_spec=module_args,
        add_file_common_args=True,
        supports_check_mode=True,
    )

    if not HAS_HF_HUB:
        module.fail_json(
            msg='The python library "huggingface_hub" is required.'
        )

    repo_id = module.params['repo_id']
    filename = module.params['filename']
    quant_preference = module.params['quant_preference']
    local_dir = module.params['local_dir']
    repo_type = module.params['repo_type']
    subfolder = module.params.get('subfolder')
    revision = module.params.get('revision')
    token = module.params.get('token')
    force_download = module.params['force_download']
    local_files_only = module.params['local_files_only']
    local_dir_use_symlinks = module.params['local_dir_use_symlinks']
    api = HfApi(token=token)

    # Resolve target filename if not explicitly supplied
    if not filename:
        filename = resolve_target_file(
            api=api,
            repo_id=repo_id,
            repo_type=repo_type,
            revision=revision,
            token=token,
            quant_preference=quant_preference,
        )

    result['resolved_filename'] = filename
    target_path = (
        os.path.join(local_dir, subfolder, filename)
        if subfolder
        else os.path.join(local_dir, filename)
    )

    # Check existing file presence
    file_exists = os.path.exists(target_path)

    if module.check_mode:
        # Give the helper a real path so it populates secontext, owner, etc.
        file_args = module.load_file_common_arguments(
            module.params, path=target_path
        )
        # (or the older style below if you must stay compatible with very
        # old Ansible)
        # tmp_params = dict(module.params)
        # tmp_params['path'] = target_path
        # file_args = module.load_file_common_arguments(tmp_params)

        file_changed = module.set_fs_attributes_if_different(
            file_args, False, expand=False
        )
        result['changed'] = not file_exists or force_download or file_changed
        result['downloaded_files'] = [target_path]
        module.exit_json(**result)

    # Execute Hugging Face Download
    try:
        # Download with built-in ETag/cache verification
        download_kwargs = dict(
            repo_id=repo_id,
            filename=filename,
            local_dir=local_dir,
            repo_type=repo_type,
            force_download=force_download,
            local_files_only=local_files_only,
            local_dir_use_symlinks=local_dir_use_symlinks,
        )
        if subfolder:
            download_kwargs['subfolder'] = subfolder
        if revision:
            download_kwargs['revision'] = revision
        if token:
            download_kwargs['token'] = token

        downloaded_path = hf_hub_download(**download_kwargs)
    except Exception as e:
        module.fail_json(
            msg=f"Failed to download Hugging Face model '{repo_id}': {str(e)}"
        )

    # Apply permissions, ownership, and SELinux attributes
    try:
        file_args = module.load_file_common_arguments(
            module.params, path=downloaded_path
        )

        # Optional: only force a 'leave SELinux alone' context when the
        # user did not supply any se* parameters.  The helper already
        # built a correct secontext from those parameters.
        if not any(
            module.params.get(k)
            for k in ('seuser', 'serole', 'setype', 'selevel')
        ):
            # Keep the individual keys and the composite key consistent
            file_args['seuser'] = None
            file_args['serole'] = None
            file_args['setype'] = None
            file_args['selevel'] = None
            file_args['secontext'] = [None, None, None]
            if module.selinux_mls_enabled():
                file_args['secontext'].append(None)

        file_changed = module.set_fs_attributes_if_different(
            file_args, False, expand=False
        )

        # Determine if file changed, was newly created, or permissions updated
        result['changed'] = not file_exists or force_download or file_changed
        result['downloaded_files'] = [downloaded_path]
    except Exception as e:
        module.fail_json(
            msg=f"Failed to set file attributes/permissions on "
            f"'{downloaded_path}': {str(e)}"
        )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
