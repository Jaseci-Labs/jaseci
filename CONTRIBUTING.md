# Contributing to the Jaseci Open Source Project

- [How to start contributing](#how-to-start-contributing)
  - [Working on a new feature or fixing a bug you found](#working-on-a-new-feature-or-fixing-a-bug-you-found)
  - [Work on an existing issue](#work-on-an-existing-issue)
- [How to contribute code](#how-to-contribute-code)
  - [What is a Pull Request (PR)?](#what-is-a-pull-request--pr--)
  - [How to open a PR and contribute code to Jaseci Open Source](#how-to-open-a-pr-and-contribute-code-to-jaseci-open-source)
    - [1. Forking the Jaseci Repository](#1-forking-the-jaseci-repository)
    - [2. Cloning the Forked Repository Locally](#2-cloning-the-forked-repository-locally)
    - [3. Update your Forked Repository](#3-update-your-forked-repository)
    - [4. Implement your code contribution on a feature branch](#4-implement-your-code-contribution-on-a-feature-branch)
    - [5. Push changes to your forked repository on GitHub](#5-push-changes-to-your-forked-repository-on-github)
    - [6. Opening the Pull Request on Jaseci Open Source](#6-opening-the-pull-request-on-jaseci-open-source)
    - [8. Merging your PR and the final steps of your contribution](#8-merging-your-pr-and-the-final-steps-of-your-contribution)
  - [Things to know about creating a PR](#things-to-know-about-creating-a-pr)
    - [Opening issues before PRs](#opening-issues-before-prs)
    - [Draft/Work-in-progress(WIP) PRs](#draft-work-in-progress-wip--prs)
    - [Code style & Linting](#code-style---linting)
  - [CI/CD](#ci-cd)
- [How to Update the Official Documentation](#how-to-update-the-official-documentation)

---

## How to start contributing

Welcome to Jaseci! To start contributing, we would like you to start with issues.

### Working on a new feature or fixing a bug you found

If you would like to add a new feature or fix a bug you have found, we prefer that you open a new issue in the Github repo before creating a pull request.

It’s important to note that when opening an issue, you should first do a quick search of existing issues to make sure your suggestion hasn’t already been added as an issue.
If your issue doesn’t already exist, and you’re ready to create a new one, make sure to state what you would like to implement, improve or bugfix.

### Work on an existing issue

If you want to contribute code, but don't know what to work on, check out the existing list of issues

Certain issues are marked with the "good first issue" label. These are issues that we think are great for first time contributor to work on while they are still getting familarized with the Jaseci codebase.

To work on an existing issue, go to the issue in Github, add a comment stating you would like to work on it and include any solutions you may already have in mind. Assign the issue to yourself.

The Jaseci team will then work with you on the issue and the downstream pull request to guide you through merging your code into the Jaseci codebase.

---

## How to contribute code

Code contribution will be in the form of Pull Request (PR) on Github.

### What is a Pull Request (PR)?

This is how the GitHub team defines a PR:

> “Pull requests let you tell others about changes you’ve pushed to a branch in a repository on GitHub. Once a pull request is opened, you can discuss and review the potential changes with collaborators and add follow-up commits before your changes are merged into the base branch.”

This process is used by both Jaseci team members and Jaseci contributors to make changes and improvements.

### How to open a PR and contribute code to Jaseci Open Source

#### 1. Forking the Jaseci Repository

Head to Jaseci repository and click ‘Fork’. Forking a repository creates you a copy of the project which you can edit and use to propose changes to the original project.

Once you fork it, a copy of the Jaseci repository will appear inside your GitHub repository list, under your username.

#### 2. Cloning the Forked Repository Locally

To make changes to your copy of the Jaseci repository, clone the repository on your local machine. To do that, run the following command in your terminal:

```
git clone https://github.com/your_github_username/jaseci.git
```

Note: this assumes you have git installed on your local machine. If not, check out the [following guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to learn how to install it.

#### 3. Update your Forked Repository

Before you make any changes to your cloned repository, make sure you have the latest version of the original Jaseci repository. To do that, run the following commands in your terminal:

```
cd jaseci
git remote add upstream https://github.com/Jaseci-Labs/jaseci.git
git pull upstream main
```

This will update the local copy of the Jaseci repository to the latest version.

#### 4. Implement your code contribution on a feature branch

We recommend you to add your code contribution to a new branch (different from main). Then you can continuously run the previous step to always keep the `main` branch in your forked repo up-to-date with the original repo. This way you have the flexibility to easily inspect your changes and resolve any potential merge conflicts all within the forked repo.

```
git checkout -b name-of-your-new-branch
```

#### 5. Push changes to your forked repository on GitHub

Once you are happy with the changes you made in the local files, push them to the forked repository on GitHub. To do that, run the following commands:

```
git add .
git commit -m ‘fixed a bug’
git push origin name-of-your-new-branch
```

This will create a new branch on your forked Jaseci repository, and now you’re ready to create a Pull Request with your proposed changes!

#### 6. Opening the Pull Request on Jaseci Open Source

Head to the forked repository and click on a _Compare & pull_ request button.

This will open a window where you can choose the repository and branch you would like to propose your changes to, as well as specific details of your contribution. In the top panel menu choose the following details:

- Base repository: `Jaseci-Labs/jaseci`
- Base branch: `main`
- Head repository: `your-github-username/jaseci`
- Head branch: `name-of-your-new-branch`

Next, make sure to update the pull request card with as many details about your contribution as possible. _Proposed changes_ section should contain the details of what has been fixed/implemented, and Status should reflect the status of your contributions. Any reasonable change (not like a typo) should include a changelog entry, a bug fix should have a test, a new feature should have documentation, etc.

Once you are happy with everything, click the _Create pull request_ button. This will create a Pull Request with your proposed changes.

If you are ready to get feedback on your contribution from the Jaseci team, leave a comment on the PR.

#### 8. Merging your PR and the final steps of your contribution

A member from the Jaseci team will review your PR and might ask you to make additional changes and update. To update your PR, head back to the local copy of your repo, implement the changes requested and repeat the same steps above. Your PR will _automatically_ be updated with your latest changes. Once you've implemented all of the suggested changes, tag the person who first reviewed your PR in a comment of the PR to ask them to review again.

Finally, if your contribution is accepted, one of the Jaseci team member will merge it to the codebase!

### Things to know about creating a PR

#### Opening issues before PRs

Like, mentioned above, We recommend opening an issue before a pull request if there isn’t already an issue for the problem you’d like to solve. This helps facilitate discussions and tracking progress.

#### Draft/Work-in-progress(WIP) PRs

If you're ready to get some quick initial feedback from the Jaseci team, you can create a draft pull request. You can prefix the PR title with [WIP] to indicate this is still work in progres.

#### Validate your changes through test

Jaseci has a set of automated tests and PRs are required to pass these tests for them to be merge into the main branch. So we recommend you to validate your changes via these tests before creating a PR. Checkout `scripts/script_sync_code_kube_test` to see how to run the tests.

#### Code style & Linting

To standardize coding style, Jaseci code is enforeced by the flake8 linter and a set of linting rules. Please run the linting command to check your code style before creating a PR.

```
flake8 --exclude=settings.py,*migrations*,jac_parse --max-line-length=88 --extend-ignore = E203,
```

---
## CI/CD

Jaseci uses the Github Actions to handle a series of Continuous Integration (CI) and Continuous Deployment (CD) processes.

### Regression Tests on PR

Every PR automatically triggers a set of regression tests for each of the main module of Jaseci, as well as a liniting check. PRs are required to pass all tests including linting before it can be merged. You can check the status of the regression tests in your PR summary view. It will look like the following:

![](https://lh5.googleusercontent.com/0H4GQQ0ljj0SxRf9yjSJA5O0xMpcd6TQWp1bXmO2El-SwoZbU340vhIYTZha1yt8Kcw=w2400)

### Build and Release

Jaseci is released through two channels: Python packages on pypi and docker images on DockerHub. On every new tag creation, a github action workflow `build-and-release` will trigger and build and release the python packages and docker images for that tag.

* Three python packages are built and released to pypi, `jaseci`, `jaseci-serv` and `jaseci-ai-kit`
* Two docker images are built and released to DockerHub, `jaseci/jaseci:VERSION` which contains the core jaseci modules and `jaseci/jaseci-ai:VERSION` which also include the AI modules in `jaseci-ai-kit`. The tag of the repo, python package version and docker image tags are kept in sync. For example, when a tag `v2.0.3` is created for the code repo, the python packages will be versioned `2.0.3` and the docker images will have the same tag, as `jaseci/jaseci:2.0.3` and `jaseci/jaseci-ai:2.0.3`.

![](https://lh5.googleusercontent.com/7MthpUaanAXO9kMhgFzZ9jHd0InjJOrrZaQfOXMp9S9Og8LwcI-WHG6CtWSQzb1GKF8=w2400)

---

## How to Update the Official Documentation

The source of the Jaseci Official Documentation comes from the collection of `README.md` files placed in specific folders throughout the codebase. Developers and Maintainers must ensure that their contributions are properly documented according to the following procedures outlined in this section.

### Adding a new module or library

Ensure that you follow the prevailing directory sturcture convention when adding a new module or library to Jaseci.

* All source files belonging to your module or library must be contained within a folder bearing the non-whitespace, lowercase name of your module or library.
* You must author a `README.md` document to describe the purpose of your module or library, any features, configurations or uses as well as code excerpts on how to implement your module's functionaliy.
* The `README.md` must be included in the root folder of the module or library.
* Ensure you update the related `README.md` in the subsection (if applicable) which contains your module, e.g. `jaseci_ai_kit/README.md` as well as the main `README.md` in the root directory of the codebase to include references to your new module or library.


### Adding a new code lab example

All codelabs are organized within the `/support/codelabs` folder. You may add new codelabs to this folder by following the prescribed guidelines below:

* Ensure that your codelab is organized within its own named folder. Ensure you use all lowercase, non-whitespace names.
* Ensure your new codelab has its own `README.md` file placed in its root folder. This should be the main page of the documented codelab.
* If any images are used, ensure they are stored in the `[your_code_lab]/assets` folder and referenced using relative paths.
* Once the codelab is added, ensure that you update the main `README.md` in the root directory of the codebase to include references to your new codelab under the section "Samples and Tutorials".

### Adding a new guide

All informational content which do not directly refer to modules / libraries or codelabs are typically stored under the `/support/guide` folder.

* Ensure that your new guide is contained within its own named folder. Ensure you use all lowercase, non-whitespace names.
* If any images are used, ensure they are stored in the `[your_guide]/assets` folder and referenced using relative paths.
* The markdown pages of your guide must be named based on the title of the rendered page in lowercase, non-whitepsace characters, e.g. `this_is_my_guide.md`.
* Once the guide is added, ensure that you update the main `README.md` in the root directory of the codebase to include references to your new guide under the applicable section.
* To include your images to the documentation include the path to the folder in to this file `scripts/gen_mdbook.py` in the ` imageFiles` list .