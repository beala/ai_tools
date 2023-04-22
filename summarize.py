import argparse
import sys

import openai
import tiktoken

import chunk
from utils import p, openai_api_key, chat

openai.api_key = openai_api_key()

def split(*args, **kwargs):
    chunks = chunk.chunk(*args, **kwargs)
    cur_chunk = chunks[0]
    if len(chunks) > 1:
        tail = "".join(chunks[1:])
    else:
        tail = None
    return (cur_chunk, tail)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run", action="store_true", help="Don't actually run the model.")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="Model to use. Defaults to gpt-3.5-turbo.")
    args = parser.parse_args()

    input_ = sys.stdin.read()

    max_chunk_size = 4096 if args.model == "gpt-3.5-turbo" else 8192
    max_chunk_size -= 2000 # Leave room for response, prompt, etc.

    first_system_prompt = "Your task is to summarize podcasts from transcripts. Before giving you the transcript, " \
                          "I've divided it up into chunks. This is the first chunk from the transcript. Summarize as " \
                          "a list of bullet points about the main topics and ideas."
    consecutive_system_prompt = "Your task is to summarize podcasts from transcripts. Before giving you the " \
                                "transcript, I've divided it up into chunks. This chunk comes from where in the " \
                                "middle of the podcast, so I've also provided you with a summary of the previous " \
                                "chunks. Please continue the summary. Summarize as a list of bullet points about the " \
                                "main topics and ideas."

    first_prompt = """

---

The text above is the first part of a transcript from a podcast. Summarize the main ideas as a list of bullet points."""

    second_prompt = """# Transcript

{}

# Summary

{}

---

The text above is a partial transcript from a podcast. Summarize the main ideas as a list of bullet points. The transcript
leading up to the excerpt has already been summarized and is also provided above."""

    i = 0
    tail = input_
    summary = []
    while tail:
        encoding = tiktoken.encoding_for_model(args.model)

        head, tail = split(text=tail, chunk_size=max_chunk_size, overlap=0, model=args.model)

        if i == 0:
            messages = [
                {"role": "user", "content": head + first_prompt}
            ]
        else:
            last_summary = encoding.decode(encoding.encode(summary[-1])[-100:])
            last_transcript = encoding.decode(encoding.encode(head)[-100:])
            messages = [
                {"role": "user", "content": second_prompt.format(last_transcript+head, last_summary)}
            ]

        if args.dry_run:
            for m in messages:
                p(m["content"])

        p(f"Summarizing chunk {i+1}... ", end="", flush=True)
        if args.dry_run:
            summary.append("This is a mock summary from a dry run. " * 10)
        else:
            resp = chat(model=args.model, messages=messages)
            summary.append(resp)
        p("✅")
        i += 1

    final_prompt = """

---

This is an automatically generated summary of a podcast. Please rewrite it into the following format:

tl;dr: {One or two sentences summarizing the podcast}

{Longer paragraph long summary of the main ideas}
"""

    if args.dry_run:
        resp = "This is a mock response from a dry run. " * 10
    else:
        p("Generating final summary... ", end="", flush=True)
        resp = chat(
            model="gpt-4",
            messages=[
                {"role": "user", "content": "\n".join(summary) + final_prompt}
            ])
        p("✅")

    print()
    print(resp)
    print("\nNotes:")
    print("\n".join(summary))