from __future__ import absolute_import

from threading import Lock


class SpanContext(object):
    """SpanContext satisfies the opentracing.SpanContext contract.

    trace_id and span_id are uint64's, so their range is [0, 2^64).
    """

    def __init__(
            self,
            trace_id=None,
            span_id=None,
            baggage=None,
            sampled=True):
        self._lock = Lock()
        self.trace_id = trace_id
        self.span_id = span_id
        self.sampled = sampled
        self.baggage = baggage

    def set_baggage_item(self, key, value):
        with self._lock:
            if self.baggage is None:
                self.baggage = {}

            self.baggage[key] = value
        return self

    def get_baggage_item(self, key):
        with self._lock:
            if self.baggage is None:
                return None
            return self.baggage.get(key, None)
