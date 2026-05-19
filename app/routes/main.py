from flask import Blueprint, render_template
from app.db import get_db_connection
from app.utils import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) as count FROM donors")
    total_donors = cur.fetchone()['count']
    
    cur.execute("SELECT SUM(units) as total FROM blood_inventory")
    total_units = cur.fetchone()['total'] or 0
    
    cur.execute("SELECT COUNT(*) as count FROM blood_requests WHERE status='Pending'")
    pending_requests = cur.fetchone()['count']
    
    cur.execute("SELECT COUNT(*) as count FROM hospitals")
    total_hospitals = cur.fetchone()['count']
    
    cur.execute("SELECT * FROM blood_inventory WHERE units < 5")
    low_stock = cur.fetchall()
    
    cur.execute("SELECT * FROM blood_inventory ORDER BY blood_type")
    inventory = cur.fetchall()
    labels = [item['blood_type'] for item in inventory]
    data = [item['units'] for item in inventory]
    
    cur.close()
    conn.close()
    
    return render_template('dashboard.html', 
                           total_donors=total_donors, 
                           total_units=total_units, 
                           pending_requests=pending_requests, 
                           total_hospitals=total_hospitals,
                           low_stock=low_stock,
                           labels=labels,
                           data=data)
