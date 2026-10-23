# =========================================================
# Pillow 10+ FIX (MUST BE AT TOP, BEFORE MOVIEPY IMPORTS)
# =========================================================
from PIL import Image

# MoviePy still expects Image.ANTIALIAS (removed in Pillow 10)
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# =========================================================
# IMPORTS
# =========================================================
import os
import subprocess
from pathlib import Path

# =========================================================
# CONFIG
# =========================================================
OUTPUT_DIR = "output"
TEMP_DIR = "temp"
ASSETS_DIR = "assets"
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "smartkitab_avatar.mp4")

# =========================================================
# HELPERS
# =========================================================
def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)

# =========================================================
# SETUP
# =========================================================
def setup_dirs():
    for d in [OUTPUT_DIR, TEMP_DIR, ASSETS_DIR]:
        os.makedirs(d, exist_ok=True)

def check_ffmpeg():
    try:
        run(["ffmpeg", "-version"])
        print("✅ ffmpeg OK")
        return True
    except:
        print("❌ ffmpeg missing → brew install ffmpeg")
        return False

# =========================================================
# AUDIO (gTTS)
# =========================================================
def create_audio():
    print("🎵 Creating audio...")
    from gtts import gTTS

    script = (
        "Socho agar tum roz sirf one percent better ho jao. "
        "Small habits compound hoti hain. "
        "Consistency motivation se zyada powerful hoti hai. "
        "Atomic Habits ka yehi secret hai. "
        "Subscribe to SmartKitab."
    )

    audio_path = os.path.join(TEMP_DIR, "audio.mp3")
    gTTS(text=script, lang="hi").save(audio_path)
    return audio_path

# =========================================================
# AVATAR FRAMES (PIL)
# =========================================================
def create_avatar_frames():
    print("🎨 Creating avatar frames...")
    from PIL import ImageDraw

    frames = []
    for i in range(24):
        img = Image.new("RGBA", (400, 600), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)

        # Head
        d.ellipse([100, 40, 300, 240], fill="#FFD966", outline="black", width=3)

        # Eyes
        d.ellipse([150, 120, 170, 140], fill="black")
        d.ellipse([230, 120, 250, 140], fill="black")

        # Mouth animation (talking illusion)
        if i % 2 == 0:
            d.ellipse([180, 175, 220, 195], fill="black")
        else:
            d.line([180, 185, 220, 185], fill="black", width=4)

        # Body
        d.rectangle([170, 240, 230, 430], fill="#4A90E2")

        path = os.path.join(ASSETS_DIR, f"avatar_{i:03d}.png")
        img.save(path)
        frames.append(path)

    return frames

# =========================================================
# VIDEO (MoviePy + PIL)
# =========================================================
def create_video(audio_path, avatar_frames):
    print("🎬 Creating video...")
    from moviepy.editor import (
    ImageClip,
    ImageSequenceClip,
    AudioFileClip,
    CompositeVideoClip
    )
    from PIL import ImageDraw, ImageFont

    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # Background
    bg_img = Image.new("RGB", (1920, 1080), (15, 23, 42))
    bg_path = os.path.join(TEMP_DIR, "bg.png")
    bg_img.save(bg_path)
    bg_clip = ImageClip(bg_path).set_duration(duration)

    # Avatar animation
    avatar_anim = (
        ImageSequenceClip(avatar_frames, fps=8)
        .resize(0.6)
        .set_position(("right", "bottom"))
        .set_duration(duration)
    )

    # Text overlay using PIL (NO TextClip)
    text_img = Image.new("RGBA", (1600, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(text_img)

    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf", 80
        )
    except:
        font = ImageFont.load_default()

    title = "ATOMIC HABITS\nSmall Changes = Big Results"
    d.multiline_text(
        (200, 80),
        title,
        fill=(255, 204, 0),
        font=font,
        align="center"
    )

    text_path = os.path.join(TEMP_DIR, "text.png")
    text_img.save(text_path)

    text_clip = (
        ImageClip(text_path)
        .set_duration(duration)
        .set_position(("center", "top"))
    )

    final = CompositeVideoClip([bg_clip, text_clip, avatar_anim])
    final = final.set_audio(audio)

    final.write_videofile(
        FINAL_VIDEO,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

# =========================================================
# MAIN
# =========================================================
def main():
    print("=" * 50)
    print("SMARTKITAB AVATAR VIDEO (PYTHON)")
    print("=" * 50)

    setup_dirs()

    if not check_ffmpeg():
        return

    audio = create_audio()
    frames = create_avatar_frames()
    create_video(audio, frames)

    print("\n🎉 DONE!")
    print(f"📁 Output video: {os.path.abspath(FINAL_VIDEO)}")

if __name__ == "__main__":
    main()
