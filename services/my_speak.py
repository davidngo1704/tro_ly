import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import time

OUTPUT_FILE = "test_prompt.wav"
SAMPLE_RATE = 16000
CHANNELS = 1

FRAME_DURATION = 0.1          # 100ms
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION)

SILENCE_THRESHOLD = 0.01      # chỉnh nếu mic nhạy / yếu
MAX_SILENCE_TIME = 1.2        # im lặng 1.2s thì dừng

audio_queue = queue.Queue()
recorded_frames = []


def audio_callback(indata, frames, time_info, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())


def is_silent(frame):
    energy = np.sqrt(np.mean(frame ** 2))
    return energy < SILENCE_THRESHOLD


def record_until_silence():
    print("🎤 Đang lắng nghe... (nói đi, dừng khi bạn im lặng)")

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
            recorded_frames.append(frame)

            if is_silent(frame):
                if silence_start is None:
                    silence_start = time.time()
                elif time.time() - silence_start >= MAX_SILENCE_TIME:
                    print("⏹️  Phát hiện im lặng, kết thúc thu.")
                    break
            else:
                silence_start = None

    audio = np.concatenate(recorded_frames, axis=0)
    return audio


def normalize(audio):
    peak = np.max(np.abs(audio))
    if peak < 1e-6:
        print("⚠️ Âm lượng quá nhỏ.")
        return audio
    return audio / peak * 0.9


def save_wav(audio):
    audio = normalize(audio)
    sf.write(OUTPUT_FILE, audio, SAMPLE_RATE, subtype="PCM_16")
    print(f"💾 Đã lưu file: {OUTPUT_FILE}")


if __name__ == "__main__":
    audio = record_until_silence()
    save_wav(audio)
