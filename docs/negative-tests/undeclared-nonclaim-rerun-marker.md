# Negative-test rerun marker

This file exists only to trigger a fresh PR validation run after SocioSphere began printing strict-validation logs, exit codes, failure context, and materialized adapter snippets in the job log.

Expected result: this branch still fails strict adapter validation because `BSD-M6-002-four-descent-named-primes` references undeclared non-claim `bsd.no-such-nonclaim`.

Rerun marker: verify printed failure bundle summary after SocioSphere commit `77d54ee96b4257869e8b71ac5887af6d91d4d49c`.
