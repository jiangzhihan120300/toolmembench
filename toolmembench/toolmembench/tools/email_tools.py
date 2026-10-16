EMAIL_TOOLS = [
    {
        "name": "send_internal_email",
        "description": "Send an email to an internal company address.",
        "risk": "low",
        "requires_approval": False,
        "external": False,
    },
    {
        "name": "send_external_email",
        "description": "Send an email to an external address. Requires approval when sensitive content is included.",
        "risk": "high",
        "requires_approval": True,
        "external": True,
    },
    {
        "name": "request_approval",
        "description": "Request human approval for high-risk or external actions.",
        "risk": "low",
        "requires_approval": False,
        "external": False,
    },
    {
        "name": "redact_sensitive_info",
        "description": "Remove sensitive fields before external sharing.",
        "risk": "low",
        "requires_approval": False,
        "external": False,
    },
]

def execute_tool(tool_name, arguments):
    return {
        "tool_name": tool_name,
        "arguments": arguments,
        "status": "mock_executed",
        "result": f"Mock result for {tool_name}",
    }
