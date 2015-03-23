#!/bin/bash

speech_min_length=1.7
retry=1
while [ $retry -eq 1 ]
do
  rec -q dude.wav silence -l 1 0 1% 1 0.5 1% pad 1.0
  sox dude.wav -n stat 2> sox.info
  length=$(cat sox.info | grep "Length" | cut -d':' -f2)
  echo "Audio length:" $length
  retry=$(echo $length'<'$speech_min_length | bc -l)
  echo "Retry:" $retry
done

sox dude.wav -t flac -c 1 -r 16000 dude.flac
#wget -q -U "Mozilla/5.0" --post-file dude.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyCNtR-Gkh4uhob8J1oxy6MtpyNn_FNs7vg" | cut -d\" -f8 > stt.txt
#wget -q -U "Mozilla/5.0" --post-file dude.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyBhDRjJDmZ23ZvYPni8--O3dxUauAZKYvs" | cut -d\" -f8 > stt.txt
#wget -q -U "Mozilla/5.0" --post-file dude.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyAY7G3fRXOVODejFit7isph3OOvY-bmJPI" | cut -d\" -f8 > stt.txt
wget -q -U "Mozilla/5.0" --post-file dude.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyCCJMVMpF-prxcR9_vCoyhbVUsNjAqMw4w" | cut -d\" -f8 > stt.txt
