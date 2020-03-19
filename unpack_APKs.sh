#!/bin/bash

# Auth: Paul Franklin

# If no CLI args are provided, the script works from its current directory on an APK directory called APK_DIR
# If 1 CLI arg is provided, the script works from the provided directory on an APK directory called APK_DIR
# If 2 CLI args are provided, the script works from the arg-1 directory on an APK directory provided by arg-2 relative to arg-1

###############################################

# Working directories
APK_DIR="./APK_DIR"
PROCESSING_DIR="./UNPACKED_DIR"

###############################################

# CD to root working directory if CLI arg 1 exists
if [ ! -z "$1" ]; then
	cd "$1"
fi

# Set the APK_DIR if CLI arg 2 exists
if [ ! -z "$2" ]; then
	APK_DIR="$2"
fi

###############################################

# Create list of all APKs in the APK directory
APK_LIST=$(ls -1 $APK_DIR | grep -i ".apk")

# Command to access apktool
if [ $(uname -a | grep -i "Linux" | wc -l) -gt 0 ]; then
	# Linux
	APKTOOL="apktool"
elif [ $(uname -a | grep -i "NT" | wc -l) -gt 0 ]; then
	# Windows
	APKTOOL="apktool.bat"
else
	# MAC
	APKTOOL="apktool"
fi

###############################################

# Make processing directory
mkdir $PROCESSING_DIR

# Process
for APK in $APK_LIST; do
	# Unpack
	$APKTOOL d $APK_DIR/$APK -o $PROCESSING_DIR/$APK -q
done
