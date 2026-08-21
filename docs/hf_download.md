
```shell
$ ansible --version
ansible [core 2.21.2]
  config file = None
  configured module search path = ['/Users/ljohnson/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /Users/ljohnson/.pyenv/versions/3.13.5/lib/python3.13/site-packages/ansible
  ansible collection location = /Users/ljohnson/tmp/_1CfXWw:/Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm
  executable location = /Users/ljohnson/.pyenv/versions/3.13.5/bin/ansible
  python version = 3.13.5 (main, Sep 18 2025, 19:11:35) [Clang 16.0.0 (clang-1600.0.26.6)] (/Users/ljohnson/.pyenv/versions/3.13.5/bin/python3.13)
  jinja version = 3.1.6
  pyyaml version = 6.0.3 (with libyaml v0.2.5)
$ REPO_DIR="$( git rev-parse --show-toplevel )"
$ cd ${REPO_DIR}
$ env ANSIBLE_NOCOLOR=True ansible-doc -t module dettonville.llm.hf_download | tee /Users/ljohnson/repos/ansible/ansible_collections/dettonville/llm/docs/hf_download.md
> MODULE dettonville.llm.hf_download (/Users/ljohnson/tmp/_1CfXWw/ansible_collections/dettonville/llm/plugins/modules/hf_download.py)

  Downloads models, datasets, or specific files from Hugging Face Hub
  using the huggingface_hub library. Features dynamic filename
  resolution, etag/hash checking for updates, authentication tokens,
  revisions, subfolders, force-download controls, file permission
  adjustments, and idempotent local cache management.

OPTIONS (= indicates it is required):

- attributes  The attributes the resulting filesystem object should
               have.
               To get supported flags look at the man page for
               `chattr' on the target system.
               This string should contain the attributes in the same
               order as the one displayed by `lsattr'.
               The `=' operator is assumed as default, otherwise `+'
               or `-' operators need to be included in the string.
        aliases: [attr]
        default: null
        type: str

- filename  Name of the specific file to download. If omitted, the
             module can resolve filenames matching standard patterns
             or download all repo files.
        default: null
        type: str

- force_download  Whether to force downloading files even if they
                   already match remote checksums.
        default: false
        type: bool

- group   Name of the group that should own the filesystem object, as
           would be fed to `chown'.
           When left unspecified, it uses the current group of the
           current user unless you are root, in which case it can
           preserve the previous ownership.
           Specifying a numeric group name (for example, "1000") will
           be assumed to be a group ID (GID) and not a group name. To
           prevent confusion, avoid using purely numeric group names.
        default: null
        type: str

= local_dir  Local folder where the file(s) should be downloaded.
        type: str

- local_dir_use_symlinks  Whether to use symlinks when downloading
                           files locally.
                           Auto-detects based on system capabilities
                           by default.
                           Option deprecated in recent huggingface_hub
                           versions; kept for signature backward
                           compatibility.
        default: auto
        type: raw

- local_files_only  Whether to only inspect local files without
                     checking HF Hub for remote updates.
        default: false
        type: bool

- mode    The permissions the resulting filesystem object should
           have.
           For those used to `/usr/bin/chmod' remember that modes are
           actually octal numbers. You must give Ansible enough
           information to parse them correctly. For consistent
           results, quote octal numbers (for example, `'644'' or
           `'1777'') so Ansible receives a string and can do its own
           conversion from string into number. Adding a leading zero
           (for example, `0755') works sometimes, but can fail in
           loops and some other circumstances.
           Giving Ansible a number without following either of these
           rules will end up with a decimal number which will have
           unexpected results.
           As of Ansible 1.8, the mode may be specified as a symbolic
           mode (for example, `u+rwx' or `u=rw,g=r,o=r').
           If `mode' is not specified and the destination filesystem
           object *does not* exist, the default `umask' on the system
           will be used when setting the mode for the newly created
           filesystem object.
           If `mode' is not specified and the destination filesystem
           object *does* exist, the mode of the existing filesystem
           object will be used.
           Specifying `mode' is the best way to ensure filesystem
           objects are created with the correct permissions. See
           CVE-2020-1736 for further details.
        default: null
        type: raw

- owner   Name of the user that should own the filesystem object, as
           would be fed to `chown'.
           When left unspecified, it uses the current user unless you
           are root, in which case it can preserve the previous
           ownership.
           Specifying a numeric username (for example, "1000") will be
           assumed to be a user ID (UID) and not a username. To
           prevent confusion, avoid using purely numeric usernames.
        default: null
        type: str

- quant_preference  Target quantization pattern (e.g., 'Q4_K_M',
                     'NVFP4') to automatically select a matching file
                     if `filename` is omitted.
        default: null
        type: str

= repo_id  The Hugging Face repository ID (e.g.,
            'unsloth/Qwen3.8-27B-GGUF').
        type: str

- repo_type  Type of repository ('model', 'dataset', 'space').
        choices: [model, dataset, space]
        default: model
        type: str

- revision  An optional revision ID (branch name, tag, or commit
             hash).
        default: null
        type: str

- selevel  The level part of the SELinux filesystem object context.
            This is the MLS/MCS attribute, sometimes known as the
            `range'.
            When set to `_default', it will use the `level' portion of
            the policy if available.
        default: null
        type: str

- serole  The role part of the SELinux filesystem object context.
           When set to `_default', it will use the `role' portion of
           the policy if available.
        default: null
        type: str

- setype  The type part of the SELinux filesystem object context.
           When set to `_default', it will use the `type' portion of
           the policy if available.
        default: null
        type: str

- seuser  The user part of the SELinux filesystem object context.
           By default it uses the `system' policy, where applicable.
           When set to `_default', it will use the `user' portion of
           the policy if available.
        default: null
        type: str

- subfolder  Subfolder inside the repository where the file is
              located.
        default: null
        type: str

- token   Hugging Face API token for authenticating gated or private
           repos.
        default: null
        type: str

- unsafe_writes  Influence when to use atomic operation to prevent
                  data corruption or inconsistent reads from the
                  target filesystem object.
                  By default this module uses atomic operations to
                  prevent data corruption or inconsistent reads from
                  the target filesystem objects, but sometimes systems
                  are configured or just broken in ways that prevent
                  this. One example is docker mounted filesystem
                  objects, which cannot be updated atomically from
                  inside the container and can only be written in an
                  unsafe manner.
                  This option allows Ansible to fall back to unsafe
                  methods of updating filesystem objects when atomic
                  operations fail (however, it doesn't force Ansible
                  to perform unsafe writes).
                  IMPORTANT! Unsafe writes are subject to race
                  conditions and can lead to data corruption.
        default: false
        type: bool

ATTRIBUTES:

        `check_mode:`
        description: Supports check mode to predict changes without downloading files.
        support: full

        `diff_mode:`
        description: Does not support diff mode.
        support: none

        `platform:`
        description: Target system must be POSIX-compliant.
        platforms: posix
        support: full

        `safe_file_operations:`
        description: Uses Ansible's atomic file creation and attributes handlers.
        support: full

        `vault:`
        description: Does not directly decrypt vault-encrypted payload files.
        support: none

AUTHOR: Lee Johnson (@lj020326)

EXAMPLES:
- name: Ensure LLM models are present and up to date
  dettonville.llm.hf_download:
    repo_id: "unsloth/Qwen3.8-27B-NVFP4"
    quant_preference: "UD-Q4_K_M"
    local_dir: "/opt/llm/models"
    token: "{{ lookup('env', 'HF_TOKEN') }}"
    owner: "vllm"
    group: "vllm"
  register: model_download_results

- name: Download a GGUF model file
  dettonville.llm.hf_download:
    repo_id: "TheBloke/Llama-2-7B-Chat-GGUF"
    filename: "llama-2-7b-chat.Q4_K_M.gguf"
    local_dir: "/opt/llm/models"
    owner: "vllm"
    group: "vllm"

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

- changed  Whether any downloads or file updates took place.
        returned: always
        type: bool

- downloaded_files  List of files downloaded or verified.
        returned: success
        type: list

- resolved_filename  Primary resolved filename that was downloaded.
        returned: success
        type: str

```
