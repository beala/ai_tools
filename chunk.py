import argparse
import codecs
import json
import sys
from pathlib import Path
from pprint import pprint

import tiktoken

from utils import p


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="File to read. Otherwise, stdin is used.")
    parser.add_argument("--encoding", type=str, help="Encoding to use. See: https://github.com/openai/tiktoken/blob/46287bfa493f8ccca4d927386d7ea9cc20487525/tiktoken/model.py#L6-L53")
    parser.add_argument("--model", type=str, help="Model to use. Overrides --encoding. See: https://github.com/openai/tiktoken/blob/46287bfa493f8ccca4d927386d7ea9cc20487525/tiktoken/model.py#L6-L53")
    parser.add_argument("--chunk_size", type=int, default=4096, help="Chunk size. Defaults to 4096.")
    parser.add_argument("--separator", type=str, default="\n\n", help="Separator to use when joining chunks. Defaults "
                                                                    "to two newlines.")
    parser.add_argument("--json", action="store_true", help="Output as JSON.")
    parser.add_argument("--overlap", type=int, default=0, help="Overlap between chunks. Defaults to 0.")
    args = parser.parse_args()

    if args.file:
        input = Path(args.file).read_text()
    else:
        input = sys.stdin.read()

    if args.encoding:
        encoding = tiktoken.get_encoding(args.encoding)
    elif args.model:
        encoding = tiktoken.encoding_for_model(args.model)
    else:
        p("Warning: no encoding or model specified. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    encoded = encoding.encode(input)

    output = []
    overlap = args.chunk_size - (2 * args.overlap)
    if overlap <= 0:
        raise Exception("Overlap * 2 must be less than chunk size.")
    for i in range(0, len(encoded), overlap):
        start = max(0, i - args.overlap)
        end = min(len(encoded), i + args.chunk_size + args.overlap)
        encoded_chunk = encoded[start:end]
        output.append(encoding.decode(encoded_chunk))

    if args.json:
        print(json.dumps(output))
    else:
        if args.separator:
            sep = codecs.decode(args.separator, "unicode_escape")
            print(sep.join(output), end="")
        else:
            pprint(output)
