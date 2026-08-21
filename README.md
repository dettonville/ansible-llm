[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](LICENSE.md)

# Dettonville Ansible LLM Collection

## Table of Contents

* [Summary](#summary)
* [CI Status](#ci-status)
* [Requirements](#requirements)
* [Ansible Version Compatibility](#ansible-version-compatibility)
* [Included Content](#included-content)
* [Installing This Collection](#installing-this-collection)
* [Using This Collection](#using-this-collection)
* [Contributing to This Collection](#contributing-to-this-collection)
* [Testing](#testing)
* [Code of Conduct](#code-of-conduct)
* [🛡Identity & Maintainer](#identity-maintainer)
* [More Information](#more-information)

---

## Summary

The Ansible `dettonville.llm` collection includes plugins and modules designed to integrate Large Language Models (LLMs) and local AI services into Ansible playbooks. This collection provides tools to streamline AI-driven workflows, manage models, and query LLM APIs with a focus on simplicity and reliability.

## CI Status

[![🧪 GitHub Actions CI/CD workflow tests badge]][GHA workflow runs list]
[![pre-commit.ci status badge]][pre-commit.ci results page]

## Requirements

The host running the tasks must have the python requirements described in [requirements.txt](https://github.com/dettonville/ansible-llm/blob/main/requirements.txt). Once the collection is installed, you can install them into a python environment using pip: `pip install -r requirements.txt`

<!--start requires_ansible-->

## Ansible Version Compatibility

This collection has been tested against the following Ansible versions: **>=2.16.0**.

Plugins and modules within a collection may be tested with only specific Ansible versions. A collection may contain metadata that identifies these versions. PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Included Content

<!--start collection content-->

### Modules

| Documentation                                                                           | Source code                                                                                           | Description                                                                                                                                           |
|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| [hf_download](https://github.com/dettonville/ansible-llm/blob/main/docs/hf_download.md) | [hf_download.py](https://github.com/dettonville/ansible-llm/blob/main/plugins/modules/hf_download.py) | Downloads models, datasets, or specific files from Hugging Face Hub using the huggingface_hub library.                                                |
| [llama_api](https://github.com/dettonville/ansible-llm/blob/main/docs/llama_api.md)     | [llama_api.py](https://github.com/dettonville/ansible-llm/blob/main/plugins/modules/llama_api.py)     | Checks health, models, server properties, and slots from a specified llama.cpp server endpoint.                                                       |
| [ollama_api](https://github.com/dettonville/ansible-llm/blob/main/docs/ollama_api.md)   | [ollama_api.py](https://github.com/dettonville/ansible-llm/blob/main/plugins/modules/ollama_api.py)   | Provides capabilities to list available models, check running models (ps), pull (download), sync, and remove models from a specified Ollama endpoint. |
| [vllm_api](https://github.com/dettonville/ansible-llm/blob/main/docs/vllm_api.md)       | [vllm_api.py](https://github.com/dettonville/ansible-llm/blob/main/plugins/modules/vllm_api.py)       | Checks health, models, version, and metrics from a specified vLLM server endpoint.                                                                    |

<!--end collection content-->

## Installing This Collection

You can install the `dettonville.llm` collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install dettonville.llm

You can also include it in a `requirements.yml` file and install it with
`ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: dettonville.llm
```

### See Also:

* [Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) in the Ansible documentation for more details.

## Contributing to This Collection

This collection is intended for LLM and AI integration plugins and modules. Simple plugin examples should be generic in nature. More complex examples can include real-world platform modules to demonstrate the utility of the plugin in a playbook.

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [dettonville.llm collection repository](https://github.com/dettonville/ansible-llm). See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections) for complete details.

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.

---

## Testing

All releases will meet the following test criteria:

* 100% success for [Unit](https://github.com/dettonville/ansible-llm/blob/main/tests/unit) tests.
* 100% success for [Sanity](https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/index.html#all-sanity-tests) tests as part of [ansible-test](https://docs.ansible.com/ansible/latest/dev_guide/testing.html#run-sanity-tests).
* 100% success for [ansible-lint](https://ansible.readthedocs.io/projects/lint/).

### Developer Notes

- Include unit tests with all PRs. PRs should not decrease code coverage.
- Filter plugins should be 1 per file, with an included DOCUMENTATION string, or reference a lookup plugin with the same name.

### How to run tests

See the [TESTING.md](TESTING.md) for information on how to run the necessary tests.

---

## Code of Conduct

This collection follows the Ansible project's [Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

---

## <a id="identity-maintainer"></a>🛡️ Identity & Maintainer

* **Maintainer:** Lee Johnson
* **Contact:** <ljohnson@dettonville.org>
* **LinkedIn:** https://www.linkedin.com/in/leejjohnson/
* **System Framework:** [Dettonville Cloud Infrastructure Services](https://dettonville.org)

---

## More Information

- [Dettonville Cloud Infrastructure Services](https://dettonville.org)
- [Dettonville Utils Collection](https://github.com/dettonville/ansible-utils)
- [Dettonville Git Inventory Collection](https://github.com/dettonville/ansible-git-inventory)
- [**Ansible Datacenter Site Example**](https://github.com/lj020326/ansible-datacenter) - An actual datacenter site.yml repository featuring roles that demonstrate practical usage of the collection modules.
- [Ansible Collection Overview](https://github.com/ansible-collections/overview)
- [Ansible User Guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

[🧪 GitHub Actions CI/CD workflow tests badge]:
https://github.com/dettonville/ansible-llm/actions/workflows/all_green_publish.yml/badge.svg?branch=main&event=push
[GHA workflow runs list]: https://github.com/dettonville/ansible-llm/actions/workflows/all_green_publish.yml?query=branch%3Amain

[pre-commit.ci status badge]:
https://results.pre-commit.ci/badge/github/dettonville/ansible-llm/main.svg
[pre-commit.ci results page]:
https://results.pre-commit.ci/latest/github/dettonville/ansible-llm/main
