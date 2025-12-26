import asyncio
import edge_tts
import os
import sounddevice as sd
import soundfile as sf

async def speak(prompt):

    output = "speak.wav"

    communicate = edge_tts.Communicate(
        text=prompt,
        voice="vi-VN-HoaiMyNeural"
    )

    await communicate.save(output)

    data, samplerate = sf.read(output, dtype="float32")
    sd.play(data, samplerate)
    sd.wait()

    os.remove(output)

