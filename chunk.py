import argparse
import codecs
import json
import sys
from pathlib import Path
from pprint import pprint
from typing import List

import tiktoken

from utils import p


def chunk(text, chunk_size, overlap, model=None, encoding=None) -> List[str]:
    if encoding:
        encoding = tiktoken.get_encoding(encoding)
    elif model:
        encoding = tiktoken.encoding_for_model(model)
    else:
        p("Warning: no encoding or model specified. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    encoded = encoding.encode(text)

    output = []
    chunk_size = chunk_size - (2 * overlap)
    if chunk_size <= 0:
        raise Exception("Overlap * 2 must be less than chunk size.")
    for i in range(0, len(encoded), chunk_size):
        start = max(0, i - overlap)
        end = min(len(encoded), i + chunk_size + overlap)
        encoded_chunk = encoded[start:end]
        output.append(encoding.decode(encoded_chunk))

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="File to read. Otherwise, stdin is used.")
    parser.add_argument("--encoding", type=str,
                        help="Encoding to use. See: https://github.com/openai/tiktoken/blob/46287bfa493f8ccca4d927386d7ea9cc20487525/tiktoken/model.py#L6-L53")
    parser.add_argument("--model", type=str,
                        help="Model to use. Overrides --encoding. See: https://github.com/openai/tiktoken/blob/46287bfa493f8ccca4d927386d7ea9cc20487525/tiktoken/model.py#L6-L53")
    parser.add_argument("--chunk_size", type=int, default=4096, help="Chunk size. Defaults to 4096.")
    parser.add_argument("--separator", type=str, default="\n\n", help="Separator to use when joining chunks. Defaults "
                                                                      "to two newlines.")
    parser.add_argument("--json", action="store_true", help="Output as JSON.")
    parser.add_argument("--overlap", type=int, default=0, help="Overlap between chunks. Defaults to 0.")
    args = parser.parse_args()

    if args.file:
        input_ = Path(args.file).read_text()
    else:
        input_ = sys.stdin.read()

    output = chunk(input_, args.chunk_size, args.overlap, args.model, args.encoding)

    if args.json:
        print(json.dumps(output))
    else:
        if args.separator:
            sep = codecs.decode(args.separator, "unicode_escape")
            print(sep.join(output), end="")
        else:
            pprint(output)
