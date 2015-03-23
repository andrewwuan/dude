#!/bin/bash

#rec -q request.wav silence -l 0 1 0.5 1%  reverse silence -l 0 1 0.5 1% reverse
rec -q request.wav silence -l 1 0 1% 1 0.5 1% pad 1.0
sox request.wav -t flac -c 1 -r 16000 request.flac
wget -q -U "Mozilla/5.0" --post-file request.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyCNtR-Gkh4uhob8J1oxy6MtpyNn_FNs7vg" | cut -d\" -f8 > stt.txt
