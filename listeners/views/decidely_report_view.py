from slack_bolt import Ack
from typing import Dict, Any
from models.report import ReportType
from listeners.commands.decidely_list import report_service


def handle_report_submission(ack: Ack, body: Dict[str, Any], view: Dict[str, Any]) -> None:
    """Handle the submission of the decidely report form."""
    # Always acknowledge first
    ack()
    
    # Extract team and user information from body
    team_id = body["team"]["id"]
    user_id = body["user"]["id"]
    
    # Extract form values from view state
    state_values = view["state"]["values"]
    report_type_value = state_values["report_type_block"]["report_type"]["selected_option"]["value"]
    description = state_values["description_block"]["description"]["value"]
    
    # Convert to enum
    report_type = ReportType(report_type_value)
    
    # Create the report
    report_service.create_report(
        user_id=user_id,
        workspace_id=team_id,
        report_type=report_type,
        description=description
    )
    
    print(f"✅ Report created: {report_type.value} by {user_id} in workspace {team_id}")