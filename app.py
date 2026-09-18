import email

from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
# from db.conn import db_connection

# from db.models import pycon_notes

from db.conn import db
from db.models import PyconNotes,User


app = Flask(__name__)

app.secret_key = 'tesing-apk-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pycon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connect SQLAlchemy to this Flask application
db.init_app(app)

#invoking table creation
# pycon_notes()
with app.app_context():
    db.create_all()
    print("Database created")

#routes
@app.route('/')
def index():
    #if session has user_id, then user is logged in
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        return render_template('index.html', user=user)
    else:
        return render_template('index.html', user=None)


#function to create a note in the db
def create_note_in_db(speaker, title, body):
    # conn, cursor = db_connection()
    # cursor.execute("INSERT INTO pycon_notes (speaker, title, body) VALUES (?, ?, ?)", (speaker, title, body))
    # conn.commit()
    # conn.close()
    note = PyconNotes(speaker=speaker, title=title, body=body)
    db.session.add(note)
    db.session.commit()


#create note
@app.route('/create-note', methods = ['POST', 'GET'])
def create_note():
    if request.method == 'POST':
        # return request.form
        speaker = request.form['speaker']
        title = request.form['title']
        body = request.form['body']

        print(f"Speaker: {speaker}, Title: {title}, Body: {body}")
        # Here you would typically save the note to a database or file
        create_note_in_db(speaker, title, body)

        flash('Note created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_note.html')

#notes list
@app.route('/notes')
def notes():
    # conn, cursor = db_connection()
    # cursor.execute("SELECT  * FROM pycon_notes")
    # notes = cursor.fetchall()
    # conn.close()
    notes = PyconNotes.query.all()
    return render_template('notes.html', data = notes)

#viewing a single note
@app.route('/note/<int:id>')
def view_note(id):
    # conn, cursor = db_connection()
    # cursor.execute("SELECT * FROM pycon_notes WHERE id = ?", (id,))
    # note = cursor.fetchone()
    # conn.close()
    note = PyconNotes.query.get(id)
    return render_template('view_note.html', note=note)

#save user
def save_user_to_db(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()

#user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        #hash the password before saving to the database
        password = generate_password_hash(password)

        try:
            save_user_to_db(username, email, password)
        
            # Here you would typically save the user to a database
            # For now, we'll just flash a message and redirect to the login page
            flash('User registered successfully!', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()  # Rollback the session to avoid issues with the next request
            flash('Username or email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

#user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        password = request.form['password']

        # Fetch the user from the database based on the provided email
        user = User.query.filter_by(email=user_email).first()

        if user and check_password_hash(user.password, password):
            # Successful login
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            # Invalid credentials
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

#logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)