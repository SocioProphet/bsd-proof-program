# Negative-test rerun marker

This file exists only to trigger a fresh PR validation run after SocioSphere began capturing strict-validation logs, exit codes, and materialized adapters in failure artifacts.

Expected result: this branch still fails strict adapter validation because `BSD-M6-002-four-descent-named-primes` has repo-local `state: promoted`.

Final artifact-bundle verification marker: this run should upload and print `failure-context.md`, `strict-adapter-validation.log`, `strict-adapter-validation.exitcode`, and `materialized-domain-proof-adapter.json`.

Rerun marker: verify printed failure bundle summary after SocioSphere commit `77d54ee96b4257869e8b71ac5887af6d91d4d49c`.
