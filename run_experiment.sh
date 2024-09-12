#!/bin/bash

# Run fetch_and_save.py to fetch articles and save them as PDFs
echo "Running fetch_and_save.py..."
python3 source/fetch_and_save.py

# Check if fetch_and_save.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: fetch_and_save.py failed."
    exit 1
fi

# Run merge.py to merge PDFs by category
echo "Running merge.py..."
python3 source/merge.py

# Check if merge.py ran successfully
if [ $? -ne 0 ]; then
    echo "Error: merge.py failed."
    exit 1
fi

echo "Experiment completed successfully."
