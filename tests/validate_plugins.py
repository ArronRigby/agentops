#!/usr/bin/env python3
"""
Validate plugin manifests (plugin.json files).

This script validates:
- JSON syntax
- Required fields
- Component paths
- Version format
- Token budget accuracy
"""

import json
import sys
from pathlib import Path
from typing import Dict, List


def load_plugin_json(path: Path) -> Dict:
    """Load and parse plugin.json."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {path}: {e}")
        return None
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        return None


def validate_required_fields(plugin_name: str, data: Dict) -> List[str]:
    """Validate required fields in plugin.json."""
    errors = []
    required_fields = ["name", "version", "description", "author", "license"]

    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Validate version format (semantic versioning)
    if "version" in data:
        version = data["version"]
        parts = version.split(".")
        if len(parts) != 3:
            errors.append(f"Version must be semantic (X.Y.Z): {version}")

    return errors


def validate_components(plugin_name: str, data: Dict, plugin_dir: Path) -> List[str]:
    """Validate component declarations and files."""
    errors = []

    if "components" not in data:
        errors.append("Missing 'components' field")
        return errors

    components = data["components"]

    # Validate each component type
    component_types = ["agents", "commands", "skills", "hooks", "mcp"]

    for comp_type in component_types:
        if comp_type in components:
            comp_list = components[comp_type]

            if not isinstance(comp_list, list):
                errors.append(f"components.{comp_type} must be an array")
                continue

            # Check each file exists
            for comp_path in comp_list:
                full_path = plugin_dir / comp_path
                if not full_path.exists():
                    errors.append(f"Component file not found: {comp_path}")

    return errors


def validate_token_budget(plugin_name: str, data: Dict, plugin_dir: Path) -> List[str]:
    """Validate token budget estimation."""
    warnings = []

    if "tokenBudget" not in data:
        warnings.append("No tokenBudget field (recommended)")
        return warnings

    budget = data["tokenBudget"]

    if "estimated" not in budget or "percentage" not in budget:
        warnings.append("tokenBudget missing 'estimated' or 'percentage'")
        return warnings

    estimated = budget["estimated"]
    percentage = budget["percentage"]

    # Calculate expected percentage (200k context window)
    expected_percentage = (estimated / 200000) * 100

    # Check if percentage matches estimated
    diff = abs(expected_percentage - percentage)
    if diff > 0.5:  # Allow 0.5% tolerance
        warnings.append(
            f"Token budget mismatch: estimated={estimated}, "
            f"percentage={percentage}%, expected={expected_percentage:.2f}%"
        )

    return warnings


def validate_plugin(plugin_dir: Path) -> tuple[bool, List[str], List[str]]:
    """Validate a single plugin."""
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    plugin_name = plugin_dir.name

    if not plugin_json.exists():
        return False, [f"Missing plugin.json"], []

    data = load_plugin_json(plugin_json)
    if data is None:
        return False, [f"Failed to load plugin.json"], []

    errors = []
    warnings = []

    # Validate required fields
    errors.extend(validate_required_fields(plugin_name, data))

    # Validate components
    errors.extend(validate_components(plugin_name, data, plugin_dir))

    # Validate token budget (warnings only)
    warnings.extend(validate_token_budget(plugin_name, data, plugin_dir))

    # Check for README
    if not (plugin_dir / "README.md").exists():
        warnings.append("Missing README.md (recommended)")

    success = len(errors) == 0
    return success, errors, warnings


def main():
    """Main validation function."""
    repo_root = Path(__file__).parent.parent
    plugins_dir = repo_root / "plugins"

    print("=================================")
    print("Plugin Manifest Validation")
    print("=================================")
    print()

    if not plugins_dir.exists():
        print(f"❌ Plugins directory not found: {plugins_dir}")
        sys.exit(1)

    # Find all plugin directories
    plugin_dirs = [d for d in plugins_dir.iterdir() if d.is_dir()]

    if not plugin_dirs:
        print("⚠️  No plugins found")
        return

    print(f"Found {len(plugin_dirs)} plugins to validate")
    print()

    all_success = True
    results = []

    for plugin_dir in sorted(plugin_dirs):
        plugin_name = plugin_dir.name
        print(f"Validating plugin: {plugin_name}")

        success, errors, warnings = validate_plugin(plugin_dir)

        if not success:
            print(f"  ❌ Validation failed")
            for error in errors:
                print(f"     - {error}")
            all_success = False
        else:
            print(f"  ✅ Validation passed")

        if warnings:
            print(f"  ⚠️  Warnings:")
            for warning in warnings:
                print(f"     - {warning}")

        results.append((plugin_name, success, len(errors), len(warnings)))
        print()

    # Summary
    print("=================================")
    print("Validation Summary")
    print("=================================")
    print()

    passed = sum(1 for _, success, _, _ in results if success)
    failed = len(results) - passed
    total_errors = sum(errors for _, _, errors, _ in results)
    total_warnings = sum(warnings for _, _, _, warnings in results)

    print(f"Total plugins: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")
    print()

    if all_success:
        print("✅ All plugin validations passed!")
        if total_warnings > 0:
            print(f"   Note: {total_warnings} warnings (non-blocking)")
    else:
        print("❌ Some plugin validations failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
