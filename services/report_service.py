from typing import List, Dict, Any
from models.report import Report, ReportType
from repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self, repository: ReportRepository):
        self._repository = repository
    
    def create_report(
        self,
        user_id: str,
        workspace_id: str,
        report_type: ReportType,
        description: str
    ) -> Report:
        report = Report(
            user_id=user_id,
            workspace_id=workspace_id,
            report_type=report_type,
            description=description
        )
        return self._repository.save(report)
    
    def get_workspace_reports(self, workspace_id: str) -> List[Report]:
        return self._repository.find_by_workspace(workspace_id)
    
    def get_user_reports(self, user_id: str) -> List[Report]:
        return self._repository.find_by_user(user_id)
    
    def get_workspace_summary(self, workspace_id: str) -> Dict[str, Any]:
        reports = self._repository.find_by_workspace(workspace_id)
        
        lacked_authority_count = sum(
            1 for r in reports 
            if r.report_type == ReportType.LACKED_AUTHORITY
        )
        expected_initiative_count = sum(
            1 for r in reports 
            if r.report_type == ReportType.EXPECTED_INITIATIVE
        )
        
        return {
            "workspace_id": workspace_id,
            "total_reports": len(reports),
            "lacked_authority_count": lacked_authority_count,
            "expected_initiative_count": expected_initiative_count
        }
    
    def format_reports_for_slack(self, reports: List[Report]) -> List[Dict[str, Any]]:
        blocks = []
        
        for i, report in enumerate(reports):
            if i > 0:
                blocks.append({"type": "divider"})
            
            report_type_text = {
                ReportType.LACKED_AUTHORITY: "🔒 *Lacked Authority*",
                ReportType.EXPECTED_INITIATIVE: "💡 *Expected Initiative*"
            }
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"{report_type_text[report.report_type]}\n"
                        f"Reported by <@{report.user_id}> on "
                        f"{report.timestamp.strftime('%Y-%m-%d at %H:%M UTC')}\n"
                        f"_{report.description}_"
                    )
                }
            })
        
        return blocks