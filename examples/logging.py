import logging
from opentracing import Tracer
from basictracer import BasicTracer
from basictracer.recorder import SpanRecorder

class LogSpanRecorder(SpanRecorder):
    """ Records spans by printing them to a log
    Fields:
        - logger (Logger): Logger used to display spans
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def record_span(self, span):
        tag_strs = ""
        if len(span.tags) > 0:
            tag_strs = "[{0:.2e} S, {1}]".format(span.duration, span.tags)

        span_logger = self.logger.getChild(span.operation_name + tag_strs)

        for log in span.logs:
            span_logger.debug(log.key_values)

logger = logging.getLogger(__name__)
recorder = LogSpanRecorder(logger)

tracer = BasicTracer(recorder=recorder)
tracer.register_required_propagators()

