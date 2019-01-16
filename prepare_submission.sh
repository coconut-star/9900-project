#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Usage: $0 bitbucket_login"
	exit 1
fi
# Pull the project from BitBucket.
git clone ssh://${1}@bitbucket.org/katspk/rusauscny.git
cd rusauscny
# Rename to skillstash
mv prototype skillstash
# Remove some files that we don't want to submit.
cd skillstash
rm -r documentation
rm readme_unwrapped.txt
cd ..
# Create the compressed archive.
tar -cvzf project.tgz skillstash
cd ..
mv rusauscny/project.tgz .
# Remove the project directory
rm -rf rusauscny
