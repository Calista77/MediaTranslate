# Media Transcription and Content Analysis Tool

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个基于Python的音频转文字工具，具备内容安全分析功能，可检测仇外言论、偏见表达、虚假信息和仇恨言论。

## 功能特性

- 🎧 支持WAV音频文件转文字
- 🌍 多语言识别（默认英语，支持中文、日语）
- ⚙️ 双模式识别：
  - 离线模式（pocketsphinx引擎）
  - 在线模式（Google Web Speech API）
- 🔍 内容安全分析：
  - 仇外言论检测
  - 偏见表达识别
  - 虚假信息标记
  - 仇恨言论筛查
- 📊 风险等级评估（低/中/高）
- 💾 结果导出功能

## 安装指南

### 前置要求
- Python 3.7+
- pip 包管理工具

### 安装步骤
```bash
# 克隆仓库（可选）
git clone https://github.com/Calista77/MediaTranslate.git
cd audio-analyzer

# 安装依赖
pip install SpeechRecognition pocketsphinx
