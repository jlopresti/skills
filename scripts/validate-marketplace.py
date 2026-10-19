#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
LINK = re.compile(r"\]\(([^)\s]+)(?:\s+[^)]*)?\)")
NAME = re.compile(r"^name:\s*([^\s]+)\s*$", re.MULTILINE)


class InvalidMarketplace(Exception):
    pass


def require(condition, message):
    if not condition:
        raise InvalidMarketplace(message)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise InvalidMarketplace(f"{path.relative_to(ROOT)}: {error}") from error


def plugin_root(raw_path):
    require(isinstance(raw_path, str) and raw_path.startswith("./"),
            f"Plugin source must be a ./ path: {raw_path!r}")
    path = (ROOT / raw_path).resolve()
    require(path.is_relative_to(ROOT) and path.is_dir(),
            f"Plugin source is missing or leaves the repository: {raw_path}")
    return path


def catalog_routes(path, host):
    catalog = load_json(path)
    require(isinstance(catalog, dict) and isinstance(catalog.get("name"), str)
            and catalog["name"], f"{host}: missing marketplace name")
    entries = catalog.get("plugins")
    require(isinstance(entries, list) and entries, f"{host}: no plugins")
    routes = set()
    for entry in entries:
        require(isinstance(entry, dict) and isinstance(entry.get("name"), str)
                and entry["name"], f"{host}: plugin has no name")
        require("version" not in entry and "description" not in entry,
                f"{host}: plugin identity belongs in plugin.json")
        source = entry.get("source")
        if host == "Codex":
            require(isinstance(source, dict) and source.get("source") == "local",
                    "Codex: expected a local source object")
            source = source.get("path")
        route = (entry["name"], plugin_root(source))
        require(route not in routes, f"{host}: duplicate plugin {entry['name']}")
        routes.add(route)
    return catalog["name"], routes


def skill_name(path):
    content = path.read_text(encoding="utf-8")
    require(content.startswith("---\n"), f"{path.relative_to(ROOT)}: missing frontmatter")
    frontmatter = content.split("\n---\n", 1)[0]
    match = NAME.search(frontmatter)
    require(match is not None, f"{path.relative_to(ROOT)}: missing skill name")
    return match.group(1)


def check_links(skill):
    checked = 0
    for document in skill.rglob("*.md"):
        for target in LINK.findall(document.read_text(encoding="utf-8")):
            if target.startswith(("#", "//")) or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            local = unquote(target.split("#", 1)[0].split("?", 1)[0])
            require(local and not local.startswith("/"),
                    f"{document.relative_to(ROOT)}: invalid local link {target}")
            resolved = (document.parent / local).resolve()
            require(resolved.is_relative_to(skill) and resolved.exists(),
                    f"{document.relative_to(ROOT)}: broken or escaping link {target}")
            checked += 1
    return checked


def validate():
    codex_name, codex_routes = catalog_routes(ROOT / ".agents/plugins/marketplace.json", "Codex")
    copilot_name, copilot_routes = catalog_routes(ROOT / ".github/plugin/marketplace.json", "Copilot")
    require(codex_name == copilot_name, "Marketplace names differ")
    require(codex_routes == copilot_routes, "Codex and Copilot plugin routes differ")
    skill_files = set()
    names = set()
    link_count = 0
    for name, package in sorted(codex_routes):
        manifest = load_json(package / "plugin.json")
        require(manifest.get("$schema") == SCHEMA and manifest.get("name") == name,
                f"{package.relative_to(ROOT)}: invalid portable schema or name")
        require(isinstance(manifest.get("version"), str) and manifest["version"]
                and isinstance(manifest.get("description"), str) and manifest["description"],
                f"{package.relative_to(ROOT)}: missing version or description")
        overlay = load_json(package / ".codex-plugin/plugin.json")
        for field in ("name", "version", "description"):
            require(overlay.get(field) == manifest[field],
                    f"{package.relative_to(ROOT)}: Codex {field} differs from plugin.json")
        interface = manifest.get("extensions", {}).get("com.openai", {}).get("interface")
        require(isinstance(interface, dict) and overlay.get("interface") == interface,
                f"{package.relative_to(ROOT)}: Codex interface differs from plugin.json")
        skills = package / "skills"
        require(skills.is_dir(), f"{package.relative_to(ROOT)}: missing skills directory")
        for skill in sorted(skills.iterdir()):
            require(skill.is_dir() and not skill.is_symlink() and (skill / "SKILL.md").is_file(),
                    f"{skill.relative_to(ROOT)}: expected an immediate skill directory")
            file = skill / "SKILL.md"
            declared = skill_name(file)
            require(declared == skill.name and declared not in names,
                    f"{file.relative_to(ROOT)}: directory and unique frontmatter name must agree")
            names.add(declared)
            skill_files.add(file.resolve())
            link_count += check_links(skill)
    require(skill_files, "No packaged skills found")
    all_skills = {path.resolve() for path in ROOT.rglob("SKILL.md")}
    require(all_skills == skill_files,
            "SKILL.md files exist outside registered immediate plugin skill directories")
    print(f"Validated {len(codex_routes)} plugin, {len(skill_files)} skills, and {link_count} local links.")


if __name__ == "__main__":
    try:
        validate()
    except (InvalidMarketplace, OSError, UnicodeError) as error:
        print(f"Marketplace validation failed: {error}", file=sys.stderr)
        sys.exit(1)
