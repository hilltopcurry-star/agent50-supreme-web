from models import Cart, CartItem, Product, Order, OrderItem, db

class CartManager:
    @staticmethod
    def get_or_create_cart(user_id):
        """
        Retrieves the active cart for a user, or creates a new one if none exists.
        """
        cart = Cart.query.filter_by(user_id=user_id, is_active=True).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        return cart

    @staticmethod
    def add_to_cart(cart_id, product_id, quantity):
        """
        Adds a product to the cart or updates the quantity if the product already exists in the cart.
        """
        cart = Cart.query.get(cart_id)
        product = Product.query.get(product_id)

        if not cart or not product:
            return False  # Cart or product not found

        cart_item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()

        if cart_item:
            # Update quantity if item already exists
            cart_item.quantity += quantity
        else:
            # Create a new cart item
            cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()
        return True

    @staticmethod
    def convert_cart_to_order(cart_id, delivery_address, payment_method):
        """
        Converts the cart to an order, marking the cart as inactive.
        """
        cart = Cart.query.get(cart_id)

        if not cart:
            return None  # Cart not found

        if not cart.cart_items:
            return None # Cart is empty
        
        user_id = cart.user_id

        order = Order(user_id=user_id, delivery_address=delivery_address, payment_method=payment_method)
        db.session.add(order)
        db.session.flush() # Need to flush to get the order ID

        for cart_item in cart.cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price  # Assuming Product model has a price attribute
            )
            db.session.add(order_item)

        cart.is_active = False
        db.session.commit()
        return order