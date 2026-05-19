import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['DB_HOST'] = os.environ.get('DB_HOST', 'localhost')
app.config['DB_USER'] = os.environ.get('DB_USER', 'root')
app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD', 'rootpassword')
app.config['DB_NAME'] = os.environ.get('DB_NAME', 'blood_bank')

def get_db_connection():
    return pymysql.connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME'],
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        blood_group = request.form['blood_group']
        location = request.form['location']
        phone = request.form['phone']
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO donors (name, email, password, blood_group, location, phone) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, email, hashed_password, blood_group, location, phone))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Email already exists.', 'danger')
        finally:
            cur.close()
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        if email == 'admin':
            cur.execute("SELECT * FROM admin WHERE username=%s", (email,))
            admin = cur.fetchone()
            if admin and password == 'admin123': # Hardcoded for demo or hash check
                session['loggedin'] = True
                session['id'] = admin['id']
                session['username'] = admin['username']
                session['role'] = 'admin'
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Incorrect admin credentials.', 'danger')
        else:
            cur.execute("SELECT * FROM donors WHERE email=%s", (email,))
            donor = cur.fetchone()
            if donor and check_password_hash(donor['password'], password):
                session['loggedin'] = True
                session['id'] = donor['id']
                session['name'] = donor['name']
                session['role'] = 'donor'
                return redirect(url_for('donor_dashboard'))
            else:
                flash('Incorrect email/password!', 'danger')
        
        cur.close()
        conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/donor_dashboard')
def donor_dashboard():
    if 'loggedin' in session and session.get('role') == 'donor':
        return render_template('donor_dashboard.html', name=session['name'])
    return redirect(url_for('login'))

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'loggedin' in session and session.get('role') == 'admin':
        conn = get_db_connection()
        cur = conn.cursor()
        
        if request.method == 'POST':
            # Update blood stock
            blood_group = request.form['blood_group']
            units = request.form['units']
            action = request.form['action'] # add or remove
            
            if action == 'add':
                cur.execute("UPDATE blood_stock SET units = units + %s WHERE blood_group = %s", (units, blood_group))
            elif action == 'remove':
                cur.execute("UPDATE blood_stock SET units = GREATEST(units - %s, 0) WHERE blood_group = %s", (units, blood_group))
            conn.commit()
            flash(f'Stock updated for {blood_group}', 'success')
            
        cur.execute("SELECT * FROM blood_stock")
        stock = cur.fetchall()
        
        cur.execute("SELECT * FROM blood_requests")
        requests = cur.fetchall()
        
        cur.close()
        conn.close()
        return render_template('admin_dashboard.html', stock=stock, requests=requests)
    return redirect(url_for('login'))

@app.route('/approve_request/<int:id>')
def approve_request(id):
    if 'loggedin' in session and session.get('role') == 'admin':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE blood_requests SET status='Approved' WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_request/<int:id>')
def reject_request(id):
    if 'loggedin' in session and session.get('role') == 'admin':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE blood_requests SET status='Rejected' WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/request_blood', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        hospital_name = request.form['hospital_name']
        blood_group = request.form['blood_group']
        units = request.form['units']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO blood_requests (patient_name, hospital_name, blood_group, units) VALUES (%s, %s, %s, %s)",
                    (patient_name, hospital_name, blood_group, units))
        conn.commit()
        cur.close()
        conn.close()
        flash('Blood request submitted successfully.', 'success')
        return redirect(url_for('home'))
        
    return render_template('request_blood.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        blood_group = request.form['blood_group']
        location = request.form['location']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, location, phone FROM donors WHERE blood_group=%s AND location LIKE %s", (blood_group, f"%{location}%"))
        results = cur.fetchall()
        cur.close()
        conn.close()
        
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
