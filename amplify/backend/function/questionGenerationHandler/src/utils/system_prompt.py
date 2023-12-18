def get_system_prompt(question_number, topic):
    return f"Directly list {question_number} questions about {topic}. The questions should be tailored based on the CV's details. No introduction, explanation, or additional remarks should be included. Only present the questions, numbered and concise."  # noqa: E501
