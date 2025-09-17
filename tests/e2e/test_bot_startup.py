import pytest
from listeners.commands.decidely_report import decidely_report_callback
from listeners.commands.decidely_list import decidely_list_callback
from listeners.views.decidely_report_view import handle_report_submission


class TestBotComponents:
    def test_decidely_commands_exist(self):
        # Verify the command functions exist and are callable
        assert callable(decidely_report_callback)
        assert callable(decidely_list_callback)
        assert callable(handle_report_submission)
    
    def test_command_registration(self):
        from listeners.commands import register
        from unittest.mock import Mock
        
        mock_app = Mock()
        register(mock_app)
        
        # Verify our commands were registered
        calls = [str(call) for call in mock_app.command.call_args_list]
        assert any("/decidely" in call for call in calls)
        assert any("/decidely-list" in call for call in calls)
    
    def test_view_registration(self):
        from listeners.views import register
        from unittest.mock import Mock
        
        mock_app = Mock()
        register(mock_app)
        
        # Verify our view was registered
        calls = [str(call) for call in mock_app.view.call_args_list]
        assert any("decidely_report_submission" in call for call in calls)