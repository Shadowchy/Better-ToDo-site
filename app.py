from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    theme = db.Column(db.String(10), default='light')

class ToDoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists!')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password!')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        session['theme'] = user.theme
        return redirect(url_for('todo'))

    return render_template('login.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    if request.method == 'POST':
        task = request.form['task']
        new_task = ToDoItem(task=task, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()

    tasks = ToDoItem.query.filter_by(user_id=user_id).all()
    theme = session.get('theme', 'light')
    return render_template('todo.html', tasks=tasks, theme=theme)

@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = ToDoItem.query.get_or_404(task_id)
    if task.user_id == session['user_id']:
        task.complete = not task.complete
        db.session.commit()
    return redirect(url_for('todo'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = ToDoItem.query.get_or_404(task_id)
    if task.user_id == session['user_id']:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('todo'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/theme/<string:theme_name>')
def switch_theme(theme_name):
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user.theme = theme_name
        session['theme'] = theme_name
        db.session.commit()
    return redirect(url_for('todo'))

@app.route('/edit', methods=['POST'])
def edit_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    task_id = request.form['task_id']
    task_content = request.form['task']

    task = ToDoItem.query.get_or_404(task_id)
    if task.user_id == session['user_id']:
        task.task = task_content
        db.session.commit()

    return redirect(url_for('todo'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
