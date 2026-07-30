
# Unit Testing

## Running the tests directly

```shell
ansible-test units --requirements --python 3.13
ansible-test units --python 3.13 ollama_api
ansible-test units --python 3.13 tests/unit/plugins/modules/test_ollama_api.py
ansible-test units ollama_api | tee -a ansible-test-unit-results.log
ansible-test units -v --color no --truncate 0 --coverage --docker --python 3.13 ollama_api | tee ansible-test-unit-docker-results.log
ansible-test units --python 3.13 --containers '{}' --color yes
ansible-test units --python 3.13 --containers '{}' --truncate 0 --color yes
ansible-test units -v --python 3.13 --containers '{}' --coverage --truncate 0 --color yes
ansible-test units --docker -v --python 3.13 ollama_api
ansible-test units --docker -v --python 3.13 git_pacp
```

### To run individual test

```shell
$ ansible-test units --python 3.13 -v plugins/modules/test_ollama_api.py::test_ollama_pull_model
```

### To enable/view module log output during test

1) Add this block at the top of the test file (right after imports, before the class definition):
```Python
# Force module logging to console during tests
import logging
logging.getLogger('ansible_collections.dettonville.llm.plugins.modules.ollama_api').setLevel(logging.DEBUG)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
```
This will make all log.debug, log.info, log.warning, log.error calls from the module appear in the pytest console output when the test runs.

2) Force the module to use a known logging level (optional but helpful)

In the test, explicitly set:
```python
params = {
    "content": raw_pem,
    "validate_expired": True,
    "logging_level": "DEBUG",          # ← changed to DEBUG
}
```
This ensures maximum verbosity from the module itself.

3) Run the test with verbose output

Run the failing test with extra verbosity so you see both pytest output and the module's log lines:
```Bash
ansible-test units --python 3.13 ollama_api -v | grep -E 'raw_pem|DEBUG|INFO|WARNING|ERROR|fail_json|exception|content'
#ansible-test units --python 3.13 -v plugins/modules/test_ollama_api.py::TestX509CertificateVerifyModule::test_content_raw_pem_success
```

### Create test coverage results
```shell
ansible-test units --python 3.13 ollama_api --coverage --verbose
```

Generate a new coverage report
```shell
ansible-test coverage report
ansible-test coverage html
open tests/output/reports/coverage/index.html
```

Check if the coverage for ollama_api.py improves (e.g., closer to 90–95%). If missed lines remain, review the HTML report to identify them.

```shell
## ref: https://github.com/ansible/ansible/issues/27446#issuecomment-318777441
export PYTHONPATH=$PYTHONPATH:/path/to/your/ansible_collections
pytest -r a --color yes path/to/the/test(s) -vvv
```

```shell
cd ${HOME}/repos/ansible/ansible_collections/dettonville/llm
export PYTHONPATH=${HOME}/repos/ansible
## show logs for failed tests
pytest -s --color yes tests/unit/plugins/modules/test_ollama_api.py
## show logs for all tests (success and failed)
pytest -rP --color yes tests/unit/plugins/modules/test_ollama_api.py
## turn up verbosity
pytest -vvv -r a --color yes tests/unit/plugins/modules/test_ollama_api.py
pytest -r a --color yes tests/unit/plugins/modules/test_git_pacp.py -vvv
pytest -r a --color yes tests/unit/plugins/modules/test_git_pacp.py::TestGitPacpModule::test_setup_module_object
pytest -s --color yes tests/unit/plugins/modules/test_git_pacp.py::TestGitActions::test_write_ssh_wrapper_content

```

when using the python 'logging' module, need to specify to turn on logging output in addition to -s for generic stdout. Based on Logging within pytest tests:
ref: https://stackoverflow.com/questions/4673373/logging-within-pytest-tests

```shell
pytest --log-cli-level=DEBUG -s --color yes tests/unit/plugins/modules/test_git_pacp.py::TestGitActions::test_write_ssh_wrapper_content
pytest --log-cli-level=DEBUG -s --color yes tests/unit/plugins/modules/test_git_pacp.py::TestGitActions::test_get_url_scheme_https
pytest --log-cli=true -s --color yes tests/unit/plugins/modules/test_git_pacp.py::TestGitActionsErrorHandling::test_push_remote_add_failure
```

To avoid having to add the log-cli option to the pytest command each time, add the following content to the pytest.ini:
```ini
[pytest]
log_cli = 1
log_cli_level = ERROR
log_cli_format = %(message)s

log_file = pytest.log
log_file_level = DEBUG
log_file_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
log_file_date_format=%Y-%m-%d %H:%M:%S

```

```shell
ansible-test units --docker -v --python 3.13
```

```shell
pytest -r a -n auto --color yes -p no:cacheprovider \
  --rootdir /Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm \
  --confcutdir /Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm \
  tests/unit/plugins/modules/test_ollama_api.py

pytest -r a -n auto --color yes -p no:cacheprovider \
  -c /Users/ljohnson/.pyenv/versions/3.13.3/lib/python3.13/site-packages/ansible_test/_data/pytest/config/default.ini \
  --junit-xml /Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm/tests/output/junit/python3.13-modules-units.xml \
  --strict-markers \
  --rootdir /Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm \
  --confcutdir /Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm \
  tests/unit/plugins/modules/test_ollama_api.py
```



```shell
cd ${PROJECT_DIR}/tests/unit/plugins/modules

# Run all tests
python -m unittest test_ollama_api.py -v
python -m unittest test_ollama_api -v

# Run individual test
python -m unittest test_ollama_api.test_ollama_pull_model -v
```
