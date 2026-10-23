# SmartKitab — Text-to-Speech & Avatar Video Generator

A Python toolkit that converts Hindi/Hinglish scripts to audio using **gTTS** / **edge-tts**, then assembles YouTube-ready MP4 videos featuring an animated talking-head avatar and text overlays.

---

## 📁 Project Structure

```
texttospeech/
├── ttos.py                      # Simple gTTS → MP3 script
├── smartkitab_video_generator.py # Full video pipeline (audio + frames → MP4)
├── avatar_video_generator.py    # Avatar frame generation + video composition
├── avatar_mouth_synced.py       # Real-time audio-amplitude mouth-sync video
├── avatar.py                    # Interactive avatar generator (multi-method)
├── install_deps.py              # Convenience installer for all packages
├── requirements.txt             # Pinned Python dependencies
├── assets/                      # Runtime-generated avatar frames (git-ignored)
├── temp/                        # Intermediate files (git-ignored)
└── output/                      # Final MP4 / metadata output (git-ignored)
```

---

## 🚀 Quick Start

### 1. Clone & enter the repo
```bash
git clone <repo-url>
cd texttospeech
```

### 2. Create & activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate.bat     # Windows
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg (required for video assembly)
```bash
# macOS (Homebrew)
brew install ffmpeg

# Ubuntu / Debian
sudo apt update && sudo apt install ffmpeg

# Windows → https://ffmpeg.org/download.html
```

---

## 🎬 Scripts Overview

### `ttos.py` — Basic TTS
Converts the Atomic Habits Hinglish script to an MP3 file.
```bash
python ttos.py
# Output: youtube_intro.mp3
```

### `smartkitab_video_generator.py` — Full Video Pipeline
Generates per-scene audio, renders PIL image frames, and assembles an MP4.
```bash
python smartkitab_video_generator.py
# Output: output/smartkitab_Atomic_Habits.mp4
#         output/youtube_metadata.json
```

### `avatar_video_generator.py` — Animated Avatar Video
Creates animated PIL avatar frames and composites them with a background clip.
```bash
python avatar_video_generator.py
# Output: output/smartkitab_avatar.mp4
```

### `avatar_mouth_synced.py` — Mouth-Synced Avatar
Analyses audio amplitude frame-by-frame and renders a live mouth-sync avatar.
```bash
python avatar_mouth_synced.py
# Output: output/smartkitab_mouth_synced.mp4
```

### `avatar.py` — Interactive Avatar Generator
Multi-method interactive tool (PIL cartoon, MoviePy, premade download, slideshow).
```bash
python avatar.py
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `gtts` | Google Text-to-Speech (Hindi) |
| `edge-tts` | Microsoft Edge TTS (higher quality) |
| `pydub` | Audio loading & amplitude analysis |
| `moviepy` | Video clip composition |
| `Pillow` | Image / avatar frame generation |
| `numpy` | Array operations for audio & image |
| `requests` | Downloading external avatar assets |
| `python-dotenv` | Environment variable management |

> **Note:** MoviePy requires FFmpeg to be installed system-wide.

---

## ⚙️ Configuration

Copy `.env.example` (if provided) or set the following environment variables when using API-based avatar generation:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Required for DALL-E avatar generation |

---

## 🗂️ Git-ignored Paths

The following are generated at runtime and are **not** committed to the repo:

- `venv/` — Python virtual environment
- `output/` — Generated MP4 videos & metadata
- `temp/` — Intermediate audio/image files
- `assets/` — Runtime avatar PNG frames
- `*.mp3`, `*.mp4` — Any media files in the root

---

## 🛠️ Development Notes

- **Pillow ≥ 10 compatibility** — `Image.ANTIALIAS` was removed in Pillow 10. The scripts that use MoviePy patch this at import time:
  ```python
  if not hasattr(Image, "ANTIALIAS"):
      Image.ANTIALIAS = Image.Resampling.LANCZOS
  ```
- **macOS audio playback** — Use `os.system("afplay file.mp3")` instead of `playsound`.
- **Font path** — Arial Bold is loaded from `/System/Library/Fonts/Supplemental/Arial Bold.ttf`; scripts gracefully fall back to `ImageFont.load_default()`.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
