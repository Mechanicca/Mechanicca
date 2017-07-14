#! /bin/sh
# Purpose: Prepare CMake build for current project
# Author: Martin Kopecky <martin.monster696@gmail.com> 

DIRECTORY=Build

if [ ! -d "$DIRECTORY" ]; then
	echo "Making build directory..."
	mkdir ./$DIRECTORY
	echo "done"
fi

echo "Configuring CMake build"
cd ./$DIRECTORY && cmake ../