import time

from opentracing import Format, Tracer
from opentracing import UnsupportedFormatException
from .context import Context
from .propagation import BinaryPropagator, TextPropagator
from .recorder import SpanRecorder, DefaultSampler
from .span import BasicSpan
from .util import generate_id

class BasicTracer(Tracer):

    def __init__(self, recorder=None, sampler=None):
        self.recorder = NoopRecorder() if recorder is None else recorder
        self.sampler = DefaultSampler(1) if sampler is None else sampler
        self._binary_propagator = BinaryPropagator(self)
        self._text_propagator = TextPropagator(self)
        return

    def start_span(self,
            operation_name=None,
            parent=None,
            tags=None,
            start_time=None):
        start_time = time.time() if start_time is None else start_time
        context = Context(span_id=generate_id())
        sp = BasicSpan(self, operation_name=operation_name, tags=tags,
                context=context,
                start_time=start_time)

        if parent is None:
            sp.context.trace_id = generate_id()
            sp.context.sampled = self.sampler.sampled(sp.context.trace_id)
        else:
            sp.context.trace_id = parent.context.trace_id
            sp.context.parent_id = parent.context.span_id
            sp.context.sampled = parent.context.sampled
            if parent.context.baggage is not None:
                sp.context.baggage = parent.context.baggage.copy()

        return sp


    def inject(self, span, format, carrier):
        if format == Format.BINARY:
            self._binary_propagator.inject(span, carrier)
        elif format == Format.TEXT_MAP:
            self._text_propagator.inject(span, carrier)
        else:
            raise UnsupportedFormatException()

    def join(self, operation_name, format, carrier):
        if format == Format.BINARY:
            return self._binary_propagator.join(operation_name, carrier)
        elif format == Format.TEXT_MAP:
            return self._text_propagator.join(operation_name, carrier)
        else:
            raise UnsupportedFormatException()

    def record(self, span):
        self.recorder.record_span(span)

class NoopRecorder(SpanRecorder):
    def record_span(self, span):
        pass
