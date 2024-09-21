from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'OPMP11232lppKDS'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {
    'admin': {'password': 'adminpass', 'role': 'admin'},
    'user': {'password': 'userpass', 'role': 'user'}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = users[username]['role']

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def home():
    return "Главная страница. <a href='/login'>Войти</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('user'))
        else:
            flash('Неправильный логин или пароль')
    return render_template('login.html')

@app.route('/user')
@login_required
def user():
    if current_user.role != 'user':
        return redirect(url_for('admin'))
    return f"Привет, пользователь! <a href='/logout'>Выйти</a>"

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        return redirect(url_for('user'))
    return f"Добро пожаловать, админ! <a href='/logout'>Выйти</a>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
