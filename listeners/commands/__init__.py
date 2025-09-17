from slack_bolt import App
from .sample_command import sample_command_callback
from .decidely_report import decidely_report_callback
from .decidely_list import decidely_list_callback


def register(app: App):
    app.command("/sample-command")(sample_command_callback)
    app.command("/decidely")(decidely_report_callback)
    app.command("/decidely-list")(decidely_list_callback)
