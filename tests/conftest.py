import os
import sys
import matplotlib.pyplot as plt
import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

"""
Contains global test configuration, including a custom pytest hook that generates a 
visual summary of test outcomes. 
This file ensures that common test setup and reporting are centralized.
"""

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Hook function called after the test session is complete.
    This function creates a horizontal bar chart for each outcome category,
    where each bar represents a test (displaying a short version of the test name).
    The y-axis labels (test names).
    The chart is saved to a common 'reports' folder in the project root as 'test_results.png'.
    """

    stats = terminalreporter.stats
    outcomes = {
        "passed": ("Passed", "green"),
        "failed": ("Failed", "red"),
        "skipped": ("Skipped", "blue"),
        "error": ("Errors", "orange")
    }

    outcome_keys = [k for k in outcomes if k in stats and stats[k]]
    if not outcome_keys:
        return

    max_tests = max(len(stats[k]) for k in outcome_keys)
    fig_height = max(len(outcome_keys) * 2, max_tests * 0.5 + len(outcome_keys))

    fig, axes = plt.subplots(len(outcome_keys), 1, figsize=(8, fig_height), squeeze=False)

    for subplot_index, outcome in enumerate(outcome_keys):
        label, color = outcomes[outcome]
        nodeids = [r.nodeid.split("::")[-1] for r in stats[outcome]]
        num_tests = len(nodeids)
        ax = axes[subplot_index][0]
        ax.barh(range(num_tests), [1] * num_tests, color=color, align='center')
        ax.set_yticks(range(num_tests))
        ax.set_yticklabels(nodeids, fontsize=8)
        ax.invert_yaxis()
        ax.set_xlabel(label + " Tests")
        ax.set_xlim(0, 1.5)
        ax.set_ylim(num_tests - 0.5, -0.5)

    plt.suptitle("Test Results Summary (Test Names by Outcome)", fontsize=12)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    results_file = os.path.join(reports_dir, "test_results.png")
    plt.savefig(results_file)
    plt.show()


def pytest_configure(config):
    """
    Register custom pytest markers.
    """

    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )

