# Implementation note

Working V1 scope: Classify breaking versus compatible changes in JSON-schema tool contracts before agents discover them at runtime.

Verified with `python -m unittest discover -s tests -v`.

Known boundary: V1 targets the JSON Schema subset commonly used for tool arguments; composition keywords such as oneOf/allOf are reported as unsupported rather than guessed.
