[![codecov](https://codecov.io/gh/thclark/wagtail_events/branch/master/graph/badge.svg)](https://codecov.io/gh/thclark/wagtail_events)
[![Build Status](https://travis-ci.com/thclark/wagtail_events.svg?branch=master)](https://travis-ci.com/thclark/wagtail_events)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![black-girls-code](https://img.shields.io/badge/black%20girls-code-f64279.svg)](https://www.blackgirlscode.com/)

# Wagtail Events

Events calendar management for wagtail, with tools for filtering by date.

## Templates

**"But, where are the templates?!"** is a natural question. Answer: There aren't any templates or tags so far...
I run all my wagtail installations in headless mode with a react front end [like this example](https://www.traffickingpast.uk/events), so can only justify putting in place the
templates for managing the events on wagtail (for now). But see below for how to do it yourself.

If you'd like to make a PR with decent quality templates, I'm very open to collaboration, providing you're committed to maintaing them for a decent period of time :)

I'm gradually improving wagtail admin templates, I'll do an ever-better job as the library gets more traction and users.
**Bottom line: Star this repo on Github if you use or like it, so I know it's getting traction!**

## Background

This project is a hard fork of [omni-wagtail-events](http://github.com/omni-digital-omni-wagtail-events), and we owe a
debt of gratitude to those folks for getting us started. So why did I hard-fork (duplicate and start again) rather than
fork from omni-digital?

 - Well, github keeps the releases of the repo you fork from. I want to put this on pypi so it's easily available,
and have control of the release versioning (which isn't close to ready for v1.x where it started with omni-digital), so
 it needs to be here.
 - I'm basically about to break *everything* for django 2.x and wagtail 2.x, so I'd need a major version bump anyway, and
 figured that the chances of getting my changes merged into the upstream were nil.
 - The rich text fields make ``omni-wagtail-events`` a nightmare to use in headless API mode, and mean that most of the
 events data is unstructured. Here, we move to Wagtail's ``StreamField``... but that creates a
 [migration headache](http://docs.wagtail.io/en/v2.4/topics/streamfield.html#migrating-richtextfields-to-streamfield)
 unless we start fresh.
 - The migrations in the original project won't work with an in-memory database, so testing is slow.
 - I've majorly simplified the model structure to singleton events. I think this is all that's reqiured in 99.9% of cases.

I'm extremely open to collaboration - in fact, I really don't want to be maintaining this (it's only for one client) so
I'm open to transferring ownership or collaboration to anyone who wants to take this on and enhance it. @omni-digital,
this originated as your baby so if you'd like to take back maintenance, please reach out and I'll help you.


## Requirements

Wagtail events is tested against a range of python, django and wagtail versions - see tox.ini for the full test matrix.
Use out of these bounds and you're on your own!

## Getting started

Installing from pip:

```
pip install wagtail_events
```

Adding to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'wagtail_events',
    ...
]
```

Running the migrations:

```
python manage migrate wagtail_events
```

## Models

### EventIndex

An index/listing page for EventSeries instances, with optional pagination.

### Event

A detail page for an event, with start_date and optional end_date, implementing a manager which allows filtering on those dates.


## Abstract Models

You can use the abstract models and change them to suit your own needs:
- Do not install the app (don't enter it in `INSTALLED_APPS`)
- Create your own models inheriting from `wagtail_events.abstract_models.AbstractEvent` and `wagtail_events.abstract_models.AbstractEventIndex`




# Developer Notes

This section is only relevant if you plan to develop wagtail_events.

### Setup

Library is set up with the following integrations / features / life choices:

 - black style
 - pre-commit hooks
 - tox tests
 - travis ci + cd
 - code coverage

### Pre-Commit

You need to install pre-commit to get the hooks working. Do:
```
pip install pre-commit
pre-commit install
```

Once that's done, each time you make a commit, the following checks are made:

- valid github repo and files
- code style
- import order
- PEP8 compliance
- documentation build
- branch name

Upon failure, the commit will halt. **Re-running the commit will automatically fix most issues** except:

- The flake8 checks... hopefully over time Black (which fixes most things automatically already) will negate need for it.
- You'll have to fix documentation yourself prior to a successful commit (there's no auto fix for that!!).

You can run pre-commit hooks without making a commit, too, like:
```
pre-commit run black --all-files
```
or
```
pre-commit run build-docs
```


### Contributing

- Please raise an issue on the board (or add your $0.02 to an existing issue) so the maintainers know
what's happening and can advise / steer you.

- Create a fork of `wagtail_events`, undertake your changes on a new branch, named like *issue-84* or similar. To run tests and make commits,
you'll need to do something like:
```
git clone git@github.com:windpioneers/power-curve-utilities.git    # fetches the repo to your local machine
cd power_curve_utilities                # move into the repo directory
pyenv virtualenv 3.6.9 we-env          # Makes a virtual environment for you to install the dev tools into. Use any python >= 3.6
pyend activate we-env                  # Activates the virtual environment so you don't screw up other installations
pip install -r requirements-dev.txt     # Installs the testing and code formatting utilities
pre-commit install                      # Installs the pre-commit code formatting hooks in the git repo
tox                                     # Runs the tests with coverage. NB you can also just set up pycharm or vscode to run these.
```

- Adopt a Test Driven Development approach to implementing new features or fixing bugs.

- Ask the maintainers *where* to make your pull request. We'll create a version branch, according to the
roadmap, into which you can make your PR. We'll help review the changes and improve the PR.

- Once checks have passed, test coverage of the new code is >=95%, documentation is updated and the Review is passed, we'll merge into the version branch.

- Once all the roadmapped features for that version are done, we'll release.


### Release process

The process for creating a new release is as follows:

1. Check out a branch for the next version, called `release/X.Y.Z`
2. Create a Pull Request into the `master` branch.
3. Undertake your changes, committing and pushing to branch `release/X.Y.Z`
4. Ensure that documentation is updated to match changes, and increment the changelog. **Pull requests which do not update documentation will be refused.**
5. Ensure that test coverage is sufficient. **Pull requests that decrease test coverage will be refused.**
6. Ensure code meets style guidelines (pre-commit scripts and flake8 tests will fail otherwise)
7. Address Review Comments on the PR
8. Ensure the version in `setup.py` is correct and matches the branch version.
9. Merge to master. Successful test, doc build, flake8 and a new version number will automatically create the release on pypi.
10. Go to code > releases and create a new release on GitHub at the same SHA.
