import sounddevice as sd
import soundfile as sf
import numpy as np

OUTPUT_FILE = "test_prompt.wav"
SAMPLE_RATE = 16000
CHANNELS = 1
DURATION = 5  # thu đúng 5 giây

def record_5_seconds():
    print("🎤 Bắt đầu thu âm 5 giây...")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    )
    sd.wait()

    print("⏹️  Thu xong.")
    return audio


def normalize(audio):
    peak = np.max(np.abs(audio))
    if peak < 1e-6:
        print("⚠️ Âm lượng quá nhỏ, mic có thể chưa đúng.")
        return audio
    return audio / peak * 0.9  # tránh clipping


def save_wav(audio):
    audio = normalize(audio)

    sf.write(
        OUTPUT_FILE,
        audio,
        SAMPLE_RATE,
        subtype="PCM_16"
    )
    print(f"💾 Đã lưu file: {OUTPUT_FILE}")


if __name__ == "__main__":
    audio = record_5_seconds()
    save_wav(audio)
