# smartkitab_video_generator.py
import os
import json
import subprocess
from pathlib import Path

class SmartKitabVideoCreator:
    def __init__(self):
        self.output_file = "smartkitab_Atomic_Habits.mp4"
        self.assets_dir = "assets"
        self.temp_dir = "temp"
        self.output_dir = "output"
        self.final_audio = None

    # --------------------------------------------------
    # SETUP
    # --------------------------------------------------
    def setup_directories(self):
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def check_dependencies(self):
        print("\n🔍 Checking dependencies...")
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            print("✅ ffmpeg installed")
            return True
        except:
            print("❌ ffmpeg not found. Install using: brew install ffmpeg")
            return False

    # --------------------------------------------------
    # AUDIO (gTTS)
    # --------------------------------------------------
    def create_audio_files(self):
        print("\n🎵 Creating audio using gTTS...")

        script_parts = [
            "Socho agar tum roz sirf one percent better ho jao.",
            "Gym nahi, motivation nahi, bas thoda sa improvement.",
            "Saal ke end tak tum bilkul different person ban jaoge.",
            "Yahi idea hai Atomic Habits ka.",
            "Chhoti habits compound hoti hain.",
            "Goals se zyada systems matter karte hain.",
            "Consistency motivation se zyada powerful hoti hai.",
            "SmartKitab ko subscribe karo."
        ]

        try:
            from gtts import gTTS
        except ImportError:
            print("❌ gTTS missing. Run: pip install gtts")
            return False

        audio_files = []
        for i, text in enumerate(script_parts, 1):
            path = os.path.join(self.temp_dir, f"scene_{i}.mp3")
            gTTS(text=text, lang="hi").save(path)
            audio_files.append(path)
            print(f"  Created: {path}")

        self.combine_audio(audio_files)
        return True

    def combine_audio(self, files):
        print("\n🔊 Combining audio files...")
        list_file = os.path.join(self.temp_dir, "audio_list.txt")

        with open(list_file, "w") as f:
            for file in files:
                f.write(f"file '{os.path.abspath(file)}'\n")

        output = os.path.join(self.temp_dir, "final_audio.mp3")
        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", list_file, "-c", "copy", output, "-y"
        ]

        subprocess.run(cmd, check=True)
        self.final_audio = output
        print("✅ Audio combined")

    # --------------------------------------------------
    # VIDEO (MoviePy + PIL, macOS SAFE)
    # --------------------------------------------------
    def create_video_with_moviepy(self):
        print("\n🎬 Creating video using MoviePy (macOS safe)...")

        try:
            from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            print("❌ Required libs missing. Run: pip install moviepy pillow")
            return False

        texts = [
            "ATOMIC HABITS",
            "1% Better Every Day",
            "Systems > Goals",
            "Identity Builds Habits",
            "Consistency > Motivation",
            "Small Habits = Big Results",
            "Take Action Today",
            "Subscribe to SmartKitab"
        ]

        clips = []

        for i, text in enumerate(texts):
            img = Image.new("RGB", (1920, 1080), (15, 23, 42))
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype(
                    "/System/Library/Fonts/Supplemental/Arial Bold.ttf", 100
                )
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), text, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

            draw.text(
                ((1920 - w) / 2, (1080 - h) / 2),
                text,
                fill=(255, 204, 0) if i % 2 == 0 else (255, 255, 255),
                font=font
            )

            frame_path = os.path.join(self.temp_dir, f"frame_{i}.png")
            img.save(frame_path)

            clip = ImageClip(frame_path).set_duration(5)
            clips.append(clip)

        final_video = concatenate_videoclips(clips, method="compose")

        if self.final_audio:
            audio = AudioFileClip(self.final_audio)
            final_video = final_video.set_audio(audio)

        output_path = os.path.join(self.output_dir, self.output_file)
        final_video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        print(f"🎉 Video created: {output_path}")
        return True

    # --------------------------------------------------
    # YOUTUBE METADATA
    # --------------------------------------------------
    def generate_youtube_metadata(self):
        print("\n📝 Generating YouTube metadata...")

        metadata = {
            "title": "Atomic Habits Explained in Hinglish | SmartKitab",
            "description": (
                "Atomic Habits explained in simple Hinglish.\n\n"
                "Learn how small habits create massive results.\n\n"
                "Subscribe to SmartKitab for more book summaries!"
            ),
            "tags": [
                "Atomic Habits", "James Clear", "Hinglish",
                "Self Improvement", "SmartKitab"
            ],
            "category": "27"
        }

        path = os.path.join(self.output_dir, "youtube_metadata.json")
        with open(path, "w") as f:
            json.dump(metadata, f, indent=2)

        print("✅ Metadata saved")

    # --------------------------------------------------
    # CLEANUP
    # --------------------------------------------------
    def cleanup(self):
        print("\n🧹 Cleaning temp files...")
        for f in Path(self.temp_dir).glob("*"):
            f.unlink()
        print("✅ Cleanup done")

    # --------------------------------------------------
    # RUN
    # --------------------------------------------------
    def run(self):
        print("\n" + "=" * 60)
        print("SMARTKITAB VIDEO GENERATOR")
        print("=" * 60)

        self.setup_directories()

        if not self.check_dependencies():
            return

        if not self.create_audio_files():
            return

        if not self.create_video_with_moviepy():
            return

        self.generate_youtube_metadata()
        self.cleanup()

        print("\n🎯 DONE!")
        print("📁 Check the output folder")
        print("🚀 Ready for YouTube upload!")


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    creator = SmartKitabVideoCreator()
    creator.run()
