# Media Transcription & Content Safety Analyzer

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python-based tool for converting audio to text with built-in content safety analysis, detecting xenophobia, bias, misinformation, and hate speech.

## Key Features

- 🎧 WAV audio file transcription
- 🌍 Multilingual support (Arabic, Chinese, English, French, Russian, and Spanish)
- ⚙️ Dual recognition modes:
  - Offline (pocketsphinx engine)
  - Online (Google Web Speech API)
- 🔍 Content safety analysis:
  - Xenophobic speech detection
  - Bias expression identification
  - Misinformation flagging
  - Hate speech screening
- 📊 Risk level assessment (Low/Medium/High)
- 💾 Result export functionality

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup
```bash
# Clone repository (optional)
git clone https://github.com/Calista77/MediaTranslate.git
cd audio-analyzer

# Install dependencies
pip install SpeechRecognition pocketsphinx
