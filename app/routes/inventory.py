from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db_connection
from app.utils import login_required

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blood_inventory ORDER BY blood_type")
    inventory = cur.fetchall()
    
    cur.execute("SELECT * FROM inventory_history ORDER BY recorded_at DESC LIMIT 20")
    history = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('inventory/index.html', inventory=inventory, history=history)

@inventory_bp.route('/update', methods=['POST'])
@login_required
def update():
    blood_type = request.form['blood_type']
    units = int(request.form['units'])
    action = request.form['action'] # add or remove
    reason = request.form['reason']
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT units FROM blood_inventory WHERE blood_type=%s", (blood_type,))
    current_stock = cur.fetchone()
    if not current_stock:
        flash('Invalid blood type.', 'danger')
        return redirect(url_for('inventory.index'))
        
    current_units = current_stock['units']
    change = units if action == 'add' else -units
    new_units = current_units + change
    
    if new_units < 0:
        flash('Cannot remove more units than available.', 'danger')
        return redirect(url_for('inventory.index'))
        
    cur.execute("UPDATE blood_inventory SET units=%s WHERE blood_type=%s", (new_units, blood_type))
    cur.execute("""
        INSERT INTO inventory_history (blood_type, change_amount, units_after, reason)
        VALUES (%s, %s, %s, %s)
    """, (blood_type, change, new_units, reason))
    
    conn.commit()
    cur.close()
    conn.close()
    
    flash(f'Successfully {action}ed {units} units of {blood_type}.', 'success')
    return redirect(url_for('inventory.index'))
