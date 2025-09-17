import pytest
from datetime import datetime
from uuid import UUID
from models.report import Report, ReportType


class TestReportModel:
    def test_create_report_with_lacked_authority_type(self):
        report = Report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Needed approval to increase server capacity but manager was unavailable"
        )
        
        assert report.user_id == "U123456"
        assert report.workspace_id == "W123456"
        assert report.report_type == ReportType.LACKED_AUTHORITY
        assert report.description == "Needed approval to increase server capacity but manager was unavailable"
        assert isinstance(report.id, UUID)
        assert isinstance(report.timestamp, datetime)
    
    def test_create_report_with_expected_initiative_type(self):
        report = Report(
            user_id="U789012",
            workspace_id="W789012",
            report_type=ReportType.EXPECTED_INITIATIVE,
            description="Team member waited for explicit instruction to fix obvious bug"
        )
        
        assert report.user_id == "U789012"
        assert report.workspace_id == "W789012"
        assert report.report_type == ReportType.EXPECTED_INITIATIVE
        assert report.description == "Team member waited for explicit instruction to fix obvious bug"
    
    def test_report_to_dict(self):
        report = Report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Test description"
        )
        
        report_dict = report.to_dict()
        
        assert report_dict["user_id"] == "U123456"
        assert report_dict["workspace_id"] == "W123456"
        assert report_dict["report_type"] == "lacked_authority"
        assert report_dict["description"] == "Test description"
        assert "id" in report_dict
        assert "timestamp" in report_dict
    
    def test_report_from_dict(self):
        report_data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "user_id": "U123456",
            "workspace_id": "W123456",
            "report_type": "expected_initiative",
            "description": "Test description",
            "timestamp": "2024-01-01T12:00:00"
        }
        
        report = Report.from_dict(report_data)
        
        assert str(report.id) == "550e8400-e29b-41d4-a716-446655440000"
        assert report.user_id == "U123456"
        assert report.workspace_id == "W123456"
        assert report.report_type == ReportType.EXPECTED_INITIATIVE
        assert report.description == "Test description"
        assert report.timestamp == datetime(2024, 1, 1, 12, 0, 0)
    
    def test_report_str_representation(self):
        report = Report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Test description"
        )
        
        str_repr = str(report)
        assert "U123456" in str_repr
        assert "lacked_authority" in str_repr
        assert report.timestamp.strftime("%Y-%m-%d %H:%M") in str_repr


class TestReportType:
    def test_report_type_values(self):
        assert ReportType.LACKED_AUTHORITY.value == "lacked_authority"
        assert ReportType.EXPECTED_INITIATIVE.value == "expected_initiative"
    
    def test_report_type_from_string(self):
        assert ReportType("lacked_authority") == ReportType.LACKED_AUTHORITY
        assert ReportType("expected_initiative") == ReportType.EXPECTED_INITIATIVE
    
    def test_invalid_report_type_raises_error(self):
        with pytest.raises(ValueError):
            ReportType("invalid_type")