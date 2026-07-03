from __future__ import annotations

from signalforge.sprints import (
    enabled_repositories,
    generate_sprint_label,
    load_json,
    measurable_tests_present,
    select_next_sprints,
)


def test_repository_registry_has_enabled_repositories() -> None:
    registry = load_json("config/repositories.json")

    repositories = enabled_repositories(registry)

    assert "LanternProtocol/signalforge" in repositories
    assert "LanternProtocol/.github" in repositories


def test_every_ready_sprint_has_measurable_tests_and_docs() -> None:
    registry = load_json("config/repositories.json")
    backlog = load_json("config/sprints.json")
    known_repositories = set(enabled_repositories(registry))
    sprint_ids: set[str] = set()

    for sprint in backlog["sprints"]:
        assert sprint["id"] not in sprint_ids
        sprint_ids.add(sprint["id"])
        assert sprint["repository_full_name"] in known_repositories
        assert sprint["documentation_targets"]
        assert sprint["done_definition"]
        if sprint["status"] == "ready":
            assert measurable_tests_present(sprint)


def test_next_sprint_selection_returns_one_ready_item_per_repo() -> None:
    registry = load_json("config/repositories.json")
    backlog = load_json("config/sprints.json")

    selections = select_next_sprints(registry, backlog, run_id="20260703T0000Z")

    selected_repos = {selection.repository_full_name for selection in selections}
    assert "LanternProtocol/signalforge" in selected_repos
    assert "LanternProtocol/.github" in selected_repos
    assert len(selections) == len(selected_repos)


def test_generated_sprint_label_is_deterministic_and_repo_scoped() -> None:
    label = generate_sprint_label(
        "SFG-RFC-002",
        "LanternProtocol/signalforge",
        run_id="20260703T0000Z",
    )

    assert label == "run:20260703T0000Z:lanternprotocol-signalforge:sfg-rfc-002"
