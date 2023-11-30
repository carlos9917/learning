import whisper


model = whisper.load_model("base")
audio = "/home/cperalta/Downloads/kapitalet-327-argentina-dynamisk.mp3"
#result = model.transcribe(audio)
result = model.transcribe(audio, language="sv") #sv for swedish, sw is for swahili!


with open("transcription.txt", "w", encoding="utf-8") as txt:
    txt.write(result["text"])

