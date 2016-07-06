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
