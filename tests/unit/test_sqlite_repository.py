import pytest
import os
import tempfile
from pathlib import Path
from models.report import Report, ReportType
from repositories.report_repository import ReportRepository


class TestSQLiteRepository:
    def test_sqlite_repository_implements_interface(self):
        """Test that SQLiteReportRepository implements all required methods."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        
        # Create instance with temp database
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            repo = SQLiteReportRepository(str(db_path))
            
            # Verify it's a ReportRepository
            assert isinstance(repo, ReportRepository)
            
            # Verify all interface methods exist
            assert hasattr(repo, 'save')
            assert hasattr(repo, 'find_by_id')
            assert hasattr(repo, 'find_by_workspace')
            assert hasattr(repo, 'find_by_user')
            assert hasattr(repo, 'find_by_type')
            assert hasattr(repo, 'find_by_workspace_and_type')
    
    def test_create_tables_on_init(self):
        """Test that database tables are created on initialization."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        import sqlite3
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            
            # Create repository
            repo = SQLiteReportRepository(str(db_path))
            
            # Check if database file exists
            assert db_path.exists()
            
            # Check if reports table exists
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='reports'"
            )
            result = cursor.fetchone()
            conn.close()
            
            assert result is not None
            assert result[0] == 'reports'
    
    def test_save_report_persists_to_db(self):
        """Test that save() actually persists report to database."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        import sqlite3
        from uuid import uuid4
        from datetime import datetime, UTC
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            repo = SQLiteReportRepository(str(db_path))
            
            # Create a report
            report = Report(
                id=uuid4(),
                user_id="U123456",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Test report",
                timestamp=datetime.now(UTC)
            )
            
            # Save it
            saved_report = repo.save(report)
            
            # Verify it returns the report
            assert saved_report == report
            
            # Verify it's in the database
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reports WHERE id = ?", (str(report.id),))
            row = cursor.fetchone()
            conn.close()
            
            assert row is not None
            assert row[0] == str(report.id)  # id
            assert row[1] == report.user_id
            assert row[2] == report.workspace_id
            assert row[3] == report.report_type.value
            assert row[4] == report.description
    
    def test_find_by_id_retrieves_from_db(self):
        """Test that find_by_id retrieves the correct report."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        from uuid import uuid4
        from datetime import datetime, UTC
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            repo = SQLiteReportRepository(str(db_path))
            
            # Create and save a report
            report = Report(
                id=uuid4(),
                user_id="U123456",
                workspace_id="W123456",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="Test find by id",
                timestamp=datetime.now(UTC)
            )
            repo.save(report)
            
            # Find it by ID
            found_report = repo.find_by_id(report.id)
            
            assert found_report is not None
            assert found_report.id == report.id
            assert found_report.user_id == report.user_id
            assert found_report.workspace_id == report.workspace_id
            assert found_report.report_type == report.report_type
            assert found_report.description == report.description
            
            # Test non-existent ID
            non_existent = repo.find_by_id(uuid4())
            assert non_existent is None
    
    def test_find_by_workspace_filters_correctly(self):
        """Test that find_by_workspace returns only reports from that workspace."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        from uuid import uuid4
        from datetime import datetime, UTC
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            repo = SQLiteReportRepository(str(db_path))
            
            # Create reports for different workspaces
            report1 = Report(
                id=uuid4(),
                user_id="U111",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 1",
                timestamp=datetime.now(UTC)
            )
            report2 = Report(
                id=uuid4(),
                user_id="U222",
                workspace_id="W123456",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="Report 2",
                timestamp=datetime.now(UTC)
            )
            report3 = Report(
                id=uuid4(),
                user_id="U333",
                workspace_id="W789012",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 3",
                timestamp=datetime.now(UTC)
            )
            
            repo.save(report1)
            repo.save(report2)
            repo.save(report3)
            
            # Find by workspace
            workspace_reports = repo.find_by_workspace("W123456")
            
            assert len(workspace_reports) == 2
            report_ids = [r.id for r in workspace_reports]
            assert report1.id in report_ids
            assert report2.id in report_ids
            assert report3.id not in report_ids
    
    def test_find_by_user_filters_correctly(self):
        """Test that find_by_user returns only reports from that user."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        from uuid import uuid4
        from datetime import datetime, UTC
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            repo = SQLiteReportRepository(str(db_path))
            
            # Create reports for different users
            report1 = Report(
                id=uuid4(),
                user_id="U123456",
                workspace_id="W111",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 1",
                timestamp=datetime.now(UTC)
            )
            report2 = Report(
                id=uuid4(),
                user_id="U123456",
                workspace_id="W222",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="Report 2",
                timestamp=datetime.now(UTC)
            )
            report3 = Report(
                id=uuid4(),
                user_id="U789012",
                workspace_id="W111",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 3",
                timestamp=datetime.now(UTC)
            )
            
            repo.save(report1)
            repo.save(report2)
            repo.save(report3)
            
            # Find by user
            user_reports = repo.find_by_user("U123456")
            
            assert len(user_reports) == 2
            report_ids = [r.id for r in user_reports]
            assert report1.id in report_ids
            assert report2.id in report_ids
            assert report3.id not in report_ids
    
    def test_find_by_type_filters_correctly(self):
        """Test that find_by_type returns only reports of that type."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        from uuid import uuid4
        from datetime import datetime, UTC
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            repo = SQLiteReportRepository(str(db_path))
            
            # Create reports of different types
            report1 = Report(
                id=uuid4(),
                user_id="U111",
                workspace_id="W111",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 1",
                timestamp=datetime.now(UTC)
            )
            report2 = Report(
                id=uuid4(),
                user_id="U222",
                workspace_id="W222",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="Report 2",
                timestamp=datetime.now(UTC)
            )
            report3 = Report(
                id=uuid4(),
                user_id="U333",
                workspace_id="W333",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 3",
                timestamp=datetime.now(UTC)
            )
            
            repo.save(report1)
            repo.save(report2)
            repo.save(report3)
            
            # Find by type
            authority_reports = repo.find_by_type(ReportType.LACKED_AUTHORITY)
            
            assert len(authority_reports) == 2
            report_ids = [r.id for r in authority_reports]
            assert report1.id in report_ids
            assert report3.id in report_ids
            assert report2.id not in report_ids
    
    def test_find_by_workspace_and_type_filters_correctly(self):
        """Test that find_by_workspace_and_type filters by both criteria."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        from uuid import uuid4
        from datetime import datetime, UTC
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            repo = SQLiteReportRepository(str(db_path))
            
            # Create various reports
            report1 = Report(
                id=uuid4(),
                user_id="U111",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 1",
                timestamp=datetime.now(UTC)
            )
            report2 = Report(
                id=uuid4(),
                user_id="U222",
                workspace_id="W123456",
                report_type=ReportType.EXPECTED_INITIATIVE,
                description="Report 2",
                timestamp=datetime.now(UTC)
            )
            report3 = Report(
                id=uuid4(),
                user_id="U333",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 3",
                timestamp=datetime.now(UTC)
            )
            report4 = Report(
                id=uuid4(),
                user_id="U444",
                workspace_id="W789012",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Report 4",
                timestamp=datetime.now(UTC)
            )
            
            repo.save(report1)
            repo.save(report2)
            repo.save(report3)
            repo.save(report4)
            
            # Find by workspace and type
            filtered_reports = repo.find_by_workspace_and_type(
                "W123456", 
                ReportType.LACKED_AUTHORITY
            )
            
            assert len(filtered_reports) == 2
            report_ids = [r.id for r in filtered_reports]
            assert report1.id in report_ids
            assert report3.id in report_ids
            assert report2.id not in report_ids
            assert report4.id not in report_ids
    
    def test_data_survives_restart(self):
        """Test that data persists when creating a new repository instance."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        from uuid import uuid4
        from datetime import datetime, UTC
        
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            
            # Create first instance and save report
            repo1 = SQLiteReportRepository(str(db_path))
            report = Report(
                id=uuid4(),
                user_id="U123456",
                workspace_id="W123456",
                report_type=ReportType.LACKED_AUTHORITY,
                description="Persistent report",
                timestamp=datetime.now(UTC)
            )
            repo1.save(report)
            
            # Create second instance and retrieve report
            repo2 = SQLiteReportRepository(str(db_path))
            found_report = repo2.find_by_id(report.id)
            
            assert found_report is not None
            assert found_report.id == report.id
            assert found_report.description == report.description
    
    def test_in_memory_mode_for_tests(self):
        """Test that repository can work with in-memory database."""
        from repositories.sqlite_report_repository import SQLiteReportRepository
        from uuid import uuid4
        from datetime import datetime, UTC
        
        # Use ":memory:" for in-memory database
        repo = SQLiteReportRepository(":memory:")
        
        report = Report(
            id=uuid4(),
            user_id="U123456",
            workspace_id="W123456",
            report_type=ReportType.EXPECTED_INITIATIVE,
            description="In-memory report",
            timestamp=datetime.now(UTC)
        )
        
        saved_report = repo.save(report)
        found_report = repo.find_by_id(report.id)
        
        assert saved_report == report
        assert found_report is not None
        assert found_report.id == report.id