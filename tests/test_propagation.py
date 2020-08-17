import pytest
from opentracing import (
    Format,
    UnsupportedFormatException,
    SpanContextCorruptedException,
)
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


def test_span_missing_all_fields():
    tracer = BasicTracer()
    tracer.register_required_propagators()

    # Given an empty carrier
    headers = {}

    # When .extract is called
    ctx = tracer.extract(Format.TEXT_MAP, headers)

    # Then it should return None
    assert ctx is None


def test_span_missing_all_headers():
    tracer = BasicTracer()
    tracer.register_required_propagators()

    # Given an carrier with no ot-headers
    headers = {
       'Content-Type': 'text/html',
       'Authorization': 'Digest 123456',
    }

    # When .extract is called
    ctx = tracer.extract(Format.TEXT_MAP, headers)

    # Then it should return None
    assert ctx is None


def test_span_missing_one_field():
    tracer = BasicTracer()
    tracer.register_required_propagators()

    # Given a carrier missing ot-tracer-sampled:
    headers = {
        'ot-tracer-spanid': 'deadbeaf',
        'ot-tracer-traceid': '1c3b00da',
    }

    # When .extract is called
    with pytest.raises(SpanContextCorruptedException) as exc:
        tracer.extract(Format.TEXT_MAP, headers)

    # Then it should raise SpanContextCorruptedException
    assert str(exc.value) == 'expected to parse 3 fields, but parsed 2 instead'


def test_span_missing_two_fields():
    tracer = BasicTracer()
    tracer.register_required_propagators()

    # Given a carrier with only ot-tracer-traceid:
    headers = {
        'ot-tracer-traceid': '1c3b00da',
    }

    # When .extract is called
    with pytest.raises(SpanContextCorruptedException) as exc:
        tracer.extract(Format.TEXT_MAP, headers)

    # Then it should raise SpanContextCorruptedException
    assert str(exc.value) == 'expected to parse 3 fields, but parsed 1 instead'


def test_span_with_baggage_only():
    tracer = BasicTracer()
    tracer.register_required_propagators()

    # Given a carrier with only baggage:
    headers = {
        'ot-baggage-example': 'ok',
    }

    # When .extract is called
    with pytest.raises(SpanContextCorruptedException) as exc:
        tracer.extract(Format.TEXT_MAP, headers)

    # Then it should raise SpanContextCorruptedException
    assert str(exc.value) == 'found baggage without required fields'


def test_span_corrupted_invalid_sampled_value():
    tracer = BasicTracer()
    tracer.register_required_propagators()

    # Given a carrier with invalid "ot-tracer-sampled" value
    headers = {
        'ot-tracer-spanid': 'deadbeef',
        'ot-tracer-sampled': 'notbool',
        'ot-tracer-traceid': '1c3b00da',
    }

    # When .extract is called
    with pytest.raises(SpanContextCorruptedException) as exc:
        tracer.extract(Format.TEXT_MAP, headers)

    # Then it should raise SpanContextCorruptedException
    assert str(exc.value) == (
        "ot-tracer-sampled got an invalid value 'notbool', "
        "should be one of 'true', 'false', '0', '1'"
    )


def test_span_corrupted_invalid_spanid_value():
    tracer = BasicTracer()
    tracer.register_required_propagators()

    # Given a carrier with invalid "ot-tracer-spanid" value
    headers = {
        'ot-tracer-spanid': 'nothex',
        'ot-tracer-sampled': 'false',
        'ot-tracer-traceid': '1c3b00da',
    }

    # When .extract is called
    with pytest.raises(SpanContextCorruptedException) as exc:
        tracer.extract(Format.TEXT_MAP, headers)

    # Then it should raise SpanContextCorruptedException
    assert str(exc.value) == (
        "ot-tracer-spanid got an invalid hexadecimal value 'nothex'"
    )


def test_span_corrupted_invalid_traceid_value():
    tracer = BasicTracer()
    tracer.register_required_propagators()

    # Given a carrier with invalid 'ot-tracer-traceid' value
    headers = {
        'ot-tracer-traceid': 'nothex',
        'ot-tracer-sampled': 'false',
        'ot-tracer-spanid': '1c3b00da',
    }

    # When .extract is called
    with pytest.raises(SpanContextCorruptedException) as exc:
        tracer.extract(Format.TEXT_MAP, headers)

    # Then it should raise SpanContextCorruptedException
    assert str(exc.value) == (
        "ot-tracer-traceid got an invalid hexadecimal value 'nothex'"
    )
