from typing import Optional, List

from functions.encoder import get_encoder
from .output import SearchDocument

def combined_prompt(example_context_prompt: str, question: str, selected_documents: List[SearchDocument]):
    return f"""Please answer the question according to the given context.
{example_context_prompt}
===
Context: {' '.join([d.text for d in selected_documents])}
Q: {question}
A:"""

def better_answers_prompt(
    model: str,
    max_tokens: int,
    question: str,
    selected_documents:
    List[SearchDocument],
    examples: Optional[List[List[str]]] = [],
    examples_context: Optional[str] = None,
):
    """
    Prompts the user for an answer to the given question.
    """

    if 'codex' in model:
        encoder = get_encoder('codex')
        max_quota = 4096
    else:
        encoder = get_encoder('gpt3')
        max_quota = 2048

    example_context_prompt = ''

    for example in examples:
        if isinstance(example, list) and len(example) == 2:
            example_context_prompt += f"""===
Context: {examples_context}
Q: {example[0]}
A: {example[1]}""" if examples_context is not None else ""

    i = 0
    prompt = combined_prompt(example_context_prompt, question, selected_documents[i:])

    while len(encoder.encode(prompt)) + max_tokens > max_quota:
        i += 1
        prompt = combined_prompt(example_context_prompt, question, selected_documents[i:])

    return prompt, i
