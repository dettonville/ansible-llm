from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import patch

# Import the module under test
from ansible_collections.dettonville.llm.plugins.modules import hf_download

# noinspection PyUnresolvedReferences
from ansible_collections.dettonville.llm.tests.unit.plugins.modules.utils import (  # noqa: E501
    MODULES_IMPORT_PATH,
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    make_absolute,
    set_module_args,
)


class TestHfDownloadModule(ModuleTestCase):
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    def test_download_success(self, mock_hf_hub_download, mock_path_exists):
        """Test successful standard file download."""
        mock_path_exists.return_value = False
        mock_hf_hub_download.return_value = "/opt/llm/models/model.gguf"

        set_args = {
            'repo_id': 'TheBloke/Llama-2-7B-Chat-GGUF',
            'filename': 'model.gguf',
            'local_dir': '/opt/llm/models',
            'repo_type': 'model',
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleExitJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertTrue(result['changed'])
        self.assertEqual(result['path'], '/opt/llm/models/model.gguf')

        mock_hf_hub_download.assert_called_once_with(
            repo_id='TheBloke/Llama-2-7B-Chat-GGUF',
            filename='model.gguf',
            local_dir='/opt/llm/models',
            local_dir_use_symlinks=False,
            repo_type='model',
            force_download=False,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    def test_download_with_token(self, mock_hf_hub_download, mock_path_exists):
        """Test authentication via token parameter."""
        mock_path_exists.return_value = False
        mock_hf_hub_download.return_value = "/opt/llm/models/model.safetensors"

        set_args = {
            'repo_id': 'meta-llama/Meta-Llama-3-8B-Instruct',
            'filename': 'model.safetensors',
            'local_dir': '/opt/llm/models',
            'token': 'hf_test_token_xyz',
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleExitJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertTrue(result['changed'])
        mock_hf_hub_download.assert_called_once_with(
            repo_id='meta-llama/Meta-Llama-3-8B-Instruct',
            filename='model.safetensors',
            local_dir='/opt/llm/models',
            local_dir_use_symlinks=False,
            repo_type='model',
            token='hf_test_token_xyz',
            force_download=False,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    def test_download_with_revision(
        self, mock_hf_hub_download, mock_path_exists
    ):
        """Test revision control via revision parameter."""
        mock_path_exists.return_value = False
        mock_hf_hub_download.return_value = "/opt/llm/models/config.json"

        set_args = {
            'repo_id': 'mistralai/Mistral-7B-v0.1',
            'filename': 'config.json',
            'local_dir': '/opt/llm/models',
            'revision': 'refs/pr/1',
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleExitJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertTrue(result['changed'])
        mock_hf_hub_download.assert_called_once_with(
            repo_id='mistralai/Mistral-7B-v0.1',
            filename='config.json',
            local_dir='/opt/llm/models',
            local_dir_use_symlinks=False,
            repo_type='model',
            revision='refs/pr/1',
            force_download=False,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    def test_download_with_subfolder(
        self, mock_hf_hub_download, mock_path_exists
    ):
        """Test subfolder routing via subfolder parameter."""
        mock_path_exists.return_value = False
        mock_hf_hub_download.return_value = "/opt/llm/models/tokenizer.json"

        set_args = {
            'repo_id': 'unsloth/llama-3-8b-Instruct-bnb-4bit',
            'filename': 'tokenizer.json',
            'local_dir': '/opt/llm/models',
            'subfolder': 'tokenizers',
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleExitJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertTrue(result['changed'])
        mock_hf_hub_download.assert_called_once_with(
            repo_id='unsloth/llama-3-8b-Instruct-bnb-4bit',
            filename='tokenizer.json',
            local_dir='/opt/llm/models',
            local_dir_use_symlinks=False,
            repo_type='model',
            subfolder='tokenizers',
            force_download=False,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    def test_download_with_force_download(
        self, mock_hf_hub_download, mock_path_exists
    ):
        """Test force re-downloads via force_download parameter."""
        mock_path_exists.return_value = True
        mock_hf_hub_download.return_value = "/opt/llm/models/model.gguf"

        set_args = {
            'repo_id': 'TheBloke/Llama-2-7B-Chat-GGUF',
            'filename': 'model.gguf',
            'local_dir': '/opt/llm/models',
            'force_download': True,
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleExitJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertTrue(result['changed'])
        mock_hf_hub_download.assert_called_once_with(
            repo_id='TheBloke/Llama-2-7B-Chat-GGUF',
            filename='model.gguf',
            local_dir='/opt/llm/models',
            local_dir_use_symlinks=False,
            repo_type='model',
            force_download=True,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    def test_download_with_local_files_only(
        self, mock_hf_hub_download, mock_path_exists
    ):
        """Test local cache overrides via local_files_only parameter."""
        mock_path_exists.return_value = True
        mock_hf_hub_download.return_value = "/opt/llm/models/model.gguf"

        set_args = {
            'repo_id': 'TheBloke/Llama-2-7B-Chat-GGUF',
            'filename': 'model.gguf',
            'local_dir': '/opt/llm/models',
            'local_files_only': True,
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleExitJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertFalse(result['changed'])
        mock_hf_hub_download.assert_called_once_with(
            repo_id='TheBloke/Llama-2-7B-Chat-GGUF',
            filename='model.gguf',
            local_dir='/opt/llm/models',
            local_dir_use_symlinks=False,
            repo_type='model',
            force_download=False,
            local_files_only=True,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    def test_download_check_mode(self, mock_hf_hub_download, mock_path_exists):
        """Test module execution behavior in check mode."""
        mock_path_exists.return_value = False

        set_args = {
            'repo_id': 'TheBloke/Llama-2-7B-Chat-GGUF',
            'filename': 'model.gguf',
            'local_dir': '/opt/llm/models',
            '_ansible_check_mode': True,
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleExitJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertTrue(result['changed'])
        self.assertEqual(result['path'], '/opt/llm/models/model.gguf')
        mock_hf_hub_download.assert_not_called()

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), False)
    def test_missing_library_failure(self):
        """Test failure handling when huggingface_hub Python library is
        missing."""
        set_args = {
            'repo_id': 'TheBloke/Llama-2-7B-Chat-GGUF',
            'filename': 'model.gguf',
            'local_dir': '/opt/llm/models',
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleFailJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertIn(
            'The python library "huggingface_hub" is required', result['msg']
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    def test_download_exception_handling(
        self, mock_hf_hub_download, mock_path_exists
    ):
        """Test module handling of exceptions raised during the Hugging Face
        download process."""
        mock_path_exists.return_value = False
        mock_hf_hub_download.side_effect = Exception("Network timeout error")

        set_args = {
            'repo_id': 'TheBloke/Llama-2-7B-Chat-GGUF',
            'filename': 'model.gguf',
            'local_dir': '/opt/llm/models',
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleFailJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertIn(
            "Failed to download file from Hugging Face: Network timeout error",
            result['msg'],
        )
