"""Tests for run.py script."""

from unittest.mock import patch
import runpy


class TestRunScript:
    """Test cases for the run.py convenience script."""

    @patch("subprocess.call")
    @patch("sys.exit")
    def test_run_script_success(self, mock_exit, mock_subprocess_call):
        """Test run.py executes uv run python main.py and exits with return code 0."""
        # Arrange
        mock_subprocess_call.return_value = 0

        # Act
        runpy.run_path("run.py", run_name="__main__")

        # Assert
        mock_subprocess_call.assert_called_once_with(["uv", "run", "python", "main.py"])
        mock_exit.assert_called_once_with(0)

    @patch("subprocess.call")
    @patch("sys.exit")
    def test_run_script_failure(self, mock_exit, mock_subprocess_call):
        """Test run.py exits with non-zero code when subprocess fails."""
        # Arrange
        mock_subprocess_call.return_value = 1

        # Act
        runpy.run_path("run.py", run_name="__main__")

        # Assert
        mock_subprocess_call.assert_called_once_with(["uv", "run", "python", "main.py"])
        mock_exit.assert_called_once_with(1)

    @patch("subprocess.call")
    @patch("sys.exit")
    def test_run_script_custom_exit_code(self, mock_exit, mock_subprocess_call):
        """Test run.py propagates custom exit codes from subprocess."""
        # Arrange
        mock_subprocess_call.return_value = 42

        # Act
        runpy.run_path("run.py", run_name="__main__")

        # Assert
        mock_subprocess_call.assert_called_once_with(["uv", "run", "python", "main.py"])
        mock_exit.assert_called_once_with(42)

    @patch("subprocess.call")
    @patch("sys.exit")
    def test_run_script_negative_exit_code(self, mock_exit, mock_subprocess_call):
        """Test run.py handles negative exit codes (signals)."""
        # Arrange - negative exit codes indicate process was terminated by signal
        mock_subprocess_call.return_value = -9  # SIGKILL

        # Act
        runpy.run_path("run.py", run_name="__main__")

        # Assert
        mock_subprocess_call.assert_called_once_with(["uv", "run", "python", "main.py"])
        mock_exit.assert_called_once_with(-9)

    def test_run_script_not_as_main(self):
        """Test that importing run.py doesn't execute the script."""
        # Arrange & Act - import the module without running as __main__
        with patch("subprocess.call") as mock_subprocess_call:
            with patch("sys.exit") as mock_exit:
                # Import without running as main
                runpy.run_path("run.py", run_name="not_main")

                # Assert - should not call subprocess or exit
                mock_subprocess_call.assert_not_called()
                mock_exit.assert_not_called()
