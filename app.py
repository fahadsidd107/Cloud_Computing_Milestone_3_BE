# app.py
from flask import Flask
from auth.routes import auth_bp
from users.routes import users_bp
from cart.routes import cart_bp
from products.routes import products_bp
from payment.routes import payment_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(cart_bp, url_prefix='/cart')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(payment_bp, url_prefix='/payment')

# Simple Hello World route
@app.route('/')
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)

