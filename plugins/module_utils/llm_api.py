# -*- coding: utf-8 -*-
# Copyright: (c) 2026, Lee Johnson (ljohnson@dettonville.com)
# MIT license (https://opensource.org/license/mit/)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import os

try:
    # noinspection PyPackageRequirements,PyUnusedImports
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    # noinspection PyPackageRequirements,PyUnusedImports
    import truststore

    HAS_TRUSTSTORE = True
except ImportError:
    HAS_TRUSTSTORE = False


class LlmApiClient(object):
    """Core client to interact with LLM backends like Ollama and llama.cpp."""

    def __init__(self, module):
        self.module = module

        if not HAS_REQUESTS:
            self.module.fail_json(
                msg='The python "requests" library is required.'
            )

        self.base_url = module.params.get('url', '').rstrip('/')
        self.api_key = module.params.get('api_key') or os.environ.get(
            'OLLAMA_API_KEY'
        )
        self.api_auth_type = module.params.get('api_auth_type', 'bearer')
        self.use_system_certs = module.params.get('use_system_certs', True)
        self.validate_certs = module.params.get('validate_certs', True)

        self._configure_truststore()

    def _configure_truststore(self):
        if self.use_system_certs:
            if HAS_TRUSTSTORE:
                truststore.inject_into_ssl()
            else:
                self.module.fail_json(
                    msg="The python 'truststore' library is required "
                    "when 'use_system_certs=true'."
                )

    def get_auth_headers(self):
        headers = {'Content-Type': 'application/json'}
        if not self.api_key:
            return headers

        if self.api_auth_type == 'basic':
            if ':' in self.api_key:
                encoded = base64.b64encode(
                    self.api_key.encode('utf-8')
                ).decode('utf-8')
                headers['Authorization'] = f'Basic {encoded}'
            else:
                headers['Authorization'] = f'Basic {self.api_key}'
        else:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    def execute_llama_action(self):
        action = self.module.params.get('action', 'health')
        headers = self.get_auth_headers()

        try:
            if action == 'health':
                resp = requests.get(
                    f"{self.base_url}/health",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code in [200, 503]:
                    status_data = (
                        resp.json()
                        if resp.headers.get('content-type', '').startswith(
                            'application/json'
                        )
                        else {"status": resp.text.strip()}
                    )
                    self.module.exit_json(
                        changed=False,
                        msg="llama.cpp server health checked",
                        status=status_data,
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"llama.cpp health check failed, status code: "
                        f"{resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'models':
                resp = requests.get(
                    f"{self.base_url}/v1/models",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="llama.cpp available models fetched",
                        status=resp.json(),
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"Failed to fetch llama.cpp models, status code: "
                        f"{resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'props':
                resp = requests.get(
                    f"{self.base_url}/props",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="llama.cpp server properties fetched",
                        status=resp.json(),
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"Failed to fetch llama.cpp server properties, "
                        f"status code: {resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'slots':
                resp = requests.get(
                    f"{self.base_url}/v1/slots",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="llama.cpp slot states fetched",
                        status=resp.json(),
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"Failed to fetch llama.cpp slots, status code: "
                        f"{resp.status_code}",
                        base_url=self.base_url,
                    )
            else:
                self.module.fail_json(
                    msg=f"Unsupported action: {action}", base_url=self.base_url
                )

        except (requests.exceptions.RequestException, OSError) as e:
            self.module.fail_json(
                msg=f"An error occurred connecting to llama.cpp API: {str(e)}",
                base_url=self.base_url,
            )

    def execute_vllm_action(self):
        action = self.module.params.get('action', 'health')
        headers = self.get_auth_headers()

        try:
            if action == 'health':
                resp = requests.get(
                    f"{self.base_url}/health",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code in [200, 503]:
                    status_data = (
                        resp.json()
                        if resp.headers.get('content-type', '').startswith(
                            'application/json'
                        )
                        else {"status": resp.text.strip()}
                    )
                    self.module.exit_json(
                        changed=False,
                        msg="vLLM server health checked",
                        status=status_data,
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"vLLM health check failed, status code: "
                        f"{resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'models':
                resp = requests.get(
                    f"{self.base_url}/v1/models",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="vLLM available models fetched",
                        status=resp.json(),
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"Failed to fetch vLLM models, "
                        f"status code: {resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'ping':
                resp = requests.get(
                    f"{self.base_url}/health",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="vLLM API is healthy",
                        status={"status": "ok"},
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"vLLM API unhealthy, status code: "
                        f"{resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'version':
                resp = requests.get(
                    f"{self.base_url}/version",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="vLLM API version fetched",
                        status=resp.json(),
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"vLLM API version check failed, "
                        f"status code: {resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'metrics':
                resp = requests.get(
                    f"{self.base_url}/metrics",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="vLLM metrics fetched",
                        status={"metrics": resp.text},
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"Failed to fetch vLLM metrics, "
                        f"status code: {resp.status_code}",
                        base_url=self.base_url,
                    )
            else:
                self.module.fail_json(
                    msg=f"Unsupported action: {action}", base_url=self.base_url
                )

        except (requests.exceptions.RequestException, OSError) as e:
            self.module.fail_json(
                msg=f"An error occurred connecting to vLLM API: {str(e)}",
                base_url=self.base_url,
            )

    def execute_ollama_action(self):
        action = self.module.params.get('action', 'list')
        model_name = self.module.params.get('model_name')
        model_list = self.module.params.get('model_list') or []
        model_file_path = self.module.params.get('model_file_path')

        # Normalize single model input into model_list if provided (except
        # for sync)
        if model_name and model_name not in model_list and action != 'sync':
            model_list.append(model_name)

        if action in ['pull', 'delete'] and not model_list:
            self.module.fail_json(
                msg=f"At least one model must be specified via 'model_name' "
                f"or 'model_list' for {action} action.",
                base_url=self.base_url,
            )

        if action == 'sync' and not model_list:
            self.module.fail_json(
                msg="Parameter 'model_list' must be specified when using "
                "the 'sync' action.",
                base_url=self.base_url,
            )

        headers = self.get_auth_headers()

        try:
            if action == 'ping':
                resp = requests.get(
                    f"{self.base_url}/health",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    status_data = (
                        resp.json()
                        if resp.headers.get('content-type', '').startswith(
                            'application/json'
                        )
                        else {"status": resp.text.strip()}
                    )
                    self.module.exit_json(
                        changed=False,
                        msg="Ollama API is healthy",
                        status=status_data,
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"Ollama API unhealthy, status code: "
                        f"{resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'version':
                resp = requests.get(
                    f"{self.base_url}/api/version",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="Ollama API version fetched",
                        status=resp.json(),
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"Ollama API version check failed, "
                        f"status code: {resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'list':
                resp = requests.get(
                    f"{self.base_url}/api/tags",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="Ollama API available models",
                        status=resp.json(),
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"Ollama API unhealthy, status code: "
                        f"{resp.status_code}",
                        base_url=self.base_url,
                    )

            elif action == 'pull':
                pull_results = []
                for model in model_list:
                    payload = {'name': model, 'stream': False}
                    resp = requests.post(
                        f"{self.base_url}/api/pull",
                        headers=headers,
                        json=payload,
                        verify=self.validate_certs,
                        timeout=300,
                    )
                    if resp.status_code != 200:
                        self.module.fail_json(
                            msg=f"Failed to pull model '{model}': {resp.text}",
                            base_url=self.base_url,
                        )
                    pull_results.append({'model': model, 'status': 'pulled'})

                self.module.exit_json(
                    changed=True, results=pull_results, base_url=self.base_url
                )

            elif action == 'create':
                if not model_name:
                    self.module.fail_json(
                        msg="Parameter 'model_name' is required for create "
                        "action.",
                        base_url=self.base_url,
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
                    f"{self.base_url}/api/create",
                    headers=headers,
                    json=payload,
                    verify=self.validate_certs,
                    timeout=300,
                )
                if resp.status_code != 200:
                    self.module.fail_json(
                        msg=f"Failed to create custom "
                        f"model '{model_name}': {resp.text}",
                        base_url=self.base_url,
                    )

                self.module.exit_json(
                    changed=True,
                    msg=f"Custom model '{model_name}' successfully created.",
                    base_url=self.base_url,
                )

            elif action == 'delete':
                if not model_list:
                    self.module.fail_json(
                        msg="At least one model must be specified for delete "
                        "action.",
                        base_url=self.base_url,
                    )

                delete_results = []
                for model in model_list:
                    payload = {'name': model}
                    resp = requests.delete(
                        f"{self.base_url}/api/delete",
                        headers=headers,
                        json=payload,
                        verify=self.validate_certs,
                        timeout=60,
                    )
                    if resp.status_code != 200:
                        self.module.fail_json(
                            msg=f"Failed to delete model '{model}': "
                            f"{resp.text}",
                            base_url=self.base_url,
                        )
                    delete_results.append(
                        {'model': model, 'status': 'deleted'}
                    )

                self.module.exit_json(
                    changed=True,
                    results=delete_results,
                    base_url=self.base_url,
                )

            elif action == 'sync':
                resp = requests.get(
                    f"{self.base_url}/api/tags",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code != 200:
                    self.module.fail_json(
                        msg=f"Failed to fetch existing models for sync, "
                        f"status code: {resp.status_code}",
                        base_url=self.base_url,
                    )

                existing_models_data = resp.json().get('models', [])
                existing_model_names = [
                    m.get('name') for m in existing_models_data
                ]

                sync_actions = []
                changed = False

                for model in existing_model_names:
                    if model not in model_list:
                        if not self.module.check_mode:
                            del_resp = requests.delete(
                                f"{self.base_url}/api/delete",
                                headers=headers,
                                json={'name': model},
                                verify=self.validate_certs,
                                timeout=60,
                            )
                            if del_resp.status_code != 200:
                                self.module.fail_json(
                                    msg=f"Failed to delete model '{model}' "
                                    f"during sync: {del_resp.text}",
                                    base_url=self.base_url,
                                )
                        sync_actions.append(
                            {'model': model, 'action': 'deleted'}
                        )
                        changed = True

                for model in model_list:
                    if model not in existing_model_names:
                        if not self.module.check_mode:
                            pull_resp = requests.post(
                                f"{self.base_url}/api/pull",
                                headers=headers,
                                json={'name': model, 'stream': False},
                                verify=self.validate_certs,
                                timeout=300,
                            )
                            if pull_resp.status_code != 200:
                                self.module.fail_json(
                                    msg=f"Failed to pull model '{model}' "
                                    f"during sync: {pull_resp.text}",
                                    base_url=self.base_url,
                                )
                        sync_actions.append(
                            {'model': model, 'action': 'pulled'}
                        )
                        changed = True

                self.module.exit_json(
                    changed=changed,
                    results=sync_actions,
                    base_url=self.base_url,
                )

            elif action == 'ps':
                resp = requests.get(
                    f"{self.base_url}/api/ps",
                    headers=headers,
                    verify=self.validate_certs,
                    timeout=10,
                )
                if resp.status_code == 200:
                    self.module.exit_json(
                        changed=False,
                        msg="Ollama running models",
                        status=resp.json(),
                        base_url=self.base_url,
                    )
                else:
                    self.module.fail_json(
                        msg=f"Ollama API unhealthy, status code: "
                        f"{resp.status_code}",
                        base_url=self.base_url,
                    )

            else:
                self.module.fail_json(
                    msg=f"Unsupported action: {action}", base_url=self.base_url
                )

        except (requests.exceptions.RequestException, OSError) as e:
            self.module.fail_json(
                msg=f"An error occurred connecting to Ollama API: {str(e)}",
                base_url=self.base_url,
            )
