from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db_connection
from app.utils import login_required
from datetime import datetime, timedelta

donors_bp = Blueprint('donors', __name__, url_prefix='/donors')

@donors_bp.route('/')
@login_required
def index():
    blood_type = request.args.get('blood_type')
    conn = get_db_connection()
    cur = conn.cursor()
    if blood_type:
        cur.execute("SELECT * FROM donors WHERE blood_type = %s ORDER BY created_at DESC", (blood_type,))
    else:
        cur.execute("SELECT * FROM donors ORDER BY created_at DESC")
    donors = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('donors/index.html', donors=donors)

@donors_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        blood_type = request.form['blood_type']
        phone = request.form['phone']
        email = request.form['email']
        city = request.form['city']
        last_donated_str = request.form['last_donated']
        
        last_donated = None
        if last_donated_str:
            last_donated = datetime.strptime(last_donated_str, '%Y-%m-%d').date()
            if (datetime.now().date() - last_donated).days < 90:
                flash('Donor must wait 90 days between donations.', 'danger')
                return render_template('donors/register.html')

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO donors (name, age, blood_type, phone, email, city, last_donated)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, age, blood_type, phone, email, city, last_donated))
            conn.commit()
            flash('Donor registered successfully.', 'success')
            return redirect(url_for('donors.index'))
        except Exception as e:
            flash('Error registering donor. Email might already exist.', 'danger')
        finally:
            cur.close()
            conn.close()
            
    return render_template('donors/register.html')
