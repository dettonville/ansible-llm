from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

# Import the module under test
# noinspection PyUnresolvedReferences
from ansible_collections.dettonville.llm.plugins.modules import llama_api

# noinspection PyUnresolvedReferences
from ansible_collections.dettonville.llm.tests.unit.plugins.modules.utils import (  # noqa: E501
    MODULE_UTILS_IMPORT_PATH,
    AnsibleExitJson,
    ModuleTestCase,
    make_absolute,
    set_module_args,
)


class TestLlamaCppApiModule(ModuleTestCase):
    """Test cases for the llama_api ansible module"""

    @patch(make_absolute(MODULE_UTILS_IMPORT_PATH, "llm_api.truststore"))
    @patch(make_absolute(MODULE_UTILS_IMPORT_PATH, "llm_api.requests.get"))
    def test_llama_cpp_health(self, mock_get, mock_truststore):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = {"status": "ok", "slots_idle": 1}
        mock_get.return_value = mock_response

        with set_module_args(
            {'endpoint': 'https://llama-cpp.example.com', 'action': 'health'}
        ):
            with self.assertRaises(AnsibleExitJson) as exc_info:
                llama_api.run_module()

        result = exc_info.exception.args[0]
        self.assertFalse(result['changed'])
        self.assertEqual(result['status']['status'], 'ok')
        mock_get.assert_called_once()
        mock_truststore.inject_into_ssl.assert_called_once()

    @patch(make_absolute(MODULE_UTILS_IMPORT_PATH, "llm_api.truststore"))
    @patch(make_absolute(MODULE_UTILS_IMPORT_PATH, "llm_api.requests.get"))
    def test_llama_cpp_models(self, mock_get, mock_truststore):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"id": "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"}]
        }
        mock_get.return_value = mock_response

        with set_module_args(
            {'endpoint': 'https://llama-cpp.example.com', 'action': 'models'}
        ):
            with self.assertRaises(AnsibleExitJson) as exc_info:
                llama_api.run_module()

        result = exc_info.exception.args[0]
        self.assertFalse(result['changed'])
        self.assertEqual(len(result['status']['data']), 1)
        self.assertEqual(
            result['status']['data'][0]['id'],
            'Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf',
        )
        mock_get.assert_called_once()
        mock_truststore.inject_into_ssl.assert_called_once()
