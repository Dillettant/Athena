import re
import os
from collections import defaultdict
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager


def generate_chat(topic):
    """
    Generate a chat between a subject expert and a critic to create an IB essay plan.

    :param topic: The topic of the essay.
    :return: A dictionary containing the chat messages.
    """
    subject_expert_system_prompt = """
    As a Subject Expert in IB essay writing, your task is to guide the creation of a
    comprehensive and engaging essay.
    The focus is on detailed planning for each section,
    ensuring academic rigor and relevance to the essay title. The plan should include:

    Title: [Your Essay Title Here]

    1. Introduction/Rationale (Word Count: XX)
    - Purpose: Explain the choice of this topic.Begin the rationale by relating
        the topic to a personal experience. Make up a personal story about what
        motivates you to choose this topic. Conclude the introduction with a clear
        statement of the research objective. Explicitly mention what specific
        aspect or question you aim to investigate in your study


    2. Background Information (Word Count: XX)
    - Content: Outline basic mathematical formulas or models that will be further developed in the essay. Don't mention that model here, only basic knowledge
    - If a graph is needed to illustrate concepts, annotate with '- GRAPH: [Describe the graph content]'.
    - Make sure the model is within the syllybus of IB, if not, use simper model, only explains the model

    3. Exploration (Total Word Count: XX)
    3.1. Definition (Word Count: XX): Define key terms, particularly for mathematical models.
            - If a graph is needed, annotate with '- GRAPH: [Describe the graph content]'.
    3.2. Model Building (Word Count: XX): Enhance and refine the base model.
            Break it into different sections, for each section, annoate with (Word Count: XX)
            If a graph is needed, annotate with '- GRAPH: [Describe the graph content]'. Put it at the end
            Format example:
            Section A - Classic SIR Model Adaptation (Word Count: 500)
            - Explanation of the SIR model adaptation to zombie dynamics, with zombies as the 'Infected' and fates of the 'Removed'.
            - GRAPH: Transition diagram for the adapted SIR model including zombie-specific transitions.

            Clearly specify the final model used in the Modeling section. Provide a
            detailed description of the model, including its structure, components,
            and how it was developed.
            When deducing the formulas/models, make sure you clearly write out each step, how you plug-in values, combine functions, use what theorem, etc

            Annotate each section with (Word Count: XX)

    3.3. Experiment (Word Count: XX): Detail the process of data collection (whether real or simulated) and its application to the model.
            Break it into different sections, for each section, annoate with (Word Count: XX)
            If a graph is needed, annotate with '- GRAPH: [Describe the graph content]'.  Put it at the end
            Format example:
            Section A - Classic SIR Model Adaptation (Word Count: 500)
            - Explanation of the SIR model adaptation to zombie dynamics, with zombies as the 'Infected' and fates of the 'Removed'.
            - GRAPH: Transition diagram for the adapted SIR model including zombie-specific transitions.
            - Try your best to design a meaningful experiment that would best reflect how the model defined in part 3.2 works
            - Detail the process of data collection (whether real or simulated) and its application to the model.
            - Write out the final conclusion for this experiment AND very importantly the insights from this experiment
            - Annotate each section with (Word Count: XX)

    4. Conclusion (Total Word Count: XX)
    4.1. Summary (Word Count: XX): Recapitulate the main findings, conclusions, and insights. Address the initial question in the Rationale.
    4.2. Reflection (Word Count: XX): Evaluate the strengths and weaknesses of the model and the essay.
    4.3. Extension (Word Count: XX): Propose potential enhancements and future explorations given more time.

    Ensure the plan is logical, detailed, and academically sound, with each section and subsection clearly connected to the essay's title. Incorporate critical feedback and format the plan within 'plan' tags without adding extra comments or brackets.
    Please ensure the plan within the tag consists only of the main content for each section and subsection, directly addressing the essay's title without any additional sentences or explanations.

    Make sure the graph is plotable with Python


    REPLAY THE PLAN ONLY NO MATTER WHAT

    If GRPAH is not needed, just don't use it, don't use N/A

    PLease have the plan tag [plan] [/plan]

    """
    openai_api_key=os.getenv("OPENAI_API_KEY")
    config_list = [{'model': 'gpt-4-1106-preview', 'api_key': openai_api_key}]
    subject_expert = AssistantAgent("subject_expert", system_message=subject_expert_system_prompt, llm_config={"config_list": config_list})

    critic_system_prompt = """
    Your role involves a thorough examination of the IB essay plan developed by a
    subject expert. Your feedback is essential in enhancing the plan’s academic
    strength, ensuring relevance to the essay's title, and maintaining a logical
    structure. Focus on the following key areas:

    Assess Each Section and Subsection:

    Confirm that each part of the plan is well-defined and contributes meaningfully
    to the essay's overall objective.
    Check that word counts are included for each section and subsection, indicating
    the depth and detail required.
    Evaluate Graph Requirements:

    For the Background Information and other relevant sections, assess if a graph is
    necessary to illustrate concepts. When required, specify the type of graph and
    annotate using 'GRAPH: [Describe the graph content]'.
    In the Exploration section, particularly the Experiment subsection, provide
    specific advice on the representation of data. If the topic is suitable for
    simulated data, and it is preferable, annotate this requirement with
    'GRAPH: [Describe the graph content]'. This option should be chosen when feasible.
    Feedback Delivery:

    Offer your feedback in a constructive, clear, and detailed manner.
    Focus on enhancing the clarity, academic integrity, and overall effectiveness of
    the essay plan.
    Refrain from adding any comments or annotations that are not directly related to
    improving the structure, content, and academic rigor of the plan.
    Your critical analysis and recommendations are vital in refining the essay plan
    to meet high academic standards and to ensure a coherent and impactful essay.
    Make sure the graph is plotable with Python.

    """
    critic = AssistantAgent(
        name="Critic",
        system_message=critic_system_prompt,
        llm_config={"config_list": config_list}
    )

    subject_expert_admin_system_prompt = """
    "A human admin. Initialize the converstion. Alternate between critic and Subject Expert
    """
    termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

    subject_expert_admin1 = UserProxyAgent("Admin", code_execution_config=False, system_message=subject_expert_admin_system_prompt, human_input_mode="NEVER",  is_termination_msg=termination_msg)

    groupchat = GroupChat(agents=[critic, subject_expert, subject_expert_admin1], messages=[], max_round=2)
    manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})
    subject_expert_admin1.initiate_chat(manager, message=f"Write an IB essay {topic} with 4000 words.")
    
    # print(f"[DEBUG] Chat messages: {subject_expert_admin1.chat_messages}, type: {type(subject_expert_admin1.chat_messages)}")
    return subject_expert_admin1.chat_messages

def extract_latest_plan(chat_messages):
    """
    Extract the latest essay plan from the chat messages.
    :param chat_messages: A dictionary containing the chat messages.
    """
    for chat_key in chat_messages:
        for message in reversed(chat_messages[chat_key]):
            if '[plan]' in message['content']:
                start_index = message['content'].find('[plan]') + len('[plan]')
                end_index = message['content'].find('[/plan]', start_index)
                if end_index != -1:
                    return message['content'][start_index:end_index].strip()
    return None

def parse_document_to_dict(text):
    """
    Parse the document into a dictionary.
    :param text: The text of the document.
    """
    lines = text.split('\n')
    idx = 0
    res = {}
    while idx < len(lines):
      if 'Title' in lines[idx]:
        extracted_text = lines[idx].split("Title: ")[1]
        res['title'] = extracted_text
        idx += 1
        break
      else:
        idx += 1
    idx_list = [idx]
    while idx_list[0] < len(lines):
      try:
        extract_section(res, idx_list, lines)
      except Exception as e:
        print(f"Error while extracting section: {e}")
    return res

def generate_plan_dict(topic):
    """
    Generate an IB essay plan dictionary for a given topic.
    :param topic: The topic of the essay.
    """
    chat_messages = generate_chat(topic)
    latest_plan = extract_latest_plan(chat_messages)
    latest_plan_dict = parse_document_to_dict(latest_plan)
    return latest_plan,latest_plan_dict


def extract_subsubsection(current_res, idx, lines, parent_number, pp_number):
    while idx[0] < len(lines) and lines[idx[0]].strip() == '':
        idx[0] += 1

    section_check_pattern = r"Section\s+[A-Z]+"
    remove_section_pattern = r"Section\s+[A-Z]+\s+-\s+"
    content = []

    if re.search(section_check_pattern, lines[idx[0]]):
        modified_string = re.sub(remove_section_pattern, "", lines[idx[0]])
        content.append(modified_string)
        idx[0] += 1

        while idx[0] < len(lines) and lines[idx[0]].strip() != '' and not re.search(section_check_pattern, lines[idx[0]]) and '3.3.' not in lines[idx[0]] and '4.' not in lines[idx[0]]:
            if 'GRAPH:' in lines[idx[0]]:
                lines[idx[0]] = lines[idx[0]].replace('GRAPH:', 'GRAPH_DESCRIPTION')
            content.append(lines[idx[0]])
            idx[0] += 1

        current_res[pp_number]['sub_section'][parent_number]['content'].append(content)

def extract_subsection(current_res, idx, lines, parent_number):
    while idx[0] < len(lines) and lines[idx[0]] == '':
        idx[0] += 1

    number_match = re.search(r"\b\d+\.\d+\b", lines[idx[0]])
    number = number_match.group(0) if number_match else None
    lines[idx[0]] = lines[idx[0]].replace("Total Word Count", "Word Count")

    if ('):' not in lines[idx[0]]):
        lines[idx[0]] += ':'

    pattern = r"(\w+) \(Word Count: (\d+)\):(.*)"
    match = re.search(pattern, lines[idx[0]])
    if match:
        title, word_count, content = match.groups()
    else:
        title, word_count, content = None, None, None

    if number not in ['3.2', '3.3']:
        current_res[parent_number]['sub_section'][number] = {
            'title': title,
            'word_count': word_count,
            'content': [content]
        }

        idx[0] += 1
        if idx[0] >= len(lines) or lines[idx[0]] == '':
            return

        while idx[0] < len(lines) and '-' in lines[idx[0]] and 'GRAPH' not in lines[idx[0]] and '3.2' not in lines[idx[0]] and '3.3' not in lines[idx[0]] and '4.1' not in lines[idx[0]] and '4.2' not in lines[idx[0]] and '4.3' not in lines[idx[0]]:
            current_res[parent_number]['sub_section'][number]['content'].append(lines[idx[0]])
            idx[0] += 1

        if idx[0] >= len(lines) or lines[idx[0]] == '':
            return

        graph_idx = lines[idx[0]].find('GRAPH')
        if graph_idx != -1:
            current_res[parent_number]['sub_section'][number]['graph_description'] = lines[idx[0]][graph_idx + 7:]
            idx[0] += 1
    else:
        current_res[parent_number]['sub_section'][number] = {
            'title': title,
            'word_count': word_count,
            'content': []
        }
        idx[0] += 1
        section_check_pattern = r"Section\s+[A-Z]+"
        remove_section_pattern = r"Section\s+[A-Z]+\s+-\s+"
        while idx[0] < len(lines) and '3.3' not in lines[idx[0]] and '4.' not in lines[idx[0]]:
            extract_subsubsection(current_res, idx, lines, number, parent_number)

def extract_section(current_res, idx, lines):
    while idx[0] < len(lines) and lines[idx[0]] == '':
        idx[0] += 1

    number_match = re.search(r"^\b(\d+(\.\d+)*)\b", lines[idx[0]])
    number = number_match.group(0) if number_match else None
    current_res[number] = {}
    has_sub_section = "Total Word Count" in lines[idx[0]]

    if not has_sub_section:
        word_count_match = re.search(r"Word Count: (\d+)", lines[idx[0]])
        word_count = int(word_count_match.group(1)) if word_count_match else None
        content = re.sub(r"^\d+(\.\d+)*\.\s+|\s+\(Word Count: \d+\)$", "", lines[idx[0]])
        current_res[number] = {
            'title': content,
            'word_count': word_count,
            'content': []
        }
    else:
        content = re.sub(r"^\d+(\.\d+)*\.\s+|\s+\(Total Word Count: \d+\)$", "", lines[idx[0]])
        current_res[number] = {
            'title': content,
            'sub_section': {}
        }

    idx[0] += 1
    if not has_sub_section:
        while idx[0] < len(lines) and lines[idx[0]] != '':
            if 'GRAPH' in lines[idx[0]]:
                current_res[number]['graph_description'] = lines[idx[0]][12:]
            else:
                current_res[number]['content'].append(lines[idx[0]][5:])
            idx[0] += 1
    else:
        first_non_whitespace = next((char for char in lines[idx[0]] if not char.isspace()), None)
        while idx[0] < len(lines) and lines[idx[0]] and first_non_whitespace == number:
            extract_subsection(current_res, idx, lines, number)
            while (idx[0] < len(lines) and lines[idx[0]].strip() == ''):
                idx[0] += 1
            if idx[0] >= len(lines):
                break
            first_non_whitespace = next((char for char in lines[idx[0]] if not char.isspace()), None)

def parse_document_to_dict(text):
    lines = text.split('\n')
    idx = 0
    res = {}
    while idx < len(lines):
        if 'Title' in lines[idx]:
            extracted_text = lines[idx].split("Title: ")[1]
            res['title'] = extracted_text
            idx += 1
            break
        else:
            idx += 1
    idx_list = [idx]
    while idx_list[0] < len(lines):
        try:
            extract_section(res, idx_list, lines)
        except Exception as e:
            raise Exception("Error while extracting section: {}".format(e))
    return res

def test_generate_outline(topic):
    chat_messages = generate_chat(topic)
    latest_plan = extract_latest_plan(chat_messages)
    latest_plan_dict = parse_document_to_dict(latest_plan)
    return latest_plan,latest_plan_dict
