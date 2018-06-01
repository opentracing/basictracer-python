""" Example usage of the BasicTracer implementation which log spans to the console.

Ensure the following pip packages are installed:

    - opentracing
    - basictracer

Run with the command:

    python3 examples/span_logging.py

Example output:

    [DEBUG   ] span_logging.loop[1.00e+00 S, {'i': 0}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.loop[1.00e+00 S, {'i': 1}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.loop[1.00e+00 S, {'i': 2}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.loop[1.01e+00 S, {'i': 3}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.loop[1.00e+00 S, {'i': 4}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.loop[1.00e+00 S, {'i': 5}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.loop[1.00e+00 S, {'i': 6}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.loop[1.00e+00 S, {'i': 7}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.loop[1.00e+00 S, {'i': 8}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.loop[1.00e+00 S, {'i': 9}]: {'message': 'Sleeping for 1 second'}
    [DEBUG   ] span_logging.main[1.00e+01 S]: finished
"""

import logging
import sys
import time

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
        # Assemble metadata about span
        tag = "{0}[{1:.2e} S".format(span.operation_name, span.duration)

        if len(span.tags) > 0:
            tag += ", {}".format(span.tags)

        tag += "]"

        # Create logger for span
        span_logger = self.logger.getChild(tag)

        # Print span logs
        if len(span.logs) > 0:
            for log in span.logs:
                span_logger.debug(log.key_values)
        else:
            # If no span logs exist simply print span finished
            span_logger.debug("finished")

def main():
    # Setup BasicTracer to log to console
    logger = logging.getLogger('span_logging')

    logger.setLevel(logging.DEBUG)

    hndlr = logging.StreamHandler(sys.stdout)
    hndlr.setFormatter(logging.Formatter("[%(levelname)-8s] %(name)s: %(message)s"))

    logger.addHandler(hndlr)

    recorder = LogSpanRecorder(logger)

    tracer = BasicTracer(recorder=recorder)
    tracer.register_required_propagators()

    # Use tracer to create spans
    span = tracer.start_span(operation_name='main')

    for i in range(10):
        child_span = tracer.start_span(operation_name='loop', child_of=span)
        child_span.set_tag('i', i)

        child_span.log_kv({'message': "Sleeping for 1 second"})

        time.sleep(1)

        child_span.finish()

    span.finish()

if __name__ == '__main__':
    main()
