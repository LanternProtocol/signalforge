from __future__ import annotations

from pathlib import Path

from signalforge.sprints import enabled_repositories, load_json, measurable_tests_present, select_next_sprints

ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = ROOT / "config" / "repositories.json"
SPRINTS = ROOT / "config" / "sprints.json"


def test_registry_and_backlog_are_measurable() -> None:
    registry = load_json(REPOSITORIES)
    backlog = load_json(SPRINTS)
    known_repositories = set(enabled_repositories(registry))

    assert known_repositories
    assert backlog["sprints"]

    seen: set[str] = set()
    for sprint in backlog["sprints"]:
        assert sprint["id"] not in seen
        seen.add(sprint["id"])
        assert sprint["repository_full_name"] in known_repositories
        assert sprint["documentation_targets"]
        assert sprint["done_definition"]
        assert measurable_tests_present(sprint)


def test_selector_returns_ready_items_for_enabled_repositories() -> None:
    registry = load_json(REPOSITORIES)
    backlog = load_json(SPRINTS)
    selections = select_next_sprints(registry, backlog, run_id="20260703T0000Z")

    selected_repos = {selection.repository_full_name for selection in selections}
    assert "LanternProtocol/signalforge" in selected_repos
    assert "LanternProtocol/.github" in selected_repos
