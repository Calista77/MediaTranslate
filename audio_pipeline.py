import speech_recognition as sr
import os
import re
from collections import Counter

def analyze_content(text):
    """
    分析文本内容是否存在风险言论
    返回分析结果字典
    """
    analysis = {
        'xenophobia': False,
        'bias': False,
        'misinformation': False,
        'hate_speech': False,
        'flags': []
    }
    
    # 定义关键词库（实际应用中应该使用更全面的词库）
    xenophobia_terms = ['foreigner', 'immigrant', 'alien', 'invader', 'go back to',
                      '外国人', '移民', '异族', '滚回']
    bias_terms = ['all women are', 'all men are', 'always', 'never', 'everyone knows',
                '女人都', '男人都', '总是', '从不']
    misinformation_terms = ['fact', 'proven', 'scientifically', 'everyone knows',
                          '事实', '科学证明', '众所周知']
    hate_speech_terms = ['hate', 'kill', 'exterminate', '消灭', '仇恨', '杀死']
    
    # 转换为小写方便匹配
    lower_text = text.lower()
    
    # 检测仇外言论
    xenophobia_matches = [term for term in xenophobia_terms 
                         if re.search(r'\b' + re.escape(term.lower()) + r'\b', lower_text)]
    if xenophobia_matches:
        analysis['xenophobia'] = True
        analysis['flags'].append(f"仇外言论关键词: {', '.join(xenophobia_matches)}")
    
    # 检测偏见
    bias_matches = [term for term in bias_terms 
                   if re.search(r'\b' + re.escape(term.lower()) + r'\b', lower_text)]
    if bias_matches:
        analysis['bias'] = True
        analysis['flags'].append(f"偏见表达: {', '.join(bias_matches)}")
    
    # 检测虚假信息
    misinfo_matches = [term for term in misinformation_terms 
                      if re.search(r'\b' + re.escape(term.lower()) + r'\b', lower_text)]
    if misinfo_matches:
        analysis['misinformation'] = True
        analysis['flags'].append(f"可能虚假信息标记: {', '.join(misinfo_matches)}")
    
    # 检测仇恨言论
    hate_matches = [term for term in hate_speech_terms 
                   if re.search(r'\b' + re.escape(term.lower()) + r'\b', lower_text)]
    if hate_matches:
        analysis['hate_speech'] = True
        analysis['flags'].append(f"仇恨言论关键词: {', '.join(hate_matches)}")
    
    return analysis

def transcribe_audio(audio_path=None, language='en-US', offline=True):
    """
    将WAV音频文件转换为文字（默认英文识别）
    
    参数:
        audio_path (str): 音频文件路径（绝对或相对路径）
        language (str): 识别语言，默认英语(en-US)
                       中文: zh-CN, 日语: ja-JP
        offline (bool): 是否使用离线模式，默认True
        
    返回:
        str: 识别结果或错误信息
    """
    # 处理路径输入
    if audio_path is None:
        audio_path = input("Enter audio file path: ").strip()
    audio_path = os.path.expanduser(audio_path)  # 处理 ~ 路径
    
    # 验证文件
    if not os.path.isfile(audio_path):
        return f"Error: File {audio_path} does not exist"
    if not audio_path.lower().endswith('.wav'):
        print("Warning: Non-WAV file may cause issues")
    
    # 初始化识别器
    r = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_path) as source:
            print(f"Processing: {os.path.basename(audio_path)}...")
            audio = r.record(source)
            
            if offline:
                print("Using offline engine (pocketsphinx)...")
                return r.recognize_sphinx(audio, language=language)
            else:
                print("Using online engine (Google Web Speech API)...")
                return r.recognize_google(audio, language=language)
    
    except sr.UnknownValueError:
        return "Error: Audio not understandable"
    except sr.RequestError as e:
        return f"Error: API request failed - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """命令行交互界面"""
    print("\n=== Audio Transcription & Analysis Tool ===")
    print("1. Offline mode (default)")
    print("2. Online mode (requires internet)")
    choice = input("Select mode [1/2]: ").strip()
    offline = choice != '2'
    
    # 语言选择
    lang = input("Language [en-US/zh-CN/ja-JP] (default en-US): ").strip()
    language = lang if lang else 'en-US'
    
    # 文件输入
    while True:
        file_path = input("\nEnter WAV file path: ").strip()
        file_path = os.path.expanduser(file_path)
        if os.path.isfile(file_path):
            break
        print(f"Error: File not found - {file_path}")
    
    # 执行转换
    result = transcribe_audio(file_path, language=language, offline=offline)
    
    # 输出结果
    print("\n=== Transcription Result ===")
    print(result)
    
    # 内容分析
    print("\n=== Content Analysis ===")
    analysis = analyze_content(result)
    
    if not any([analysis['xenophobia'], analysis['bias'], 
               analysis['misinformation'], analysis['hate_speech']]):
        print("✅ Content analysis: No significant risks detected")
    else:
        print("⚠️ Potential risks detected:")
        for flag in analysis['flags']:
            print(f"- {flag}")
        
        # 风险等级评估
        risk_score = sum([analysis['xenophobia'], analysis['bias'],
                        analysis['misinformation'], analysis['hate_speech']])
        print(f"\nRisk level: {'Low' if risk_score == 1 else 'Medium' if risk_score == 2 else 'High'}")
    
    # 保存结果
    if input("\nSave to file? [y/N]: ").lower() == 'y':
        output_file = f"{os.path.splitext(file_path)[0]}_transcript.txt"
        try:
            with open(output_file, 'w') as f:
                f.write(result)
                if analysis['flags']:
                    f.write("\n\n=== Analysis Results ===\n")
                    for flag in analysis['flags']:
                        f.write(f"- {flag}\n")
            print(f"Saved to: {output_file}")
        except IOError as e:
            print(f"Save failed: {str(e)}")

if __name__ == "__main__":
    main()
