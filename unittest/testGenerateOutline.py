import unittest
from unittest.mock import patch, MagicMock
from your_module_name import (
    write_paragraph,
    extract_latest_paragraph,
    extract_graph_descriptions,
    generate_paragraph_helper,
    generate_subsection_paragraph,
    assemble_dict,
    save_images,
    generate_graphs
)

class TestEssayGeneration(unittest.TestCase):

    @patch('your_module_name.AssistantAgent')
    def test_write_paragraph(self, MockAssistantAgent):
        # Setup mock
        mock_instance = MockAssistantAgent.return_value
        mock_instance.chat_messages = {"academic_writer": [{"content": "[WRITING]This is a test paragraph[/WRITING]"}]}

        # Call the function
        result = write_paragraph("instructions", "input", "critic_system_prompt")

        # Assertions
        self.assertEqual(result, "This is a test paragraph")

    def test_extract_latest_paragraph(self):
        chat_messages = {
            "academic_writer": [
                {"content": "Some irrelevant text"},
                {"content": "[WRITING]Extract this paragraph[/WRITING]"}
            ]
        }
        result = extract_latest_paragraph(chat_messages)
        self.assertEqual(result, "Extract this paragraph")

    def test_extract_graph_descriptions(self):
        text = "Some text with [GRAPH: Description for graph] inside."
        result = extract_graph_descriptions(text)
        self.assertEqual(result, ["Description for graph"])

    @patch('your_module_name.write_paragraph')
    def test_generate_paragraph_helper(self, mock_write_paragraph):
        mock_write_paragraph.return_value = "Generated paragraph content"

        latest_plan = "latest plan"
        latest_plan_dict = {
            "1": {"title": "Test Section", "content": ["Test content"], "word_count": 100}
        }
        current_writing = "Current writing"
        critic_prompt = "Critic prompt"

        result_writing, result_paragraph = generate_paragraph_helper(latest_plan, latest_plan_dict, 1, current_writing, critic_prompt)

        self.assertIn("Generated paragraph content", result_writing)
        self.assertEqual(result_paragraph, "Generated paragraph content")

    @patch('your_module_name.write_paragraph')
    def test_generate_subsection_paragraph(self, mock_write_paragraph):
        mock_write_paragraph.return_value = "Generated subsection paragraph content"

        latest_plan = "latest plan"
        latest_plan_dict = {
            "1": {
                "sub_section": {
                    "1.1": {"title": "Subsection Title", "content": ["Subsection content"], "word_count": 100}
                }
            }
        }
        current_writing = "Current writing"
        critic_prompt = "Critic prompt"

        result_writing, result_paragraph = generate_subsection_paragraph(latest_plan, latest_plan_dict, 1, 1, current_writing, critic_prompt)

        self.assertIn("Generated subsection paragraph content", result_writing)
        self.assertEqual(result_paragraph, "Generated subsection paragraph content")

    @patch('your_module_name.os.makedirs')
    @patch('your_module_name.plt.savefig')
    def test_save_images(self, mock_savefig, mock_makedirs):
        # Create some mock images
        mock_images = [MagicMock(), MagicMock()]

        # Call the function
        save_images(mock_images, 'mock/path', 'prefix')

        # Assert the images were saved correctly
        mock_savefig.assert_called()
        mock_makedirs.assert_called_with('mock/path')

    @patch('your_module_name.drawing_graph')
    def test_generate_graphs(self, mock_drawing_graph):
        mock_drawing_graph.return_value = "Mock Image"
        paragraph = "Some text with [GRAPH: Description for graph] inside."
        result = generate_graphs(paragraph)
        self.assertEqual(result, ["Mock Image"])

if __name__ == '__main__':
    unittest.main()