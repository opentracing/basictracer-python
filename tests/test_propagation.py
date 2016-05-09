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

        assert child.context.trace_id == sp.context.trace_id
        assert child.context.parent_id == sp.context.span_id
        assert child.context.sampled == sp.context.sampled
        assert child.baggage == sp.baggage

