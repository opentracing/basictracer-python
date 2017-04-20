from __future__ import absolute_import

from abc import ABCMeta, abstractmethod
import six


class Propagator(six.with_metaclass(ABCMeta, object)):

    @abstractmethod
    def inject(self, span_context, carrier):
        pass

    @abstractmethod
    def extract(self, carrier):
        pass
