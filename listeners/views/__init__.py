from slack_bolt import App
from .sample_view import sample_view_callback
from .decidely_report_view import handle_report_submission


def register(app: App):
    app.view("sample_view_id")(sample_view_callback)
    app.view("decidely_report_submission")(handle_report_submission)
