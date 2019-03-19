# Wagtail Events [![Build Status](https://travis-ci.com/thclark/wagtail_events.svg?branch=master)](https://travis-ci.com/thclark/wagtail_events)

Events calendar management for wagtail, with tools for filtering by date.

This project is a hard fork of [omni-wagtail-events](http://github.com/omni-digital-omni-wagtail-events), and we owe a
debt of gratitude to those folks for getting us started. So why did I hard-fork (duplicate and start again) rather than
fork from omni-digital?

Well, github keeps the releases of the repo you fork from. Since I want to put this on pypi so it's easily available,
and have control of the release versioning, it needs to be here. Plus, I'm basically about to break *everything* for 
django 2.x and wagtail 2.x, so figured that the chances of getting my changes merged into the upstream were nil anyway.

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

An index/listing page for EventDetail instances, with optional pagination.

### EventDetail

A detail page for an event series, the EventDetail can contain single or multiple EventOccurrence instances.

### EventOccurrence

An single occurrence of an event.

## Future Development Plans:

- EventSingleton: A single event that will only have a single occurrence.

