---
title: Real-Time Trigger and Event Engine Spec
tags: [events, triggers, webhooks, queues]
status: spec
---

# Real-Time Trigger and Event Engine Spec

## Objective
Enable real-time or near-real-time automation using:
- webhooks
- internal events
- queue-driven execution
- retryable background jobs

## Trigger Sources
- new opportunity created
- opportunity stage changed
- recommendation approved
- Google Sheet row imported
- form submission received
- webhook from external system
- scheduled time-based trigger

## Event Types
- domain events
- integration events
- agent events
- approval events
- sync events

## Engine Responsibilities
- receive trigger
- validate payload
- normalize event
- enqueue job
- route to workflow or agent
- record status
- emit completion event

## Core Rule
No webhook should directly execute heavy business logic synchronously.
Always normalize and enqueue.
