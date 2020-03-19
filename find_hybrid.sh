#!/bin/bash

# Auth: Paul Franklin

# If no CLI args are provided, the script works from its current directory
# If 1 CLI arg is provided, the script works from the provided directory path

###############################################

# Working directories
LOG_DIR="./LOG_DIR"
PROCESSING_DIR="./UNPACKED_DIR"

# Log file names
FOUND_HYBRID_LOG="FOUND_HYBRID.txt"
FOUND_NATIVE_LOG="FOUND_NATIVE.txt"
HTML_PATH_LOG="HTML_Paths.txt"
JS_PATH_LOG="JavaScript_Paths.txt"

###############################################

# CD to root working directory if CLI arg 1 exists
if [ ! -z "$1" ]; then
	cd "$1"
fi

###############################################

# Create list of all APKs in the APK directory
APK_LIST=$(ls -1 $PROCESSING_DIR)

# Create a timestamp for logs produced from this run
LOG_TIMESTAMP_DIR="$(date +%Y-%m-%d--%H-%M-%S)"

###############################################

# Make log parent directory if does not exist
# Create log directory for this run
mkdir -p $LOG_DIR/$LOG_TIMESTAMP_DIR

# Process
for APK in $APK_LIST; do
	# If contains html files, then hybrid
	if [ $(find $PROCESSING_DIR/$APK -iname "*.html" | wc -l) -gt 0 ]; then
		# Log hybrid APKs
		echo $APK >> $LOG_DIR/$LOG_TIMESTAMP_DIR/$FOUND_HYBRID_LOG

		mkdir -p $LOG_DIR/$LOG_TIMESTAMP_DIR/$APK
		# Log location of HTML files
		find $PROCESSING_DIR/$APK -iname "*.html" > $LOG_DIR/$LOG_TIMESTAMP_DIR/$APK/$HTML_PATH_LOG
		# Log location of JavaScript files
		find $PROCESSING_DIR/$APK -iname "*.js" > $LOG_DIR/$LOG_TIMESTAMP_DIR/$APK/$JS_PATH_LOG
	else
		# Log native APKs
		echo $APK >> $LOG_DIR/$LOG_TIMESTAMP_DIR/$FOUND_NATIVE_LOG
	fi
done
