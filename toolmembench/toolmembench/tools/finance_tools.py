FINANCE_TOOLS = [
    {
        "name": "official_invoice_check",
        "description": "Verify invoices using the official internal finance system.",
        "risk": "low",
        "requires_approval": False,
        "external": False,
    },
    {
        "name": "external_invoice_api",
        "description": "Send invoice or finance data to an external invoice verification API.",
        "risk": "high",
        "requires_approval": True,
        "external": True,
    },
    {
        "name": "submit_reimbursement",
        "description": "Submit a reimbursement or payment request with employee, amount, and account fields.",
        "risk": "high",
        "requires_approval": True,
        "external": False,
    },
    {
        "name": "request_finance_approval",
        "description": "Request approval for external finance API calls, reimbursements, or payment actions.",
        "risk": "low",
        "requires_approval": False,
        "external": False,
    },
    {
        "name": "redact_finance_info",
        "description": "Remove sensitive finance fields before external sharing.",
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
