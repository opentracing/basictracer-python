import time

from opentracing import Format, Tracer
from opentracing import UnsupportedFormatException
from .context import SpanContext
from .propagation import BinaryPropagator, TextPropagator
from .recorder import SpanRecorder, DefaultSampler
from .span import BasicSpan
from .util import generate_id


class BasicTracer(Tracer):

    def __init__(self, recorder=None, sampler=None):
        super(BasicTracer, self).__init__()
        self.recorder = NoopRecorder() if recorder is None else recorder
        self.sampler = DefaultSampler(1) if sampler is None else sampler
        self._binary_propagator = BinaryPropagator(self)
        self._text_propagator = TextPropagator(self)
        return

    def start_span(
            self,
            operation_name=None,
            references=None,
            tags=None,
            start_time=None):

        start_time = time.time() if start_time is None else start_time

        # See if we have a parent_ctx in `references`
        parent_ctx = None
        if references is not None:
            if isinstance(references, list):
                # TODO only first reference is currently used
                for ref in references:
                    parent_ctx = ref.referee
                    break
            else:
                parent_ctx = references.referee

        # Assemble the child ctx
        ctx = SpanContext(span_id=generate_id())
        if parent_ctx is not None:
            if parent_ctx.baggage is not None:
                ctx.baggage = parent_ctx.baggage.copy()
            ctx.trace_id = parent_ctx.trace_id
            ctx.sampled = parent_ctx.sampled
        else:
            ctx.trace_id = generate_id()
            ctx.sampled = self.sampler.sampled(ctx.trace_id)

        # Tie it all together
        return BasicSpan(
            self,
            operation_name=operation_name,
            context=ctx,
            parent_id=(None if parent_ctx is None else parent_ctx.span_id),
            tags=tags,
            start_time=start_time)

    def inject(self, span_context, format, carrier):
        if format == Format.BINARY:
            self._binary_propagator.inject(span_context, carrier)
        elif format == Format.TEXT_MAP:
            self._text_propagator.inject(span_context, carrier)
        else:
            raise UnsupportedFormatException()

    def extract(self, format, carrier):
        if format == Format.BINARY:
            return self._binary_propagator.extract(carrier)
        elif format == Format.TEXT_MAP:
            return self._text_propagator.extract(carrier)
        else:
            raise UnsupportedFormatException()

    def record(self, span):
        self.recorder.record_span(span)


class NoopRecorder(SpanRecorder):
    def record_span(self, span):
        pass
