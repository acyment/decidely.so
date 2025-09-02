import pytest
from unittest.mock import Mock, MagicMock, patch
from models.report import ReportType
from services.report_service import ReportService
from repositories.report_repository import InMemoryReportRepository


class TestDecidelyReportCommand:
    def test_report_command_shows_dialog(self):
        from listeners.commands.decidely_report import decidely_report_callback
        
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
        mock_respond.assert_not_called()
        
        view_args = mock_client.views_open.call_args[1]
        assert view_args["trigger_id"] == "123.456"
        
        view = view_args["view"]
        assert view["type"] == "modal"
        assert view["title"]["text"] == "Report Decision"
        assert len(view["blocks"]) == 2  # Report type selector and description input
    
    def test_report_submission_creates_report(self):
        from listeners.views.decidely_report_view import handle_report_submission
        
        mock_ack = Mock()
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
                            "value": "Could not approve budget increase"
                        }
                    }
                }
            },
        }
        mock_body = {
            "user": {
                "id": "U123456"
            },
            "team": {
                "id": "T123456"
            }
        }
        
        with patch('listeners.views.decidely_report_view.report_service') as mock_service:
            handle_report_submission(
                ack=mock_ack,
                body=mock_body,
                view=mock_view
            )
            
            mock_ack.assert_called_once()
            mock_service.create_report.assert_called_once_with(
                user_id="U123456",
                workspace_id="T123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Could not approve budget increase"
            )
    
    def test_inline_command_creates_report_directly(self):
        from listeners.commands.decidely_report import decidely_report_callback
        
        mock_ack = Mock()
        mock_client = Mock()
        mock_respond = Mock()
        mock_command = {
            "trigger_id": "123.456",
            "user_id": "U123456",
            "team_id": "T123456",
            "text": "authority couldn't approve the budget increase"
        }
        
        with patch('listeners.commands.decidely_report.report_service') as mock_service:
            decidely_report_callback(
                ack=mock_ack,
                command=mock_command,
                client=mock_client,
                respond=mock_respond
            )
            
            mock_ack.assert_called_once()
            mock_client.views_open.assert_not_called()  # Should not open form
            mock_service.create_report.assert_called_once_with(
                user_id="U123456",
                workspace_id="T123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="couldn't approve the budget increase"
            )
            mock_respond.assert_called_once()
            
            # Check confirmation message
            respond_args = mock_respond.call_args[1]
            assert "✅ Report created" in respond_args["text"]
    
    def test_inline_command_with_initiative_shortcut(self):
        from listeners.commands.decidely_report import decidely_report_callback
        
        mock_ack = Mock()
        mock_client = Mock()
        mock_respond = Mock()
        mock_command = {
            "trigger_id": "123.456",
            "user_id": "U123456",
            "team_id": "T123456",
            "text": "ei developer didn't fix obvious typo"
        }
        
        with patch('listeners.commands.decidely_report.report_service') as mock_service:
            decidely_report_callback(
                ack=mock_ack,
                command=mock_command,
                client=mock_client,
                respond=mock_respond
            )
            
            mock_service.create_report.assert_called_once_with(
                user_id="U123456",
                workspace_id="T123456",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="developer didn't fix obvious typo"
            )
    
    def test_incomplete_inline_command_shows_help(self):
        from listeners.commands.decidely_report import decidely_report_callback
        
        mock_ack = Mock()
        mock_client = Mock()
        mock_respond = Mock()
        mock_command = {
            "trigger_id": "123.456",
            "user_id": "U123456",
            "team_id": "T123456",
            "text": "authority"  # Missing description
        }
        
        decidely_report_callback(
            ack=mock_ack,
            command=mock_command,
            client=mock_client,
            respond=mock_respond
        )
        
        mock_ack.assert_called_once()
        mock_client.views_open.assert_not_called()
        mock_respond.assert_called_once()
        
        # Check help message
        respond_args = mock_respond.call_args[1]
        assert "Usage:" in respond_args["text"]
    
    def test_spanish_command_creates_report(self):
        from listeners.commands.decidely_report import decidely_report_callback
        
        mock_ack = Mock()
        mock_client = Mock()
        mock_respond = Mock()
        mock_command = {
            "trigger_id": "123.456",
            "user_id": "U123456",
            "team_id": "T123456",
            "text": "autoridad no pude aprobar el presupuesto"
        }
        
        with patch('listeners.commands.decidely_report.report_service') as mock_service:
            with patch('listeners.commands.decidely_report.get_user_locale') as mock_locale:
                mock_locale.return_value = "es_ES"
                
                decidely_report_callback(
                    ack=mock_ack,
                    command=mock_command,
                    client=mock_client,
                    respond=mock_respond
                )
                
                mock_service.create_report.assert_called_once_with(
                    user_id="U123456",
                    workspace_id="T123456",
                    report_type=ReportType.LACKED_AUTHORITY,
                    description="no pude aprobar el presupuesto"
                )
                
                # Check Spanish confirmation message
                respond_args = mock_respond.call_args[1]
                assert "¡Reporte creado!" in respond_args["blocks"][0]["text"]["text"]
    
    def test_spanish_shortcut_ie(self):
        from listeners.commands.decidely_report import decidely_report_callback
        
        mock_ack = Mock()
        mock_client = Mock()
        mock_respond = Mock()
        mock_command = {
            "trigger_id": "123.456",
            "user_id": "U123456",
            "team_id": "T123456",
            "text": "ie desarrollador no corrigió error"
        }
        
        with patch('listeners.commands.decidely_report.report_service') as mock_service:
            decidely_report_callback(
                ack=mock_ack,
                command=mock_command,
                client=mock_client,
                respond=mock_respond
            )
            
            mock_service.create_report.assert_called_once_with(
                user_id="U123456",
                workspace_id="T123456",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="desarrollador no corrigió error"
            )


class TestDecidelyListCommand:
    def test_list_command_shows_workspace_reports(self):
        from listeners.commands.decidely_list import decidely_list_callback
        
        mock_ack = Mock()
        mock_respond = Mock()
        mock_command = {
            "team_id": "T123456",
            "user_id": "U123456"
        }
        
        with patch('listeners.commands.decidely_list.report_service') as mock_service:
            mock_service.get_workspace_reports.return_value = []
            mock_service.get_workspace_summary.return_value = {
                "total_reports": 0,
                "lacked_authority_count": 0,
                "expected_initiative_count": 0,
                "workspace_id": "T123456"
            }
            
            decidely_list_callback(
                ack=mock_ack,
                command=mock_command,
                respond=mock_respond
            )
            
            mock_ack.assert_called_once()
            mock_service.get_workspace_reports.assert_called_once_with("T123456")
            mock_respond.assert_called_once()
            
            blocks = mock_respond.call_args[1]["blocks"]
            assert blocks[0]["type"] == "header"
            assert "Decision Reports" in blocks[0]["text"]["text"]
    
    def test_list_command_formats_reports(self):
        from listeners.commands.decidely_list import decidely_list_callback
        from models.report import Report
        
        mock_ack = Mock()
        mock_respond = Mock()
        mock_command = {
            "team_id": "T123456",
            "user_id": "U123456"
        }
        
        mock_reports = [
            Report(
                user_id="U123456",
                workspace_id="T123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Test report"
            )
        ]
        
        with patch('listeners.commands.decidely_list.report_service') as mock_service:
            mock_service.get_workspace_reports.return_value = mock_reports
            mock_service.get_workspace_summary.return_value = {
                "total_reports": 1,
                "lacked_authority_count": 1,
                "expected_initiative_count": 0,
                "workspace_id": "T123456"
            }
            mock_service.format_reports_for_slack.return_value = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Test formatted report"
                    }
                }
            ]
            
            decidely_list_callback(
                ack=mock_ack,
                command=mock_command,
                respond=mock_respond
            )
            
            mock_service.format_reports_for_slack.assert_called_once_with(mock_reports)