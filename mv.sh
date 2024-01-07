#!/bin/bash

# Navigate to the 'modules' directory
cd modules

# Loop through each directory in 'modules'
for dir in */; do
    # Navigate into the directory
    cd "$dir"

    # Check if 'pages' subdirectory exists
    if [ -d "pages" ]; then
        # Move all files from 'pages' to the parent directory (one level up)
        mv pages/* .

        # Remove the 'pages' directory
        rmdir pages
    fi

    # Navigate back to the 'modules' directory
    cd ..

    # Move the directory to the parent directory (one level up)
    mv "$dir" ..
done

# Return to the original directory
cd ..