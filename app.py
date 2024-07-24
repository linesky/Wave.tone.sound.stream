from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_FILE = 'data.txt'

def load_users():
    users = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            for line in file:
                username, password, content = line.strip().split(',')
                users[username] = {'password': password, 'content': content}
    return users

def save_users(users):
    with open(DATA_FILE, 'w') as file:
        for username, data in users.items():
            file.write(f"{username},{data['password']},{data['content']}\n")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            flash('Usuário já registrado.', 'error')
            return redirect(url_for('login'))
        
        users[username] = {'password': password, 'content': ''}
        save_users(users)
        session['username'] = username
        return redirect(url_for('edit'))

    return render_template('index.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    users = load_users()
    user_data = users[username]

    if request.method == 'POST':
        user_data['content'] = request.form['content']
        users[username] = user_data
        save_users(users)
        flash('Conteúdo salvo com sucesso.', 'success')

    return render_template('edit.html', content=user_data['content'])
print("\x1bc\x1b[47;34m")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

