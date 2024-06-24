import subprocess
import os
import argparse

# Function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Process AsciiDoc files using a specified script.")
    parser.add_argument('script', help="Path to the script to process AsciiDoc files.")
    parser.add_argument('file_list', help="Path to the text file containing the list of AsciiDoc files.")
    return parser.parse_args()

# Function to read the list of AsciiDoc files from a text file
def read_file_list(file_list_path):
    with open(file_list_path, 'r') as file:
        files = [line.strip() for line in file if line.strip()]
    return files

# Function to run the specified script against each AsciiDoc file
def process_asciidoc_file(script, file):
    # Check if the script exists
    if not os.path.exists(script):
        print(f"Script not found: {script}")
        return
    # Execute the script with the file as an argument using bash
    result = subprocess.run(['bash', script, file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)  # Print or handle the output as needed
    if result.stderr:
        print(f"Error processing {file}: {result.stderr}")

def main():
    args = parse_args()
    asciidoc_files = read_file_list(args.file_list)
    for file in asciidoc_files:
        process_asciidoc_file(args.script, file)

if __name__ == "__main__":
    main()
