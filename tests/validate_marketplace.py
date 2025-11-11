#!/usr/bin/env python3
"""
Validate marketplace.json structure and content.

This script validates:
- JSON syntax
- Required fields
- Plugin references
- External marketplace links
- Schema compliance
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def load_marketplace_json(path: Path) -> Dict:
    """Load and parse marketplace.json."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {path}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        sys.exit(1)


def validate_required_fields(data: Dict) -> List[str]:
    """Validate required fields in marketplace.json."""
    errors = []
    required_fields = ["name", "owner", "plugins"]

    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Validate owner structure
    if "owner" in data:
        if not isinstance(data["owner"], dict):
            errors.append("Field 'owner' must be an object")
        else:
            if "name" not in data["owner"]:
                errors.append("Missing required field: owner.name")

    # Validate plugins array
    if "plugins" in data:
        if not isinstance(data["plugins"], list):
            errors.append("Field 'plugins' must be an array")

    return errors


def validate_plugins(data: Dict, repo_root: Path) -> List[str]:
    """Validate plugin entries."""
    errors = []

    if "plugins" not in data:
        return errors

    plugins = data["plugins"]
    plugin_names = set()

    for idx, plugin in enumerate(plugins):
        plugin_path = f"plugins[{idx}]"

        # Check required fields
        if "name" not in plugin:
            errors.append(f"{plugin_path}: Missing required field 'name'")
            continue

        plugin_name = plugin["name"]

        # Check for duplicates
        if plugin_name in plugin_names:
            errors.append(f"{plugin_path}: Duplicate plugin name '{plugin_name}'")
        plugin_names.add(plugin_name)

        # Check source field
        if "source" not in plugin:
            errors.append(f"{plugin_path} ({plugin_name}): Missing required field 'source'")
            continue

        source = plugin["source"]

        # Validate local source paths
        if isinstance(source, str) and source.startswith("./"):
            plugin_dir = repo_root / "plugins" / source[2:]
            if not plugin_dir.exists():
                errors.append(
                    f"{plugin_path} ({plugin_name}): Plugin directory not found: {plugin_dir}"
                )
            else:
                # Check for plugin.json
                plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
                if not plugin_json.exists():
                    errors.append(
                        f"{plugin_path} ({plugin_name}): Missing plugin.json: {plugin_json}"
                    )

        # Validate optional fields
        if "version" in plugin:
            if not isinstance(plugin["version"], str):
                errors.append(f"{plugin_path} ({plugin_name}): Field 'version' must be a string")

        if "keywords" in plugin:
            if not isinstance(plugin["keywords"], list):
                errors.append(f"{plugin_path} ({plugin_name}): Field 'keywords' must be an array")

    return errors


def validate_external_marketplaces(data: Dict) -> List[str]:
    """Validate external marketplace references."""
    errors = []

    if "externalMarketplaces" not in data:
        return errors  # Optional field

    external = data["externalMarketplaces"]

    if not isinstance(external, list):
        errors.append("Field 'externalMarketplaces' must be an array")
        return errors

    for idx, marketplace in enumerate(external):
        mp_path = f"externalMarketplaces[{idx}]"

        # Check required fields
        if "name" not in marketplace:
            errors.append(f"{mp_path}: Missing required field 'name'")

        if "source" not in marketplace:
            errors.append(f"{mp_path}: Missing required field 'source'")

    return errors


def main():
    """Main validation function."""
    repo_root = Path(__file__).parent.parent
    marketplace_json = repo_root / ".claude-plugin" / "marketplace.json"

    print("=================================")
    print("Marketplace Validation")
    print("=================================")
    print()

    # Load marketplace.json
    print(f"Loading {marketplace_json}...")
    data = load_marketplace_json(marketplace_json)
    print("✅ JSON syntax valid")
    print()

    # Validate required fields
    print("Checking required fields...")
    errors = validate_required_fields(data)
    if errors:
        print("❌ Required field errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    print("✅ All required fields present")
    print()

    # Validate plugins
    print("Validating plugins...")
    errors = validate_plugins(data, repo_root)
    if errors:
        print("❌ Plugin validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    plugin_count = len(data.get("plugins", []))
    print(f"✅ All {plugin_count} plugins valid")
    print()

    # Validate external marketplaces
    if "externalMarketplaces" in data:
        print("Validating external marketplaces...")
        errors = validate_external_marketplaces(data)
        if errors:
            print("❌ External marketplace errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)

        external_count = len(data.get("externalMarketplaces", []))
        print(f"✅ All {external_count} external marketplaces valid")
        print()

    # Summary
    print("=================================")
    print("✅ Marketplace validation passed!")
    print("=================================")
    print()
    print("Summary:")
    print(f"  - Marketplace name: {data.get('name', 'N/A')}")
    print(f"  - Plugins: {plugin_count}")
    print(f"  - External marketplaces: {len(data.get('externalMarketplaces', []))}")
    print()


if __name__ == "__main__":
    main()
