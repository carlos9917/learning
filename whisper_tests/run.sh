#whisper.exe demo.mp4 --model medium --language 'Chinese' --output_format txt --task transcribe
audio="/home/cperalta/Downloads/kapitalet-327-argentina-dynamisk.mp3"
audio="/home/cperalta/antilop_149.mp3"
audio="/home/cperalta/Downloads/program_torsdag_7_december_2023_20231207_1536137199.mp3"
audio="/home/cperalta/Downloads/program_onsdag_6_december_2023_20231206_1429503442.mp3"
audio="/home/cperalta/Downloads/program_fredag_8_december_2023_20231208_1606000615.mp3"
whisper $audio --language=Swedish --output_format txt --task transcribe



