from opentracing import Format
from basictracer import BasicTracer

def test_propagation():
    tracer = BasicTracer()
    sp = tracer.start_span(operation_name="test")
    sp.set_baggage_item("foo", "bar")
    opname = 'op'

    tests = [(Format.BINARY, bytearray()),
             (Format.TEXT_MAP, {})]
    for format, carrier in tests:
        tracer.inject(sp, format, carrier)

        child = tracer.join(opname, format, carrier)

        assert child.raw.context.trace_id == sp.raw.context.trace_id
        assert child.raw.context.parent_id == sp.raw.context.span_id
        assert child.raw.context.sampled == sp.raw.context.sampled
        assert child.raw.baggage == sp.raw.baggage

