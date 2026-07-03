"""Sprint orchestration helpers for SignalForge continuous motion."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPOSITORY_REGISTRY = REPO_ROOT / "config" / "repositories.json"
DEFAULT_SPRINT_BACKLOG = REPO_ROOT / "config" / "sprints.json"


@dataclass(frozen=True)
class SprintSelection:
    """A sprint selected for an hourly orchestration run."""

    sprint_id: str
    repository_full_name: str
    title: str
    priority: int
    issue: int | None
    generated_label: str
    labels: tuple[str, ...]
    completion_tests: tuple[dict[str, Any], ...]
    documentation_targets: tuple[str, ...]
    done_definition: tuple[str, ...]


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON from a path."""

    return json.loads(path.read_text(encoding="utf-8"))


def repo_slug(repository_full_name: str) -> str:
    """Return a label-safe repository slug."""

    return repository_full_name.lower().replace("/", "-").replace(".", "dot")


def generate_sprint_label(sprint_id: str, repository_full_name: str, run_id: str | None = None) -> str:
    """Generate a deterministic label for a sprint during a run."""

    resolved_run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%HZ")
    return f"run:{resolved_run_id}:{repo_slug(repository_full_name)}:{sprint_id.lower()}"


def enabled_repositories(registry: dict[str, Any]) -> list[str]:
    """Return enabled repositories in registry order."""

    repositories = registry.get("repositories", [])
    return [repo["repository_full_name"] for repo in repositories if repo.get("enabled", False)]


def measurable_tests_present(sprint: dict[str, Any]) -> bool:
    """Return whether a sprint declares at least one measurable completion test."""

    tests = sprint.get("completion_tests", [])
    if not tests:
        return False
    for test in tests:
        if not test.get("name") or not test.get("type"):
            return False
        if not test.get("command") and not test.get("evidence_required"):
            return False
    return True


def select_next_sprints(
    registry: dict[str, Any],
    backlog: dict[str, Any],
    *,
    run_id: str | None = None,
) -> list[SprintSelection]:
    """Select the next ready sprint for each enabled repository."""

    policy = backlog["selection_policy"]
    max_items = int(policy.get("max_items_per_repo_per_run", 1))
    skip_blocked = bool(policy.get("skip_blocked", True))
    require_tests = bool(policy.get("require_measurable_tests", True))
    repo_names = enabled_repositories(registry)
    selections: list[SprintSelection] = []

    for repository_full_name in repo_names:
        candidates = [
            sprint
            for sprint in backlog["sprints"]
            if sprint["repository_full_name"] == repository_full_name
        ]
        if skip_blocked:
            candidates = [sprint for sprint in candidates if sprint["status"] != "blocked"]
        candidates = [sprint for sprint in candidates if sprint["status"] == "ready"]
        if require_tests:
            candidates = [sprint for sprint in candidates if measurable_tests_present(sprint)]

        candidates.sort(key=lambda sprint: (-int(sprint["priority"]), sprint["id"]))
        for sprint in candidates[:max_items]:
            selections.append(
                SprintSelection(
                    sprint_id=sprint["id"],
                    repository_full_name=repository_full_name,
                    title=sprint["title"],
                    priority=int(sprint["priority"]),
                    issue=sprint.get("issue"),
                    generated_label=generate_sprint_label(
                        sprint["id"], repository_full_name, run_id=run_id
                    ),
                    labels=tuple(sprint["labels"]),
                    completion_tests=tuple(sprint["completion_tests"]),
                    documentation_targets=tuple(sprint["documentation_targets"]),
                    done_definition=tuple(sprint["done_definition"]),
                )
            )

    return selections


def selections_as_dicts(selections: list[SprintSelection]) -> list[dict[str, Any]]:
    """Serialize sprint selections for CLI output."""

    return [
        {
            "sprint_id": selection.sprint_id,
            "repository_full_name": selection.repository_full_name,
            "title": selection.title,
            "priority": selection.priority,
            "issue": selection.issue,
            "generated_label": selection.generated_label,
            "labels": list(selection.labels),
            "completion_tests": list(selection.completion_tests),
            "documentation_targets": list(selection.documentation_targets),
            "done_definition": list(selection.done_definition),
        }
        for selection in selections
    ]
