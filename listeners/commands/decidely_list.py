from slack_bolt import Ack, Respond
from typing import Dict, Any
from repositories.report_repository import InMemoryReportRepository
from services.report_service import ReportService

# Initialize the service with an in-memory repository for MVP
report_repository = InMemoryReportRepository()
report_service = ReportService(report_repository)


def decidely_list_callback(
    ack: Ack,
    command: Dict[str, Any],
    respond: Respond
) -> None:
    ack()
    
    workspace_id = command["team_id"]
    reports = report_service.get_workspace_reports(workspace_id)
    summary = report_service.get_workspace_summary(workspace_id)
    
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📊 Decision Reports"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*Summary for this workspace:*\n"
                    f"• Total reports: {summary['total_reports']}\n"
                    f"• Lacked authority/information: {summary['lacked_authority_count']}\n"
                    f"• Expected initiative: {summary['expected_initiative_count']}"
                )
            }
        }
    ]
    
    if reports:
        blocks.append({"type": "divider"})
        blocks.extend(report_service.format_reports_for_slack(reports))
    else:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_No reports yet. Use `/decidely` to submit one._"
            }
        })
    
    # Use respond() which works in any channel, even if bot is not a member
    respond(
        text=f"📊 Decision Reports - Total: {summary['total_reports']}",
        blocks=blocks
    )