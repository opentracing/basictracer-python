from __future__ import absolute_import

import time

from opentracing import Span
from opentracing.ext import tags


class BasicSpan(Span):
    """BasicSpan is a thread-safe implementation of opentracing.Span.
    """

    def __init__(
            self,
            tracer,
            operation_name=None,
            context=None,
            parent_id=None,
            tags=None,
            start_time=None):
        super(BasicSpan, self).__init__(tracer, context)
        self._tracer = tracer

        self.operation_name = operation_name
        self.start_time = start_time
        self.parent_id = parent_id
        self.tags = tags if tags is not None else {}
        self.duration = -1
        self.logs = []

    def set_operation_name(self, operation_name):
        with self.context._lock:
            self.operation_name = operation_name
        return super(BasicSpan, self).set_operation_name(operation_name)

    def set_tag(self, key, value):
        with self.context._lock:
            if key == tags.SAMPLING_PRIORITY:
                self.context.sampled = value > 0
            if self.tags is None:
                self.tags = {}
            self.tags[key] = value
        return super(BasicSpan, self).set_tag(key, value)

    def log_event(self, event, payload=None):
        with self.context._lock:
            self.logs.append(LogData(event=event, payload=payload))
        return super(BasicSpan, self).log_event(event, payload)

    def log(self, **kwargs):
        with self.context._lock:
            self.logs.append(LogData(**kwargs))
        return super(BasicSpan, self).log(**kwargs)

    def finish(self, finish_time=None):
        with self.context._lock:
            finish = time.time() if finish_time is None else finish_time
            self.duration = finish - self.start_time
            self._tracer.record(self)


class LogData(object):

    def __init__(
            self,
            event='',
            timestamp=None,
            payload=None):
        self.event = event
        self.timestamp = time.time() if timestamp is None else timestamp
        self.payload = payload
