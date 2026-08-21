from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

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


# noinspection PyUnusedLocal
class TestHfDownloadModule(ModuleTestCase):
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HfApi"))
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    @patch.object(
        hf_download.AnsibleModule,
        'set_fs_attributes_if_different',
        return_value=False,
    )
    def test_download_success(
        self,
        mock_set_fs_attrs,
        mock_hf_hub_download,
        mock_path_exists,
        mock_hf_api,
    ):
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
        self.assertEqual(
            result['downloaded_files'], ['/opt/llm/models/model.gguf']
        )
        self.assertEqual(result['resolved_filename'], 'model.gguf')

        mock_hf_hub_download.assert_called_once_with(
            repo_id='TheBloke/Llama-2-7B-Chat-GGUF',
            filename='model.gguf',
            local_dir='/opt/llm/models',
            local_dir_use_symlinks='auto',
            repo_type='model',
            force_download=False,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HfApi"))
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    @patch.object(
        hf_download.AnsibleModule,
        'set_fs_attributes_if_different',
        return_value=False,
    )
    def test_download_with_dynamic_filename_resolution(
        self,
        mock_set_fs_attrs,
        mock_hf_hub_download,
        mock_path_exists,
        mock_hf_api,
    ):
        """Test resolving target filename dynamically when filename is
        omitted."""
        mock_path_exists.return_value = False
        mock_api_instance = MagicMock()
        mock_api_instance.list_repo_files.return_value = [
            'README.md',
            'llama-2-7b.Q4_K_M.gguf',
            'llama-2-7b.Q8_0.gguf',
        ]
        mock_hf_api.return_value = mock_api_instance
        mock_hf_hub_download.return_value = (
            "/opt/llm/models/llama-2-7b.Q4_K_M.gguf"
        )

        set_args = {
            'repo_id': 'TheBloke/Llama-2-7B-Chat-GGUF',
            'quant_preference': 'Q4_K_M',
            'local_dir': '/opt/llm/models',
        }

        with set_module_args(set_args):
            with self.assertRaises(AnsibleExitJson) as exec_info:
                hf_download.run_module()

        result = exec_info.exception.kwargs
        self.assertTrue(result['changed'])
        self.assertEqual(result['resolved_filename'], 'llama-2-7b.Q4_K_M.gguf')
        self.assertEqual(
            result['downloaded_files'],
            ['/opt/llm/models/llama-2-7b.Q4_K_M.gguf'],
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HfApi"))
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    @patch.object(
        hf_download.AnsibleModule,
        'set_fs_attributes_if_different',
        return_value=False,
    )
    def test_download_with_token(
        self,
        mock_set_fs_attrs,
        mock_hf_hub_download,
        mock_path_exists,
        mock_hf_api,
    ):
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
            local_dir_use_symlinks='auto',
            repo_type='model',
            token='hf_test_token_xyz',
            force_download=False,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HfApi"))
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    @patch.object(
        hf_download.AnsibleModule,
        'set_fs_attributes_if_different',
        return_value=False,
    )
    def test_download_with_revision(
        self,
        mock_set_fs_attrs,
        mock_hf_hub_download,
        mock_path_exists,
        mock_hf_api,
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
            local_dir_use_symlinks='auto',
            repo_type='model',
            revision='refs/pr/1',
            force_download=False,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HfApi"))
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    @patch.object(
        hf_download.AnsibleModule,
        'set_fs_attributes_if_different',
        return_value=False,
    )
    def test_download_with_subfolder(
        self,
        mock_set_fs_attrs,
        mock_hf_hub_download,
        mock_path_exists,
        mock_hf_api,
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
            local_dir_use_symlinks='auto',
            repo_type='model',
            subfolder='tokenizers',
            force_download=False,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HfApi"))
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    @patch.object(
        hf_download.AnsibleModule,
        'set_fs_attributes_if_different',
        return_value=False,
    )
    def test_download_with_force_download(
        self,
        mock_set_fs_attrs,
        mock_hf_hub_download,
        mock_path_exists,
        mock_hf_api,
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
            local_dir_use_symlinks='auto',
            repo_type='model',
            force_download=True,
            local_files_only=False,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HfApi"))
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    @patch.object(
        hf_download.AnsibleModule,
        'set_fs_attributes_if_different',
        return_value=False,
    )
    def test_download_with_local_files_only(
        self,
        mock_set_fs_attrs,
        mock_hf_hub_download,
        mock_path_exists,
        mock_hf_api,
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
            local_dir_use_symlinks='auto',
            repo_type='model',
            force_download=False,
            local_files_only=True,
        )

    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HAS_HF_HUB"), True)
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HfApi"))
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    @patch.object(
        hf_download.AnsibleModule,
        'set_fs_attributes_if_different',
        return_value=False,
    )
    def test_download_check_mode(
        self,
        mock_set_fs_attrs,
        mock_hf_hub_download,
        mock_path_exists,
        mock_hf_api,
    ):
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
        self.assertEqual(
            result['downloaded_files'], ['/opt/llm/models/model.gguf']
        )
        self.assertEqual(result['resolved_filename'], 'model.gguf')
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
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.HfApi"))
    @patch('os.path.exists')
    @patch(make_absolute(MODULES_IMPORT_PATH, "hf_download.hf_hub_download"))
    def test_download_exception_handling(
        self, mock_hf_hub_download, mock_path_exists, mock_hf_api
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
            "Failed to download Hugging Face model "
            "'TheBloke/Llama-2-7B-Chat-GGUF': Network timeout error",
            result['msg'],
        )
