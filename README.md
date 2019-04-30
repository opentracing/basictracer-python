[![Gitter chat](http://img.shields.io/badge/gitter-join%20chat%20%E2%86%92-brightgreen.svg)](https://gitter.im/opentracing/public) [![Build Status](https://travis-ci.org/opentracing/basictracer-python.svg?branch=master)](https://travis-ci.org/opentracing/basictracer-python) [![PyPI version](https://badge.fury.io/py/basictracer.svg)](https://badge.fury.io/py/basictracer)

# Basictracer Python

A python version of the "BasicTracer" reference implementation for OpenTracing.

## Development

### Tests

```sh
virtualenv env
. ./env/bin/activate
make bootstrap
make test
```

You can use [tox](https://tox.readthedocs.io) to run tests as well.
```bash
tox
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

