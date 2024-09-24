#!/usr/bin/with-contenv bash

# identifies the output directory from the '--output' argument
output_dir="/downloads"

# remove files in the output directory
if [ -d "$output_dir" ]; then
  echo "deleting files ending with '.0.jpg' in directory: $output_dir"
  find "$output_dir" -type f -name "*.0.jpg" -delete

  echo "deleting files ending with '.1.jpg' in directory: $output_dir"
  find "$output_dir" -type f -name "*.1.jpg" -delete

  echo "deleting files ending with '.2.jpg' in directory: $output_dir"
  find "$output_dir" -type f -name "*.2.jpg" -delete
else
  echo "output directory not found: $output_dir"
fi