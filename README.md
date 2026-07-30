[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](LICENSE.md)

# Dettonville Ansible LLM Collection

The Ansible `dettonville.llm` collection includes plugins and modules designed to integrate Large Language Models (LLMs)
and local AI services into Ansible playbooks. This collection provides tools to streamline AI-driven workflows, manage
models, and query LLM APIs with a focus on simplicity and reliability.

## CI Status

[![CI](https://github.com/dettonville/ansible-llm/actions/workflows/all_green_publish.yml/badge.svg?branch=main)](https://github.com/dettonville/ansible-llm/actions/workflows/all_green_publish.yml)

## Requirements

The host running the tasks must have the python requirements described
in [requirements.txt](https://github.com/dettonville/ansible-llm/blob/main/requirements.txt). Once the collection is
installed, you can install them into a python environment using pip: `pip install -r requirements.txt`

<!--start requires_ansible-->

## Ansible Version Compatibility

This collection has been tested against the following Ansible versions: **>=2.16.0**.

Plugins and modules within a collection may be tested with only specific Ansible versions. A collection may contain
metadata that identifies these versions. PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Included Content

<!--start collection content-->

### Modules

| Name                                                                                             | Description                                    |
|--------------------------------------------------------------------------------------------------|------------------------------------------------|
| [ollama_api](https://github.com/dettonville/ansible-llm/blob/main/plugins/modules/ollama_api.py) | Manage Ollama models and query states via API. |

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

* [Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) in the Ansible
  documentation for more details.

## Contributing to This Collection

This collection is intended for LLM and AI integration plugins and modules. Simple plugin examples should be generic in
nature. More complex examples can include real-world platform modules to demonstrate the utility of the plugin in a
playbook.

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against
the [dettonville.llm collection repository](https://github.com/dettonville/ansible-llm).
See [Contributing to Ansible-maintained collections](https://docs.ansible.com/ansible/devel/community/contributing_maintained_collections.html#contributing-maintained-collections)
for complete details.

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on
contributing to Ansible.

---

## Testing

All releases will meet the following test criteria:

* 100% success for [Unit](https://github.com/dettonville/ansible-llm/blob/main/tests/unit) tests.
* 100% success
  for [Sanity](https://docs.ansible.com/ansible/latest/dev_guide/testing/sanity/index.html#all-sanity-tests) tests as
  part of [ansible-test](https://docs.ansible.com/ansible/latest/dev_guide/testing.html#run-sanity-tests).
* 100% success for [Integration](https://github.com/dettonville/ansible-llm/blob/main/tests/integration) tests.
* 100% success for [ansible-lint](https://ansible.readthedocs.io/projects/lint/) allowing only false positives.

### Developer Notes

- 100% code coverage is the goal, although it's not always possible.
- Include unit and integration tests with all PRs. PRs should not decrease code coverage.
- Filter plugins should be 1 per file, with an included DOCUMENTATION string, or reference a lookup plugin with the same
  name.

### How to run tests

See the [TESTING.md](TESTING.md) for information on how to run the necessary tests.

---

## Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

---

## Release Notes

Release notes are available [here](https://github.com/dettonville/ansible-llm/blob/main/changelogs/CHANGELOG.rst).
For automated release announcements, refer [here](https://twitter.com/AnsibleContent).

---

## Roadmap

For information on releasing, versioning, and deprecation, see
the [strategy document](https://access.redhat.com/articles/4993781).

In general, major versions can contain breaking changes, while minor versions only contain new features (like new plugin
addition) and bugfixes. The releases will be done on an as-needed basis when new features and/or bugfixes are done.

---

## 🛡️ Identity & Maintainer

* **Maintainer:** Lee Johnson
* **Contact:** <ljohnson@dettonville.org>
* **LinkedIn:** https://www.linkedin.com/in/leejjohnson/
* **System Framework:** [Dettonville Cloud Infrastructure Services](https://dettonville.org)

---

## More Information

- [Dettonville Cloud Infrastructure Services](https://dettonville.org)
- [Ansible Datacenter Site Example](https://github.com/lj020326/ansible-datacenter) - An actual datacenter site.yml
  repository featuring roles that demonstrate
  practical usage of the collection modules.
- [Ansible Collection Overview](https://github.com/ansible-collections/overview)
- [Ansible User Guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
