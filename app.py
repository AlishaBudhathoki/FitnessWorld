from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from flask import flash

app = Flask(__name__)
app.secret_key = 'IAMSUPERSECRETKEY'

try:
    conn = psycopg2.connect(
        dbname="Fitness_World",
        user="DB",
        password="Alisha123@",
        host="localhost",
        port="5432"
    )
    c = conn.cursor()
    print("Database connection established successfully.")
except (psycopg2.OperationalError, psycopg2.Error) as e:
    print(f"Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            c.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            error = 'Username already exists. Please choose a different username.'
            return render_template('register.html', error=error)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        c.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = c.fetchone()
        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/members')
def members():
    c.execute('SELECT * FROM members')
    members = c.fetchall()
    return render_template('members.html', members=members)


@app.route('/member_details')
def member_details_form():
    return render_template('member_details.html')

@app.route('/fee_calculator', methods=['GET', 'POST'])
def fee_calculator():
    if request.method == 'POST':
        sessions_per_week = int(request.form['sessions_per_week'])
        training_plan = request.form['training_plan']
        total_fee = 0

        if training_plan == 'Beginner':
            total_fee += 1000 * sessions_per_week
        elif training_plan == 'Intermediate':
            total_fee += 2000 * sessions_per_week
        elif training_plan == 'Elite':
            total_fee += 3000 * sessions_per_week

        if 'private_trainer' in request.form:
            total_fee += 500  # Per Hour

        if 'sauna' in request.form:
            total_fee += 1500  # Per Session

        if 'swimming' in request.form:
            total_fee += 500  # Per Session

        return render_template('fee_calculator.html', total_fee=total_fee)
    return render_template('fee_calculator.html')



@app.route('/add_member', methods=['POST'])
def add_member():
    try:
        full_name = request.form['full_name']
        gender = request.form['gender']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']
        email = request.form['email']
        training_plan = request.form['training_plan']
        gym_time = request.form['gym_time']
        current_weight = request.form['current_weight']
        target_weight = request.form['target_weight']
        join_date = request.form['join_date']

        c.execute('INSERT INTO members (full_name, gender, phone, dob, address, email, training_plan, gym_time, current_weight, target_weight, join_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                  (full_name, gender, phone, dob, address, email, training_plan, gym_time, current_weight, target_weight, join_date))
        conn.commit()
        flash('Member added successfully!', 'success')
    except Exception as e:
        conn.rollback()  # Roll back any changes made before the error occurred
        flash('Failed to add member: {}'.format(str(e)), 'error')
        return redirect(url_for('dashboard'))


    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        c.execute('SELECT * FROM members')
        members = c.fetchall()
        return render_template('dashboard.html', members=members)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
