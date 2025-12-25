
from faster_whisper import WhisperModel

model = WhisperModel(
    "vinai/PhoWhisper-medium",
    device="cuda",
    compute_type="float16"
)

segments, info = model.transcribe(
    "audio.wav",
    language="vi",
    beam_size=5,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=300)
)

print("Detected language:", info.language)

text = []

for seg in segments:

    text.append(seg.text)

final_text = " ".join(text)

print(final_text)
