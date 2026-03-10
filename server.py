import requests
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BOT_TOKEN = "8427068930:AAGSygGuAfl27uEkJjOxQXWOouX3XQM0unI"
CHAT_ID = "6421195166"

@app.route('/upload', methods=['POST'])
def upload_to_telegram():
    file = request.files.get('file')
    if not file: return jsonify({"ok": False}), 400

    is_video = file.content_type.startswith('video/')
    method = "sendVideo" if is_video else "sendPhoto"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    files = {'video' if is_video else 'photo': (file.filename, file.read(), file.content_type)}
    
    try:
        response = requests.post(url, data={'chat_id': CHAT_ID}, files=files).json()
        return jsonify(response)
    except:
        return jsonify({"ok": False}), 500

@app.route('/stream/<file_id>')
def stream(file_id):
    if "." in file_id: return "Invalid File", 404
    res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
    if res.get("ok"):
        return redirect(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{res['result']['file_path']}")
    return "Not Found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
