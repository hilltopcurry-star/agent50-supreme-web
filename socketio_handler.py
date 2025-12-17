from flask_socketio import SocketIO, emit, disconnect
from flask import session
from models import User, Driver, Order  # Import necessary models
from extensions import db
import json

socketio = SocketIO()

def init_socketio(app):
    socketio.init_app(app)

@socketio.on('connect')
def connect_handler():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if not user:
        disconnect()
    else:
        print(f"Client connected: {user.username}")
        emit('my_response', {'data': 'Connected'})

@socketio.on('driver_location_update')
def handle_driver_location_update(data):
    """
    Handle driver location updates and emit to relevant clients.
    Requires: {'driver_id': int, 'latitude': float, 'longitude': float}
    """
    driver_id = data.get('driver_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not all([driver_id, latitude, longitude]):
        print("Missing data in driver_location_update")
        return

    driver = Driver.query.get(driver_id)
    if not driver:
        print(f"Driver not found with id: {driver_id}")
        return

    driver.latitude = latitude
    driver.longitude = longitude
    db.session.commit()

    # Emit to all clients.  Consider scoping to order-specific rooms.
    emit('driver_location', {'driver_id': driver_id, 'latitude': latitude, 'longitude': longitude}, broadcast=True)


def emit_order_status_change(order_id, new_status):
    """
    Emit order status changes to relevant clients (e.g., customer, driver).
    """
    order = Order.query.get(order_id)

    if not order:
        print(f"Order not found with id: {order_id}")
        return

    # Emit to a room specific to the order.  This requires clients to join the room when viewing the order.
    socketio.emit('order_status_update', {'order_id': order_id, 'status': new_status}, room=f'order_{order_id}')