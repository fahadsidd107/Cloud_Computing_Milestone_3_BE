# payment/routes.py
from flask import Blueprint, render_template, request, redirect, url_for

payment_bp = Blueprint('payment', __name__)

# Checkout route
@payment_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Process payment (stub for now)
        return redirect(url_for('payment.payment_confirmation'))
    return render_template('checkout.html')

# Payment confirmation route
@payment_bp.route('/confirmation')
def payment_confirmation():
    # Show confirmation after payment (stub for now)
    return render_template('payment_confirmation.html')
