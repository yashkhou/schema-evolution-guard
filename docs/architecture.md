# Architecture

The comparator recursively walks object properties and selected scalar constraints. Findings carry a JSON-pointer-like path, severity and reason; CI exits nonzero when any breaking finding exists.

## Design constraints

- deterministic offline behavior
- explicit machine-readable inputs and outputs
- small standard-library surface area
- failures are surfaced rather than hidden

## V1 limitation

V1 targets the JSON Schema subset commonly used for tool arguments; composition keywords such as oneOf/allOf are reported as unsupported rather than guessed.
