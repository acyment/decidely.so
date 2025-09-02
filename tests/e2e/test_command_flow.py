import pytest
from unittest.mock import Mock, MagicMock, patch
from models.report import Report, ReportType
from repositories.report_repository import InMemoryReportRepository
from services.report_service import ReportService


class TestCommandFlow:
    def test_full_report_and_list_flow(self):
        # Create a fresh repository and service
        repository = InMemoryReportRepository()
        service = ReportService(repository)
        
        # Simulate report creation
        report = service.create_report(
            user_id="U123456",
            workspace_id="T123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Could not approve overtime without manager"
        )
        
        assert report.user_id == "U123456"
        assert report.workspace_id == "T123456"
        assert report.report_type == ReportType.LACKED_AUTHORITY
        
        # Verify the report can be retrieved
        workspace_reports = service.get_workspace_reports("T123456")
        assert len(workspace_reports) == 1
        assert workspace_reports[0] == report
        
        # Verify summary is correct
        summary = service.get_workspace_summary("T123456")
        assert summary["total_reports"] == 1
        assert summary["lacked_authority_count"] == 1
        assert summary["expected_initiative_count"] == 0
        
        # Add another report
        report2 = service.create_report(
            user_id="U789012",
            workspace_id="T123456",
            report_type=ReportType.EXPECTED_INITIATIVE,
            description="Developer didn't fix obvious typo in UI"
        )
        
        # Verify updated summary
        summary = service.get_workspace_summary("T123456")
        assert summary["total_reports"] == 2
        assert summary["lacked_authority_count"] == 1
        assert summary["expected_initiative_count"] == 1
        
        # Verify formatting for Slack
        all_reports = service.get_workspace_reports("T123456")
        formatted = service.format_reports_for_slack(all_reports)
        
        assert len(formatted) == 3  # 2 reports + 1 divider
        assert "Lacked Authority" in formatted[0]["text"]["text"]
        assert "Expected Initiative" in formatted[2]["text"]["text"]
    
    def test_command_handlers_integration(self):
        from listeners.commands.decidely_report import decidely_report_callback
        from listeners.commands.decidely_list import decidely_list_callback
        from listeners.views.decidely_report_view import handle_report_submission
        
        # Test report command opens dialog
        mock_ack = Mock()
        mock_client = Mock()
        mock_respond = Mock()
        mock_command = {
            "trigger_id": "123.456",
            "user_id": "U123456",
            "team_id": "T123456",
            "text": ""
        }
        
        decidely_report_callback(
            ack=mock_ack,
            command=mock_command,
            client=mock_client,
            respond=mock_respond
        )
        
        mock_ack.assert_called_once()
        mock_client.views_open.assert_called_once()
        
        # Test view submission creates report
        mock_ack.reset_mock()
        mock_view = {
            "state": {
                "values": {
                    "report_type_block": {
                        "report_type": {
                            "selected_option": {
                                "value": "lacked_authority"
                            }
                        }
                    },
                    "description_block": {
                        "description": {
                            "value": "Test description"
                        }
                    }
                }
            }
        }
        mock_body = {
            "user": {"id": "U123456"},
            "team": {"id": "T123456"}
        }
        
        handle_report_submission(
            ack=mock_ack,
            body=mock_body,
            view=mock_view
        )
        
        mock_ack.assert_called_once()
        
        # Test list command shows the report
        mock_ack.reset_mock()
        mock_respond = Mock()
        
        decidely_list_callback(
            ack=mock_ack,
            command={"team_id": "T123456", "user_id": "U123456"},
            respond=mock_respond
        )
        
        mock_ack.assert_called_once()
        mock_respond.assert_called_once()
        
        blocks = mock_respond.call_args[1]["blocks"]
        assert any("Decision Reports" in str(block) for block in blocks)
        assert any("Total reports:" in str(block) for block in blocks)