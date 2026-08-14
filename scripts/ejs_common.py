#!/usr/bin/env python3
"""Deterministic helpers: init bundle, write concept, pack, validate."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "untitled"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    if yaml:
        meta = yaml.safe_load(parts[1]) or {}
    else:
        for line in parts[1].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, parts[2].lstrip("\n")


def dump_frontmatter(meta: dict) -> str:
    lines = ["---"]
    for k, v in meta.items():
        if v is None:
            continue
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                if isinstance(item, dict):
                    lines.append(f"  - target: {item.get('target', '')}")
                    if item.get("rel"):
                        lines.append(f"    rel: {item['rel']}")
                else:
                    lines.append(f"  - {item}")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def bundle_root(path: Path) -> Path:
    p = Path(path)
    if p.exists() and p.is_dir():
        return p
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_concept(path: Path, meta: dict, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = dump_frontmatter(meta) + "\n" + body.rstrip() + "\n"
    path.write_text(content, encoding="utf-8")
    return path


def catalog_index(bundle: Path, folder: str, title: str) -> None:
    d = bundle / folder
    d.mkdir(parents=True, exist_ok=True)
    idx = d / "index.md"
    if not idx.exists():
        write_concept(
            idx,
            {"type": "Index", "title": title, "timestamp": now_iso()},
            f"# {title}\n\nCatalog of `{folder}` concepts.\n",
        )


def cmd_init(args) -> int:
    bundle = bundle_root(Path(args.bundle))
    catalogs = args.catalogs.split(",") if args.catalogs else []
    write_concept(
        bundle / "index.md",
        {
            "okf_version": "0.2",
            "title": args.title,
            "description": args.description or args.title,
            "timestamp": now_iso(),
        },
        f"# {args.title}\n\nShared second-brain bundle. Progressive disclosure starts here.\n",
    )
    log = bundle / "log.md"
    if not log.exists():
        log.write_text(f"# Log\n\n- {now_iso()} — bundle initialized\n", encoding="utf-8")
    for cat in catalogs:
        catalog_index(bundle, cat.strip(), cat.strip().replace("-", " ").title())
    print(json.dumps({"ok": True, "bundle": str(bundle), "catalogs": catalogs}))
    return 0


def cmd_write(args) -> int:
    bundle = bundle_root(Path(args.bundle))
    slug = args.slug or slugify(args.title)
    folder = args.folder
    dest = bundle / folder / f"{slug}.md"
    meta = {
        "type": args.type,
        "title": args.title,
        "status": args.status or "active",
        "timestamp": now_iso(),
        "author": args.author or "",
    }
    if args.tags:
        meta["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
    body = args.body or f"# {args.title}\n"
    write_concept(dest, meta, body)
    catalog_index(bundle, folder, folder.replace("-", " ").title())
    print(json.dumps({"ok": True, "path": str(dest)}))
    return 0


def iter_concepts(bundle: Path):
    for p in bundle.rglob("*.md"):
        if p.name in {"index.md", "log.md"}:
            continue
        text = p.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        if not meta.get("type"):
            continue
        rel = "/" + str(p.relative_to(bundle)).replace("\\", "/")
        yield {"path": rel, "file": p, "meta": meta, "body": body}


def cmd_validate(args) -> int:
    bundle = Path(args.bundle)
    errors = []
    seen = []
    for c in iter_concepts(bundle):
        seen.append(c["path"])
        for req in ("type", "title"):
            if not c["meta"].get(req):
                errors.append(f"{c['path']}: missing {req}")
        for link in c["meta"].get("links") or []:
            if isinstance(link, dict):
                target = link.get("target", "")
                if target.startswith("/") and not (bundle / target.lstrip("/")).exists():
                    errors.append(f"{c['path']}: broken link {target}")
    result = {"ok": len(errors) == 0, "concepts": len(seen), "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


def cmd_pack(args) -> int:
    bundle = Path(args.bundle)
    concepts = {c["path"]: c for c in iter_concepts(bundle)}
    root = args.root
    if not root.startswith("/"):
        # resolve by title or slug
        matches = [p for p, c in concepts.items() if c["meta"].get("title", "").lower() == root.lower() or p.endswith("/" + root + ".md") or p.endswith(root + ".md")]
        if not matches:
            print(json.dumps({"error": f"root not found: {root}"}))
            return 1
        root = matches[0]
    hops = int(args.hops)
    max_nodes = int(args.max_nodes)

    def neighbors(path: str):
        c = concepts.get(path)
        if not c:
            return []
        out = []
        for link in c["meta"].get("links") or []:
            if isinstance(link, dict) and link.get("target"):
                out.append(link["target"])
            elif isinstance(link, str):
                out.append(link)
        for m in re.findall(r"\(/[^\)]+\.md\)", c["body"]):
            out.append(m[1:-1])
        return out

    included = []
    frontier = [(root, 0)]
    seen = set()
    while frontier and len(included) < max_nodes:
        node, d = frontier.pop(0)
        if node in seen or node not in concepts:
            continue
        seen.add(node)
        included.append(node)
        if d < hops:
            for n in neighbors(node):
                if n not in seen:
                    frontier.append((n, d + 1))

    lines = [
        f"# Context pack: {concepts[root]['meta'].get('title', root)}",
        "",
        f"Hops: {hops} | Nodes: {len(included)} | Generated: {now_iso()}",
        "",
    ]
    for p in included:
        c = concepts[p]
        lines.append(f"## {c['meta'].get('title')} (`{c['meta'].get('type')}`)")
        lines.append(f"Path: `{p}`")
        desc = c["meta"].get("description") or c["body"].strip().split("\n")[0][:240]
        lines.append(desc)
        lines.append("")
    out = Path(args.out) if args.out else bundle / "packs" / f"{slugify(concepts[root]['meta'].get('title', 'pack'))}-pack.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"ok": True, "path": str(out), "nodes": included}))
    return 0


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init-bundle")
    i.add_argument("--bundle", required=True)
    i.add_argument("--title", default="Second Brain")
    i.add_argument("--description", default="")
    i.add_argument("--catalogs", default="")

    w = sub.add_parser("write")
    w.add_argument("--bundle", required=True)
    w.add_argument("--type", required=True)
    w.add_argument("--title", required=True)
    w.add_argument("--folder", required=True)
    w.add_argument("--slug", default="")
    w.add_argument("--status", default="active")
    w.add_argument("--author", default="")
    w.add_argument("--tags", default="")
    w.add_argument("--body", default="")

    v = sub.add_parser("validate")
    v.add_argument("--bundle", required=True)

    k = sub.add_parser("pack")
    k.add_argument("--bundle", required=True)
    k.add_argument("--root", required=True)
    k.add_argument("--hops", default="2")
    k.add_argument("--max-nodes", default="20")
    k.add_argument("--out", default="")

    args = p.parse_args()
    fn = {"init-bundle": cmd_init, "write": cmd_write, "validate": cmd_validate, "pack": cmd_pack}[args.cmd]
    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
