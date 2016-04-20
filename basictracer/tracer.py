import time

from opentracing import Format, Tracer
from opentracing import UnsupportedFormatException
from .context import Context
from .propagation import BinaryPropagator, TextPropagator
from .recorder import SpanRecorder
from .span import BasicSpan, RawSpan
from .util import generate_id

class BasicTracer(Tracer):

    def __init__(self, recorder=None):
        self.recorder = NoopRecorder() if recorder is None else recorder
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
        raw = RawSpan(operation_name=operation_name, tags=tags,
                context=context,
                start_time=start_time)

        if parent is None:
            raw.context.trace_id=generate_id()
        else:
            raw.context.trace_id = parent.raw.context.trace_id
            raw.context.parent_id = parent.raw.context.span_id
            raw.context.sampled = parent.raw.context.sampled
            if parent.raw.baggage is not None:
                raw.baggage = parent.raw.baggage.copy()

        return BasicSpan(self, raw)

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

class NoopRecorder(SpanRecorder):
    def record_span(self, span):
        pass
