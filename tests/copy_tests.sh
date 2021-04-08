#!/usr/bin/env bash

#
# Copy the file or directory into each sub-directory
# Run this from the parent directory of all student repository directories.
# Expects a command line argument for the path to the test directory to copy into each repository
#

# expect the test file path as a command line argument
COPY_FILEPATH=$1


for i in *
    do                 # Line breaks are important
        if [ -d "$i" ]   # Spaces are important
            then
                echo "$i"
                cp -r $COPY_FILEPATH "$i"
        fi
    done
