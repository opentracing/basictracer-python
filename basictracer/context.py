class Context(object):
    def __init__(self, trace_id=None, span_id=None, parent_id=None, sampled=True):
        self.trace_id=trace_id
        self.span_id=span_id
        self.parent_id=parent_id
        self.sampled=sampled

