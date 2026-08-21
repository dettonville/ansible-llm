
```shell
$ ansible --version
ansible [core 2.21.2]
  config file = None
  configured module search path = ['/Users/ljohnson/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /Users/ljohnson/.pyenv/versions/3.13.5/lib/python3.13/site-packages/ansible
  ansible collection location = /Users/ljohnson/tmp/_eGKuJl:/Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm
  executable location = /Users/ljohnson/.pyenv/versions/3.13.5/bin/ansible
  python version = 3.13.5 (main, Sep 18 2025, 19:11:35) [Clang 16.0.0 (clang-1600.0.26.6)] (/Users/ljohnson/.pyenv/versions/3.13.5/bin/python3.13)
  jinja version = 3.1.6
  pyyaml version = 6.0.3 (with libyaml v0.2.5)
$ REPO_DIR="$( git rev-parse --show-toplevel )"
$ cd ${REPO_DIR}
$ env ANSIBLE_NOCOLOR=True ansible-doc -t module dettonville.llm.ollama_api | tee /Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm/docs/ollama_api.md
> MODULE dettonville.llm.ollama_api (/Users/ljohnson/tmp/_eGKuJl/ansible_collections/dettonville/llm/plugins/modules/ollama_api.py)

  Manages Ollama models and checks service health using standard HTTP
  API endpoints.
  Provides capabilities to list available models, check running models
  in VRAM (ps), pull (download), create custom models, remove, and
  sync models against a target Ollama endpoint.
  Supports API key authentication via parameter or OLLAMA_API_KEY
  environment variable.

OPTIONS (= indicates it is required):

- action  Action to perform.
        choices: [health, version, list, ps, pull, create, delete, sync]
        default: list
        type: str

- api_auth_type  Type of HTTP authentication header to use.
        choices: [bearer, basic]
        default: bearer
        type: str

- api_key  Optional API token/key for authentication.
            API key or user:password basic auth credential for the
            Ollama endpoint.
            Can also be supplied via OLLAMA_API_KEY environment
            variable.
        default: null
        type: str

- model_file_path  Path to local Modelfile content for custom model
                    creation.
        default: null
        type: str

- model_list  List of model name strings to process in batch or sync
               against.
        aliases: [models]
        default: null
        elements: str
        type: list

- model_name  Single model name string to process or target for
               custom creation.
        aliases: [model]
        default: null
        type: str

= url     Base URL of the Ollama API service.
        aliases: [endpoint]
        type: str

- use_system_certs  Whether to use the truststore library to hook
                     Python's ssl module into the native system
                     certificate store.
        default: true
        type: bool

- validate_certs  Whether to validate SSL certificates for HTTPS
                   requests.
        default: true
        type: bool

AUTHOR: Lee Johnson (@lj020326)

EXAMPLES:
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

RETURN VALUES:

- base_url  The target endpoint URL used.
        returned: always
        type: str

- changed  Whether any modification or state change occurred.
        returned: always
        type: bool

- result  The JSON response dictionary or message returned from the
           Ollama API or action.
        returned: always
        type: raw

```
