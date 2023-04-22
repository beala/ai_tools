import os
import sys
from pathlib import Path

import openai


def openai_api_key() -> str:
    if openai.api_key:
        return openai.api_key
    script_path = os.path.dirname(os.path.realpath(__file__))
    return Path(script_path, "OPENAI_API_KEY").read_text().strip()


SILENT = False

def p(*args, **kwargs):
    if "file" not in kwargs:
        kwargs["file"] = sys.stderr
    if not SILENT:
        print(*args, **kwargs)


def chat(*args, **kwargs):
    resp = openai.ChatCompletion.create(
        *args, **kwargs
    )
    return resp['choices'][0]['message']['content']