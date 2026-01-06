#!/bin/bash

# This script iterates through all JPEG files in the current directory,
# resizes them, and adjusts their quality using the 'convert' command.

# Check if the 'convert' command is available (part of ImageMagick)
if ! command -v convert &> /dev/null
then
    echo "Error: 'convert' command not found. Please install ImageMagick."
    exit 1
fi

# Create a 'converted' directory if it doesn't exist
mkdir -p converted

# Loop through all files with a .jpg extension in the current directory
for file in *.jpg; do
    # Check if a file was found to prevent errors if no .jpg files exist
    if [ -f "$file" ]; then
        # Get the base filename without the extension
        filename=$(basename -- "$file")
        filename="${filename%.*}"

        # Define the output filename with a prefix
        output_file="./converted/resized_${filename}.jpg"

        echo "Processing '$file'..."

        # Use the 'convert' command to resize and set the quality
        # The -resize 1920x will resize the image to a maximum width of 1920 pixels,
        # while maintaining the aspect ratio.
        # The -quality 85 will set the compression quality to 85.
        convert "$file" -resize 1920x -quality 85 "$output_file"

        echo "Saved resized image to '$output_file'."
    fi
done

echo "Script finished."
