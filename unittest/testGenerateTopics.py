import unittest
from unittest.mock import patch, MagicMock
from src.topic_gen.topic_gen_utils import generate_topics

class TestGenerateTopics(unittest.TestCase):
    @patch('src.topic_gen.topic_gen_utils.openai.ChatCompletion.create')
    def test_generate_single_topic(self, mock_openai_chat):
        # Setup mock response to match expected format
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text="1. Mocked Topic\n")]
        mock_openai_chat.return_value = mock_response

        # Execute
        result = generate_topics(1)

        # Assert
        self.assertTrue("1. Mocked Topic" in result)
        self.assertEqual(len(result.strip().split('\n')), 1)

    @patch('src.topic_gen.topic_gen_utils.openai.ChatCompletion.create')
    def test_generate_multiple_topics(self, mock_openai_chat):
        # Setup mock response to match expected format
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text="1. Mocked Topic 1\n2. Mocked Topic 2\n")]
        mock_openai_chat.return_value = mock_response

        # Execute
        result = generate_topics(2)

        # Assert
        self.assertTrue("1. Mocked Topic 1" in result and "2. Mocked Topic 2" in result)
        self.assertEqual(len(result.strip().split('\n')), 2)

        # Test for handling special characters in topics
    @patch('src.topic_gen.topic_gen_utils.openai.ChatCompletion.create')
    def test_generate_topics_with_special_characters(self, mock_openai_chat):
        special_chars = "!@#$%^&*()"
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text=f"1. Topic with special characters: {special_chars}\n")]
        mock_openai_chat.return_value = mock_response

        result = generate_topics(1)
        self.assertIn(special_chars, result)

    # Test for handling very long topic names
    @patch('src.topic_gen.topic_gen_utils.openai.ChatCompletion.create')
    def test_generate_long_topic_names(self, mock_openai_chat):
        long_topic = "a" * 1000  # A very long topic name
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text=f"1. {long_topic}\n")]
        mock_openai_chat.return_value = mock_response

        result = generate_topics(1)
        self.assertIn(long_topic, result)

    # Test for API failure (e.g., network error, API limit exceeded)
    @patch('src.topic_gen.topic_gen_utils.openai.ChatCompletion.create')
    def test_generate_topics_api_failure(self, mock_openai_chat):
        mock_openai_chat.side_effect = Exception("API failure")

        with self.assertRaises(Exception):
            generate_topics(1)

    # Test for empty response from API
    @patch('src.topic_gen.topic_gen_utils.openai.ChatCompletion.create')
    def test_generate_topics_empty_response(self, mock_openai_chat):
        mock_response = MagicMock()
        mock_response.choices = []
        mock_openai_chat.return_value = mock_response

        result = generate_topics(1)
        self.assertEqual(result, "")

    # Test for generating topics with a specific keyword
    @patch('src.topic_gen.topic_gen_utils.openai.ChatCompletion.create')
    def test_generate_topics_with_keyword(self, mock_openai_chat):
        keyword = "Technology"
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text=f"1. {keyword} advances in the 21st century\n")]
        mock_openai_chat.return_value = mock_response

        result = generate_topics(1)
        self.assertIn(keyword, result)

if __name__ == '__main__':
    unittest.main()
