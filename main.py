from flask import Flask, render_template, request, jsonify
import threading
import assistent
app = Flask(__name__)
conversation = []
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/start_assistant', methods=['POST'])
def start_assistant():
    global conversation
    conversation = []
    threading.Thread(target=run_assistant).start()
    return jsonify(success=True)
@app.route('/get_conversation', methods=['GET'])
def get_conversation():
    global conversation
    return jsonify(conversation=conversation)
def run_assistant():
    global conversation
    speech_synthesizer = assistent.initialize_speech_synthesizer()
    online_recognizer = assistent.initialize_speech_recognizer()
    offline_recognizer = assistent.initialize_vosk_recognizer()
    while True:
        conversation.append("Скажите что-нибудь:")
        user_input = assistent.recognize_speech_online(online_recognizer)
        if user_input:
            conversation.append(f"Вы сказали: {user_input}")
            print(f"Вы сказали: {user_input}")
            if "подбрось монетку" in user_input.lower():
                assistent.flip_coin(speech_synthesizer)
            elif assistent.greet_or_farewell(speech_synthesizer, user_input):
                break
            elif "английский" in user_input.lower():
                assistent.change_language_settings(online_recognizer, speech_synthesizer, "en-US")
            elif "русский" in user_input.lower():
                assistent.change_language_settings(online_recognizer, speech_synthesizer, "ru-RU")
            else:
                assistent.synthesize_speech(speech_synthesizer, f"Вы сказали: {user_input}")
if __name__ == '__main__':
    app.run(debug=True)
