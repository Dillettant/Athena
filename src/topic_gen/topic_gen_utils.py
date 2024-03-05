import openai
import re
import os

def generate_topics(topic_count):
    """
    Generate essay topics using OpenAI's GPT-4 model.

    :param topic_count: The number of topics to generate.
    :return: A string containing the generated topics.
    """

    topic_generation_prompt = f"""
    Generate {topic_count} IB essay topics. The topics should generally follow:
    1. The difficulty is within the expected range. Should be within or a little bit
    beyond IB math syllabus.
    2. Preferably to have some real-life implications.
    3. The topic should be represented with with synthetic data (no need to look up real world data).

    Output the topic only!
    """
    # Set up OpenAI client
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    while True:
        chat_completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": topic_generation_prompt}]
        )
        generated_content = chat_completion.choices[0].message.content

        # Check if the generated content meets the requirements
        if re.search(r'\d+\.\s*(.+)', generated_content):
            print(f"[DEBUG] Topics: \n{generated_content}")
            return generated_content
        # If not, the loop will continue and generate new content


def select_topic_from_string_regex(input_string, number):
    """
    Select a topic from a string using a regular expression.
    
    :param input_string: The string to search for topics.
    :param number: The number of the topic to select.
    :return: The selected topic.
    """
    # Regular expression to match topic lines
    regex_pattern = r'\d+\.\s*(.+)'

    try:
        # Find all matches in the input string
        topics = re.findall(regex_pattern, input_string)

        # Convert number to integer if it's a string
        if isinstance(number, str):
            number = int(number)

        # Validate the selection number
        if 1 <= number <= len(topics):
            return topics[number - 1]
        else:
            raise ValueError("Invalid selection. Please select a number between 1 and the total number of topics.")
    except ValueError as e:
        print(e)

def test_generate_topics():
    # Generate
    topics = generate_topics(3)
    
    # Select
    selection = input("select one of the topic.. ")
    topic = select_topic_from_string_regex(topics, selection)
    return topic

