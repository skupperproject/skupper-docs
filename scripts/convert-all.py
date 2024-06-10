import yaml
import subprocess
import os
import argparse

# Function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Process AsciiDoc files using a specified script.")
    parser.add_argument('script', help="Path to the script to process AsciiDoc files.")
    parser.add_argument('yaml_file', help="Path to the YAML file containing the list of AsciiDoc files.")
    return parser.parse_args()

# Function to read the YAML content from a file
def read_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

# Function to retrieve AsciiDoc files list
def get_asciidoc_files(data):
    asciidoc_files = []
    # Navigate through the nested dictionary to find the 'files' list
    for job_name, job_details in data.get('jobs', {}).items():
        steps = job_details.get('steps', [])
        for step in steps:
            if step.get('name') == 'Convert specified AsciiDoc files to HTML':
                run_content = step.get('run', '')
                if 'files=(' in run_content:
                    start = run_content.find('files=(') + len('files=(')
                    end = run_content.find(')', start)
                    files_list = run_content[start:end].strip().split('\n')
                    # Clean and add the files to the list
                    for file in files_list:
                        clean_file = file.strip().strip('"')
                        if clean_file:
                            asciidoc_files.append(clean_file)
    return asciidoc_files

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
    data = read_yaml(args.yaml_file)
    asciidoc_files = get_asciidoc_files(data)
    for file in asciidoc_files:
        process_asciidoc_file(args.script, file)

if __name__ == "__main__":
    main()
