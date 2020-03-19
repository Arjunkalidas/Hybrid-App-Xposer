#!/bin/bash

LOG_DIR="./LOG_DIR"
APK_LOG_DIRS=$(find ./LOG_DIR -type d | grep -i ".apk")
JS_PATH_LOG="JavaScript_Paths.txt"
FOUND_API_LOG="Found_APIs_JS.txt"
UNSAFE_APIS=("document.write" "document.writeln" ".innerHTML" ".outerHTML" ".html(" ".append(" ".prepend(" ".before(" ".after(" ".replaceAll(" ".replaceWith(")
UNSAFE_APK_LOG="APKs_With_Unsafe_JS.txt"

# Start the log file for unsafe APKs
echo "" > $LOG_DIR/*/$UNSAFE_APK_LOG

for APK_LOG_DIR in $APK_LOG_DIRS; do
	# Assume the APK is unsafe
	UNSAFE=$(false)

	# Start the log files for unsafe APIs found in JS files
	echo "" > $APK_LOG_DIR/$FOUND_API_LOG

	# For each file path in the source of JS file found
	for FILE_PATH in $(cat $APK_LOG_DIR/$JS_PATH_LOG); do
		# Log the file path
		echo $FILE_PATH >> $APK_LOG_DIR/$FOUND_API_LOG
		
		: '
		LINE_COUNT=$(python ./Karthik/JSParser.py $FILE_PATH | wc -l)
		if [ $LINE_COUNT -gt 0 ]; then
			# Set the APK-level predicate to true
			UNSAFE=true

			# Log the lines found for the unsafe APIs
			python ./Karthik/JSParser.py $FILE_PATH >> $APK_LOG_DIR/$FOUND_API_LOG
		else
			# If no lines found, log not found
			echo "Not Found" >> $APK_LOG_DIR/$FOUND_API_LOG
		fi
		echo -e "\n" >> $APK_LOG_DIR/$FOUND_API_LOG
		'
		# For each unsafe API
		for UNSAFE_API in ${UNSAFE_APIS[@]}; do
			# Log the unsafe API being checked
			echo $UNSAFE_API >> $APK_LOG_DIR/$FOUND_API_LOG

			# Count the number of lines found
			LINE_COUNT=$(grep -nh $FILE_PATH -e $UNSAFE_API | wc -l)

			# If there are lines, then the unsafe API was found
			if [ $LINE_COUNT -gt 0 ]; then
				# Set the APK-level predicate to true
				UNSAFE=true

				# Log the lines found for the unsafe API
				#grep -nh $FILE_PATH -e $UNSAFE_API >> $APK_LOG_DIR/$FOUND_API_LOG
				python ./API_Analyzer/JSParser_v4.0.0.py "$FILE_PATH" "$UNSAFE_API" >> $APK_LOG_DIR/$FOUND_API_LOG
			else
				# If no lines found, log not found
				echo "Not Found" >> $APK_LOG_DIR/$FOUND_API_LOG
			fi
			# Log an empty line before checking the next unsafe API
			echo -e "\n" >> $APK_LOG_DIR/$FOUND_API_LOG
		done
	done

	# Log if the APK was unsafe
	if [ $UNSAFE ]; then
		echo $APK_LOG_DIR >> $APK_LOG_DIR/../$UNSAFE_APK_LOG
	fi
done
