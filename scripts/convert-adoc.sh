# Function to process a single file
process_file() {
    local input_file="$1"
    local base_name=$(basename "$input_file" .adoc)
    local dir_name=$(dirname "$input_file")
    local output_file="build/${dir_name}/${base_name}.html"

    # Run asciidoctor to convert the input file to HTML
    asciidoctor -a data-uri -a allow-uri-read "$input_file" -o "$output_file"
}

# Check if at least one input file is provided
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <input-file-1> [input-file-2] ..."
    exit 1
fi

# Process each file passed as an argument
for input_file in "$@"; do
    process_file "$input_file"
done