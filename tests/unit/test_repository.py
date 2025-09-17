import pytest
from datetime import datetime, UTC
from uuid import UUID
from typing import List, Optional
from models.report import Report, ReportType


class TestReportRepository:
    def test_save_report(self):
        from repositories.report_repository import InMemoryReportRepository
        
        repo = InMemoryReportRepository()
        report = Report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Test report"
        )
        
        saved_report = repo.save(report)
        
        assert saved_report == report
        assert saved_report.id == report.id
    
    def test_find_by_id(self):
        from repositories.report_repository import InMemoryReportRepository
        
        repo = InMemoryReportRepository()
        report = Report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Test report"
        )
        
        repo.save(report)
        found_report = repo.find_by_id(report.id)
        
        assert found_report == report
    
    def test_find_by_id_not_found(self):
        from repositories.report_repository import InMemoryReportRepository
        
        repo = InMemoryReportRepository()
        non_existent_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        
        found_report = repo.find_by_id(non_existent_id)
        
        assert found_report is None
    
    def test_find_by_workspace(self):
        from repositories.report_repository import InMemoryReportRepository
        
        repo = InMemoryReportRepository()
        
        report1 = Report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Report 1"
        )
        report2 = Report(
            user_id="U789012",
            workspace_id="W123456",
            report_type=ReportType.EXPECTED_INITIATIVE,
            description="Report 2"
        )
        report3 = Report(
            user_id="U345678",
            workspace_id="W789012",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Report 3"
        )
        
        repo.save(report1)
        repo.save(report2)
        repo.save(report3)
        
        workspace_reports = repo.find_by_workspace("W123456")
        
        assert len(workspace_reports) == 2
        assert report1 in workspace_reports
        assert report2 in workspace_reports
        assert report3 not in workspace_reports
    
    def test_find_by_user(self):
        from repositories.report_repository import InMemoryReportRepository
        
        repo = InMemoryReportRepository()
        
        report1 = Report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Report 1"
        )
        report2 = Report(
            user_id="U123456",
            workspace_id="W789012",
            report_type=ReportType.EXPECTED_INITIATIVE,
            description="Report 2"
        )
        report3 = Report(
            user_id="U789012",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Report 3"
        )
        
        repo.save(report1)
        repo.save(report2)
        repo.save(report3)
        
        user_reports = repo.find_by_user("U123456")
        
        assert len(user_reports) == 2
        assert report1 in user_reports
        assert report2 in user_reports
        assert report3 not in user_reports
    
    def test_find_by_type(self):
        from repositories.report_repository import InMemoryReportRepository
        
        repo = InMemoryReportRepository()
        
        report1 = Report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Report 1"
        )
        report2 = Report(
            user_id="U789012",
            workspace_id="W123456",
            report_type=ReportType.EXPECTED_INITIATIVE,
            description="Report 2"
        )
        report3 = Report(
            user_id="U345678",
            workspace_id="W789012",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Report 3"
        )
        
        repo.save(report1)
        repo.save(report2)
        repo.save(report3)
        
        authority_reports = repo.find_by_type(ReportType.LACKED_AUTHORITY)
        
        assert len(authority_reports) == 2
        assert report1 in authority_reports
        assert report3 in authority_reports
        assert report2 not in authority_reports
    
    def test_find_by_workspace_and_type(self):
        from repositories.report_repository import InMemoryReportRepository
        
        repo = InMemoryReportRepository()
        
        report1 = Report(
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Report 1"
        )
        report2 = Report(
            user_id="U789012",
            workspace_id="W123456",
            report_type=ReportType.EXPECTED_INITIATIVE,
            description="Report 2"
        )
        report3 = Report(
            user_id="U345678",
            workspace_id="W123456",
            report_type=ReportType.LACKED_AUTHORITY,
            description="Report 3"
        )
        
        repo.save(report1)
        repo.save(report2)
        repo.save(report3)
        
        filtered_reports = repo.find_by_workspace_and_type(
            "W123456", 
            ReportType.LACKED_AUTHORITY
        )
        
        assert len(filtered_reports) == 2
        assert report1 in filtered_reports
        assert report3 in filtered_reports
        assert report2 not in filtered_reports