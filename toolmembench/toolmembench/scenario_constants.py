VALID_SCENARIOS = [
    "email",
    "finance",
    "calendar",
    "crm",
    "devops",
]

VALID_ATTACK_TYPES = [
    "tool_selection_hijacking",
    "tool_parameter_hijacking",
    "permission_boundary_violation",
    "implicit_data_leakage",
]

VALID_WRITEBACK_MODES = [
    "benign",
    "risky_descriptive",
    "directive",
]

VALID_MEMORY_CONDITIONS = [
    "no_memory",
    "initial_only",
    "writeback_only",
    "both",
]

VALID_DEFENSE_MODES = [
    "none",
    "prompt",
]

VALID_MEMORY_GUARD_MODES = [
    "no_filter",
    "risk_retrieval_filter",
    "risk_writeback_guard",
    "risk_combined_guard",
]

BASE_CLOSED_LOOP_REQUIRED_FIELDS = [
    "id",
    "closed_loop_id",
    "scenario",
    "attack_type",
    "closed_loop_goal",
    "expected_poisoned_memory",
    "expected_safe_behavior",
    "safe_tool",
    "risky_tool",
    "safe_arguments",
    "unsafe_arguments",
    "sensitive_fields",
    "round1_task",
    "round2_task",
    "future_task",
    "round1_writeback_expected_role",
]