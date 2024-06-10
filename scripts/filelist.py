import yaml
import subprocess
import os

# Read the YAML content from a file
with open('./.github/workflows/asciidoc-convert-check.yml', 'r') as file:
    data = yaml.safe_load(file)

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

# Function to run a script/command against each AsciiDoc file
def process_asciidoc_file(file):
    script_path = './scripts/convert-adoc.sh'
    # Check if the script exists
    if  os.path.exists(script_path):
        print(f"Script not found: {script_path}")
        return

    # Example command: print the file name (replace with actual command)
    print(f"Processing file: {file}")
    # Replace the below line with the actual command you want to run
    subprocess.run(['./scripts/convert-adoc.sh ', file], check=True)

# Retrieve and process each AsciiDoc file
asciidoc_files = get_asciidoc_files(data)
for file in asciidoc_files:
    process_asciidoc_file(file)
