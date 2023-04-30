import argparse
import sys

import openai

import utils

openai.api_key = utils.openai_api_key()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="Model to use. Defaults to gpt-3.5-turbo. Other optiosn: gpt-4, gpt-4-32k")
    args = parser.parse_args()

    input_ = sys.stdin.read()

    resp = utils.chat(
        model=args.model,
        messages=[{"role":"user", "content": input_}]
    )

    print(resp)