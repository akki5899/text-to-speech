# =========================================================
# Pillow 10+ FIX (MoviePy compatibility)
# =========================================================
from PIL import Image
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# =========================================================
# IMPORTS
# =========================================================
import os
import numpy as np
from gtts import gTTS
from pydub import AudioSegment
from moviepy.editor import VideoClip, AudioFileClip
from PIL import ImageDraw

# =========================================================
# CONFIG
# =========================================================
OUTPUT_DIR = "output"
AUDIO_FILE = "speech.mp3"
VIDEO_FILE = os.path.join(OUTPUT_DIR, "smartkitab_mouth_synced.mp4")
FPS = 24

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# STEP 1: CREATE AUDIO
# =========================================================
print("🎵 Creating audio...")

script = (
    "Socho agar tum roz sirf one percent better ho jao. "
    "Small habits compound hoti hain. "
    "Consistency motivation se zyada powerful hoti hai. "
    "Atomic Habits ka yehi secret hai. "
    "Subscribe to SmartKitab."
)

gTTS(text=script, lang="hi", slow=False).save(AUDIO_FILE)

# =========================================================
# STEP 2: LOAD AUDIO SAFELY (PYDUB)
# =========================================================
print("📊 Analyzing audio amplitude (safe method)...")

audio_seg = AudioSegment.from_mp3(AUDIO_FILE)

# Convert to mono
audio_seg = audio_seg.set_channels(1)

samples = np.array(audio_seg.get_array_of_samples()).astype(np.float32)

# Normalize
samples /= np.max(np.abs(samples)) + 1e-6

# Downsample amplitude to FPS
samples_per_frame = int(audio_seg.frame_rate / FPS)
amplitude = [
    np.mean(np.abs(samples[i:i + samples_per_frame]))
    for i in range(0, len(samples), samples_per_frame)
]

# =========================================================
# STEP 3: FRAME GENERATOR (MOUTH SYNCED)
# =========================================================
def make_frame(t):
    idx = min(int(t * FPS), len(amplitude) - 1)
    amp = amplitude[idx]

    img = Image.new("RGB", (1280, 720), (15, 23, 42))
    d = ImageDraw.Draw(img)

    # HEAD
    d.ellipse([500, 120, 780, 400], fill="#FFD966", outline="black", width=3)

    # EYES
    d.ellipse([570, 210, 590, 230], fill="black")
    d.ellipse([690, 210, 710, 230], fill="black")

    # MOUTH (REAL AUDIO SYNC)
    mouth_open = int(amp * 50)

    if mouth_open < 6:
        d.line([610, 300, 670, 300], fill="black", width=4)
    else:
        d.ellipse([610, 300, 670, 300 + mouth_open], fill="black")

    # BODY
    d.rectangle([630, 400, 650, 560], fill="#4A90E2")

    # BRANDING
    d.text((40, 40), "SmartKitab", fill=(255, 204, 0))

    return np.array(img)

# =========================================================
# STEP 4: CREATE VIDEO
# =========================================================
print("🎬 Rendering video...")

audio_clip = AudioFileClip(AUDIO_FILE)
duration = audio_clip.duration

video = VideoClip(make_frame, duration=duration)
video = video.set_audio(audio_clip)

video.write_videofile(
    VIDEO_FILE,
    fps=FPS,
    codec="libx264",
    audio_codec="aac"
)

print("\n🎉 DONE!")
print("📁 Output video:", os.path.abspath(VIDEO_FILE))
