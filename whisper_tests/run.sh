#whisper.exe demo.mp4 --model medium --language 'Chinese' --output_format txt --task transcribe
audio="/home/cperalta/Downloads/kapitalet-327-argentina-dynamisk.mp3"
whisper $audio --language=Swedish --output_format txt --task transcribe



