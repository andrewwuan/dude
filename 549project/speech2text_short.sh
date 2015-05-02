#!/bin/bash

#echo "Recording..."
arecord -D "plughw:1,0" -d 3 -q -f cd -t wav -r 16000 -c 1 dude.wav
flac dude.wav -f --best --sample-rate 16000 -s -o dude.flac
#echo "Uploading to Google..."
wget -q -U "Mozilla/5.0" --post-file dude.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyCNtR-Gkh4uhob8J1oxy6MtpyNn_FNs7vg" | cut -d\" -f8 > stt.txt
#echo "You just said: $(cat stt.txt)"

