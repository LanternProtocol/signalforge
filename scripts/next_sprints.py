#!/usr/bin/env python3
"""Emit the next SignalForge sprint selections for an orchestration run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from signalforge.sprints import (
    DEFAULT_REPOSITORY_REGISTRY,
    DEFAULT_SPRINT_BACKLOG,
    load_json,
    selections_as_dicts,
    select_next_sprints,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repositories", type=Path, default=DEFAULT_REPOSITORY_REGISTRY)
    parser.add_argument("--backlog", type=Path, default=DEFAULT_SPRINT_BACKLOG)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    registry = load_json(args.repositories)
    backlog = load_json(args.backlog)
    selections = select_next_sprints(registry, backlog, run_id=args.run_id)
    serialized = selections_as_dicts(selections)

    if args.output == "json":
        print(json.dumps({"selected_sprints": serialized}, indent=2, sort_keys=True))
    else:
        print("# Selected sprints")
        for selection in serialized:
            print()
            print(f"## {selection['sprint_id']} — {selection['title']}")
            print(f"- Repository: `{selection['repository_full_name']}`")
            print(f"- Priority: `{selection['priority']}`")
            print(f"- Generated label: `{selection['generated_label']}`")
            if selection["issue"]:
                print(f"- Issue: `#{selection['issue']}`")
            print("- Completion tests:")
            for test in selection["completion_tests"]:
                print(f"  - {test['name']} ({test['type']})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
