import requests
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # ব্রাউজারের "সার্ভার কানেকশন নেই" এরর বন্ধ করার জন্য

# কনফিগারেশন
BOT_TOKEN = "8427068930:AAGSygGuAfl27uEkJjOxQXWOouX3XQM0unI"
CHAT_ID = "6421195166"

@app.route('/upload', methods=['POST'])
def upload_to_telegram():
    if 'file' not in request.files:
        return jsonify({"ok": False, "description": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"ok": False, "description": "No selected file"}), 400

    # ফাইলের ধরন চেক করা (Image নাকি Video)
    is_video = file.content_type.startswith('video/')
    method = "sendVideo" if is_video else "sendPhoto"
    file_key = "video" if is_video else "photo"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    payload = {'chat_id': CHAT_ID}
    files = {file_key: (file.filename, file.read(), file.content_type)}

    try:
        response = requests.post(url, data=payload, files=files)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"ok": False, "description": str(e)}), 500

@app.route('/stream/<file_id>', methods=['GET'])
def stream_file(file_id):
    try:
        # টেলিগ্রাম থেকে ফাইলের পাথ বের করা
        file_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        if file_info.get("ok"):
            file_path = file_info['result']['file_path']
            download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            # সরাসরি টেলিগ্রাম সার্ভার থেকে স্ট্রীম করার জন্য রিডাইরেক্ট
            return redirect(download_url)
    except:
        pass
    return "File Not Found", 404

if __name__ == '__main__':
    # host='0.0.0.0' দিলে আপনার নেটওয়ার্কের অন্য ডিভাইস থেকেও এক্সেস করা যাবে
    app.run(host='0.0.0.0', port=5000, debug=True)
