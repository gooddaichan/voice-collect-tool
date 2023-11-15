from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'secretkey'  # 今回は適当。

#ユーザーデータベース
users = {
    "user1": "password1",
    "user2": "password2"
}

def load_texts(filename):
    texts = {}
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(": ")
            if len(parts) == 2:
                texts[parts[0]] = parts[1]
    return texts

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['userid']
    password = request.form['password']
    if user_id in users and users[user_id] == password:
        texts = load_texts('sampletexts.txt')  # 外部テキストファイルからテキストを読み込む
        return render_template('recorder.html', user_id=user_id,texts=texts)
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    user_id = request.form['user_id']
    text_id = request.form['text_id']
    audio_file = request.files['audio_data']

    if audio_file:
        filename = f"{user_id}_{text_id}.webm"  # WebM形式で保存
        audio_file.save(os.path.join('uploads', filename))

    return 'Success', 200

if __name__ == '__main__':
    app.run(debug=True)
