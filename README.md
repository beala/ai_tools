# transcribe_podcast.py

This script allows you to transcribe podcast episodes from Overcast.fm using OpenAI's GPT-4. The resulting transcript can be saved to an output file or printed to stdout.

## Dependencies
Install the required dependencies using:

```
pip install -r requirements.txt
```

## Usage

```
usage: transcribe_podcast.py [-h] [--output OUTPUT] [--tmp TMP] [--preserve] [--silent] [--dry_run] OVERCAST_LINK

positional arguments:
  OVERCAST_LINK    Overcast link to podcast episode (eg https://overcast.fm/+YsPQCIdOs)

options:
  -h, --help       show this help message and exit
  --output OUTPUT  Output file to write transcript to. Otherwise, prints to stdout.
  --tmp TMP        Temporary directory to use for downloading and chunking audio. Defaults to a new temporary directory.
  --preserve       Preserve temporary directory after running. Defaults to False.
  --silent         Silence all status updates. Defaults to False.
  --dry_run        Don't actually query OpenAI. Useful for debugging. Defaults to False.

```

### Arguments

- `OVERCAST_LINK`: The Overcast link to the podcast episode you want to transcribe (e.g., https://overcast.fm/+YsPQCIdOs).

### Options

- `--output`: The output file to write the transcript to. If not provided, the transcript will be printed to stdout.
- `--tmp`: The temporary directory to use for downloading and chunking audio. If not provided, a new temporary directory will be created.
- `--preserve`: Keep the temporary directory after running. By default, the temporary directory will be removed.
- `--silent`: Silence all status updates. By default, status updates will be printed.
- `--dry_run`: Don't actually query OpenAI. Useful for debugging. By default, OpenAI will be queried.

## Example

```
python transcribe_podcast.py https://overcast.fm/+YsPQCIdOs --output transcript.txt
```

This will transcribe the podcast episode from the provided Overcast link and save the transcript to a file named `transcript.txt`.

# chunk.py

This script encodes and chunks text using TikToken encodings, which are useful for processing large text files that need to be divided into smaller pieces. This can be helpful when working with APIs that have token or character limits.

See the OpenAI docs for token limits: https://platform.openai.com/docs/models/gpt-3-5

## Features

- Read input from file or standard input (stdin)
- Supports various encodings provided by TikToken
- Customizable chunk size and overlap between chunks
- Output in JSON format or plain text with a custom separator
- Select encoding based on model name

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
                        Separator to use when joining chunks. Defaults to newline.
  --json                Output as JSON.
  --overlap OVERLAP     Overlap between chunks. Defaults to 0.

```

## Example

```
python chunk.py --file input.txt --model gpt-3.5-turbo --chunk_size 1024 --separator "\n\n"
```

This command will read the input from `input.txt`, divide it into chunks of 1024 tokens with no overlap, and output the result separated by two newline characters.

## Dependencies

Install the required dependencies using:

```
pip install -r requirements.txt
```