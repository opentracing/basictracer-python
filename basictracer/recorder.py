from abc import ABCMeta, abstractmethod

class SpanRecorder(object):
    """ SpanRecorder's job is record and report a BasicSpan.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def record_span(self, span):
        pass


class Sampler(object):
    """ Sampler determines the sampling status of a span given it's trace ID.

    Expected to return a boolean.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def sampled(self, id):
        pass

class DefaultSampler(Sampler):
    """ DefaultSampler determines the sampling status via ID % rate == 0
    """
    def __init__(self, rate):
        self.rate = rate

    def sampled(self, id):
        return id % self.rate == 0
