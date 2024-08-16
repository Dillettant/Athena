import unittest
from unittest.mock import patch, MagicMock
from src.essay_gen.essay_gen_utils import write_paragraph


class TestWriteParagraph(unittest.TestCase):

    @patch('essay_gen_utils.GroupChatManager')
    @patch('essay_gen_utils.GPTAssistantAgent')
    def test_write_paragraph_basic(self, mock_gpt_agent, mock_chat_manager):
        # Mocking the behavior of GPTAssistantAgent and GroupChatManager
        mock_agent_instance = MagicMock()
        mock_gpt_agent.return_value = mock_agent_instance
        mock_agent_instance.some_method.return_value = "Expected output"

        mock_manager_instance = MagicMock()
        mock_chat_manager.return_value = mock_manager_instance
        mock_manager_instance.another_method.return_value = "Another expected output"

        instructions = "Please write a paragraph about AI."
        input_str = "Artificial Intelligence (AI)"
        critic_system_prompt = "Ensure accuracy and relevance."

        # Call the function under test
        result = write_paragraph(instructions, input_str, critic_system_prompt)

        # Validate the results
        self.assertIn("Expected output", result)
        self.assertIn("Another expected output", result)

        # Verify interactions
        mock_gpt_agent.assert_called_once()
        mock_chat_manager.assert_called_once()
        mock_agent_instance.some_method.assert_called_with(instructions, input_str, critic_system_prompt)
        mock_manager_instance.another_method.assert_called_once_with(instructions)

    @patch('essay_gen_utils.GroupChatManager')
    @patch('essay_gen_utils.GPTAssistantAgent')
    def test_write_paragraph_with_invalid_input(self, mock_gpt_agent, mock_chat_manager):
        """
        Test handling of invalid input parameters.
        """
        # Setup: Assuming that write_paragraph checks for invalid input and raises a ValueError
        instructions = ""  # Empty instructions, considered invalid
        input_str = "Artificial Intelligence (AI)"
        critic_system_prompt = "Ensure accuracy and relevance."

        with self.assertRaises(ValueError):
            write_paragraph(instructions, input_str, critic_system_prompt)

        # Ensure no external calls are made with invalid input
        mock_gpt_agent.assert_not_called()
        mock_chat_manager.assert_not_called()

    @patch('essay_gen_utils.GroupChatManager')
    @patch('essay_gen_utils.GPTAssistantAgent')
    def test_write_paragraph_external_dependency_failure(self, mock_gpt_agent, mock_chat_manager):
        """
        Test handling when an external dependency fails (e.g., API call fails).
        """
        # Setup: Mock an external dependency to raise an exception
        mock_gpt_agent.side_effect = Exception("External API failure")

        instructions = "Please write a paragraph about AI."
        input_str = "Artificial Intelligence (AI)"
        critic_system_prompt = "Ensure accuracy and relevance."

        # Assuming write_paragraph is designed to handle external failures gracefully
        with self.assertRaises(Exception) as context:
            write_paragraph(instructions, input_str, critic_system_prompt)

        self.assertIn("External API failure", str(context.exception))

    @patch('essay_gen_utils.GroupChatManager')
    @patch('essay_gen_utils.GPTAssistantAgent')
    def test_write_paragraph_multiple_calls(self, mock_gpt_agent, mock_chat_manager):
        """
        Test that write_paragraph can handle being called multiple times with different inputs.
        """
        # Setup: Mock the dependencies to return different outputs on subsequent calls
        mock_agent_instance = MagicMock()
        mock_gpt_agent.return_value = mock_agent_instance
        mock_agent_instance.some_method.side_effect = ["Output 1", "Output 2"]

        mock_manager_instance = MagicMock()
        mock_chat_manager.return_value = mock_manager_instance
        mock_manager_instance.another_method.side_effect = ["Output A", "Output B"]

        # First call
        result1 = write_paragraph("Instructions 1", "Input 1", "Prompt 1")
        self.assertIn("Output 1", result1)
        self.assertIn("Output A", result1)

        # Second call with different parameters
        result2 = write_paragraph("Instructions 2", "Input 2", "Prompt 2")
        self.assertIn("Output 2", result2)
        self.assertIn("Output B", result2)

        # Verify that the methods were called with the correct parameters for each call
        mock_agent_instance.some_method.assert_has_calls([
            call("Instructions 1", "Input 1", "Prompt 1"),
            call("Instructions 2", "Input 2", "Prompt 2"),
        ])
        mock_manager_instance.another_method.assert_has_calls([
            call("Instructions 1"),
            call("Instructions 2"),
        ])


if __name__ == '__main__':
    unittest.main()
