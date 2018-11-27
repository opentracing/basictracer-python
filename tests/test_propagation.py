import pytest
from opentracing import Format, UnsupportedFormatException
from basictracer import BasicTracer


def test_propagation():
    tracer = BasicTracer()
    tracer.register_required_propagators()
    sp = tracer.start_span(operation_name='test')
    sp.context.sampled = False
    sp.set_baggage_item('foo', 'bar')

    # Test invalid types
    with pytest.raises(UnsupportedFormatException):
        tracer.inject(sp.context, 'invalid', {})
    with pytest.raises(UnsupportedFormatException):
        tracer.extract('invalid', {})

    tests = [(Format.BINARY, bytearray()),
             (Format.TEXT_MAP, {})]
    for format, carrier in tests:
        tracer.inject(sp.context, format, carrier)
        extracted_ctx = tracer.extract(format, carrier)

        assert extracted_ctx.trace_id == sp.context.trace_id
        assert extracted_ctx.span_id == sp.context.span_id
        assert extracted_ctx.sampled == sp.context.sampled
        assert extracted_ctx.baggage == sp.context.baggage

    # Test string value of sampled field
    headers = {}
    tracer.inject(sp.context, Format.HTTP_HEADERS, headers)
    headers['ot-tracer-sampled'] = '0'
    span_ctx0 = tracer.extract(Format.HTTP_HEADERS, headers)
    assert not span_ctx0.sampled

    headers['ot-tracer-sampled'] = '1'
    span_ctx1 = tracer.extract(Format.HTTP_HEADERS, headers)
    assert span_ctx1.sampled


def test_start_span():
    """ Test in process child span creation."""
    tracer = BasicTracer()
    tracer.register_required_propagators()
    sp = tracer.start_span(operation_name='test')
    sp.set_baggage_item('foo', 'bar')

    child = tracer.start_span(
        operation_name='child', child_of=sp.context)
    assert child.context.trace_id == sp.context.trace_id
    assert child.context.sampled == sp.context.sampled
    assert child.context.baggage == sp.context.baggage
    assert child.parent_id == sp.context.span_id
