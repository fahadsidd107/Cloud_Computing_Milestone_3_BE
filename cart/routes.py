from flask import Blueprint, render_template, request

cart_bp = Blueprint('cart', __name__)

# View cart route
@cart_bp.route('/')
def view_cart():
    # Retrieve user's cart (stub for now)
    return render_template('cart.html')

# Add item to cart route
@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Add product to cart (stub for now)
    return redirect(url_for('cart.view_cart'))

# Remove item from cart route
@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    # Remove item from cart (stub for now)
    return redirect(url_for('cart.view_cart'))
