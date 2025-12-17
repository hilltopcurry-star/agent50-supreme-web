from models import Order, OrderItem, Product
from extensions import db

class OrderStateMachine:

    TRANSITIONS = {
        'pending': ['processing', 'cancelled'],
        'processing': ['shipped', 'cancelled'],
        'shipped': ['delivered'],
        'delivered': [],
        'cancelled': []
    }

    @staticmethod
    def transition(order, new_state):
        """
        Transitions an order to a new state, handling inventory and database updates.
        """
        if new_state not in OrderStateMachine.TRANSITIONS.get(order.status, []):
            raise ValueError(f"Invalid transition from {order.status} to {new_state}")

        if new_state == 'processing' and order.status == 'pending':
            if not OrderStateMachine.hold_inventory(order):
                raise ValueError("Insufficient stock to fulfill order.")

        if new_state == 'cancelled':
            OrderStateMachine.release_inventory(order)

        order.status = new_state
        db.session.commit()

    @staticmethod
    def hold_inventory(order):
        """
        Attempts to hold inventory for an order.  Returns True if successful, False otherwise.
        """
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product.stock_quantity < item.quantity:
                return False
            product.stock_quantity -= item.quantity

        db.session.commit()
        return True

    @staticmethod
    def release_inventory(order):
        """
        Releases inventory held for an order (e.g., when cancelled).
        """
        for item in order.items:
            product = Product.query.get(item.product_id)
            product.stock_quantity += item.quantity
        db.session.commit()