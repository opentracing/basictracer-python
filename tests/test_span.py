from basictracer import BasicTracer
from basictracer.recorder import InMemoryRecorder
from opentracing.ext import tags


def test_span_sampling_priority():
    recorder = InMemoryRecorder()
    tracer = BasicTracer(recorder=recorder)

    span = tracer.start_span('x')
    assert span.context.sampled is True

    span.set_tag(tags.SAMPLING_PRIORITY, 0)
    assert span.context.sampled is False

    span.finish()

    assert len(recorder.get_spans()) == 1

    def get_sampled_spans():
        return [span for span in recorder.get_spans() if span.context.sampled]

    assert len(get_sampled_spans()) == 0


def test_span_log_kv():
    recorder = InMemoryRecorder()
    tracer = BasicTracer(recorder=recorder)

    span = tracer.start_span('x')
    span.log_kv({
        'foo': 'bar',
        'baz': 42,
        })
    span.finish()

    finished_spans = recorder.get_spans()
    assert len(finished_spans) == 1
    assert len(finished_spans[0].logs) == 1
    assert len(finished_spans[0].logs[0].key_values) == 2
    assert finished_spans[0].logs[0].key_values['foo'] == 'bar'
    assert finished_spans[0].logs[0].key_values['baz'] == 42
