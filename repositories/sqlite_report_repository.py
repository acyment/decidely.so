from typing import List, Optional, Tuple, Any
from uuid import UUID
from datetime import datetime
import sqlite3
from contextlib import contextmanager
from models.report import Report, ReportType
from repositories.report_repository import ReportRepository


class SQLiteReportRepository(ReportRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn = None
        
        # For in-memory databases, keep connection open
        if db_path == ":memory:":
            self._conn = sqlite3.connect(":memory:")
        
        # Create table
        with self._database_operation() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    workspace_id TEXT NOT NULL,
                    report_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
    
    def _get_connection(self):
        """Get database connection, using persistent connection for in-memory databases."""
        return self._conn if self._conn else sqlite3.connect(self.db_path)
    
    @contextmanager
    def _database_operation(self):
        """Context manager for database operations."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            if not self._conn:
                conn.close()
    
    def _row_to_report(self, row: Tuple[Any, ...]) -> Report:
        """Convert database row to Report object."""
        return Report(
            id=UUID(row[0]),
            user_id=row[1],
            workspace_id=row[2],
            report_type=ReportType(row[3]),
            description=row[4],
            timestamp=datetime.fromisoformat(row[5])
        )
    
    def _execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> List[Report]:
        """Execute query and return list of Reports."""
        with self._database_operation() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [self._row_to_report(row) for row in rows]
    
    def save(self, report: Report) -> Report:
        with self._database_operation() as cursor:
            cursor.execute("""
                INSERT INTO reports (id, user_id, workspace_id, report_type, description, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(report.id),
                report.user_id,
                report.workspace_id,
                report.report_type.value,
                report.description,
                report.timestamp.isoformat()
            ))
        return report
    
    def find_by_id(self, report_id: UUID) -> Optional[Report]:
        with self._database_operation() as cursor:
            cursor.execute(
                "SELECT * FROM reports WHERE id = ?", 
                (str(report_id),)
            )
            row = cursor.fetchone()
            return self._row_to_report(row) if row else None
    
    def find_by_workspace(self, workspace_id: str) -> List[Report]:
        return self._execute_query(
            "SELECT * FROM reports WHERE workspace_id = ?", 
            (workspace_id,)
        )
    
    def find_by_user(self, user_id: str) -> List[Report]:
        return self._execute_query(
            "SELECT * FROM reports WHERE user_id = ?", 
            (user_id,)
        )
    
    def find_by_type(self, report_type: ReportType) -> List[Report]:
        return self._execute_query(
            "SELECT * FROM reports WHERE report_type = ?", 
            (report_type.value,)
        )
    
    def find_by_workspace_and_type(
        self, workspace_id: str, report_type: ReportType
    ) -> List[Report]:
        return self._execute_query(
            "SELECT * FROM reports WHERE workspace_id = ? AND report_type = ?", 
            (workspace_id, report_type.value)
        )