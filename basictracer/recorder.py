import threading

from abc import ABCMeta, abstractmethod


class SpanRecorder(object):
    """ SpanRecorder's job is to record and report a BasicSpan."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def record_span(self, span):
        pass


class InMemoryRecorder(SpanRecorder):
    """InMemoryRecorder stores all received spans in an internal list.

    This recorder is not suitable for production use, only for testing.
    """
    def __init__(self):
        self.spans = []
        self.mux = threading.Lock()

    def record_span(self, span):
        with self.mux:
            self.spans.append(span)

    def get_spans(self):
        with self.mux:
            return self.spans[:]


class Sampler(object):
    """ Sampler determines the sampling status of a span given its trace ID.

    Expected to return a boolean.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def sampled(self, trace_id):
        pass


class DefaultSampler(Sampler):
    """ DefaultSampler determines the sampling status via ID % rate == 0
    """
    def __init__(self, rate):
        self.rate = rate

    def sampled(self, trace_id):
        return trace_id % self.rate == 0
