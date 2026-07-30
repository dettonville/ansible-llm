from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

# Import the module under test
# noinspection PyUnresolvedReferences
from ansible_collections.dettonville.llm.plugins.modules import ollama_api

# noinspection PyUnresolvedReferences
from ansible_collections.dettonville.llm.tests.unit.plugins.modules.utils import (
    MODULES_IMPORT_PATH,
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    make_absolute,
    set_module_args,
)


class TestOllamaApiModule(ModuleTestCase):
    """Test cases for the ollama_api ansible module using the requests library"""

    @patch(make_absolute(MODULES_IMPORT_PATH, "ollama_api.requests.get"))
    def test_ollama_list_models(self, mock_get):
        # Mock successful tag listing response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "models": [{"name": "qwen2.5:7b"}, {"name": "llama3:8b"}]
        }
        mock_get.return_value = mock_response

        with set_module_args(
            {'endpoint': 'https://ollama.example.com', 'action': 'list'}
        ):
            with self.assertRaises(AnsibleExitJson) as exc_info:
                ollama_api.run_module()

        result = exc_info.exception.args[0]
        self.assertFalse(result['changed'])
        self.assertEqual(len(result['status']['models']), 2)
        self.assertEqual(result['status']['models'][0]['name'], 'qwen2.5:7b')
        mock_get.assert_called_once()

    @patch(make_absolute(MODULES_IMPORT_PATH, "ollama_api.requests.get"))
    def test_ollama_ping(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"version": "0.1.0"}
        mock_get.return_value = mock_response

        with set_module_args(
            {'endpoint': 'https://ollama.example.com', 'action': 'ping'}
        ):
            with self.assertRaises(AnsibleExitJson) as exc_info:
                ollama_api.run_module()

        result = exc_info.exception.args[0]
        self.assertFalse(result['changed'])
        self.assertEqual(result['msg'], "Ollama API is ready")
        self.assertEqual(result['status']['version'], '0.1.0')
        mock_get.assert_called_once()

    @patch(make_absolute(MODULES_IMPORT_PATH, "ollama_api.requests.post"))
    def test_ollama_pull_model(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        with set_module_args(
            {
                'endpoint': 'https://ollama.example.com',
                'action': 'pull',
                'model_name': 'qwen2.5-coder:7b',
            }
        ):
            with self.assertRaises(AnsibleExitJson) as exc_info:
                ollama_api.run_module()

        result = exc_info.exception.args[0]
        self.assertTrue(result['changed'])
        self.assertEqual(result['results'][0]['model'], 'qwen2.5-coder:7b')
        self.assertEqual(result['results'][0]['status'], 'pulled')
        mock_post.assert_called_once()

    @patch(make_absolute(MODULES_IMPORT_PATH, "ollama_api.requests.delete"))
    def test_ollama_delete_model(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response

        with set_module_args(
            {
                'endpoint': 'https://ollama.example.com',
                'action': 'delete',
                'model_name': 'obsolete-model:latest',
            }
        ):
            with self.assertRaises(AnsibleExitJson) as exc_info:
                ollama_api.run_module()

        result = exc_info.exception.args[0]
        self.assertTrue(result['changed'])
        self.assertEqual(result['results'][0]['model'], 'obsolete-model:latest')
        self.assertEqual(result['results'][0]['status'], 'deleted')
        mock_delete.assert_called_once()

    def test_ollama_missing_model_parameter(self):
        with set_module_args(
            {
                'endpoint': 'https://ollama.example.com',
                'action': 'pull',
                # missing 'model_name' / 'model_list'
            }
        ):
            with self.assertRaises(AnsibleFailJson) as exc_info:
                ollama_api.run_module()

        result = exc_info.exception.args[0]
        self.assertIn("model must be specified", result['msg'])

    @patch(make_absolute(MODULES_IMPORT_PATH, "ollama_api.requests.delete"))
    @patch(make_absolute(MODULES_IMPORT_PATH, "ollama_api.requests.post"))
    @patch(make_absolute(MODULES_IMPORT_PATH, "ollama_api.requests.get"))
    def test_ollama_sync_models(self, mock_get, mock_post, mock_delete):
        # Mock initial state: server currently has 'old-model:latest' and 'keep-model:7b'
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = {
            "models": [{"name": "old-model:latest"}, {"name": "keep-model:7b"}]
        }
        mock_get.return_value = mock_get_response

        # Mock successful delete response for 'old-model:latest'
        mock_delete_response = MagicMock()
        mock_delete_response.status_code = 200
        mock_delete.return_value = mock_delete_response

        # Mock successful pull response for missing 'new-model:13b'
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_post_response

        with set_module_args(
            {
                'endpoint': 'https://ollama.example.com',
                'action': 'sync',
                'model_list': ['keep-model:7b', 'new-model:13b'],
            }
        ):
            with self.assertRaises(AnsibleExitJson) as exc_info:
                ollama_api.run_module()

        result = exc_info.exception.args[0]
        self.assertTrue(result['changed'])

        # Verify actions taken: 'old-model:latest' deleted, 'new-model:13b' pulled
        actions = result['results']
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0], {'model': 'old-model:latest', 'action': 'deleted'})
        self.assertEqual(actions[1], {'model': 'new-model:13b', 'action': 'pulled'})

        mock_get.assert_called_once()
        mock_delete.assert_called_once()
        mock_post.assert_called_once()

    def test_ollama_sync_missing_model_list(self):
        with set_module_args(
            {
                'endpoint': 'https://ollama.example.com',
                'action': 'sync',
                # missing 'model_list'
            }
        ):
            with self.assertRaises(AnsibleFailJson) as exc_info:
                ollama_api.run_module()

        result = exc_info.exception.args[0]
        self.assertIn(
            "Parameter 'model_list' must be specified when using the 'sync' action",
            result['msg'],
        )
