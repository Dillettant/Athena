import re
import os
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from PIL import Image
import io
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt
from markdown_pdf import MarkdownPdf, Section

def write_paragraph(instructions: str, input:str, critic_system_prompt, max_round = 4):
    academic_writer_system_prompt = """
    As an Academic Writer focusing on the International Baccalaureate (IB) program,
    your key role is to compose essays that are compelling, insightful, and conform
    to IB standards. Ensure your essays are content-rich, relevant, and directly
    aligned with IB criteria, excluding any extraneous information.

    Present your essays with the main content enclosed within [WRITING] tags.
    This format is essential to differentiate the main text from other elements.
    Your submission should include only the essay's core content, without titles or
    headings.

    When incorporating formulas or concepts, use LaTeX format.

    If you receive feedback or critiques, thoroughly revise your essay and resubmit.
    Present the entire essay, with revisions clearly highlighted within [WRITING]
    tags. This approach preserves the essay's context and flow while clearly indicating
    the modifications.

    If your task includes a GRAPH_DESCRIPTION, indicating the need for graphical
    representations, integrate the [GRAPH: ##] marker in your text where plots are
    required, with line breaks before and after the marker. Specify what you need
    plotted as follows:

    [GRAPH: Detailed description for the graph]

    If there is no GRAPH_DESCRIPTION, do not include any graph-related content.

    Ensure that your submission is comprised strictly of the main essay content
    within the [WRITING] tags. Refrain from adding comments or extraneous information.
    Focus solely on material that is relevant and adheres to IB standards.

    Key points to remember:

    Always provide the complete essay content, including any
    [GRAPH: Description for graph plotting and detailed parameters with numbers] if required by the GRAPH_DESCRIPTION.
    Use LaTeX formatting for necessary mathematical expressions.
    Exclude comments from your response; only include the essay content and the
    [GRAPH: Description for graph plotting and  detailed parameters with numbers] if applicable.
    All content between [WRITING] tags should exclusively pertain to the IB essay.
    Encapsulate all contents within [WRITING] [/WRITING] tags.
    Do not mention any procedures related to revisions. Don't INCLUDE word count.
    If the user's request does not include GRAPH_DESCRIPTION, omit the GRAPH
    indicator from your response. \n
    Otherwise, always include GRAPH indicator if requests has GRAPH_DESCRIPTION

    You should connect the graph with the main text with explaination,
    like using "Demonstrate in the follwoing graph"

    Also, please expalain in detail the parameter value in the graph description
    as well as in the text around the graph

    Please don't use uncommon words like epiphany，waltzes

    For the introduction part, Please put the personal story at the beginning of
    the paragraph

    For the background part, if the model is not in the IB syllybus, please explain
    the model by induction.

    For the summary part, need to summarize the model results and get insights from
    the experiments

    Please make sure the word accounts is accurate

    Make sure you have output exactly the word count

    Please don't include sentence like "the introduction aligns with IB guidelines,",
    they don't belcong to the writings!!!

    Don't mention IB or IB syllabus since it does not belong to the essay. sentence
    like "aligns with the curriculum of the IB Mathematics syllabus, " is strictly
    forbidden

    Don't mention IB by any means in the main text or any educational purpose,
    the writer represents the student know should write as the student, don't refer
    to student or anything, the writer is the student

    If there is [GRAPH], augment the text surrounding the [GRAPH] with numerical
    examples or hypothetical values for the bite rate and removal rate.
    These should not only be depicted in the graph but also explained in the text for deeper understanding.



    REPLAY THE CONTNET BLEONG TO THE ESSAY ONLY NO MATTER WHAT!!!
    """
    openai_api_key=os.getenv("OPENAI_API_KEY")
    config_list = [{'model': 'gpt-4-1106-preview', 'api_key': openai_api_key}]
 
    academic_writer_system_prompt += instructions
    academic_writer = AssistantAgent("academic_writer", system_message=academic_writer_system_prompt, llm_config={"config_list": config_list})

    academic_writer_critic = AssistantAgent(
        name="Critic",
        system_message=critic_system_prompt,
        llm_config={"config_list": config_list}
    )

    academic_writer_admin_system_prompt = """
    "A human admin. Initialize the converstion. Alternate between critic and Academic Writer, start with Academic Writer
    """
    termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

    academic_writer_admin = UserProxyAgent("Admin", code_execution_config=False, system_message=academic_writer_admin_system_prompt, human_input_mode="NEVER",  is_termination_msg=termination_msg)
    groupchat = GroupChat(agents=[academic_writer_critic, academic_writer, academic_writer_admin], messages=[], max_round=max_round)
    manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})
    academic_writer_admin.initiate_chat(manager, message=input)
    def extract_latest_paragraph(chat_messages):
        # Iterate through each key in the chat_messages dictionary
        for chat_key in chat_messages:
            # Iterate through the messages in reverse order
            for message in reversed(chat_messages[chat_key]):
                # Check if the message content contains the start of the plan marker
                if '[WRITING]' in message['content']:
                    # Find the start and end indices of the plan
                    start_index = message['content'].find('[WRITING]') + len('[WRITING]')
                    end_index = message['content'].find('[/WRITING]', start_index)

                    # Extract and return the plan text if end marker is found
                    if end_index != -1:
                        return message['content'][start_index:end_index].strip()

        # Return None if no plan is found
        return None
    extract_latest_paragraph = extract_latest_paragraph(academic_writer_admin.chat_messages)
    return extract_latest_paragraph

def generate_paragraph_helper(latest_plan, latest_plan_dict, section_number, current_writing, critic_prompt):
    paragraph_instruction = f"Write the following paragraph:\n {section_number}." + latest_plan_dict[str(section_number)]['title'] + '\n' + '\n'.join(latest_plan_dict[str(section_number)]['content']) + " \n total words:" + str(latest_plan_dict[str(section_number)]['word_count'])
    if 'graph_description' in latest_plan_dict[str(section_number)]:
        paragraph_instruction += '\n GRAPH_DESCRIPTION:' + latest_plan_dict[str(section_number)]['graph_description']
    paragraph = write_paragraph(latest_plan + "\nCurrent Writing: \n" + current_writing, paragraph_instruction, critic_prompt)

    # Add the new paragraph to the current writing
    current_writing += latest_plan_dict[str(section_number)]['title']+'\n' + paragraph + '\n'

    return current_writing, paragraph

def generate_subsection_paragraph(latest_plan, latest_plan_dict, section_number, subsection_number, current_writing, critic_prompt):
    subsection_key = f"{section_number}.{subsection_number}"
    # new
    content = latest_plan_dict[str(section_number)]['sub_section'][subsection_key]['content']
    content_str = '.\n'.join(str(item) for item in content)
    subsection_instruction = f"Write the following paragraph:\n {subsection_key} " + latest_plan_dict[str(section_number)]['sub_section'][subsection_key]['title'] + '\n' + content_str + " \n total words:" + str(latest_plan_dict[str(section_number)]['sub_section'][subsection_key]['word_count'])
    # before
    # subsection_instruction = f"Write the following paragraph:\n {subsection_key} " + latest_plan_dict[str(section_number)]['sub_section'][subsection_key]['title'] + '\n' + '.\n'.join(latest_plan_dict[str(section_number)]['sub_section'][subsection_key]['content']) + " \n total words:" + str(latest_plan_dict[str(section_number)]['sub_section'][subsection_key]['word_count'])

    if 'graph_description' in latest_plan_dict[str(section_number)]['sub_section'][subsection_key]:
        subsection_instruction += '\n GRAPH_DESCRIPTION:' + latest_plan_dict[str(section_number)]['sub_section'][subsection_key]['graph_description']
    subsection_paragraph = write_paragraph(latest_plan + "\nCurrent Writing: \n" + current_writing, subsection_instruction, critic_prompt)

    # Add the new paragraph to the current writing
    title = latest_plan_dict[str(section_number)]['sub_section'][subsection_key]['title']
    title = "" if title is None else title

    subsection_paragraph = subsection_paragraph or ""

    current_writing += title + '\n' + subsection_paragraph + '\n'

    return current_writing, subsection_paragraph

def gen_fir(latest_plan, latest_plan_dict,current_writing):
    introduction_critic_prompt = """
    As a Critic, your task is to thoroughly review and provide constructive feedback
    on essays submitted by the Academic Writer. These essays are crafted for the
    International Baccalaureate (IB) program and must meet high standards of quality
    and relevance. When evaluating the essays, please focus on the following key aspects:

    Word Count Compliance: Ensure that the essay adheres to the specified word count.
    This is crucial for meeting IB standards.

    Alignment with the Outline: Verify that the essay aligns with the provided outline.
    It should cover all the necessary points and maintain a coherent structure throughout.

    Quality of Content: Assess the essay for its insightfulness, clarity, and overall quality.
    The writing should be compelling, well-argued, and adhere strictly to IB criteria.

    Stick to syllybus: Stick to the IB syllybus

    Sentence structure: Use simple and short sentence without complicated structure

    Relevance and Precision: Check that the essay stays on topic and does not
    include unnecessary or irrelevant information. Each part of the essay should
    contribute meaningfully to the overall argument or discussion.

    If there is GRAPH(s) inserted in the paragraph, review the accuracy of the
    graph based on the description. Also, the paragraph around the GRAPH should
    be connected to the GRAPH and expalins it

    Make sure the background introduction with personal sotry first.

    Make sure the latex experssion is correct

    Make sure the paragraph has enough words

    Make sure the word used is within the vocabulary of foreign high school students

    Please encapsulate your feedback within feedback and feedback for clarity.
    This will help the Academic Writer easily identify and implement your suggestions.

    Your role as a Critic is vital to ensure that the essays not only meet the
    academic standards but also provide valuable insights in accordance with the
    IB program guidelines.

    Ask the writer to rewrite the paragrah like it is written by high school student while keeping
    the word count and use simple sentense structure and simple words


    If there is GRAPH in the essay, make sure it has context paragraph connected
    to the graph
    """

    return generate_paragraph_helper(latest_plan, latest_plan_dict, 1, current_writing, introduction_critic_prompt)


def gen_sec(latest_plan,latest_plan_dict,current_writing):
    background_critic_prompt = """
    As a Critic, your task is to thoroughly review and provide constructive feedback
    on essays submitted by the Academic Writer. These essays are crafted for the
    International Baccalaureate (IB) program and must meet high standards of quality
    and relevance. When evaluating the essays, please focus on the following key aspects:

    Word Count Compliance: Ensure that the essay adheres to the specified word count.
    This is crucial for meeting IB standards.

    Alignment with the Outline: Verify that the essay aligns with the provided outline.
    It should cover all the necessary points and maintain a coherent structure throughout.

    Quality of Content: Assess the essay for its insightfulness, clarity, and overall quality.
    The writing should be compelling, well-argued, and adhere strictly to IB criteria.

    Stick to syllybus: Stick to the IB syllybus

    Sentence structure: Use simple and short sentence without complicated structure

    Relevance and Precision: Check that the essay stays on topic and does not
    include unnecessary or irrelevant information. Each part of the essay should
    contribute meaningfully to the overall argument or discussion.

    If there is GRAPH(s) inserted in the paragraph, review the accuracy of the
    graph based on the description. Also, the paragraph around the GRAPH should
    be connected to the GRAPH and expalins it

    Make sure the latex experssion is correct

    Make sure the paragraph has enough words


    Don't mention IB by any means in the main text or any educational purpose,
    the writer represents the student know should write as the student, don't refer
    to student or anything, the writer is the student

    Make sure the word used is within the vocabulary of foreign high school students


    If there is GRAPH in the essay, make sure the main text connected to the graph

    Ask the writer to rewrite the paragrah like it is written by high school student while keeping
    the word count and use simple sentense structure and simple words

    """
    
    return generate_paragraph_helper(latest_plan, latest_plan_dict, 2, current_writing, background_critic_prompt)

def gen_thi_fir(latest_plan,latest_plan_dict,current_writing):
    background_critic_prompt = """
    As a Critic, your task is to thoroughly review and provide constructive feedback
    on essays submitted by the Academic Writer. These essays are crafted for the
    International Baccalaureate (IB) program and must meet high standards of quality
    and relevance. When evaluating the essays, please focus on the following key aspects:

    Word Count Compliance: Ensure that the essay adheres to the specified word count.
    This is crucial for meeting IB standards.

    Alignment with the Outline: Verify that the essay aligns with the provided outline.
    It should cover all the necessary points and maintain a coherent structure throughout.

    Quality of Content: Assess the essay for its insightfulness, clarity, and overall quality.
    The writing should be compelling, well-argued, and adhere strictly to IB criteria.

    Stick to syllybus: Stick to the IB syllybus

    Sentence structure: Use simple and short sentence without complicated structure

    Relevance and Precision: Check that the essay stays on topic and does not
    include unnecessary or irrelevant information. Each part of the essay should
    contribute meaningfully to the overall argument or discussion.

    If there is GRAPH(s) inserted in the paragraph, review the accuracy of the
    graph based on the description. Also, the paragraph around the GRAPH should
    be connected to the GRAPH and expalins it

    Make sure the latex experssion is correct

    Make sure the paragraph has enough words


    Don't mention IB by any means in the main text or any educational purpose,
    the writer represents the student know should write as the student, don't refer
    to student or anything, the writer is the student

    Make sure the word used is within the vocabulary of foreign high school students


    If there is GRAPH in the essay, make sure the main text connected to the graph

    Ask the writer to rewrite the paragrah like it is written by high school student while keeping
    the word count and use simple sentense structure and simple words

    """
    return generate_subsection_paragraph(latest_plan, latest_plan_dict, 3, 1, current_writing, background_critic_prompt)

def gen_thi_sec(latest_plan,latest_plan_dict,current_writing):
    building_critic_prompt = """
    As a Critic, your task is to thoroughly review and provide constructive feedback
    on essays submitted by the Academic Writer. These essays are crafted for the
    International Baccalaureate (IB) program and must meet high standards of quality
    and relevance. When evaluating the essays, please focus on the following key aspects:

    Word Count Compliance: Ensure that the essay adheres to the specified word count.
    This is crucial for meeting IB standards.

    Alignment with the Outline: Verify that the essay aligns with the provided outline.
    It should cover all the necessary points and maintain a coherent structure throughout.

    Quality of Content: Assess the essay for its insightfulness, clarity, and overall quality.
    The writing should be compelling, well-argued, and adhere strictly to IB criteria.

    Use Common words: Avoid using uncommon words

    Stick to syllybus: Stick to the IB syllybus

    Sentence structure: Use simple sentence and avoid using long complicated sentence

    Relevance and Precision: Check that the essay stays on topic and does not
    include unnecessary or irrelevant information. Each part of the essay should
    contribute meaningfully to the overall argument or discussion.

    If there is GRAPH(s) inserted in the paragraph, review the accuracy of the
    graph based on the description. Also, the paragraph around the GRAPH should
    be connected to the GRAPH and expalins it

    Make sure the latex experssion is correct

    Make sure the paragraph has enough words

    Make sure the word used is not rare

    Makre sure the [GRAPH] is belongs to the current section as well as the
    text around the [GRAPH] have detailed parameters with numers

    Make sure the sections are well connected
    Make sure the buiding paraph has step by step explaination of the building process

    If there is GRAPH in the essay, make sure the main text connected to the graph
    Make sure there is context around the GRAPH explain the paramters used to draw
    the graph



    Please encapsulate your feedback within feedback and feedback for clarity.
    This will help the Academic Writer easily identify and implement your suggestions.


    Ask the writer to rewrite the paragrah like it is written by high school student while keeping
    the word count and use simple sentense structure and simple words. Avoid nonsense
    words for the sake of keeping the word count and keep the graph tag. If there is graph tag,
    make sure text around and graph description has detailed parameters with numbers.
    Make sure we have set the detailed numbers in the parameters in the graph description
    and the text around it. For example, gamma 0.1, beta 0.3 etc. To have  consistant view of the graph. This is very important

    """
    return generate_subsection_paragraph(latest_plan, latest_plan_dict, 3, 2, current_writing, building_critic_prompt)

def gen_thi_thi(latest_plan,latest_plan_dict,current_writing):
    building_critic_prompt = """
    As a Critic, your task is to thoroughly review and provide constructive feedback
    on essays submitted by the Academic Writer. These essays are crafted for the
    International Baccalaureate (IB) program and must meet high standards of quality
    and relevance. When evaluating the essays, please focus on the following key aspects:

    Word Count Compliance: Ensure that the essay adheres to the specified word count.
    This is crucial for meeting IB standards.

    Alignment with the Outline: Verify that the essay aligns with the provided outline.
    It should cover all the necessary points and maintain a coherent structure throughout.

    Quality of Content: Assess the essay for its insightfulness, clarity, and overall quality.
    The writing should be compelling, well-argued, and adhere strictly to IB criteria.

    Use Common words: Avoid using uncommon words

    Stick to syllybus: Stick to the IB syllybus

    Sentence structure: Use simple sentence and avoid using long complicated sentence

    Relevance and Precision: Check that the essay stays on topic and does not
    include unnecessary or irrelevant information. Each part of the essay should
    contribute meaningfully to the overall argument or discussion.

    If there is GRAPH(s) inserted in the paragraph, review the accuracy of the
    graph based on the description. Also, the paragraph around the GRAPH should
    be connected to the GRAPH and expalins it

    Make sure the latex experssion is correct

    Make sure the paragraph has enough words

    Make sure the word used is not rare

    Makre sure the [GRAPH] is belongs to the current section as well as the
    text around the [GRAPH] have detailed parameters with numers

    Make sure the sections are well connected
    Make sure the buiding paraph has step by step explaination of the building process

    If there is GRAPH in the essay, make sure the main text connected to the graph
    Make sure there is context around the GRAPH explain the paramters used to draw
    the graph



    Please encapsulate your feedback within feedback and feedback for clarity.
    This will help the Academic Writer easily identify and implement your suggestions.


    Ask the writer to rewrite the paragrah like it is written by high school student while keeping
    the word count and use simple sentense structure and simple words. Avoid nonsense
    words for the sake of keeping the word count and keep the graph tag. If there is graph tag,
    make sure text around and graph description has detailed parameters with numbers.
    Make sure we have set the detailed numbers in the parameters in the graph description
    and the text around it. For example, gamma 0.1, beta 0.3 etc. To have  consistant view of the graph. This is very important

    """
    return generate_subsection_paragraph(latest_plan, latest_plan_dict, 3, 3, current_writing, building_critic_prompt)

def gen_four_fir(latest_plan,latest_plan_dict,current_writing):
    background_critic_prompt = """
    As a Critic, your task is to thoroughly review and provide constructive feedback
    on essays submitted by the Academic Writer. These essays are crafted for the
    International Baccalaureate (IB) program and must meet high standards of quality
    and relevance. When evaluating the essays, please focus on the following key aspects:

    Word Count Compliance: Ensure that the essay adheres to the specified word count.
    This is crucial for meeting IB standards.

    Alignment with the Outline: Verify that the essay aligns with the provided outline.
    It should cover all the necessary points and maintain a coherent structure throughout.

    Quality of Content: Assess the essay for its insightfulness, clarity, and overall quality.
    The writing should be compelling, well-argued, and adhere strictly to IB criteria.

    Stick to syllybus: Stick to the IB syllybus

    Sentence structure: Use simple and short sentence without complicated structure

    Relevance and Precision: Check that the essay stays on topic and does not
    include unnecessary or irrelevant information. Each part of the essay should
    contribute meaningfully to the overall argument or discussion.

    If there is GRAPH(s) inserted in the paragraph, review the accuracy of the
    graph based on the description. Also, the paragraph around the GRAPH should
    be connected to the GRAPH and expalins it

    Make sure the latex experssion is correct

    Make sure the paragraph has enough words


    Don't mention IB by any means in the main text or any educational purpose,
    the writer represents the student know should write as the student, don't refer
    to student or anything, the writer is the student

    Make sure the word used is within the vocabulary of foreign high school students


    If there is GRAPH in the essay, make sure the main text connected to the graph

    Ask the writer to rewrite the paragrah like it is written by high school student while keeping
    the word count and use simple sentense structure and simple words

    """
    return generate_subsection_paragraph(latest_plan, latest_plan_dict, 4, 1, current_writing, background_critic_prompt)


def gen_four_sec(latest_plan,latest_plan_dict,current_writing):
    background_critic_prompt = """
    As a Critic, your task is to thoroughly review and provide constructive feedback
    on essays submitted by the Academic Writer. These essays are crafted for the
    International Baccalaureate (IB) program and must meet high standards of quality
    and relevance. When evaluating the essays, please focus on the following key aspects:

    Word Count Compliance: Ensure that the essay adheres to the specified word count.
    This is crucial for meeting IB standards.

    Alignment with the Outline: Verify that the essay aligns with the provided outline.
    It should cover all the necessary points and maintain a coherent structure throughout.

    Quality of Content: Assess the essay for its insightfulness, clarity, and overall quality.
    The writing should be compelling, well-argued, and adhere strictly to IB criteria.

    Stick to syllybus: Stick to the IB syllybus

    Sentence structure: Use simple and short sentence without complicated structure

    Relevance and Precision: Check that the essay stays on topic and does not
    include unnecessary or irrelevant information. Each part of the essay should
    contribute meaningfully to the overall argument or discussion.

    If there is GRAPH(s) inserted in the paragraph, review the accuracy of the
    graph based on the description. Also, the paragraph around the GRAPH should
    be connected to the GRAPH and expalins it

    Make sure the latex experssion is correct

    Make sure the paragraph has enough words


    Don't mention IB by any means in the main text or any educational purpose,
    the writer represents the student know should write as the student, don't refer
    to student or anything, the writer is the student

    Make sure the word used is within the vocabulary of foreign high school students


    If there is GRAPH in the essay, make sure the main text connected to the graph

    Ask the writer to rewrite the paragrah like it is written by high school student while keeping
    the word count and use simple sentense structure and simple words

    """
    return generate_subsection_paragraph(latest_plan, latest_plan_dict, 4, 2, current_writing, background_critic_prompt)

def gen_four_thi(latest_plan,latest_plan_dict,current_writing):
    background_critic_prompt = """
    As a Critic, your task is to thoroughly review and provide constructive feedback
    on essays submitted by the Academic Writer. These essays are crafted for the
    International Baccalaureate (IB) program and must meet high standards of quality
    and relevance. When evaluating the essays, please focus on the following key aspects:

    Word Count Compliance: Ensure that the essay adheres to the specified word count.
    This is crucial for meeting IB standards.

    Alignment with the Outline: Verify that the essay aligns with the provided outline.
    It should cover all the necessary points and maintain a coherent structure throughout.

    Quality of Content: Assess the essay for its insightfulness, clarity, and overall quality.
    The writing should be compelling, well-argued, and adhere strictly to IB criteria.

    Stick to syllybus: Stick to the IB syllybus

    Sentence structure: Use simple and short sentence without complicated structure

    Relevance and Precision: Check that the essay stays on topic and does not
    include unnecessary or irrelevant information. Each part of the essay should
    contribute meaningfully to the overall argument or discussion.

    If there is GRAPH(s) inserted in the paragraph, review the accuracy of the
    graph based on the description. Also, the paragraph around the GRAPH should
    be connected to the GRAPH and expalins it

    Make sure the latex experssion is correct

    Make sure the paragraph has enough words


    Don't mention IB by any means in the main text or any educational purpose,
    the writer represents the student know should write as the student, don't refer
    to student or anything, the writer is the student

    Make sure the word used is within the vocabulary of foreign high school students


    If there is GRAPH in the essay, make sure the main text connected to the graph

    Ask the writer to rewrite the paragrah like it is written by high school student while keeping
    the word count and use simple sentense structure and simple words

    """
    return generate_subsection_paragraph(latest_plan, latest_plan_dict, 4, 3, current_writing, background_critic_prompt)

def extract_graph_descriptions(text):
    graph_pattern = r"\[GRAPH: (.*?)\]"
    return re.findall(graph_pattern, text, flags=re.DOTALL)

def extract_file_id(chat_messages):
    for chat_key in chat_messages:
        for message in reversed(chat_messages[chat_key]):
            if 'Received file' in message['content']:
                start_index = message['content'].find('file id=') + len('file id=')
                end_index = message['content'].find('\n', start_index)
                if end_index != -1:
                    return message['content'][start_index:end_index].strip()
    return None

def drawing_graph(instruction: str):
    openai_api_key=os.getenv("OPENAI_API_KEY")
    config_list = [{'model': 'gpt-4-1106-preview', 'api_key': openai_api_key}]
    coder_assistant = GPTAssistantAgent(
        name="Coder Assistant",
        llm_config={
            "tools": [{"type": "code_interpreter"}],
            "config_list": config_list,
        },
        instructions="You are an expert at writing python code to plot the graph Make sure it is clear and visible. Reply TERMINATE when the task is solved and there is no problem. Reply TERMNIATE WHEN FILE SUCCESFULLY GENEREATED",
    )

    user_proxy_coder = UserProxyAgent(
        name="user_proxy",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,
        },
        human_input_mode="NEVER"
    )

    user_proxy_coder.initiate_chat(coder_assistant, message=instruction, clear_history=True)
    file_id = extract_file_id(user_proxy_coder.chat_messages)

    if file_id is None:
        raise Exception("Failed to generate the graph.")

    api_response = coder_assistant.openai_client.files.with_raw_response.retrieve_content(file_id)

    if api_response.status_code != 200:
        raise Exception("Failed to retrieve the graph image.")

    image_data_bytes = io.BytesIO(api_response.content)
    image = Image.open(image_data_bytes)
    return image

def generate_graphs(paragraph):
    graphs = extract_graph_descriptions(paragraph)
    graph_images = []
    for graph in graphs:
        graph_images.append(drawing_graph(graph))
    return graph_images


def markdown_to_pdf(markdown_string, output_filename):

    pdf = MarkdownPdf(toc_level=2)

    md = MarkdownIt()
    html = md.render(markdown_string)

    pdf.add_section(Section(html))

    # Set the properties of the PDF document
    pdf.meta["title"] = "Document Title"

    # Save the PDF to a file
    pdf.save(output_filename)

def dict_to_markdown(input_dict, level=0):
    markdown_output = ""

    if 'title' in input_dict and level != 0:  # Skip the top-level title
        markdown_output += '#' * level + " " + input_dict['title'] + "\n\n"

    for key, value in input_dict.items():
        if isinstance(value, dict):
            markdown_output += dict_to_markdown(value, level + 1)
        elif key == 'content':
            for item in value:
                if isinstance(item, list):
                    for sub_item in item:
                        markdown_output += str(sub_item) + "\n\n"
                else:
                    markdown_output += str(item)+ "\n\n"
    return markdown_output

def generate_markdown(input_dict):
    markdown_output = "# " + input_dict['title'] + "\n\n"  # Add the top-level title separately
    markdown_output += dict_to_markdown(input_dict)
    return markdown_output


def update_content(input_dict, paragraphs, index=0):
    if index >= len(paragraphs):
        return input_dict, index

    new_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, dict):
            new_dict[key], index = update_content(value, paragraphs, index)
        elif key == 'content':
            new_dict[key] = [paragraphs[index]]
            index += 1
        else:
            new_dict[key] = value

    return new_dict, index

# def assemble_dict(latest_plan_dict, paragraphs):
#     new_dict, _ = update_content(latest_plan_dict, paragraphs)
#     return new_dict
def insert_images_into_text(paragraphs, image_dir):
    """
    Insert images into text before each '[GRAPH: (.*?)]' tag.

    Args:
    paragraphs (list[str]): The list of paragraphs to insert images into.
    image_dir (str): The directory where the images are saved.

    Returns:
    str: The updated text with images inserted.
    """
    # Get all images in the directory and sort them by their names
    images = sorted([img for img in os.listdir(image_dir) if img.endswith('.png')])

    updated_paragraphs = []
    image_index = 0  # Use the index of the image in the sorted list
    for paragraph in paragraphs:
        match = re.search(r'\[GRAPH: (.*?)\]', paragraph)
        while match and image_index < len(images):
            img_path = f"{image_dir}/{images[image_index]}"
            img_markdown = f"![Image {image_index+1}]({img_path})\n\n"
            start, end = match.span()
            paragraph = paragraph[:start] + img_markdown + paragraph[end:]
            image_index += 1
            match = re.search(r'\[GRAPH: (.*?)\]', paragraph)
        updated_paragraphs.append(paragraph)

    return updated_paragraphs


def assemble_dict(latest_plan_dict, paragraphs, image_dir):
    # Insert images into the paragraphs.
    paragraphs_with_images = insert_images_into_text(paragraphs, image_dir)

    # Update the content of the dictionary with the new paragraphs.
    new_dict, _ = update_content(latest_plan_dict, paragraphs_with_images)
    return new_dict


def save_images(images, path, prefix):
    if not os.path.exists(path):
        os.makedirs(path)

    for i, image in enumerate(images):
        plt.imshow(image)
        plt.axis('off') 
        img_name = f"image_{prefix}_{i+1}.png"
        img_path = os.path.join(path, img_name)
        plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
        plt.close() 

def test_generate_essay(latest_plan, latest_plan_dict):
    path = "pdffile/src"
    title=latest_plan_dict['title']
    current_writing, first_paragraph = gen_fir(latest_plan, latest_plan_dict, latest_plan_dict['title'] + '\n\n')

    current_writing, second_paragraph = gen_sec(latest_plan, latest_plan_dict, current_writing)
    sec_graph_images = generate_graphs(second_paragraph)
    save_images(sec_graph_images, path,'2')

    current_writing, third_first_paragraph = gen_thi_fir(latest_plan, latest_plan_dict, current_writing)
    third_first_graph_images = generate_graphs(third_first_paragraph)
    save_images(third_first_graph_images, path,'3_1')

    current_writing, third_second_paragraph = gen_thi_sec(latest_plan, latest_plan_dict, current_writing)
    third_second_graph_images = generate_graphs(third_second_paragraph)
    save_images(third_second_graph_images, path,'3_2')

    current_writing, third_third_paragraph = gen_thi_thi(latest_plan, latest_plan_dict, current_writing)
    third_third_graph_images = generate_graphs(third_third_paragraph)
    save_images(third_third_graph_images, path,'3_3')

    current_writing, fourth_first_paragraph = gen_four_fir(latest_plan, latest_plan_dict, current_writing)
    forth_first_graph_images = generate_graphs(fourth_first_paragraph)
    save_images(forth_first_graph_images, path,'4_1')

    current_writing, fourth_second_paragraph = gen_four_sec(latest_plan, latest_plan_dict, current_writing)
    forth_second_graph_images = generate_graphs(fourth_second_paragraph)
    save_images(forth_second_graph_images, path,'4_2')

    current_writing, fourth_third_paragraph = gen_four_thi(latest_plan, latest_plan_dict, current_writing)
    forth_third_graph_images = generate_graphs(fourth_third_paragraph)
    save_images(forth_third_graph_images, path,'4_3')

    paragraphs = [first_paragraph, second_paragraph, third_first_paragraph, third_second_paragraph, third_third_paragraph, fourth_first_paragraph, fourth_second_paragraph, fourth_third_paragraph]
    new_dict = assemble_dict(latest_plan_dict, paragraphs, path)

    md_string = generate_markdown(new_dict)
    markdown_to_pdf(md_string, f'pdffile/{title}.pdf')
    return f'pdffile/{title}.pdf'

# test1() 