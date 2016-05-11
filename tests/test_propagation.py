import pytest
from opentracing import Format, UnsupportedFormatException
from basictracer import BasicTracer

def test_propagation():
    tracer = BasicTracer()
    sp = tracer.start_span(operation_name="test")
    sp.context.sampled = False
    sp.set_baggage_item("foo", "bar")
    opname = 'op'

    # Test invalid types
    with pytest.raises(UnsupportedFormatException):
        tracer.inject(sp, "invalid", {})
    with pytest.raises(UnsupportedFormatException):
        tracer.join("", "invalid", {})

    tests = [(Format.BINARY, bytearray()),
             (Format.TEXT_MAP, {})]
    for format, carrier in tests:
        tracer.inject(sp, format, carrier)

        child = tracer.join(opname, format, carrier)

        assert child.context.trace_id == sp.context.trace_id
        assert child.context.parent_id == sp.context.span_id
        assert child.context.sampled == sp.context.sampled
        assert child.context.baggage == sp.context.baggage

def test_start_span():
    """ Test in process child span creation."""
    tracer = BasicTracer()
    sp = tracer.start_span(operation_name="test")
    sp.set_baggage_item("foo", "bar")

    child = tracer.start_span(operation_name="child", parent=sp)

    assert child.context.trace_id == sp.context.trace_id
    assert child.context.parent_id == sp.context.span_id
    assert child.context.sampled == sp.context.sampled
    assert child.context.baggage == sp.context.baggage
