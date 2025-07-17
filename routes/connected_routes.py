from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import connected_models

connected_router = Blueprint('connected', __name__)

@connected_router.route('/add_device', methods=['GET', 'POST'])
def add_device_route():
    if request.method == 'POST':
        device_name = request.form.get('device_name')
        device_id = request.form.get('device_id')

        if not device_name or not device_id:
            flash('Device Name and Device ID are required!', 'error')
            return redirect(url_for('connected.add_device_route'))

        success, message = connected_models.add_device(device_name, device_id)
        if success:
            flash('Device added successfully!', 'success')
            return redirect(url_for('connected.list_devices_route'))
        else:
            flash(f'Error: {message}', 'error')
            return redirect(url_for('connected.add_device_route'))

    return render_template('add_device.html')

@connected_router.route('/connected_devices')
def list_devices_route():
    devices = connected_models.get_all_devices()
    return render_template('list_devices.html', devices=devices)

@connected_router.route('/deactivate/<device_id>')
def deactivate_device_route(device_id):
    success, message = connected_models.deactivate_device(device_id)
    if success:
        flash(message, 'success')
    else:
        flash(f"Error: {message}", 'error')
    return redirect(url_for('connected.list_devices_route'))
