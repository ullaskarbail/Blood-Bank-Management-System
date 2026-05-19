from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db_connection
from app.utils import login_required

hospitals_bp = Blueprint('hospitals', __name__, url_prefix='/hospitals')

@hospitals_bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM hospitals ORDER BY name")
    hospitals = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('hospitals/index.html', hospitals=hospitals)

@hospitals_bp.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']
    city = request.form['city']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO hospitals (name, address, phone, email, city)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, address, phone, email, city))
    conn.commit()
    cur.close()
    conn.close()
    
    flash('Hospital added successfully.', 'success')
    return redirect(url_for('hospitals.index'))

@hospitals_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM hospitals WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Hospital deleted successfully.', 'success')
    return redirect(url_for('hospitals.index'))
