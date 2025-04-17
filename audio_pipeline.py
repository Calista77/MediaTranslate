import speech_recognition as sr
import os
import re
from collections import Counter

def analyze_content(text, language='en-US'):
    """
    Analyze text for risky content with multilingual support
    Returns analysis results dictionary
    """
    analysis = {
        'xenophobia': False,
        'bias': False,
        'misinformation': False,
        'hate_speech': False,
        'flags': []
    }
    
    # Multilingual keyword libraries
    keyword_lib = {
        # English (default)
        'en-US': {
            'xenophobia': ['foreigner', 'immigrant', 'alien', 'invader', 'go back to'],
            'bias': ['all women are', 'all men are', 'always', 'never', 'everyone knows'],
            'misinformation': ['fact', 'proven', 'scientifically', 'everyone knows'],
            'hate_speech': ['hate', 'kill', 'exterminate']
        },
        # Chinese
        'zh-CN': {
            'xenophobia': ['外国人', '移民', '异族', '滚回'],
            'bias': ['女人都', '男人都', '总是', '从不'],
            'misinformation': ['事实', '科学证明', '众所周知'],
            'hate_speech': ['消灭', '仇恨', '杀死']
        },
        # Japanese
        'ja-JP': {
            'xenophobia': ['外国人', '移民', '異民族', '帰れ'],
            'bias': ['女はみんな', '男はみんな', 'いつも', '決して'],
            'misinformation': ['事実', '科学的証明', '誰もが知っている'],
            'hate_speech': ['消せ', '憎しみ', '殺せ']
        },
        # Arabic
        'ar-AR': {
            'xenophobia': ['أجنبي', 'مهاجر', 'دخيل', 'غازي', 'ارجع إلى'],
            'bias': ['كل النساء', 'كل الرجال', 'دائما', 'أبدا'],
            'misinformation': ['حقيقة', 'مثبت', 'علميا'],
            'hate_speech': ['كراهية', 'اقتل', 'أبيد']
        },
        # French
        'fr-FR': {
            'xenophobia': ['étranger', 'immigrant', 'envahisseur', 'retourne à'],
            'bias': ['toutes les femmes sont', 'tous les hommes sont', 'toujours', 'jamais'],
            'misinformation': ['fait', 'prouvé', 'scientifiquement'],
            'hate_speech': ['haine', 'tuer', 'exterminer']
        },
        # Russian
        'ru-RU': {
            'xenophobia': ['иностранец', 'иммигрант', 'чужеземец', 'возвращайся в'],
            'bias': ['все женщины', 'все мужчины', 'всегда', 'никогда'],
            'misinformation': ['факт', 'доказано', 'научно'],
            'hate_speech': ['ненависть', 'убить', 'истребить']
        },
        # Spanish
        'es-ES': {
            'xenophobia': ['extranjero', 'inmigrante', 'invasor', 'vuelve a'],
            'bias': ['todas las mujeres son', 'todos los hombres son', 'siempre', 'nunca'],
            'misinformation': ['hecho', 'probado', 'científicamente'],
            'hate_speech': ['odio', 'matar', 'exterminar']
        }
    }
    
    # Get keywords for the specified language, default to English if not found
    keywords = keyword_lib.get(language, keyword_lib['en-US'])
    
    lower_text = text.lower()
    
    # Check each category
    for category in ['xenophobia', 'bias', 'misinformation', 'hate_speech']:
        matches = [term for term in keywords[category] 
                 if re.search(r'\b' + re.escape(term.lower()) + r'\b', lower_text)]
        if matches:
            analysis[category] = True
            # Display terms in original language for accurate reporting
            analysis['flags'].append(f"{category.capitalize()} terms detected: {', '.join(matches)}")
    
    return analysis

def transcribe_audio(audio_path=None, language='en-US', offline=True):
    """
    Convert WAV audio to text with extended language support
    
    Args:
        audio_path (str): Audio file path (absolute or relative)
        language (str): Recognition language code
        offline (bool): Use offline mode (default True)
        
    Returns:
        str: Transcription result or error message
    """
    # Supported languages mapping
    supported_languages = {
        'en-US': 'en-US',
        'zh-CN': 'zh-CN',
        'ja-JP': 'ja-JP',
        'ar-AR': 'ar-AR',
        'fr-FR': 'fr-FR',
        'ru-RU': 'ru-RU',
        'es-ES': 'es-ES'
    }
    
    # Validate language
    if language not in supported_languages:
        return f"Error: Unsupported language '{language}'"
    
    # Path handling
    if audio_path is None:
        audio_path = input("Enter audio file path: ").strip()
    audio_path = os.path.expanduser(audio_path)
    
    # File validation
    if not os.path.isfile(audio_path):
        return f"Error: File {audio_path} does not exist"
    if not audio_path.lower().endswith('.wav'):
        print("Warning: Non-WAV file may cause issues")
    
    r = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_path) as source:
            print(f"Processing: {os.path.basename(audio_path)}...")
            audio = r.record(source)
            
            if offline:
                print(f"Using offline engine (pocketsphinx) for {language}...")
                # Note: Offline mode may have limited language support
                return r.recognize_sphinx(audio, language=language)
            else:
                print(f"Using online engine (Google Web Speech API) for {language}...")
                return r.recognize_google(audio, language=language)
    
    except sr.UnknownValueError:
        return "Error: Audio not understandable"
    except sr.RequestError as e:
        return f"Error: API request failed - {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Command-line interface"""
    print("\n=== Multilingual Audio Transcription & Analysis ===")
    print("1. Offline mode (default)")
    print("2. Online mode (requires internet)")
    choice = input("Select mode [1/2]: ").strip()
    offline = choice != '2'
    
    # Language selection
    print("\nSupported languages:")
    print("en-US: English (US)\nzh-CN: Chinese")
    print("ar-AR: Arabic\nfr-FR: French\nru-RU: Russian\nes-ES: Spanish")
    lang = input("\nEnter language code (default en-US): ").strip() or 'en-US'
    
    # File input
    while True:
        file_path = input("\nEnter WAV file path: ").strip()
        file_path = os.path.expanduser(file_path)
        if os.path.isfile(file_path):
            break
        print(f"Error: File not found - {file_path}")
    
    # Transcription
    result = transcribe_audio(file_path, language=lang, offline=offline)
    
    print("\n=== Transcription Result ===")
    print(result)
    
    # Content analysis
    print("\n=== Content Analysis ===")
    analysis = analyze_content(result, language=lang)
    
    if not any([analysis['xenophobia'], analysis['bias'], 
               analysis['misinformation'], analysis['hate_speech']]):
        print("✅ Content analysis: No significant risks detected")
    else:
        print("⚠️ Potential risks detected:")
        for flag in analysis['flags']:
            print(f"- {flag}")
        
        risk_score = sum([analysis['xenophobia'], analysis['bias'],
                        analysis['misinformation'], analysis['hate_speech']])
        print(f"\nRisk level: {'Low' if risk_score == 1 else 'Medium' if risk_score == 2 else 'High'}")
    
    # Save results
    if input("\nSave to file? [y/N]: ").lower() == 'y':
        output_file = f"{os.path.splitext(file_path)[0]}_transcript.txt"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
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
