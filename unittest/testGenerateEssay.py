import unittest
from unittest.mock import patch
from src.essay_gen.essay_gen_utils import \
    extract_graph_descriptions, generate_graphs, \
        generate_paragraph_helper, generate_subsection_paragraph

class TestEssayGeneration(unittest.TestCase):

    def test_extract_graph_descriptions(self):
        test_paragraph = "Here's a description [GRAPH: Plot this graph with x and y] and another [GRAPH: Plot another graph with a and b]."
        expected = ["Plot this graph with x and y", "Plot another graph with a and b"]
        self.assertEqual(extract_graph_descriptions(test_paragraph), expected)

    @patch('your_module.drawing_graph')
    def test_generate_graphs(self, mock_drawing_graph):
        # Mocking the drawing_graph function to return a specific value
        mock_drawing_graph.return_value = "mocked_image"

        paragraph = "This is a test paragraph with a [GRAPH: sample graph description]."
        expected_result = ["mocked_image"]
        
        # Test the generate_graphs function with the mocked drawing_graph
        result = generate_graphs(paragraph)
        self.assertEqual(result, expected_result)

    @patch('my_module.write_paragraph')
    def test_generate_paragraph_helper(self, mock_write_paragraph):
        # Setup mock return value for write_paragraph
        mock_write_paragraph.return_value = "This is a new paragraph."

        latest_plan = "Existing plan details."
        latest_plan_dict = {
            "1": {
                'title': "Introduction",
                'content': ["Introduction content here"],
                'word_count': 100
            }
        }
        section_number = 1
        current_writing = "Current writing content."
        critic_prompt = "Critic instructions."

        expected_instruction = ("Write the following paragraph:\n 1.Introduction\nIntroduction content here \n total words:100")
        expected_output = "Current writing content.Introduction\nThis is a new paragraph.\n"

        # Call the function under test
        output_writing, _ = generate_paragraph_helper(latest_plan, latest_plan_dict, section_number, current_writing, critic_prompt)

        # Verify the output
        self.assertEqual(output_writing, expected_output)
        mock_write_paragraph.assert_called_once_with(latest_plan + "\nCurrent Writing: \n" + current_writing, expected_instruction, critic_prompt)

    @patch('your_module.write_paragraph')
    def test_generate_subsection_paragraph(self, mock_write_paragraph):
        # Setup mock return value for write_paragraph
        mock_write_paragraph.return_value = "Generated subsection paragraph."

        # Example inputs
        latest_plan = "Plan content."
        latest_plan_dict = {
            "3": {
                'title': "Section 3",
                'sub_section': {
                    "3.1": {
                        'title': "Subsection 3.1 Title",
                        'content': ["Content of subsection 3.1."],
                        'word_count': 50,
                        'graph_description': "Graph for subsection 3.1."
                    }
                }
            }
        }
        section_number = 3
        subsection_number = 1
        current_writing = "Current writing before subsection."
        critic_prompt = "Critic instructions for subsection."

        # Expected values
        expected_instruction = (
            "Write the following paragraph:\n 3.1 Subsection 3.1 Title\nContent of subsection 3.1. \n total words:50\n GRAPH_DESCRIPTION:Graph for subsection 3.1."
        )
        expected_output = "Current writing before subsection.Subsection 3.1 Title\nGenerated subsection paragraph.\n"

        # Call the function under test
        output_writing, _ = generate_subsection_paragraph(latest_plan, latest_plan_dict, section_number, subsection_number, current_writing, critic_prompt)

        # Verify the output matches expectations
        self.assertEqual(output_writing, expected_output)
        # Verify write_paragraph was called correctly
        mock_write_paragraph.assert_called_once_with(latest_plan + "\nCurrent Writing: \n" + current_writing, expected_instruction, critic_prompt)

if __name__ == '__main__':
    unittest.main()