#!/bin/bash

# Set the directory where you want to search for file names
directory="."

# Loop through all files in the directory
for filename in "/Users/admin/Desktop/A/*"; do
  # Check if the filename contains "2023"
  if [[ "$filename" == *2023* ]]; then
    # Replace "2023" with "2024" in the filename
    new_filename="${filename//2023/2024}"
    
    # Rename the file
    mv "$filename" "$new_filename"
    
    echo "Renamed: $filename to $new_filename"
  fi
done
