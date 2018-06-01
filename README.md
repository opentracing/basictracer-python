[![Gitter chat](http://img.shields.io/badge/gitter-join%20chat%20%E2%86%92-brightgreen.svg)](https://gitter.im/opentracing/public) [![Build Status](https://travis-ci.org/opentracing/basictracer-python.svg?branch=master)](https://travis-ci.org/opentracing/basictracer-python) [![PyPI version](https://badge.fury.io/py/basictracer.svg)](https://badge.fury.io/py/basictracer)

# Basictracer Python

A python version of the "BasicTracer" reference implementation for OpenTracing.

# Example
If you would like to get started using the Open Tracing without committing to a 
logging service you may configure the Basic Tracer in your application:

```py
import logging
from opentracing import Tracer
from basictracer import BasicTracer
from basictracer.recorder import SpanRecorder

class LogSpanRecorder(SpanRecorder):
    """ Records spans by printing them to a log
    Fields:
        - logger (Logger): Logger used to display spans
    """

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def record_span(self, span):
        tag_strs = ""
        if len(span.tags) > 0:
            tag_strs = "[{0:.2e} S, {1}]".format(span.duration, span.tags)

        span_logger = self.logger.getChild(span.operation_name + tag_strs)

        for log in span.logs:
            span_logger.debug(log.key_values)

logger = logging.getLogger(__name__)
recorder = LogSpanRecorder(logger)

tracer = BasicTracer(recorder=recorder)
tracer.register_required_propagators()
```

## Development

### Tests

```sh
virtualenv env
. ./env/bin/activate
make bootstrap
make test
```

### Releases

Before new release, add a summary of changes since last version to CHANGELOG.rst

```sh
pip install zest.releaser[recommended]
prerelease
release
git push origin master --follow-tags
python setup.py sdist upload -r pypi
postrelease
git push
```

## Licensing

[Apache 2.0 License](./LICENSE).

