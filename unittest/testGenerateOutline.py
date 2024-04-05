import unittest
from unittest.mock import patch
from src.outline_gen.outline_gen_utils import generate_chat, extract_latest_plan, parse_document_to_dict, generate_plan_dict


class TestChatGeneration(unittest.TestCase):
    @patch('src.outline_gen.outline_gen_utils.openai')
    def test_generate_chat_with_mocked_response(self, mock_openai):
        # Setting up a mocked response simulating an API call.
        mock_response = {
            "id": "test_id",
            "object": "chat",
            "created": 123456789,
            "model": "gpt-4",
            "choices": [
                {
                    "message": {
                        "role": "system",
                        "content": "Mocked response for essay plan"
                    }
                }
            ]
        }
        mock_openai.ChatCompletion.create.return_value = mock_response

        # Invoking the function under test.
        topic = "Test Topic"
        result = generate_chat(topic)

        # Asserting that the mocked response is in the result.
        self.assertIn("Mocked response for essay plan", result)
        self.assertIsInstance(result, dict)
        self.assertTrue(result['choices'][0]['message']['content'].startswith('Mocked'))

    def test_extract_latest_plan_from_chat(self):
        # Creating a dictionary of chat messages as if they were received from a chat history.
        chat_messages = {
            "chat_id": [
                {"role": "system", "content": "Initial setup content."},
                {"role": "user", "content": "User input example."},
                {"role": "system", "content": "[plan]Extractable test plan[/plan]"},
            ]
        }

        # Testing the function that extracts the latest plan.
        extracted_plan = extract_latest_plan(chat_messages)

        # Verifying that the extracted plan matches the expected result.
        expected_plan_content = "Extractable test plan"
        self.assertEqual(extracted_plan, expected_plan_content)

    def test_parse_document_to_dictionary_format(self):
        # Simulating a document string that would be parsed.
        document_string = "Title: Sample Plan\n1. Introduction (Word Count: 100): Introductory content."

        # Testing the function that parses the document string into a dictionary.
        document_dict = parse_document_to_dict(document_string)

        # Verifying the contents of the resulting dictionary.
        self.assertIn("title", document_dict)
        self.assertIn("1", document_dict)
        self.assertEqual(document_dict['title'], "Sample Plan")
        self.assertEqual(document_dict['1']['title'], "Introduction")
        self.assertEqual(document_dict['1']['word_count'], "100")

    @patch('src.outline_gen.outline_gen_utils.generate_chat')
    @patch('src.outline_gen.outline_gen_utils.extract_latest_plan')
    @patch('src.outline_gen.outline_gen_utils.parse_document_to_dict')
    def test_generate_plan_dictionary(self, mock_parse, mock_extract, mock_generate):
        # Mocking the dependencies of the function under test.
        mock_chat_id = "mocked_chat_id"
        mock_content = "mocked_content"
        mock_generate.return_value = {mock_chat_id: mock_content}
        mock_extract.return_value = "Mocked latest plan content"
        mock_parse.return_value = {"title": "Mocked Title"}

        # Calling the function to generate the plan dictionary.
        topic_for_plan = "Test Topic for Plan Generation"
        plan_text, plan_dict = generate_plan_dict(topic_for_plan)

        # Asserting the expected results.
        self.assertEqual(plan_text, "Mocked latest plan content")
        self.assertDictEqual(plan_dict, {"title": "Mocked Title"})


if __name__ == '__main__':
    unittest.main()
