#!/bin/bash

#echo "Recording..."
arecord -D "plughw:1,0" -d 3 -q -f cd -t wav -r 16000 -c 1 teddy.wav
flac teddy.wav -f --best --sample-rate 16000 -s -o teddy.flac
#echo "Uploading to Google..."
#wget -q -U "Mozilla/5.0" --post-file teddy.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyCCJMVMpF-prxcR9_vCoyhbVUsNjAqMw4w" | cut -d\" -f8 > stt.txt
wget -q -U "Mozilla/5.0" --post-file teddy.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyB9p1nB1JodqUUHWuhBs7ls3RmPYEjsDSE" | cut -d\" -f8 > stt.txt
#echo "You just said: $(cat stt.txt)"

