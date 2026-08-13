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
short_description: Download files from Hugging Face Hub
description:
    - >-
      Downloads models, datasets, or specific files from Hugging Face Hub
      using the huggingface_hub library, supporting authentication tokens,
      revisions, subfolders, and force-download controls.
options:
    repo_id:
        description:
            - >-
              The Hugging Face repository ID
              (e.g., 'TheBloke/Llama-2-7B-Chat-GGUF').
        type: str
        required: true
    filename:
        description:
            - Name of the specific file to download from the repository.
        type: str
        required: true
    local_dir:
        description:
            - Local folder where the file should be downloaded.
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
            - >-
              An optional revision id which can be a branch name, a tag, or
              a commit hash.
        type: str
    token:
        description:
            - >-
              Hugging Face API token for authenticating private or gated
              repositories.
        type: str
    force_download:
        description:
            - Whether to force downloading the file even if it exists locally.
        type: bool
        default: false
    local_files_only:
        description:
            - >-
              Whether to only look at local files and avoid
              checking/downloading updates.
        type: bool
        default: false
'''

EXAMPLES = r'''
- name: Download a GGUF model file
  dettonville.llm.hf_download:
    repo_id: "TheBloke/Llama-2-7B-Chat-GGUF"
    filename: "llama-2-7b-chat.Q4_K_M.gguf"
    local_dir: "/opt/llm/models"

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
path:
    description: Path to the downloaded file.
    returned: success
    type: str
changed:
    description: Whether a download actually took place.
    returned: always
    type: bool
'''

import os

# noinspection PyPackageRequirements
from ansible.module_utils.basic import AnsibleModule

try:
    # noinspection PyPackageRequirements
    from huggingface_hub import hf_hub_download

    HAS_HF_HUB = True
except ImportError:
    hf_hub_download = None
    HAS_HF_HUB = False


def run_module():
    module_args = dict(
        repo_id=dict(type='str', required=True),
        filename=dict(type='str', required=True),
        local_dir=dict(type='str', required=True),
        repo_type=dict(
            type='str', default='model', choices=['model', 'dataset', 'space']
        ),
        subfolder=dict(type='str', required=False),
        revision=dict(type='str', required=False),
        token=dict(type='str', required=False, no_log=True),
        force_download=dict(type='bool', default=False),
        local_files_only=dict(type='bool', default=False),
    )

    result = dict(changed=False, path='')

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if not HAS_HF_HUB:
        module.fail_json(
            msg='The python library "huggingface_hub" is required. '
            'Please install it via pip.'
        )

    repo_id = module.params['repo_id']
    filename = module.params['filename']
    local_dir = module.params['local_dir']
    repo_type = module.params['repo_type']
    subfolder = module.params.get('subfolder')
    revision = module.params.get('revision')
    token = module.params.get('token')
    force_download = module.params['force_download']
    local_files_only = module.params['local_files_only']

    # Resolve target path relative to subfolder if provided
    if subfolder:
        target_file_path = os.path.join(local_dir, subfolder, filename)
    else:
        target_file_path = os.path.join(local_dir, filename)

    file_exists = os.path.exists(target_file_path)

    if module.check_mode:
        module.exit_json(
            changed=(not file_exists or force_download), path=target_file_path
        )

    try:
        # Build kwargs dynamically for optional parameters
        download_kwargs = dict(
            repo_id=repo_id,
            filename=filename,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            repo_type=repo_type,
            force_download=force_download,
            local_files_only=local_files_only,
        )

        if subfolder is not None:
            download_kwargs['subfolder'] = subfolder
        if revision is not None:
            download_kwargs['revision'] = revision
        if token is not None:
            download_kwargs['token'] = token

        downloaded_path = hf_hub_download(**download_kwargs)

        result['changed'] = not file_exists or force_download
        result['path'] = downloaded_path
    except Exception as e:
        module.fail_json(
            msg=f"Failed to download file from Hugging Face: {str(e)}"
        )

    module.exit_json(**result)


py_imports = ['huggingface_hub']


def main():
    run_module()


if __name__ == '__main__':
    main()
