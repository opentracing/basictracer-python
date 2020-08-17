from __future__ import absolute_import

from opentracing import SpanContextCorruptedException
from .context import SpanContext
from .propagator import Propagator

prefix_tracer_state = 'ot-tracer-'
prefix_baggage = 'ot-baggage-'
field_name_trace_id = prefix_tracer_state + 'traceid'
field_name_span_id = prefix_tracer_state + 'spanid'
field_name_sampled = prefix_tracer_state + 'sampled'
field_count = 3


def parse_hex_for_field(field_name, value):
    """parses the hexadecimal value of a field into an integer.
    Raises SpanContextCorruptedException in case of failure
    """
    try:
        return int(value, 16)
    except ValueError:
        msg = '{field_name} got an invalid hexadecimal value {value!r}'
        msg = msg.format(field_name=field_name, value=value)
        raise SpanContextCorruptedException(msg)


def parse_boolean_for_field(field_name, value):
    """parses the string value of a field into a boolean.
    Raises SpanContextCorruptedException in case of failure
    """
    if value in ('true', '1'):
        return True
    elif value in ('false', '0'):
        return False

    msg = (
        '{field} got an invalid value {value!r}, '
        "should be one of \'true\', \'false\', \'0\', \'1\'"
    )
    raise SpanContextCorruptedException(msg.format(
        value=value,
        field=field_name_sampled
    ))


class TextPropagator(Propagator):
    """A BasicTracer Propagator for Format.TEXT_MAP."""

    def inject(self, span_context, carrier):
        carrier[field_name_trace_id] = '{0:x}'.format(span_context.trace_id)
        carrier[field_name_span_id] = '{0:x}'.format(span_context.span_id)
        carrier[field_name_sampled] = str(span_context.sampled).lower()
        if span_context.baggage is not None:
            for k in span_context.baggage:
                carrier[prefix_baggage+k] = span_context.baggage[k]

    def extract(self, carrier):  # noqa
        count = 0
        span_id, trace_id, sampled = (0, 0, False)
        baggage = {}
        for k in carrier:
            v = carrier[k]
            k = k.lower()
            if k == field_name_span_id:
                span_id = parse_hex_for_field(field_name_span_id, v)
                count += 1
            elif k == field_name_trace_id:
                trace_id = parse_hex_for_field(field_name_trace_id, v)
                count += 1
            elif k == field_name_sampled:
                sampled = parse_boolean_for_field(field_name_sampled, v)
                count += 1
            elif k.startswith(prefix_baggage):
                baggage[k[len(prefix_baggage):]] = v

        if count == 0:
            if len(baggage) > 0:
                raise SpanContextCorruptedException(
                                'found baggage without required fields')

            return None

        if count != field_count:
            msg = (
                'expected to parse {field_count} fields'
                ', but parsed {count} instead'
            )
            raise SpanContextCorruptedException(msg.format(
                field_count=field_count,
                count=count,
            ))

        return SpanContext(
            span_id=span_id,
            trace_id=trace_id,
            baggage=baggage,
            sampled=sampled)
