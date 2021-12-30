from typing import List, Dict, Optional, Union
from pydantic import BaseModel

class BetterAnswersInput(BaseModel):
    """
    Input model for the better_answers endpoint.
    """
    model: str
    question: str
    examples: Optional[List[List[str]]]
    examples_context: Optional[str]
    # TODO: add support between documents and file
    # documents: Optional[List[str]]
    file: str
    search_model = 'ada'
    max_rerank = 200
    z_threshold = 0.0
    temperature = 0.0
    logprobs: Optional[int]
    max_tokens = 16
    stop: Optional[Union[str, List[str]]]
    n = 1
    logit_bias: Optional[Dict[str, float]]
    return_metadata = False
    return_prompt = False
    expand: Optional[List[str]]
