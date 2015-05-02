#!/bin/bash

#echo "Recording..."
arecord -D "plughw:1,0" -d 5 -q -f cd -t wav -r 16000 | flac - -f --best --sample-rate 16000 -s -o request.flac
#echo "Uploading to Google..."
wget -q -U "Mozilla/5.0" --post-file request.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyBhDRjJDmZ23ZvYPni8--O3dxUauAZKYvs" | cut -d\" -f8 > stt.txt
#echo "You just said: $(cat stt.txt)"

