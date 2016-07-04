import pytest
from opentracing import ChildOf, Format, UnsupportedFormatException
from basictracer import BasicTracer


def test_propagation():
    tracer = BasicTracer()
    sp = tracer.start_span(operation_name='test')
    sp.context.sampled = False
    sp.context.set_baggage_item('foo', 'bar')
    opname = 'op'

    # Test invalid types
    with pytest.raises(UnsupportedFormatException):
        tracer.inject(sp.context, 'invalid', {})
    with pytest.raises(UnsupportedFormatException):
        tracer.extract('invalid', {})

    tests = [(Format.BINARY, bytearray()),
             (Format.TEXT_MAP, {})]
    for format, carrier in tests:
        tracer.inject(sp.context, format, carrier)
        extracted = tracer.extract(format, carrier)

        assert extracted.trace_id == sp.context.trace_id
        assert extracted.span_id == sp.context.span_id
        assert extracted.sampled == sp.context.sampled
        assert extracted.baggage == sp.context.baggage


def test_start_span():
    """ Test in process child span creation."""
    tracer = BasicTracer()
    sp = tracer.start_span(operation_name='test')
    sp.context.set_baggage_item('foo', 'bar')

    child = tracer.start_span(
            operation_name='child', references=ChildOf(sp.context))

    assert child.context.trace_id == sp.context.trace_id
    assert child.context.sampled == sp.context.sampled
    assert child.context.baggage == sp.context.baggage
    assert child.parent_id == sp.context.span_id
