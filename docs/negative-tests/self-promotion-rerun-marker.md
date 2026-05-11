# Negative-test rerun marker

This file exists only to trigger a fresh PR validation run after SocioSphere began capturing strict-validation logs, exit codes, and materialized adapters in failure artifacts.

Expected result: this branch still fails strict adapter validation because `BSD-M6-002-four-descent-named-primes` has repo-local `state: promoted`.
