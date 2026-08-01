#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Lee Johnson (ljohnson@dettonville.com)
# MIT license (https://opensource.org/license/mit/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: ollama_api
version_added: "2.20.0"
author:
    - "Lee Johnson (@lj020326)"
short_description: Manage Ollama models and query states via API
description:
    - Manages Ollama models and checks service health using standard HTTP API endpoints.
    - Provides capabilities to list available models, check running models (ps),
      pull (download), sync, and remove models from a specified Ollama endpoint.
    - Supports API key authentication via parameter or OLLAMA_API_KEY environment variable.
options:
    url:
      description:
          - Base URL of the Ollama API service.
      aliases: ['endpoint']
      required: true
      type: str
    api_key:
      description:
        - Optional API token/key for authentication.
        - API key or user:password basic auth credential for the Ollama endpoint.
        - Can also be supplied via OLLAMA_API_KEY environment variable.
      required: false
      type: str
    api_auth_type:
      description:
        - Type of HTTP authentication header to use.
      choices: ['bearer', 'basic']
      default: 'bearer'
      required: false
      type: str
    action:
      description: Action to perform.
      choices: [ping, version, list, ps, pull, create, delete, sync]
      default: 'list'
      required: false
      type: str
    model_name:
      description: Single model name string to process.
      aliases: ['model']
      required: false
      type: str
    model_list:
      description: List of model name strings to process in batch or sync against.
      aliases: ['models']
      required: false
      type: list
      elements: str
    model_file_path:
      description: Path to model_file_path content for custom model creation.
      required: false
      type: str
    use_system_certs:
      description:
        - Whether to use the truststore library to hook Python's ssl module into the native system certificate store.
      type: bool
      default: true
      required: false
    validate_certs:
      description:
        - Whether to validate SSL certificates for HTTPS requests.
      type: bool
      default: true
      required: false
'''

EXAMPLES = r'''
- name: Check health of Ollama endpoint
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "ping"

- name: Get Ollama version
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "version"

- name: List models on Ollama endpoint
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "list"

- name: Check running models in VRAM
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "ps"

- name: Pull a model
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "pull"
    model_name: "qwen2.5-coder:7b"

- name: Remove a model
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "delete"
    model: "llama3.1:8b"
    api_key: "my_secret_key"
    api_auth_type: "bearer"

- name: Sync models on Ollama endpoint to match specified list
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "sync"
    model_list:
      - "qwen2.5-coder:7b"
      - "llama3.1:8b"
'''

RETURN = r'''
changed:
    description: Whether any modification or state change occurred.
    type: bool
    returned: always
result:
    description: The JSON response dictionary or message returned from the Ollama API or action.
    type: raw
    returned: always
base_url:
    description: The target endpoint URL used.
    type: str
    returned: always
'''

import base64
import os

from ansible.module_utils.basic import AnsibleModule

try:
    # noinspection PyUnusedImports
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    # noinspection PyUnusedImports
    import truststore

    HAS_TRUSTSTORE = True
except ImportError:
    HAS_TRUSTSTORE = False


def get_auth_headers(api_key, api_auth_type):
    headers = {'Content-Type': 'application/json'}
    if not api_key:
        return headers

    if api_auth_type == 'basic':
        if ':' in api_key:
            encoded = base64.b64encode(api_key.encode('utf-8')).decode('utf-8')
            headers['Authorization'] = f'Basic {encoded}'
        else:
            headers['Authorization'] = f'Basic {api_key}'
    else:
        headers['Authorization'] = f'Bearer {api_key}'
    return headers


def run_module():
    module_args = dict(
        url=dict(type='str', aliases=["endpoint"], required=True),
        api_key=dict(type='str', required=False, no_log=True),
        api_auth_type=dict(
            type='str', default='bearer', required=False, choices=['bearer', 'basic']
        ),
        action=dict(
            type='str',
            default='list',
            required=False,
            choices=[
                'list',
                'ping',
                'version',
                'ps',
                'pull',
                'create',
                'delete',
                'sync',
            ],
        ),
        model_name=dict(type='str', aliases=["model"], required=False),
        model_list=dict(
            type='list', aliases=["models"], elements='str', required=False
        ),
        model_file_path=dict(type='str', required=False),
        use_system_certs=dict(type='bool', default=True, required=False),
        validate_certs=dict(type='bool', default=True, required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        mutually_exclusive=[('model_name', 'model_list')],
        supports_check_mode=True,
    )

    if not HAS_REQUESTS:
        module.fail_json(msg='The python "requests" library is required.')

    result = dict(changed=False, result={}, base_url='')

    base_url = module.params['url'].rstrip('/')
    # Check parameter or environment variable
    api_key = module.params['api_key'] or os.environ.get('OLLAMA_API_KEY')
    api_auth_type = module.params['api_auth_type']

    action = module.params['action']
    model_name = module.params['model_name']
    model_list = module.params['model_list'] or []
    model_file_path = module.params['model_file_path']
    use_system_certs = module.params['use_system_certs']
    validate_certs = module.params['validate_certs']

    # Configure truststore if requested and available
    if use_system_certs:
        if HAS_TRUSTSTORE:
            truststore.inject_into_ssl()
        else:
            module.fail_json(
                msg="The python 'truststore' library is required when 'use_system_certs=true'."
            )

    # Normalize single model input into model_list if provided (except for sync where model_list is explicitly required)
    if model_name and model_name not in model_list and action != 'sync':
        model_list.append(model_name)

    result['base_url'] = base_url

    if action in ['pull', 'delete'] and not model_list:
        module.fail_json(
            msg=f"At least one model must be specified via 'model_name' or 'model_list' for {action} action.",
            **result,
        )

    if action == 'sync' and not model_list:
        module.fail_json(
            msg="Parameter 'model_list' must be specified when using the 'sync' action.",
            **result,
        )

    headers = get_auth_headers(api_key, api_auth_type)

    try:
        if action == 'ping':
            resp = requests.get(
                f"{base_url}/health",
                headers=headers,
                verify=validate_certs,
                timeout=10,
            )
            if resp.status_code == 200:
                # /health typically returns plain text or JSON depending on context, handle gracefully
                status_data = (
                    resp.json()
                    if resp.headers.get('content-type', '').startswith(
                        'application/json'
                    )
                    else {"status": resp.text.strip()}
                )
                module.exit_json(
                    changed=False, msg="Ollama API is healthy", status=status_data
                )
            else:
                module.fail_json(
                    msg=f"Ollama API unhealthy, status code: {resp.status_code}"
                )

        elif action == 'version':
            resp = requests.get(
                f"{base_url}/api/version",
                headers=headers,
                verify=validate_certs,
                timeout=10,
            )
            if resp.status_code == 200:
                module.exit_json(
                    changed=False, msg="Ollama API version fetched", status=resp.json()
                )
            else:
                module.fail_json(
                    msg=f"Ollama API version check failed, status code: {resp.status_code}"
                )

        elif action == 'list':
            resp = requests.get(
                f"{base_url}/api/tags",
                headers=headers,
                verify=validate_certs,
                timeout=10,
            )
            if resp.status_code == 200:
                module.exit_json(
                    changed=False, msg="Ollama API available models", status=resp.json()
                )
            else:
                module.fail_json(
                    msg=f"Ollama API unhealthy, status code: {resp.status_code}"
                )

        elif action == 'pull':
            pull_results = []
            for model in model_list:
                payload = {'name': model, 'stream': False}
                resp = requests.post(
                    f"{base_url}/api/pull",
                    headers=headers,
                    json=payload,
                    verify=validate_certs,
                    timeout=300,
                )
                if resp.status_code != 200:
                    module.fail_json(msg=f"Failed to pull model '{model}': {resp.text}")
                pull_results.append({'model': model, 'status': 'pulled'})

            module.exit_json(changed=True, results=pull_results)

        elif action == 'create':
            if not model_name:
                module.fail_json(
                    msg="Parameter 'model_name' is required for create action."
                )

            model_file_content = ""
            if model_file_path:
                with open(model_file_path, 'r') as f:
                    model_file_content = f.read()

            payload = {
                'name': model_name,
                'model_file': model_file_content,
                'stream': False,
            }
            resp = requests.post(
                f"{base_url}/api/create",
                headers=headers,
                json=payload,
                verify=validate_certs,
                timeout=300,
            )
            if resp.status_code != 200:
                module.fail_json(
                    msg=f"Failed to create custom model '{model_name}': {resp.text}"
                )

            module.exit_json(
                changed=True, msg=f"Custom model '{model_name}' successfully created."
            )

        elif action == 'delete':
            if not model_list:
                module.fail_json(
                    msg="At least one model must be specified for delete action."
                )

            delete_results = []
            for model in model_list:
                payload = {'name': model}
                resp = requests.delete(
                    f"{base_url}/api/delete",
                    headers=headers,
                    json=payload,
                    verify=validate_certs,
                    timeout=60,
                )
                if resp.status_code != 200:
                    module.fail_json(
                        msg=f"Failed to delete model '{model}': {resp.text}"
                    )
                delete_results.append({'model': model, 'status': 'deleted'})

            module.exit_json(changed=True, results=delete_results)

        elif action == 'sync':
            # 1. Fetch currently available models from endpoint
            resp = requests.get(
                f"{base_url}/api/tags",
                headers=headers,
                verify=validate_certs,
                timeout=10,
            )
            if resp.status_code != 200:
                module.fail_json(
                    msg=f"Failed to fetch existing models for sync, status code: {resp.status_code}"
                )

            existing_models_data = resp.json().get('models', [])
            existing_model_names = [m.get('name') for m in existing_models_data]

            sync_actions = []
            changed = False

            # 2. Remove models present on server but NOT in model_list
            for model in existing_model_names:
                if model not in model_list:
                    if not module.check_mode:
                        del_resp = requests.delete(
                            f"{base_url}/api/delete",
                            headers=headers,
                            json={'name': model},
                            verify=validate_certs,
                            timeout=60,
                        )
                        if del_resp.status_code != 200:
                            module.fail_json(
                                msg=f"Failed to delete model '{model}' during sync: {del_resp.text}"
                            )
                    sync_actions.append({'model': model, 'action': 'deleted'})
                    changed = True

            # 3. Pull models specified in model_list that are NOT currently present on server
            for model in model_list:
                if model not in existing_model_names:
                    if not module.check_mode:
                        pull_resp = requests.post(
                            f"{base_url}/api/pull",
                            headers=headers,
                            json={'name': model, 'stream': False},
                            verify=validate_certs,
                            timeout=300,
                        )
                        if pull_resp.status_code != 200:
                            module.fail_json(
                                msg=f"Failed to pull model '{model}' during sync: {pull_resp.text}"
                            )
                    sync_actions.append({'model': model, 'action': 'pulled'})
                    changed = True

            module.exit_json(changed=changed, results=sync_actions)

        elif action == 'ps':
            resp = requests.get(
                f"{base_url}/api/ps", headers=headers, verify=validate_certs, timeout=10
            )
            if resp.status_code == 200:
                module.exit_json(
                    changed=False, msg="Ollama running models", status=resp.json()
                )
            else:
                module.fail_json(
                    msg=f"Ollama API unhealthy, status code: {resp.status_code}"
                )

        else:
            module.fail_json(msg=f"Unsupported action: {action}")

    except (requests.exceptions.RequestException, OSError) as e:
        module.fail_json(msg=f"An error occurred connecting to Ollama API: {str(e)}")


if __name__ == '__main__':
    run_module()
