
```shell
$ ansible --version
ansible [core 2.21.2]
  config file = None
  configured module search path = ['/Users/ljohnson/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /Users/ljohnson/.pyenv/versions/3.13.5/lib/python3.13/site-packages/ansible
  ansible collection location = /Users/ljohnson/tmp/_DdDkHx:/Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm
  executable location = /Users/ljohnson/.pyenv/versions/3.13.5/bin/ansible
  python version = 3.13.5 (main, Sep 18 2025, 19:11:35) [Clang 16.0.0 (clang-1600.0.26.6)] (/Users/ljohnson/.pyenv/versions/3.13.5/bin/python3.13)
  jinja version = 3.1.6
  pyyaml version = 6.0.3 (with libyaml v0.2.5)
$ REPO_DIR="$( git rev-parse --show-toplevel )"
$ cd ${REPO_DIR}
$ env ANSIBLE_NOCOLOR=True ansible-doc -t module dettonville.llm.hf_download | tee /Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm/docs/hf_download.md
> MODULE dettonville.llm.hf_download (/Users/ljohnson/tmp/_DdDkHx/ansible_collections/dettonville/llm/plugins/modules/hf_download.py)

  Downloads models, datasets, or specific files from Hugging Face Hub
  using the huggingface_hub library, supporting authentication tokens,
  revisions, subfolders, and force-download controls.

OPTIONS (= indicates it is required):

= filename  Name of the specific file to download from the
             repository.
        type: str

- force_download  Whether to force downloading the file even if it
                   exists locally.
        default: false
        type: bool

= local_dir  Local folder where the file should be downloaded.
        type: str

- local_files_only  Whether to only look at local files and avoid
                     checking/downloading updates.
        default: false
        type: bool

= repo_id  The Hugging Face repository ID (e.g.,
            'TheBloke/Llama-2-7B-Chat-GGUF').
        type: str

- repo_type  Type of repository ('model', 'dataset', 'space').
        choices: [model, dataset, space]
        default: model
        type: str

- revision  An optional revision id which can be a branch name, a
             tag, or a commit hash.
        default: null
        type: str

- subfolder  Subfolder inside the repository where the file is
              located.
        default: null
        type: str

- token   Hugging Face API token for authenticating private or gated
           repositories.
        default: null
        type: str

AUTHOR: Lee Johnson (@lj020326)

EXAMPLES:
- name: Download a GGUF model file
  dettonville.llm.hf_download:
    repo_id: "TheBloke/Llama-2-7B-Chat-GGUF"
    filename: "llama-2-7b-chat.Q4_K_M.gguf"
    local_dir: "/opt/llm/models"

- name: Download a gated model file using authentication token
  dettonville.llm.hf_download:
    repo_id: "meta-llama/Meta-Llama-3-8B-Instruct"
    filename: "model.safetensors"
    local_dir: "/opt/llm/models/llama3"
    token: "{{ lookup('env', 'HF_TOKEN') }}"

- name: Download a file from a specific revision/branch
  dettonville.llm.hf_download:
    repo_id: "mistralai/Mistral-7B-v0.1"
    filename: "config.json"
    local_dir: "/opt/llm/models/mistral"
    revision: "refs/pr/1"

- name: Download a file located within a repository subfolder
  dettonville.llm.hf_download:
    repo_id: "unsloth/llama-3-8b-Instruct-bnb-4bit"
    filename: "tokenizer.json"
    local_dir: "/opt/llm/models/unsloth"
    subfolder: "tokenizers"

- name: Force re-download a file ignoring local cache
  dettonville.llm.hf_download:
    repo_id: "TheBloke/Llama-2-7B-Chat-GGUF"
    filename: "llama-2-7b-chat.Q4_K_M.gguf"
    local_dir: "/opt/llm/models"
    force_download: true

- name: Restrict downloads to local cache only
  dettonville.llm.hf_download:
    repo_id: "TheBloke/Llama-2-7B-Chat-GGUF"
    filename: "llama-2-7b-chat.Q4_K_M.gguf"
    local_dir: "/opt/llm/models"
    local_files_only: true

RETURN VALUES:

- changed  Whether a download actually took place.
        returned: always
        type: bool

- path    Path to the downloaded file.
        returned: success
        type: str

```
