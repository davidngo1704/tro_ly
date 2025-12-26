import pvporcupine
import pyaudio
import struct
import json
from vosk import Model, KaldiRecognizer
from services.my_speak_old import speak
import asyncio


ACCESS_KEY = "gzJck4CWGwlmSdI0ENDbH+XSg7FKVqZKyNBCnYQWGO5Mi6rTzfrHtQ=="


KEYWORD = "jarvis"


vosk_model = Model(r"D:\Models\VoiceDetector\vosk-model-small-vn-0.4")


rec = KaldiRecognizer(vosk_model, 16000)


def listen_command(pa):
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4000
    )

    print("🎙️ Đang nghe lệnh...")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            stream.stop_stream()
            stream.close()
            return text


# ---------- WAKE WORD ----------


def main():

    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keywords=[KEYWORD],
        sensitivities=[0.85]
    )

    pa = pyaudio.PyAudio()

    wake_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("  Jarvis  đang  chờ   wake  word  ")

    try:
        while True:

            pcm = wake_stream.read(porcupine.frame_length, exception_on_overflow=False)

            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm) >= 0:

                asyncio.run(speak("Tôi xin lắng nghe"))

                command_text = listen_command(pa)
                
                print("📄 Bạn nói:", command_text)


    except KeyboardInterrupt:
        
        print("Stopping...")

    finally:
        wake_stream.stop_stream()
        wake_stream.close()
        pa.terminate()
        porcupine.delete()

main()


