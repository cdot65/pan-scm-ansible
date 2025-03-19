# Strata Cloud Manager Ansible Collection - Contributing Guide

Hi there! We're excited to have you as a contributor.

If you have questions about this document or anything not covered here, feel free to create a topic using the [Strata Cloud Manager tag on the Ansible Forum](https://forum.ansible.com/tag/scm).

## Table of Contents

- [Things to Know Prior to Submitting Code](#things-to-know-prior-to-submitting-code)
- [Setting up Your Development Environment](#setting-up-your-development-environment)
  - [Fork and Clone the Repository](#fork-and-clone-the-repository)
  - [Build and Run the Development Environment](#build-and-run-the-development-environment)
- [What Should I Work On?](#what-should-i-work-on)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Reporting Issues](#reporting-issues)

## Things to Know Prior to Submitting Code

- All code submissions are done through pull requests against the `main` branch.
- Take care to make sure no merge commits are in the submission, and use `git rebase` vs `git merge` for this reason.
  - If collaborating with someone else on the same branch, consider using `--force-with-lease` instead of `--force`. This will prevent you from accidentally overwriting commits pushed by someone else. For more information, see [git push docs](https://git-scm.com/docs/git-push#git-push---force-with-leaseltrefnamegt).

## Setting up Your Development Environment

The development environment for the Strata Cloud Manager Ansible Collection can be managed using our `scripts/build.py` Typer application. This tool helps streamline the build, install, linting, and testing processes.

### Fork and Clone the Repository

If you have not done so already, you'll need to fork the Strata Cloud Manager Ansible Collection repository on GitHub. For more on how to do this, see [Fork a Repo](https://help.github.com/articles/fork-a-repo/).

### Build and Run the Development Environment

We provide a `scripts/build.py` Typer application to help you manage the development environment. Here are some common commands you can use:

- To build the collection:

  ```sh
  python scripts/build.py build --force
  ```

- To install the collection:

  ```sh
  python scripts/build.py install --force --version "0.1.0"
  ```

- To run linters:

  ```sh
  python scripts/build.py lint
  ```

- To run tests:

  ```sh
  python scripts/build.py pytest
  ```

For additional options, you can use `--help` with any command. For example:

```sh
python scripts/build.py build --help
```

## What Should I Work On?

Fixing bugs and updating documentation are always appreciated, so reviewing the backlog of issues is always a good place to start.

For feature work, take a look at the current enhancements in the issue tracker.

If you see an issue that has someone assigned to it, that person is responsible for working on the enhancement. If you feel like you could contribute, then reach out to that person.

**NOTES**

> Issue assignment will only be done for maintainers of the project. If you decide to work on an issue, please feel free to add a comment in the issue to let others know that you are working on it, but know that we will accept the first pull request from whoever is able to fix an issue. Once your PR is accepted, we can add you as an assignee to an issue upon request.

> If you work in a part of the codebase that is going through active development, your changes may be rejected, or you may be asked to rebase. A good idea before starting work is to have a discussion with us in the [Ansible Forum](https://forum.ansible.com/tag/scm).

## Submitting Pull Requests

Fixes and features for SCM will go through the GitHub pull request process. Submit your pull request (PR) against the `main` branch.

Here are a few things you can do to help the visibility of your change and increase the likelihood that it will be accepted:

- No issues when running linters/code checkers
  - Run linting using:

    ```sh
    python scripts/build.py lint
    ```

- No issues from unit tests
  - Run unit tests using:

    ```sh
    python scripts/build.py pytest
    ```

- Write tests for new functionality, update/add tests for bug fixes
- Make the smallest change possible
- Write good commit messages. See [How to write a Git commit message](https://chris.beams.io/posts/git-commit/).

We like to keep our commit history clean, and will require resubmission of pull requests that contain merge commits. Use `git pull --rebase`, rather than `git pull`, and `git rebase`, rather than `git merge`.

Sometimes it might take us a while to fully review your PR. We try to keep the `main` branch in good working order, so we review requests carefully. Please be patient.

When your PR is initially submitted, the checks will not be run until a maintainer allows them to. Once a maintainer has done a quick review of your work, the PR will have the linter and unit tests run against them via GitHub Actions, and the status reported in the PR.

## Reporting Issues

We welcome your feedback, and encourage you to file an issue when you run into a problem. But before opening a new issue, please view our [Issues guide](./ISSUES.md).
