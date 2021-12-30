import regex as re

# Should haved added re.IGNORECASE so BPE merges can happen for capitalized versions of contractions
pat_regex = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""")
