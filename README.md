# Wagtail Events [![Build Status](https://travis-ci.com/thclark/wagtail_events.svg?branch=master)](https://travis-ci.com/thclark/wagtail_events)

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

Wagtail events is tested against python 3.6-3.9, Django 2.1-3.0 or later and Wagtail 2.3-2.9, anything outside those bounds and you're on your own.

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
