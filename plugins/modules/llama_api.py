#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Lee Johnson (ljohnson@dettonville.com)
# MIT license (https://opensource.org/license/mit/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: llama_api
version_added: "2.20.0"
author:
    - "Lee Johnson (@lj020326)"
short_description: Manage and query llama.cpp server states via API
description:
    - >-
      Checks health, models, server properties, and slots from a specified
      llama.cpp server endpoint.
options:
    url:
      description:
          - Base URL of the llama.cpp API service.
      aliases: ['endpoint']
      required: true
      type: str
    api_key:
      description:
        - Optional API token/key for authentication.
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
      choices: [health, models, props, slots]
      default: 'health'
      required: false
      type: str
    use_system_certs:
      description:
        - Whether to use the truststore library.
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
- name: Check health of llama.cpp server
  dettonville.llm.llama_api:
    url: "https://llama-cpp.example.com"
    action: "health"

- name: List models on llama.cpp server
  dettonville.llm.llama_api:
    url: "https://llama-cpp.example.com"
    action: "models"
'''

RETURN = r'''
changed:
    description: Whether any modification or state change occurred.
    type: bool
    returned: always
status:
    description: The JSON response dictionary or message returned from the API.
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
            default='health',
            required=False,
            choices=['health', 'models', 'props', 'slots'],
        ),
        use_system_certs=dict(type='bool', default=True, required=False),
        validate_certs=dict(type='bool', default=True, required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    client = LlmApiClient(module)
    client.execute_llama_action()


if __name__ == '__main__':
    run_module()
