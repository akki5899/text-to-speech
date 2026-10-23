# avatar.py — Interactive multi-method avatar video generator
from PIL import Image
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

import os
import json
import subprocess
from pathlib import Path
import random

class SmartKitabAvatarVideo:
    def __init__(self):
        self.output_dir = "output"
        self.temp_dir = "temp_avatar"
        self.assets_dir = "avatar_assets"
        self.final_video = os.path.join(self.output_dir, "smartkitab_with_avatar.mp4")
        
    def setup_directories(self):
        """Create necessary directories"""
        for dir_path in [self.output_dir, self.temp_dir, self.assets_dir]:
            os.makedirs(dir_path, exist_ok=True)
        print("✅ Directories created")
    
    def check_dependencies(self):
        """Check required tools"""
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            print("✅ FFmpeg is installed")
            return True
        except:
            print("❌ Install FFmpeg first!")
            return False
    
    def create_avatar_assets(self):
        """Create or download avatar assets"""
        print("\n🎨 Creating avatar assets...")
        
        # Create avatar animation frames using PIL
        try:
            from PIL import Image, ImageDraw
            import numpy as np
            
            # Create different avatar poses
            poses = ['thinking', 'explaining', 'pointing', 'smiling']
            
            for pose in poses:
                for frame in range(10):  # 10 frames per pose
                    img = Image.new('RGBA', (400, 600), (0, 0, 0, 0))
                    draw = ImageDraw.Draw(img)
                    
                    # Draw avatar body (simplified character)
                    # Head
                    draw.ellipse([150, 50, 250, 150], fill='#FFD700', outline='black', width=2)
                    
                    # Eyes
                    eye_y = 90
                    if pose == 'thinking':
                        # Thinking pose: looking up
                        draw.ellipse([170, eye_y-5, 185, eye_y+10], fill='black')
                        draw.ellipse([215, eye_y-5, 230, eye_y+10], fill='black')
                    elif pose == 'explaining':
                        # Explaining: normal eyes
                        draw.ellipse([170, eye_y, 185, eye_y+15], fill='black')
                        draw.ellipse([215, eye_y, 230, eye_y+15], fill='black')
                    elif pose == 'pointing':
                        # Pointing: determined look
                        draw.rectangle([170, eye_y, 185, eye_y+15], fill='black')
                        draw.rectangle([215, eye_y, 230, eye_y+15], fill='black')
                    else:  # smiling
                        draw.ellipse([170, eye_y, 185, eye_y+15], fill='black')
                        draw.ellipse([215, eye_y, 230, eye_y+15], fill='black')
                        # Smile
                        draw.arc([170, 110, 230, 130], 0, 180, fill='black', width=3)
                    
                    # Body
                    draw.rectangle([175, 150, 225, 350], fill='#4A90E2', outline='black', width=2)
                    
                    # Arms based on pose
                    if pose == 'pointing':
                        # Pointing arm
                        draw.line([225, 200, 300, 150], fill='#4A90E2', width=15)
                        draw.polygon([300, 150, 320, 140, 310, 160], fill='#4A90E2')
                    else:
                        # Normal arms
                        draw.line([125, 200, 175, 200], fill='#4A90E2', width=15)
                        draw.line([225, 200, 275, 200], fill='#4A90E2', width=15)
                    
                    # Legs
                    draw.line([190, 350, 190, 450], fill='#2C5282', width=20)
                    draw.line([210, 350, 210, 450], fill='#2C5282', width=20)
                    
                    # Add SmartKitab logo on shirt
                    draw.text((185, 250), "SK", fill='white', font_size=20)
                    
                    # Save frame
                    frame_path = os.path.join(self.assets_dir, f"avatar_{pose}_{frame:03d}.png")
                    img.save(frame_path)
            
            print("✅ Avatar frames created")
            return True
            
        except ImportError:
            print("❌ Install Pillow: pip install Pillow")
            return False
    
    def create_audio_with_pauses(self):
        """Create audio with pauses for avatar animations"""
        print("\n🎵 Creating audio with pauses...")
        
        try:
            from gtts import gTTS
            import pydub
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            # Your script parts with pauses
            script_parts = [
                ("Socho agar tum roz sirf one percent better ho jao.", 2.0),
                ("Gym nahi, motivation nahi, bas thoda sa improvement.", 2.0),
                ("Saal ke end tak tum bilkul different person ban jaoge.", 2.5),
                ("Yahi idea hai Atomic Habits ka.", 1.5),
                ("Waise ek question hai.", 1.0),
                ("Chhoti habits se sach mein kuch farak padta hai kya?", 2.0),
                ("Actually yahin hum log galat sochte hain.", 1.5),
                ("Small habits powerful hoti hain.", 1.5),
                ("Goals se zyada systems matter karte hain.", 2.0),
                ("Subscribe to SmartKitab!", 1.0)
            ]
            
            # Create silent segments for pauses
            silence = AudioSegment.silent(duration=500)  # 0.5 second silence
            
            # Combine all audio parts
            combined = AudioSegment.empty()
            
            for i, (text, pause) in enumerate(script_parts):
                # Create TTS for this part
                temp_audio = os.path.join(self.temp_dir, f"part_{i}.mp3")
                tts = gTTS(text=text, lang='hi', slow=False)
                tts.save(temp_audio)
                
                # Load and add to combined
                part_audio = AudioSegment.from_mp3(temp_audio)
                combined += part_audio + silence * pause  # Add pause after each part
            
            # Save combined audio
            self.audio_file = os.path.join(self.temp_dir, "avatar_audio.mp3")
            combined.export(self.audio_file, format="mp3")
            
            # Get duration
            self.audio_duration = len(combined) / 1000  # Convert to seconds
            print(f"✅ Audio created: {self.audio_duration:.2f} seconds")
            return True
            
        except ImportError as e:
            print(f"❌ Install required: pip install gtts pydub")
            return False
    
    def create_avatar_video_with_ffmpeg(self):
        """Create video with animated avatar using ffmpeg"""
        print("\n🎬 Creating avatar video...")
        
        # Step 1: Create avatar animation video
        avatar_video = os.path.join(self.temp_dir, "avatar_animation.mp4")
        
        # Create a sequence of avatar poses
        poses_sequence = ['thinking', 'explaining', 'thinking', 'pointing', 'smiling']
        
        # Create text file for concat
        concat_file = os.path.join(self.temp_dir, "avatar_frames.txt")
        
        with open(concat_file, 'w') as f:
            for pose in poses_sequence:
                for frame in range(10):
                    frame_file = os.path.join(self.assets_dir, f"avatar_{pose}_{frame:03d}.png")
                    if os.path.exists(frame_file):
                        f.write(f"file '{os.path.abspath(frame_file)}'\n")
                        f.write("duration 0.1\n")  # 0.1 seconds per frame
        
        # Create avatar animation
        cmd_avatar = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-r", "10",  # 10 fps for smooth animation
            "-i", concat_file,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            avatar_video,
            "-y"
        ]
        
        try:
            print("Creating avatar animation...")
            subprocess.run(cmd_avatar, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Avatar creation failed: {e.stderr.decode()[:200]}")
            return False
        
        # Step 2: Create background with text
        background_video = os.path.join(self.temp_dir, "background.mp4")
        
        # Define text for different times
        texts = [
            (0, 5, "ATOMIC HABITS"),
            (5, 10, "1% Better Every Day"),
            (10, 15, "Systems > Goals"),
            (15, 20, "Identity Builds Habits"),
            (20, 25, "Subscribe to SmartKitab")
        ]
        
        # Start with blank background
        bg_cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", f"color=c=0x0F172A:s=1920x1080:d={self.audio_duration}",
            "-c:v", "libx264",
            background_video,
            "-y"
        ]
        
        subprocess.run(bg_cmd, check=True, capture_output=True)
        
        # Add text to background
        current_video = background_video
        for i, (start, end, text) in enumerate(texts):
            if end > self.audio_duration:
                end = self.audio_duration
            
            output_video = os.path.join(self.temp_dir, f"bg_with_text_{i}.mp4")
            
            filter_text = (
                f"drawtext=text='{text}':"
                f"fontcolor=white:fontsize=70:"
                f"x=(w-text_w)/2:y=100:"
                f"enable='between(t,{start},{end})'"
            )
            
            cmd_text = [
                "ffmpeg",
                "-i", current_video,
                "-vf", filter_text,
                "-c:a", "copy",
                output_video,
                "-y"
            ]
            
            subprocess.run(cmd_text, capture_output=True)
            current_video = output_video
        
        # Step 3: Combine avatar with background
        combined_video = os.path.join(self.temp_dir, "combined_no_audio.mp4")
        
        # Scale and position avatar (bottom right corner)
        filter_complex = (
            f"[0:v]scale=400:600[avatar];"  # Scale avatar
            f"[1:v][avatar]overlay=W-w-50:H-h-50"  # Position bottom right
        )
        
        cmd_combine = [
            "ffmpeg",
            "-i", avatar_video,      # Avatar animation
            "-i", current_video,     # Background with text
            "-filter_complex", filter_complex,
            "-c:v", "libx264",
            "-t", str(self.audio_duration),
            combined_video,
            "-y"
        ]
        
        print("Combining avatar with background...")
        subprocess.run(cmd_combine, capture_output=True)
        
        # Step 4: Add audio
        cmd_final = [
            "ffmpeg",
            "-i", combined_video,
            "-i", self.audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            self.final_video,
            "-y"
        ]
        
        print("Adding audio...")
        subprocess.run(cmd_final, check=True, capture_output=True)
        
        print(f"✅ Avatar video created: {self.final_video}")
        return True
    
    def create_with_moviepy_and_avatar(self):
        """Create video with animated avatar using MoviePy"""
        print("\n🎬 Creating with MoviePy (better quality)...")
        
        try:
            from moviepy.editor import (
                AudioFileClip,
                ColorClip,
                ImageClip,
                concatenate_videoclips,
                TextClip,
                CompositeVideoClip
            )
            import numpy as np
            
            # Load audio
            audio = AudioFileClip(self.audio_file)
            duration = audio.duration
            
            # Create background
            bg = ColorClip(size=(1920, 1080), color=(15, 23, 42), duration=duration)
            
            # Create avatar animation
            avatar_clips = []
            avatar_size = (400, 600)
            
            # Generate moving avatar
            for t in np.arange(0, duration, 0.1):
                # Create avatar frame
                img = np.zeros((600, 400, 3), dtype=np.uint8)
                
                # Simple avatar drawing
                # This is a simplified version - in production, use actual images
                cv = 255 if (t * 10) % 2 == 0 else 200
                
                # Create a simple animated avatar
                avatar_img = ImageClip(img, duration=0.1)
                avatar_img = avatar_img.set_position(lambda t: ('right', 'bottom'))
                
                avatar_clips.append(avatar_img)
            
            # Combine avatar clips
            avatar = concatenate_videoclips(avatar_clips, method="compose")
            avatar = avatar.resize(0.3).set_position(('right', 'bottom')).set_duration(duration)
            
            # Create text animations
            text_clips = []
            
            # Scene texts
            scenes = [
                (0, 5, "ATOMIC HABITS\nSmall Changes = Big Results", 'yellow'),
                (5, 10, "1% Better Every Day\n37x Better in 1 Year", 'white'),
                (10, 15, "Systems > Goals\nDaily Action Matters", 'yellow'),
                (15, 20, "Identity Builds Habits\nChange Your Identity", 'white'),
                (20, duration, "SmartKitab\nKnowledge in Hinglish", 'yellow')
            ]
            
            for start, end, text, color in scenes:
                if end > duration:
                    end = duration
                
                txt = TextClip(
                    text,
                    fontsize=60,
                    color=color,
                    font='Arial-Bold',
                    size=(1600, 300),
                    method='caption',
                    align='center'
                )
                txt = txt.set_start(start).set_duration(end-start).set_position(('center', 0.2))
                text_clips.append(txt)
            
            # Create final composite
            final = CompositeVideoClip([bg] + text_clips + [avatar])
            final = final.set_audio(audio)
            
            # Write video
            final.write_videofile(
                self.final_video,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            print(f"✅ MoviePy avatar video created: {self.final_video}")
            return True
            
        except ImportError:
            print("❌ Install MoviePy: pip install moviepy")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def create_using_premade_avatar(self):
        """Use premade avatar graphics"""
        print("\n🔄 Using premade avatar assets...")
        
        # Download some free avatar graphics
        avatar_urls = [
            "https://cdn.pixabay.com/photo/2016/03/31/19/58/avatar-1295429_1280.png",
            "https://cdn.pixabay.com/photo/2016/03/31/20/31/avatar-1295831_1280.png",
        ]
        
        try:
            import requests
            
            print("Downloading avatar images...")
            for i, url in enumerate(avatar_urls):
                response = requests.get(url)
                with open(os.path.join(self.assets_dir, f"avatar_{i}.png"), 'wb') as f:
                    f.write(response.content)
                print(f"✅ Downloaded avatar {i}")
            
            # Now create video with these avatars
            return self.create_simple_avatar_video()
            
        except ImportError:
            print("❌ Install requests: pip install requests")
            return False
    
    def create_simple_avatar_video(self):
        """Simple avatar video using available assets"""
        print("\n🎬 Creating simple avatar video...")
        
        # Create a slideshow of avatar images with audio
        concat_list = os.path.join(self.temp_dir, "input.txt")
        
        # Get all avatar images
        avatar_images = []
        for ext in ['*.png', '*.jpg', '*.jpeg']:
            avatar_images.extend(Path(self.assets_dir).glob(ext))
        
        if not avatar_images:
            print("❌ No avatar images found!")
            return False
        
        # Create input file for concat
        with open(concat_list, 'w') as f:
            for img in avatar_images[:10]:  # Use first 10 images
                f.write(f"file '{img.absolute()}'\n")
                f.write("duration 2\n")  # 2 seconds per image
        
        # Create avatar video
        avatar_vid = os.path.join(self.temp_dir, "avatars.mp4")
        
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-r", "1/2",  # 1 frame every 2 seconds
            "-i", concat_list,
            "-c:v", "libx264",
            "-vf", "scale=400:600,format=yuv420p",
            avatar_vid,
            "-y"
        ]
        
        subprocess.run(cmd, capture_output=True)
        
        # Combine with background and audio
        self.combine_avatar_with_background(avatar_vid)
        return True
    
    def combine_avatar_with_background(self, avatar_video):
        """Combine avatar video with background and audio"""
        
        # Create background
        bg_video = os.path.join(self.temp_dir, "bg.mp4")
        
        bg_cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", f"color=c=0x0F172A:s=1920x1080:d={self.audio_duration}",
            "-c:v", "libx264",
            bg_video,
            "-y"
        ]
        
        subprocess.run(bg_cmd, capture_output=True)
        
        # Overlay avatar on background
        combined = os.path.join(self.temp_dir, "final_no_audio.mp4")
        
        filter_complex = (
            f"[0:v]scale=400:-1[avatar];"  # Scale avatar
            f"[1:v][avatar]overlay=W-w-50:H-h-50:shortest=1"  # Bottom right
        )
        
        cmd_overlay = [
            "ffmpeg",
            "-i", avatar_video,
            "-i", bg_video,
            "-filter_complex", filter_complex,
            "-c:v", "libx264",
            combined,
            "-y"
        ]
        
        subprocess.run(cmd_overlay, capture_output=True)
        
        # Add audio
        cmd_audio = [
            "ffmpeg",
            "-i", combined,
            "-i", self.audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            self.final_video,
            "-y"
        ]
        
        subprocess.run(cmd_audio, check=True)
        print(f"✅ Simple avatar video created: {self.final_video}")
        return True
    
    def run(self):
        """Main execution"""
        print("="*60)
        print("SMARTKITAB AVATAR VIDEO GENERATOR")
        print("="*60)
        
        # Setup
        self.setup_directories()
        
        if not self.check_dependencies():
            return
        
        # Create audio
        if not self.create_audio_with_pauses():
            return
        
        # Try different methods
        print("\n" + "="*60)
        print("SELECT AVATAR METHOD:")
        print("="*60)
        print("1. Generated cartoon avatar (PIL)")
        print("2. MoviePy animated avatar")
        print("3. Download premade avatars")
        print("4. Simple avatar slideshow")
        
        choice = input("\nChoose method (1-4): ").strip() or "4"
        
        success = False
        
        if choice == "1":
            if self.create_avatar_assets():
                success = self.create_avatar_video_with_ffmpeg()
        elif choice == "2":
            success = self.create_with_moviepy_and_avatar()
        elif choice == "3":
            success = self.create_using_premade_avatar()
        else:
            success = self.create_simple_avatar_video()
        
        if success:
            print("\n" + "="*60)
            print("🎉 AVATAR VIDEO CREATED SUCCESSFULLY!")
            print("="*60)
            print(f"\n📁 Video: {os.path.abspath(self.final_video)}")
            print("\n✨ Features:")
            print("• Animated avatar character")
            print("• Professional text animations")
            print("• Background music ready")
            print("• YouTube ready format")
        else:
            print("\n❌ Could not create avatar video.")
            print("\n💡 Try the simple method or use Canva with avatar graphics!")

# SIMPLIFIED VERSION WITH PREMADE AVATAR
def create_quick_avatar_video():
    """Quick avatar video using simple method"""
    
    print("🚀 Creating quick avatar video...")
    
    # Install required packages
    os.system("pip install moviepy gtts Pillow -q")
    
    try:
        from moviepy.editor import (
            AudioFileClip,
            ColorClip,
            TextClip,
            CompositeVideoClip,
            ImageSequenceClip
        )
        from gtts import gTTS
        from PIL import Image, ImageDraw
        import numpy as np
        
        # Create output directory
        os.makedirs("quick_output", exist_ok=True)
        
        # 1. Create audio
        print("1. Creating audio...")
        script = "SmartKitab presents Atomic Habits in Hinglish. Small changes lead to big results."
        tts = gTTS(text=script, lang='hi')
        tts.save("quick_output/audio.mp3")
        audio = AudioFileClip("quick_output/audio.mp3")
        
        # 2. Create simple avatar
        print("2. Creating avatar...")
        
        # Create avatar frames
        frames = []
        for i in range(10):
            # Create image with avatar
            img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw simple avatar (face that moves)
            # Head
            y_offset = 50 + (i % 3) * 5  # Slight bounce
            draw.ellipse([100, y_offset, 300, 200+y_offset], fill='#FFD700')
            
            # Eyes
            eye_offset = 10 if i % 2 == 0 else 0
            draw.ellipse([150+eye_offset, 80+y_offset, 170+eye_offset, 100+y_offset], fill='black')
            draw.ellipse([230+eye_offset, 80+y_offset, 250+eye_offset, 100+y_offset], fill='black')
            
            # Mouth
            mouth_y = 140 + y_offset + (i % 3) * 3
            draw.arc([150, mouth_y, 250, 160+y_offset], 0, 180, fill='black', width=5)
            
            # Body
            draw.rectangle([175, 200+y_offset, 225, 300+y_offset], fill='#4A90E2')
            
            # Convert to numpy array for MoviePy
            frame = np.array(img)
            frames.append(frame)
        
        # Create avatar clip
        avatar_clip = ImageSequenceClip(frames, fps=10)
        avatar_clip = avatar_clip.resize(0.4).set_position(('right', 'bottom'))
        
        # 3. Create background with text
        print("3. Creating background...")
        bg = ColorClip(size=(1280, 720), color=(15, 23, 42), duration=audio.duration)
        
        # Add text
        text = TextClip(
            "Atomic Habits\nin Hinglish",
            fontsize=70,
            color='yellow',
            font='Arial-Bold',
            size=(1000, 200),
            method='caption',
            align='center'
        ).set_position('center').set_duration(audio.duration)
        
        # 4. Combine everything
        print("4. Combining everything...")
        final = CompositeVideoClip([bg, text, avatar_clip])
        final = final.set_audio(audio)
        
        # 5. Save video
        output_path = "quick_output/smartkitab_avatar.mp4"
        final.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False
        )
        
        print(f"\n✅ QUICK AVATAR VIDEO CREATED: {output_path}")
        print("🎉 Your SmartKitab video with avatar is ready!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Alternative: Use Canva with avatar stickers!")

# RUN THE SCRIPT
if __name__ == "__main__":
    print("Choose option:")
    print("1. Full avatar video generator")
    print("2. Quick avatar video (recommended)")
    
    choice = input("\nEnter choice (1-2): ").strip()
    
    if choice == "1":
        creator = SmartKitabAvatarVideo()
        creator.run()
    else:
        create_quick_avatar_video()