import speech_recognition as sr
import pyttsx3
import vosk
import os
import pyaudio
import random

# Инициализация синтезатора речи
def initialize_speech_synthesizer():
    engine = pyttsx3.init()
    return engine

# Инициализация распознавателя речи (онлайн)
def initialize_speech_recognizer():
    recognizer = sr.Recognizer()
    return recognizer

# Инициализация распознавателя речи (оффлайн)
def initialize_vosk_recognizer():
    model_path = r"C:\Users\ASUS\PycharmProjects\voice\model\vosk-model-small-ru-0.22"
    if not os.path.exists(model_path):
        print("Пожалуйста, скачайте модель с https://alphacephei.com/vosk/models и распакуйте её в папку 'model' в текущем каталоге.")
        exit(1)

    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)
    return recognizer

# Функция для распознавания речи с микрофона (онлайн)
def recognize_speech_online(recognizer):
    with sr.Microphone() as source:
        print("Скажите что-нибудь:")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {text}")
            return text
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания речи; {e}")
    return None

# Функция для распознавания речи с микрофона (оффлайн)
def recognize_speech_offline(recognizer):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("Скажите что-нибудь:")
    while True:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = eval(result)
            print(f"Вы сказали: {result_dict['text']}")
            return result_dict['text']
    return None

# Функция для синтеза речи
def synthesize_speech(engine, text):
    engine.say(text)
    engine.runAndWait()

# Функция для подброса монетки
def flip_coin(engine):
    result = random.choice(["орел", "решка"])
    synthesize_speech(engine, f"Выпал {result}")

# Функция для здорования и прощания
def greet_or_farewell(engine, text):
    if "привет" in text.lower():
        synthesize_speech(engine, "Здравствуйте!")
    elif "до свидания" in text.lower():
        synthesize_speech(engine, "До свидания!")
        return True
    return False

# Функция для изменения настроек языка распознавания и синтеза речи
def change_language_settings(recognizer, engine, language_code):
    recognizer.language = language_code
    voices = engine.getProperty('voices')
    for voice in voices:
        if language_code in voice.languages:
            engine.setProperty('voice', voice.id)
            break
    synthesize_speech(engine, f"Язык изменен на {language_code}")

# Основная функция
def main():
    # Инициализация компонентов
    speech_synthesizer = initialize_speech_synthesizer()
    online_recognizer = initialize_speech_recognizer()
    offline_recognizer = initialize_vosk_recognizer()

    while True:
        # Пример использования онлайн распознавания речи
        user_input = recognize_speech_online(online_recognizer)
        if user_input:
            print(f"Вы сказали: {user_input}")
            if "подбрось монетку" in user_input.lower():
                flip_coin(speech_synthesizer)
            elif greet_or_farewell(speech_synthesizer, user_input):
                break
            elif "английский" in user_input.lower():
                change_language_settings(online_recognizer, speech_synthesizer, "en-US")
            elif "русский" in user_input.lower():
                change_language_settings(online_recognizer, speech_synthesizer, "ru-RU")
            else:
                synthesize_speech(speech_synthesizer, f"Вы сказали: {user_input}")

if __name__ == "__main__":
    main()
