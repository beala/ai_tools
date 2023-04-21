This repo contains scripts and tools that are useful for interacting with OpenAI APIs.

# transcribe_podcast.py

This script allows you to transcribe podcast episodes from Overcast.fm using OpenAI's GPT-4. The resulting transcript is printed to stdout.

## Setup
Install the required dependencies using:

```
pip install -r requirements.txt
```

Do one of the following with your OpenAI API key:
- Set the `OPENAI_API_KEY` environment variable to your OpenAI API key.
- Store it to a file called `OPENAI_API_KEY` in the same directory as `transcribe_podcast.py`.

## Usage

```
usage: transcribe_podcast.py [-h] [--output OUTPUT] [--tmp TMP] [--preserve] [--silent] [--dry_run] OVERCAST_LINK

positional arguments:
  OVERCAST_LINK    Overcast link to podcast episode (eg https://overcast.fm/+YsPQCIdOs)

options:
  -h, --help       show this help message and exit
  --tmp TMP        Temporary directory to use for downloading and chunking audio. Defaults to a new temporary directory.
  --preserve       Preserve temporary directory after running. Defaults to False.
  --silent         Silence all status updates. Defaults to False.
  --dry_run        Don't actually query OpenAI. Useful for debugging. Defaults to False.

```

## Example

```
python transcribe_podcast.py https://overcast.fm/+YsPQCIdOs
```

This will transcribe the podcast episode from the provided Overcast link and print it to stdout.

# chunk.py

This script encodes and chunks text using TikToken encodings, which are useful for processing large text files that need to be divided into smaller pieces. This can be helpful when working with APIs that have token limits.

See the OpenAI docs for token limits: https://platform.openai.com/docs/models/gpt-3-5

## Setup

Install the required dependencies using:

```
pip install -r requirements.txt
```

## Usage

```
usage: chunk.py [-h] [--file FILE] [--encoding ENCODING] [--model MODEL] [--chunk_size CHUNK_SIZE] [--separator SEPARATOR] [--json] [--overlap OVERLAP]

options:
  -h, --help            show this help message and exit
  --file FILE           File to read. Otherwise, stdin is used.
  --encoding ENCODING   Encoding to use. See: https://github.com/openai/tiktoken/blob/46287bfa493f8ccca4d927386d7ea9cc20487525/tiktoken/model.py#L6-L53
  --model MODEL         Model to use. Overrides --encoding. See: https://github.com/openai/tiktoken/blob/46287bfa493f8ccca4d927386d7ea9cc20487525/tiktoken/model.py#L6-L53
  --chunk_size CHUNK_SIZE
                        Chunk size. Defaults to 4,096.
  --separator SEPARATOR
                        Separator to use when joining chunks. Defaults to two newlines.
  --json                Output as JSON.
  --overlap OVERLAP     Overlap between chunks. Defaults to 0.

```

## Example

```
python chunk.py --file input.txt --model gpt-3.5-turbo --chunk_size 1024 --separator "\n\n"
```

This command will read the input from `input.txt`, divide it into chunks of 1024 tokens with no overlap, and output the result separated by two newline characters.
