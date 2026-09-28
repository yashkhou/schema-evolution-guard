import unittest

from schema_evolution_guard.core import compare


class CompatibilityUpgradeTests(unittest.TestCase):
    def test_array_item_narrowing_is_breaking(self):
        old = {"type": "array", "items": {"type": ["string", "null"]}}
        new = {"type": "array", "items": {"type": "string"}}
        findings = compare(old, new)
        self.assertTrue(any(f.breaking and "accepted types removed" in f.reason for f in findings))

    def test_disabling_additional_properties_is_breaking(self):
        old = {"type": "object", "properties": {"x": {"type": "string"}}}
        new = {"type": "object", "properties": {"x": {"type": "string"}}, "additionalProperties": False}
        self.assertTrue(any(f.breaking and "additional" in f.reason for f in compare(old, new)))

    def test_tighter_collection_bounds_are_breaking(self):
        old = {"type": "array", "items": {"type": "string"}, "minItems": 0, "maxItems": 10}
        new = {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 5}
        findings = compare(old, new)
        self.assertEqual(sum(f.breaking for f in findings), 2)


if __name__ == "__main__":
    unittest.main()
