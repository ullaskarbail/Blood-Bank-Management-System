from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db_connection
from app.utils import login_required

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')

@requests_bp.route('/public', methods=['GET', 'POST'])
def public_request():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        blood_type = request.form['blood_type']
        units_required = int(request.form['units_required'])
        hospital_id = request.form['hospital_id']
        urgency = request.form['urgency']
        
        cur.execute("SELECT name FROM hospitals WHERE id=%s", (hospital_id,))
        hospital = cur.fetchone()
        
        if hospital:
            cur.execute("""
                INSERT INTO blood_requests (patient_name, blood_type, units_required, hospital, hospital_id, urgency)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (patient_name, blood_type, units_required, hospital['name'], hospital_id, urgency))
            conn.commit()
            flash('Blood request submitted successfully.', 'success')
            return redirect(url_for('main.index'))
            
    cur.execute("SELECT * FROM hospitals ORDER BY name")
    hospitals = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('requests/public_request.html', hospitals=hospitals)

@requests_bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blood_requests ORDER BY FIELD(status, 'Pending', 'Approved', 'Rejected'), requested_at DESC")
    blood_requests = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('requests/index.html', requests=blood_requests)

@requests_bp.route('/<int:id>/<action>')
@login_required
def handle_request(id, action):
    if action not in ['approve', 'reject']:
        return redirect(url_for('requests.index'))
        
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM blood_requests WHERE id=%s", (id,))
    req = cur.fetchone()
    
    if req and req['status'] == 'Pending':
        if action == 'approve':
            # Check inventory
            cur.execute("SELECT units FROM blood_inventory WHERE blood_type=%s", (req['blood_type'],))
            stock = cur.fetchone()
            if stock and stock['units'] >= req['units_required']:
                new_units = stock['units'] - req['units_required']
                cur.execute("UPDATE blood_inventory SET units=%s WHERE blood_type=%s", (new_units, req['blood_type']))
                cur.execute("""
                    INSERT INTO inventory_history (blood_type, change_amount, units_after, reason)
                    VALUES (%s, %s, %s, %s)
                """, (req['blood_type'], -req['units_required'], new_units, f"Approved request #{id} for {req['patient_name']}"))
                
                cur.execute("UPDATE blood_requests SET status='Approved', resolved_at=CURRENT_TIMESTAMP WHERE id=%s", (id,))
                flash('Request approved and stock updated.', 'success')
            else:
                flash('Not enough stock to approve this request.', 'danger')
        else:
            cur.execute("UPDATE blood_requests SET status='Rejected', resolved_at=CURRENT_TIMESTAMP WHERE id=%s", (id,))
            flash('Request rejected.', 'info')
            
        conn.commit()
        
    cur.close()
    conn.close()
    return redirect(url_for('requests.index'))
