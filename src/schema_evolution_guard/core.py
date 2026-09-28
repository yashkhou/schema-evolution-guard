from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Finding:
    path: str
    breaking: bool
    reason: str

    def as_dict(self):
        return asdict(self)


def _types(schema):
    value = schema.get("type")
    if value is None:
        return set()
    return set(value) if isinstance(value, list) else {value}


def _constraint_change(old, new, key, stricter):
    if key not in old and key not in new:
        return None
    if key not in old:
        return True, f"{key} added: {new[key]}"
    if key not in new:
        return False, f"{key} removed"
    if old[key] == new[key]:
        return None
    return stricter(old[key], new[key]), f"{key} changed {old[key]} -> {new[key]}"


def compare(old, new, path=""):
    out = []
    location = path or "/"
    old_types = _types(old)
    new_types = _types(new)
    if old_types or new_types:
        removed_types = old_types - new_types
        added_types = new_types - old_types
        if removed_types:
            out.append(Finding(location, True, "accepted types removed: " + ",".join(sorted(removed_types))))
        if added_types:
            out.append(Finding(location, False, "accepted types added: " + ",".join(sorted(added_types))))
        if removed_types:
            return out
    if "enum" in old or "enum" in new:
        before = set(old.get("enum", [])); after = set(new.get("enum", []))
        removed = before - after; added = after - before
        if removed:
            out.append(Finding(location, True, "enum values removed: " + ",".join(map(str, sorted(removed, key=str)))))
        if added:
            out.append(Finding(location, False, "enum values added: " + ",".join(map(str, sorted(added, key=str)))))
    objectish = "object" in old_types or old.get("properties") is not None
    if objectish:
        old_props = old.get("properties", {}); new_props = new.get("properties", {})
        old_required = set(old.get("required", [])); new_required = set(new.get("required", []))
        for key in sorted(old_required - new_required): out.append(Finding(f"{path}/{key}", False, "field no longer required"))
        for key in sorted(new_required - old_required): out.append(Finding(f"{path}/{key}", True, "field became required"))
        for key in sorted(old_props.keys() - new_props.keys()): out.append(Finding(f"{path}/{key}", True, "property removed"))
        for key in sorted(new_props.keys() - old_props.keys()): out.append(Finding(f"{path}/{key}", key in new_required, "required property added" if key in new_required else "optional property added"))
        for key in sorted(old_props.keys() & new_props.keys()): out.extend(compare(old_props[key], new_props[key], f"{path}/{key}"))
        old_additional = old.get("additionalProperties", True); new_additional = new.get("additionalProperties", True)
        if old_additional is not False and new_additional is False:
            out.append(Finding(location, True, "additional properties are no longer accepted"))
        elif old_additional is False and new_additional is not False:
            out.append(Finding(location, False, "additional properties are now accepted"))
    if "array" in old_types or "items" in old:
        if isinstance(old.get("items"), dict) and isinstance(new.get("items"), dict):
            out.extend(compare(old["items"], new["items"], f"{path}/*"))
    constraints = [
        ("minimum", lambda before, after: after > before),
        ("exclusiveMinimum", lambda before, after: after > before),
        ("minLength", lambda before, after: after > before),
        ("minItems", lambda before, after: after > before),
        ("minProperties", lambda before, after: after > before),
        ("maximum", lambda before, after: after < before),
        ("exclusiveMaximum", lambda before, after: after < before),
        ("maxLength", lambda before, after: after < before),
        ("maxItems", lambda before, after: after < before),
        ("maxProperties", lambda before, after: after < before),
    ]
    for key, stricter in constraints:
        changed = _constraint_change(old, new, key, stricter)
        if changed:
            breaking, reason = changed
            out.append(Finding(location, breaking, reason))
    if old.get("pattern") != new.get("pattern"):
        if "pattern" in new:
            out.append(Finding(location, True, f"pattern changed {old.get('pattern')!r} -> {new['pattern']!r}"))
        elif "pattern" in old:
            out.append(Finding(location, False, "pattern constraint removed"))
    return out
