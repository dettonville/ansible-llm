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
    - Manages Ollama models and checks service health using standard HTTP API
      endpoints.
    - Provides capabilities to list available models, check running models
      in VRAM (ps), pull (download), create custom models, remove, and sync
      models against a target Ollama endpoint.
    - Supports API key authentication via parameter or OLLAMA_API_KEY
      environment variable.
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
        - API key or user:password basic auth credential for the Ollama
          endpoint.
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
      choices: [health, version, list, ps, pull, create, delete, sync]
      default: 'list'
      required: false
      type: str
    model_name:
      description: >-
        Single model name string to process or target for custom creation.
      aliases: ['model']
      required: false
      type: str
    model_list:
      description: >-
        List of model name strings to process in batch or sync against.
      aliases: ['models']
      required: false
      type: list
      elements: str
    model_file_path:
      description: Path to local Modelfile content for custom model creation.
      required: false
      type: str
    use_system_certs:
      description:
        - >-
          Whether to use the truststore library to hook Python's ssl module
          into the native system certificate store.
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
    action: "health"

- name: Get Ollama version
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "version"

- name: List models on Ollama endpoint
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "list"

- name: Check running models loaded in VRAM
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "ps"

- name: Pull a model with explicit API key authentication
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "pull"
    model_name: "qwen2.5-coder:7b"
    api_key: "{{ lookup('env', 'OLLAMA_API_KEY') }}"
    api_auth_type: "bearer"

- name: Create a custom model from a local model file
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "create"
    model_name: "my-custom-model:latest"
    model_file_path: "/path/to/Modelfile"

- name: Remove an obsolete model using basic authentication
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "delete"
    model: "llama3.1:8b"
    api_key: "admin:secretpassword"
    api_auth_type: "basic"

- name: Pull a model using basic base64 encoded authentication
  dettonville.llm.ollama_api:
    url: "https://ollama.example.com"
    action: "pull"
    model_name: "qwen2.5-coder:7b"
    api_key: "e1NTSEF9cGFzc3dvcmQ="   # explicit base64
    api_auth_type: "basic"

- name: Sync models on Ollama endpoint to match specified list exactly
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
    description: >-
      The JSON response dictionary or message returned from the Ollama API
      or action.
    type: raw
    returned: always
base_url:
    description: The target endpoint URL used.
    type: str
    returned: always
'''

# noinspection PyPackageRequirements
from ansible.module_utils.basic import AnsibleModule

# noinspection PyUnresolvedReferences,PyPackageRequirements
from ansible_collections.dettonville.llm.plugins.module_utils.llm_api import (
    LlmApiClient,
)


def run_module():
    module_args = dict(
        url=dict(type='str', aliases=["endpoint"], required=True),
        api_key=dict(type='str', required=False, no_log=True),
        api_auth_type=dict(
            type='str',
            default='bearer',
            required=False,
            choices=['bearer', 'basic'],
        ),
        action=dict(
            type='str',
            default='list',
            required=False,
            choices=[
                'list',
                'health',
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

    client = LlmApiClient(module)
    client.execute_ollama_action()


if __name__ == '__main__':
    run_module()
