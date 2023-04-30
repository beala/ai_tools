#!/usr/bin/env bash

if [[ -f venv/bin/activate ]]; then
  source venv/bin/activate
fi

get_webpage_title_as_filename() {
  local url="$1"

  # Use curl to fetch the webpage, awk to extract the title, sed to remove HTML tags,
  # and tr to replace non-alphanumeric characters with underscores
  local title=$(curl -s "$url" | \
                awk -F'<title>|</title>' '/<title>/ {print $2}' | \
                sed 's/<[^>]*>//g' | \
                tr -c '[:alnum:]' '_')

  echo "$title"
}

filename=$(get_webpage_title_as_filename "$1")

python transcribe_podcast.py "$1" |\
    tee "${filename}.txt" |\
    python summarize.py |\
    tee "${filename}_summary.txt"