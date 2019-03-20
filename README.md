# Wagtail Events [![Build Status](https://travis-ci.com/thclark/wagtail_events.svg?branch=master)](https://travis-ci.com/thclark/wagtail_events)

Events calendar management for wagtail, with tools for filtering by date.

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

I'm extremely open to collaboration - in fact, I really don't want to be maintaining this (it's only for one client) so
I'm open to transferring ownership or collaboration to anyone who wants to take this on and enhance it. @omni-digital,
this originated as your baby so if you'd like to take back maintenance, please reach out and I'll help you.


## Requirements

Wagtail events requires Django 2.1 or later and Wagtail 2.3 or later.

## Supported Versions

Python: 3.6

Django: 2.1

Wagtail: 2.3

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

### EventSeries

A detail page for an event series, the EventSeries can contain single or multiple SubEvent instances.

### SubEvent

An single occurrence of an event.

## Future Development Plans:

- EventSingleton: A single event that will only have a single occurrence.

