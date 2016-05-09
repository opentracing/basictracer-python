from __future__ import absolute_import

from threading import Lock
import time
import re

from opentracing import Span
from .context import Context
from .util import generate_id

class BasicSpan(Span):
    """BasicSpan is a thread-safe implementation of opentracing.Span.
    """

    def __init__(self, tracer, raw):
        super(BasicSpan, self).__init__(tracer)
        self.raw = raw
        self._lock = Lock()

    def set_operation_name(self, operation_name):
        with self._lock:
            self.raw.operation_name = operation_name
        return super(BasicSpan, self).set_operation_name(operation_name)

    def set_tag(self, key, value):
        with self._lock:
            if self.raw.tags is None:
                self.raw.tags = {}
            self.raw.tags[key] = value
        return super(BasicSpan, self).set_tag(key, value)

    def log_event(self, event, payload=None):
        with self._lock:
            self.raw.logs.append(LogData(event=event, payload=payload))
        return super(BasicSpan, self).log_event(event, payload)

    def log(self, **kwargs):
        with self._lock:
            self.raw.logs.append(LogData(**kwargs))
        return super(BasicSpan, self).log(**kwargs)

    def set_baggage_item(self, key, value):
        with self._lock:
            if self.raw.baggage is None:
                self.raw.baggage = {}

            canonicalKey = canonicalize_baggage_key(key)
            if canonicalKey is not None:
                key = canonicalKey

            self.raw.baggage[key] = value
        return super(BasicSpan, self).set_baggage_item(key, value)


    def get_baggage_item(self, key):
        with self._lock:
            if self.raw.baggage is None:
                return None
            canonicalKey = canonicalize_baggage_key(key)
            if canonicalKey is not None:
                key = canonicalKey
        return self.raw.baggage.get(key, None)

    def finish(self, finish_time=None):
        with self._lock:
            finish = time.time() if finish_time is None else finish_time
            self.raw.duration = finish - self.raw.start_time

            self._tracer.record(self.raw)

class RawSpan(object):
    """ RawSpan holds all state associated with a (finished) Span.
    """

    def __init__(self,
            operation_name=None,
            context=None,
            baggage=None,
            tags=None,
            sampled=False,
            start_time=None):
        self.operation_name = operation_name
        self.start_time = start_time
        self.context = context
        self.tags = tags
        self.duration = -1
        self.logs = []
        self.baggage = baggage

class LogData(object):

    def __init__(self,
            event="",
            timestamp=None,
            payload=None):
        self.event = event
        self.timestamp = time.time() if timestamp is None else timestamp
        self.payload = payload

baggage_key_re = re.compile('^(?i)([a-z0-9][-a-z0-9]*)$')

# TODO(bg): Replace use of canonicalize_baggage_key when opentracing version is
# bumped and includes this.
def canonicalize_baggage_key(key):
    """canonicalize_baggage_key returns a canonicalized key if it's valid.

    :param key: a string that is expected to match the pattern specified by
        `get_baggage_item`.

    :return: Returns the canonicalized key if it's valid, otherwise it returns
        None.
    """
    if baggage_key_re.match(key) is not None:
        return key.lower()
    return None
