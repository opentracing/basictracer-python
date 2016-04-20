from abc import ABCMeta, abstractmethod

class SpanRecorder(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def record_span(self, span):
        pass
