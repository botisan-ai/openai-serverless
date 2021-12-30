from typing import Optional, List

from .output import SearchDocument

# TODO: count tokens filter out lower-scoring documents if it reaches max tokens
def better_answers_prompt(question: str, selected_documents: List[SearchDocument], examples: Optional[List[List[str]]] = [], examples_context: Optional[str] = None):
    """
    Prompts the user for an answer to the given question.
    """
    example_context_prompt = ''
    for example in examples:
        if isinstance(example, list) and len(example) == 2:
            example_context_prompt += f"""===
Context: {examples_context}
Q: {example[0]}
A: {example[1]}""" if examples_context is not None else ""
    return f"""Please answer the question according to the given context.
{example_context_prompt}
===
Context: {' '.join([d.text for d in selected_documents])}
Q: {question}
A:"""
