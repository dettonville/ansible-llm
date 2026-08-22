## module > llama_api

Manage and query llama.cpp server states via API

- [Synopsis](#synopsis)
- [Parameters](#parameters)
- [Examples](#examples)
- [Return Values](#return-values)
- [CLI Reproducibility & Environment](#cli-reproducibility--environment)

## Synopsis

- Checks health, models, server properties, and slots from a specified llama.cpp server endpoint.

## Parameters

| Parameter | Choices / Defaults | Comments |
| :--- | :--- | :--- |
| **action**<br>`str` | Default: `"health"`<br>Choices:<br>- `health`<br>- `models`<br>- `props`<br>- `slots` | Action to perform. |
| **api_auth_type**<br>`str` | Default: `"bearer"`<br>Choices:<br>- `bearer`<br>- `basic` | Type of HTTP authentication header to use. |
| **api_key**<br>`str` |  | Optional API token/key for authentication. |
| **url**<br>`str / **required**` |  | Base URL of the llama.cpp API service.<br><br>*aliases:* `endpoint` |
| **use_system_certs**<br>`bool` | Default: `true` | Whether to use the truststore library. |
| **validate_certs**<br>`bool` | Default: `true` | Whether to validate SSL certificates for HTTPS requests. |

## Examples

```yaml
- name: Check health of llama.cpp server
  dettonville.llm.llama_api:
    url: "https://llama-cpp.example.com"
    action: "health"

- name: List models on llama.cpp server
  dettonville.llm.llama_api:
    url: "https://llama-cpp.example.com"
    action: "models"
```

## Return Values

| Key | Returned | Description |
| :--- | :--- | :--- |
| **base_url**<br>`(str)` | always | The target endpoint URL used. |
| **changed**<br>`(bool)` | always | Whether any modification or state change occurred. |
| **status**<br>`(raw)` | always | The JSON response dictionary or message returned from the API. |

## CLI Reproducibility & Environment

To view this module documentation directly in your terminal or replicate the output:

```shell
$ ansible --version
ansible [core 2.21.2]
  config file = None
  configured module search path = ['/Users/ljohnson/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /Users/ljohnson/.pyenv/versions/3.13.5/lib/python3.13/site-packages/ansible
  ansible collection location = /var/folders/w6/3rcdpp211v5cxml6vg45ww3r0000gn/T/ansible_doc_lk91a344
  executable location = /Users/ljohnson/.pyenv/versions/3.13.5/bin/ansible
  python version = 3.13.5 (main, Sep 18 2025, 19:11:35) [Clang 16.0.0 (clang-1600.0.26.6)] (/Users/ljohnson/.pyenv/versions/3.13.5/bin/python3.13)
  jinja version = 3.1.6
  pyyaml version = 6.0.3 (with libyaml v0.2.5)
$ REPO_DIR="$( git rev-parse --show-toplevel )"
cd ${REPO_DIR}
$ env ANSIBLE_NOCOLOR=True ansible-doc -t module dettonville.llm.llama_api | tee /Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm/docs/llama_api.md
> MODULE dettonville.llm.llama_api (/var/folders/w6/3rcdpp211v5cxml6vg45ww3r0000gn/T/ansible_doc_lk91a344/ansible_collections/dettonville/llm/plugins/modules/llama_api.py)

  Checks health, models, server properties, and slots from a specified
  llama.cpp server endpoint.

OPTIONS (= indicates it is required):

- action  Action to perform.
        choices: [health, models, props, slots]
        default: health
        type: str

- api_auth_type  Type of HTTP authentication header to use.
        choices: [bearer, basic]
        default: bearer
        type: str

- api_key  Optional API token/key for authentication.
        default: null
        type: str

= url     Base URL of the llama.cpp API service.
        aliases: [endpoint]
        type: str

- use_system_certs  Whether to use the truststore library.
        default: true
        type: bool

- validate_certs  Whether to validate SSL certificates for HTTPS
                   requests.
        default: true
        type: bool

AUTHOR: Lee Johnson (@lj020326)

EXAMPLES:
- name: Check health of llama.cpp server
  dettonville.llm.llama_api:
    url: "https://llama-cpp.example.com"
    action: "health"

- name: List models on llama.cpp server
  dettonville.llm.llama_api:
    url: "https://llama-cpp.example.com"
    action: "models"

RETURN VALUES:

- base_url  The target endpoint URL used.
        returned: always
        type: str

- changed  Whether any modification or state change occurred.
        returned: always
        type: bool

- status  The JSON response dictionary or message returned from the
           API.
        returned: always
        type: raw
```
