#!/usr/bin/env python3
"""Check ourSharedMagnets' config against its rails.

Usage:
  python3 scripts/check-config.py [--config config/magnets.config.yaml]
                                  [--brain ../OCR-docs/ocr-docs-brain]

Exits 1 and prints one line per problem. With --brain it also checks the config
against the brain's data-edges.yaml and product-registry.yaml.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

SECRET_NAME = re.compile(r"^[A-Z][A-Z0-9_]{2,}$")
SECRET_VALUE = re.compile(r"(Bearer\s+\S+|(?=[A-Za-z0-9+/_\-]*\d)[A-Za-z0-9+/_\-]{32,}={0,2})")
KNOWN_SOURCES = {"ose", "ow", "oaw"}
# Boundary doc section 4.4: the only fields OSM may ever emit.
E4_FIELDS = {"api_key_hash", "ritual_type", "period_bucket", "call_count",
             "franchise_id", "corridor_id", "deployment_tier", "active_since"}
REQUIRED_NEVER_IN_MOCKS = {"attendee_name", "attendee_email", "raw_anon_id", "ip_address", "request_geo"}
REQUIRED_NEVER_GATED = {"security", "audit", "isolation", "retention", "under_5_floor"}


def check_config(cfg: dict) -> list[str]:
    errs: list[str] = []
    for key in ["schema_version", "app", "environments", "api_sources", "collection_tool",
                "mock_data", "telemetry", "franchise", "never_tier_gated"]:
        if key not in cfg:
            errs.append(f"missing top-level key: {key}")
    if errs:
        return errs
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(cfg["schema_version"])):
        errs.append("schema_version must read like 1.0.0")
    app = cfg["app"]
    if app.get("id") != "osm" or app.get("side") != "anonymous":
        errs.append("app must be id osm on the anonymous side")

    envs = cfg["environments"]
    stg = envs.get("staging") or {}
    if not stg.get("enabled"):
        errs.append("environments.staging must be enabled (staging is the environment of record)")
    for k in ("ose_base_url", "ow_base_url"):
        if not str(stg.get(k, "")).startswith("https://stg."):
            errs.append(f"environments.staging.{k} must be a https://stg. host")
    if (envs.get("production") or {}).get("enabled") is not False:
        errs.append("environments.production.enabled must be false: production is closed until the owner opens it")

    for sid, src in (cfg["api_sources"] or {}).items():
        if sid not in KNOWN_SOURCES:
            errs.append(f"api_sources.{sid}: OSM documents ose, ow and oaw only")
        name = (src or {}).get("auth_secret")
        if name is not None and not SECRET_NAME.fullmatch(str(name)):
            errs.append(f"api_sources.{sid}.auth_secret must be a secret NAME, never a value")
        if not (src or {}).get("route_table"):
            errs.append(f"api_sources.{sid}.route_table must say where the product's route table is")

    md = cfg["mock_data"] or {}
    if md.get("people") != "synthetic_only":
        errs.append("mock_data.people must be synthetic_only: never a real person")
    if md.get("counts_follow_under_5_floor") is not True:
        errs.append("mock_data.counts_follow_under_5_floor must be true")
    if md.get("location") != "h3_cell_only":
        errs.append("mock_data.location must be h3_cell_only: place, not person")
    missing = REQUIRED_NEVER_IN_MOCKS - set(md.get("never_contains") or [])
    if missing:
        errs.append(f"mock_data.never_contains is missing: {', '.join(sorted(missing))}")

    tel = cfg["telemetry"] or {}
    if tel.get("edge") != "E4":
        errs.append("telemetry.edge must be E4, the one listed link from OSM")
    extra = set(tel.get("allowed_fields") or []) - E4_FIELDS
    if extra:
        errs.append(f"telemetry.allowed_fields go beyond the boundary doc 4.4: {', '.join(sorted(extra))}")
    if tel.get("enabled") is not False and not cfg["app"].get("code_present"):
        errs.append("telemetry.enabled must be false while OSM has no code (E4 is contract_only)")

    fr = cfg["franchise"] or {}
    if fr.get("deployment_handled_by") != "oaw":
        errs.append("franchise.deployment_handled_by must be oaw: OSM tells you how, OA does it")
    if "corridor-definitions.yaml" not in str(fr.get("corridors_source", "")):
        errs.append("franchise.corridors_source must point at the brain's corridor-definitions.yaml, not a copy")

    missing = REQUIRED_NEVER_GATED - set(cfg["never_tier_gated"] or [])
    if missing:
        errs.append(f"never_tier_gated is missing: {', '.join(sorted(missing))}")

    _scan(cfg, "config", errs)
    return errs


def _scan(node, where: str, errs: list[str]) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            _scan(v, f"{where}.{k}", errs)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _scan(v, f"{where}[{i}]", errs)
    elif isinstance(node, str) and SECRET_VALUE.search(node) and not node.startswith("http"):
        if not SECRET_NAME.fullmatch(node):
            errs.append(f"{where} looks like a credential value; name the secret, never paste it")


def check_against_brain(cfg: dict, brain: Path) -> list[str]:
    errs: list[str] = []
    edges = yaml.safe_load((brain / "data-edges.yaml").read_text())
    node = next((n for n in edges.get("nodes", []) if n.get("id") == "osm"), None)
    if not node or node.get("side") != cfg["app"]["side"]:
        errs.append("brain: data-edges.yaml node osm is missing or on another side")
    e4 = next((e for e in edges.get("edges", []) if e.get("id") == "E4"), None)
    if not e4 or e4.get("from") != "osm" or e4.get("to") != "oer":
        errs.append("brain: edge E4 (osm -> oer) is not in data-edges.yaml")
    elif cfg["telemetry"].get("enabled") and e4.get("status") in ("contract_only", "decided", "proposed"):
        errs.append(f"brain: telemetry is on but E4 is still {e4.get('status')}")
    reg = yaml.safe_load((brain / "product-registry.yaml").read_text())
    rows = reg if isinstance(reg, list) else reg.get("products", [])
    row = next((r for r in rows if isinstance(r, dict) and r.get("product_id") == "osm"), None)
    if not row:
        errs.append("brain: product-registry.yaml has no osm row")
    elif bool(row.get("code_present", True)) != bool(cfg["app"].get("code_present")):
        errs.append("brain: app.code_present disagrees with product-registry.yaml")
    return errs


def main(argv=None) -> int:
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(here / "config/magnets.config.yaml"))
    ap.add_argument("--brain", default=None)
    a = ap.parse_args(argv)
    cfg = yaml.safe_load(Path(a.config).read_text())
    errs = check_config(cfg)
    if not errs and a.brain:
        errs += check_against_brain(cfg, Path(a.brain))
    for e in errs:
        print(f"::error::{e}")
    if errs:
        print(f"{len(errs)} problem(s) in the ourSharedMagnets config")
        return 1
    print("ourSharedMagnets config: every rail holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
