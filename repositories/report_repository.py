from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from uuid import UUID
from models.report import Report, ReportType


class ReportRepository(ABC):
    @abstractmethod
    def save(self, report: Report) -> Report:
        pass
    
    @abstractmethod
    def find_by_id(self, report_id: UUID) -> Optional[Report]:
        pass
    
    @abstractmethod
    def find_by_workspace(self, workspace_id: str) -> List[Report]:
        pass
    
    @abstractmethod
    def find_by_user(self, user_id: str) -> List[Report]:
        pass
    
    @abstractmethod
    def find_by_type(self, report_type: ReportType) -> List[Report]:
        pass
    
    @abstractmethod
    def find_by_workspace_and_type(
        self, workspace_id: str, report_type: ReportType
    ) -> List[Report]:
        pass


class InMemoryReportRepository(ReportRepository):
    def __init__(self):
        self._reports: Dict[UUID, Report] = {}
    
    def save(self, report: Report) -> Report:
        self._reports[report.id] = report
        return report
    
    def find_by_id(self, report_id: UUID) -> Optional[Report]:
        return self._reports.get(report_id)
    
    def find_by_workspace(self, workspace_id: str) -> List[Report]:
        return [
            report for report in self._reports.values()
            if report.workspace_id == workspace_id
        ]
    
    def find_by_user(self, user_id: str) -> List[Report]:
        return [
            report for report in self._reports.values()
            if report.user_id == user_id
        ]
    
    def find_by_type(self, report_type: ReportType) -> List[Report]:
        return [
            report for report in self._reports.values()
            if report.report_type == report_type
        ]
    
    def find_by_workspace_and_type(
        self, workspace_id: str, report_type: ReportType
    ) -> List[Report]:
        return [
            report for report in self._reports.values()
            if report.workspace_id == workspace_id 
            and report.report_type == report_type
        ]