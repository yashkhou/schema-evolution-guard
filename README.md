# schema-evolution-guard

Classify breaking versus compatible changes in JSON-schema tool contracts before agents discover them at runtime.

## What it does

- detects newly required fields and removed properties
- flags type changes, enum narrowing and stricter numeric bounds
- treats optional additions and enum widening as compatible
- outputs path-addressed findings for CI gating

## Quick start

```bash
PYTHONPATH=src python -m schema_evolution_guard examples/v1.json examples/v2.json
```

No model API, network service, or third-party package is required.

## Architecture

The comparator recursively walks object properties and selected scalar constraints. Findings carry a JSON-pointer-like path, severity and reason; CI exits nonzero when any breaking finding exists.

See [`docs/architecture.md`](docs/architecture.md) for the data model and trade-offs.

## V1 boundary

V1 targets the JSON Schema subset commonly used for tool arguments; composition keywords such as oneOf/allOf are reported as unsupported rather than guessed.

## Development

```bash
python -m unittest discover -s tests -v
```

MIT licensed.
