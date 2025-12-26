import pvporcupine
import pyaudio
import struct
import asyncio
import time
import queue
import numpy as np
import sounddevice as sd

from services.voice_service import speech_to_text_from_buffer, speak

# ================= CONFIG =================
ACCESS_KEY = "gzJck4CWGwlmSdI0ENDbH+XSg7FKVqZKyNBCnYQWGO5Mi6rTzfrHtQ=="

KEYWORD = "jarvis"

SAMPLE_RATE = 16000
CHANNELS = 1
FRAME_DURATION = 0.1
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION)

SILENCE_THRESHOLD = 0.01
MAX_SILENCE_TIME = 1.2
# ==========================================

audio_queue = queue.Queue()


def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())


def is_silent(frame: np.ndarray) -> bool:
    energy = np.sqrt(np.mean(frame ** 2))
    return energy < SILENCE_THRESHOLD


def record_until_silence() -> np.ndarray:
    print("🎤 Đang nghe... (nói đi, im lặng để kết thúc)")

    frames = []
    silence_start = None

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        blocksize=FRAME_SIZE,
        dtype="float32",
        callback=audio_callback
    ):
        while True:
            frame = audio_queue.get()
            frames.append(frame)

            if is_silent(frame):
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start >= MAX_SILENCE_TIME:
                    break
            else:
                silence_start = None

    return np.concatenate(frames, axis=0).squeeze()


def listen_and_transcribe():
    audio = record_until_silence()
    if audio.size < SAMPLE_RATE * 0.3:
        print("⚠️ Âm quá ngắn, bỏ qua")
        return

    text = speech_to_text_from_buffer(audio)
    print("📄 Bạn nói:", text)


def main():

    print("🎤 bắt đầu chạy")

    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keywords=[KEYWORD],
        sensitivities=[0.85]
    )

    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("🤖 Jarvis đang chờ wake word...")

    try:
        while True:
            pcm = stream.read(
                porcupine.frame_length,
                exception_on_overflow=False
            )
            pcm = struct.unpack_from(
                "h" * porcupine.frame_length,
                pcm
            )

            if porcupine.process(pcm) >= 0:
                asyncio.run(speak("Tôi xin lắng nghe"))
                listen_and_transcribe()

    except KeyboardInterrupt:
        print("🛑 Stopping...")

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()


main()