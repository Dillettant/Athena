import unittest
from unittest.mock import patch, MagicMock
import os
from your_module_name import (
    test_generate_essay,
    generate_paragraph_helper,
    generate_subsection_paragraph,
    assemble_dict,
    save_images,
    generate_graphs
)

class TestEssayGenerationE2E(unittest.TestCase):

    @patch('your_module_name.write_paragraph')
    @patch('your_module_name.generate_graphs')
    @patch('your_module_name.save_images')
    @patch('your_module_name.assemble_dict')
    @patch('your_module_name.markdown_to_pdf')
    def test_generate_essay_e2e(self, mock_markdown_to_pdf, mock_assemble_dict, mock_save_images, mock_generate_graphs, mock_write_paragraph):
        # Mocking responses for each function
        mock_write_paragraph.return_value = "Generated paragraph content"
        mock_generate_graphs.return_value = ["Mock Image 1", "Mock Image 2"]
        mock_assemble_dict.return_value = {"title": "Generated Essay"}
        mock_markdown_to_pdf.return_value = None

        # Test data setup
        latest_plan = "Test Plan"
        latest_plan_dict = {
            'title': 'Test Title',
            '1': {'title': 'Introduction', 'content': ['Intro content'], 'word_count': 100},
            '2': {'title': 'Background', 'content': ['Background content'], 'word_count': 150},
            '3': {
                'title': 'Main Section',
                'sub_section': {
                    '3.1': {'title': 'Subsection 1', 'content': ['Subsection 1 content'], 'word_count': 50},
                    '3.2': {'title': 'Subsection 2', 'content': ['Subsection 2 content'], 'word_count': 50},
                    '3.3': {'title': 'Subsection 3', 'content': ['Subsection 3 content'], 'word_count': 50},
                }
            },
            '4': {
                'title': 'Conclusion',
                'sub_section': {
                    '4.1': {'title': 'Conclusion 1', 'content': ['Conclusion 1 content'], 'word_count': 50},
                    '4.2': {'title': 'Conclusion 2', 'content': ['Conclusion 2 content'], 'word_count': 50},
                    '4.3': {'title': 'Conclusion 3', 'content': ['Conclusion 3 content'], 'word_count': 50},
                }
            }
        }

        # Run the E2E test
        pdf_path = test_generate_essay(latest_plan, latest_plan_dict)

        # Assertions
        mock_write_paragraph.assert_called()
        mock_generate_graphs.assert_called()
        mock_save_images.assert_called()
        mock_assemble_dict.assert_called()
        mock_markdown_to_pdf.assert_called_with("# Test Title\n\n", 'pdffile/Test Title.pdf')

        # Check if the output PDF path is correct
        self.assertEqual(pdf_path, 'pdffile/Test Title.pdf')

        # Check if the PDF file was "saved" (mocked)
        self.assertTrue(os.path.exists(pdf_path))

if __name__ == '__main__':
    unittest.main()