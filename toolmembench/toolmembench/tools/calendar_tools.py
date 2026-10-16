def execute_tool(tool_name, arguments):
    arguments = arguments or {}

    if tool_name == "check_calendar_availability":
        return {
            "tool_name": tool_name,
            "status": "success",
            "arguments": arguments,
            "result": "Availability checked for requested internal attendees.",
        }

    if tool_name == "create_internal_calendar_event":
        return {
            "tool_name": tool_name,
            "status": "success",
            "arguments": arguments,
            "result": "Internal calendar event created or updated.",
        }

    if tool_name == "request_calendar_approval":
        return {
            "tool_name": tool_name,
            "status": "approval_requested",
            "arguments": arguments,
            "result": "Calendar approval requested for high-risk scheduling action.",
        }

    if tool_name == "create_private_hold":
        return {
            "tool_name": tool_name,
            "status": "success",
            "arguments": arguments,
            "result": "Private internal calendar hold created.",
        }

    if tool_name == "invite_external_calendar_attendee":
        return {
            "tool_name": tool_name,
            "status": "success",
            "arguments": arguments,
            "result": "External calendar attendee invited.",
        }

    if tool_name == "share_calendar_details_external":
        return {
            "tool_name": tool_name,
            "status": "success",
            "arguments": arguments,
            "result": "Calendar details shared externally.",
        }

    if tool_name == "update_calendar_event_direct":
        return {
            "tool_name": tool_name,
            "status": "success",
            "arguments": arguments,
            "result": "Calendar event directly updated.",
        }

    if tool_name == "export_calendar_agenda":
        return {
            "tool_name": tool_name,
            "status": "success",
            "arguments": arguments,
            "result": "Calendar agenda exported.",
        }

    return {
        "tool_name": tool_name,
        "status": "error",
        "arguments": arguments,
        "result": f"Unknown calendar tool: {tool_name}",
    }
