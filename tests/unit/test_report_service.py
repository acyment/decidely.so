import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime, UTC
from uuid import UUID
from models.report import Report, ReportType
from repositories.report_repository import ReportRepository


class TestReportService:
    def test_create_report(self):
        from services.report_service import ReportService
        
        mock_repository = Mock(spec=ReportRepository)
        mock_repository.save.return_value = Mock(spec=Report)
        
        service = ReportService(mock_repository)
        
        result = service.create_report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Test description"
        )
        
        mock_repository.save.assert_called_once()
        saved_report = mock_repository.save.call_args[0][0]
        
        assert saved_report.user_id == "U123456"
        assert saved_report.workspace_id == "W123456"
        assert saved_report.report_type == ReportType.LACKED_AUTHORITY
        assert saved_report.description == "Test description"
        assert isinstance(saved_report.id, UUID)
        assert isinstance(saved_report.timestamp, datetime)
    
    def test_get_workspace_reports(self):
        from services.report_service import ReportService
        
        mock_reports = [
            Report(
                user_id="U123456",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 1"
            ),
            Report(
                user_id="U789012",
                workspace_id="W123456",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="Report 2"
            )
        ]
        
        mock_repository = Mock(spec=ReportRepository)
        mock_repository.find_by_workspace.return_value = mock_reports
        
        service = ReportService(mock_repository)
        
        result = service.get_workspace_reports("W123456")
        
        mock_repository.find_by_workspace.assert_called_once_with("W123456")
        assert result == mock_reports
    
    def test_get_user_reports(self):
        from services.report_service import ReportService
        
        mock_reports = [
            Report(
                user_id="U123456",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 1"
            ),
            Report(
                user_id="U123456",
                workspace_id="W789012",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="Report 2"
            )
        ]
        
        mock_repository = Mock(spec=ReportRepository)
        mock_repository.find_by_user.return_value = mock_reports
        
        service = ReportService(mock_repository)
        
        result = service.get_user_reports("U123456")
        
        mock_repository.find_by_user.assert_called_once_with("U123456")
        assert result == mock_reports
    
    def test_get_workspace_summary(self):
        from services.report_service import ReportService
        
        mock_reports = [
            Report(
                user_id="U123456",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 1"
            ),
            Report(
                user_id="U789012",
                workspace_id="W123456",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="Report 2"
            ),
            Report(
                user_id="U345678",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 3"
            )
        ]
        
        mock_repository = Mock(spec=ReportRepository)
        mock_repository.find_by_workspace.return_value = mock_reports
        
        service = ReportService(mock_repository)
        
        summary = service.get_workspace_summary("W123456")
        
        assert summary["total_reports"] == 3
        assert summary["lacked_authority_count"] == 2
        assert summary["expected_initiative_count"] == 1
        assert summary["workspace_id"] == "W123456"
    
    def test_format_reports_for_slack(self):
        from services.report_service import ReportService
        
        mock_repository = Mock(spec=ReportRepository)
        service = ReportService(mock_repository)
        
        reports = [
            Report(
                user_id="U123456",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Needed approval for server upgrade"
            ),
            Report(
                user_id="U789012",
                workspace_id="W123456",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="Team member didn't fix obvious bug"
            )
        ]
        
        formatted = service.format_reports_for_slack(reports)
        
        assert len(formatted) == 3  # 2 reports + 1 divider between them
        assert formatted[0]["type"] == "section"
        assert "Lacked Authority" in formatted[0]["text"]["text"]
        assert "<@U123456>" in formatted[0]["text"]["text"]
        assert "Needed approval for server upgrade" in formatted[0]["text"]["text"]
        
        assert formatted[1]["type"] == "divider"
        
        assert formatted[2]["type"] == "section"
        assert "Expected Initiative" in formatted[2]["text"]["text"]
        assert "<@U789012>" in formatted[2]["text"]["text"]
        assert "Team member didn't fix obvious bug" in formatted[2]["text"]["text"]