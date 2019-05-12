.. :changelog:

History
-------

3.1.0 (2019-05-12)
------------------

- Unpin OpenTracing dependency and change to a range (#40) <Nathan Hsieh>
- Add support for Python 3.5+ (#39) <Aliaksei Urbanski>
- Include 0,1 as acceptable sampled value (#37) <Dominik Janků>


3.0.0 (2018-07-10)
------------------

- Update our OT dependency to 2.0.0.
- Implement ScopeManager for in-process propagation.


2.2.1 (2018-02-20)
------------------

- Update OT dependency to >=1.2.1 and <2.0.


2.2.0 (2016-09-22)
------------------

- Bump the minor version :-/


2.1.2 (2016-09-22)
------------------

- Adjust to OT logging changes


2.1.1 (2016-08-19)
------------------

- Make the RNG robust to fork()


2.1.0 (2016-08-07)
------------------

- Implement immutable SpanContext


2.0.1.dev1 (2016-08-04)
-----------------------

- Allow BasicTracer users to opt in to propagators


2.0.0.dev3 (2016-07-26)
-----------------------

- Positional arguments


2.0.0.dev2 (2016-07-26)
-----------------------

- Adapt to SpanContext changes


2.0.0.dev1 (2016-07-12)
-----------------------

- Rename ChildOf/FollowsFrom to child_of/follows_from


2.0.0.dev0 (2016-07-11)
-----------------------

- Adapt to SpanContext changes


1.0rc2 (2016-07-06)
-------------------

- Add InMemoryRecorder and respect sampling.priority tag


1.0rc1 (2015-05-11)
-------------------

- Official release


0.1.0 (2016-5-4)
----------------

- Initial public API

