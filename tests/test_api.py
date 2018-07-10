# Copyright The OpenTracing Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import unittest
from basictracer import BasicTracer
from opentracing.harness.api_check import APICompatibilityCheckMixin


class APICheckBasicTracer(unittest.TestCase, APICompatibilityCheckMixin):
    def tracer(self):
        t = BasicTracer()
        t.register_required_propagators()
        return t

    def check_baggage_values(self):
        return True

    def is_parent(self, parent, span):
        # use `Span` ids to check parenting
        if parent is None:
            return span.parent_id is None

        return parent.context.span_id == span.parent_id
