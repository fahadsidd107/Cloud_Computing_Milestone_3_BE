from datetime import datetime
from . import db

# Association table for Order and Product (many-to-many relationship)
order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False)  # Quantity of each product in the order
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_count = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(100), nullable=False, default="Uncategorized")  # New category field
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # New date added field

    def __repr__(self):
        return f"<Product {self.name}>"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='Pending')  # Default status is 'Pending'
    paid = db.Column(db.String(50), nullable=False, default='Unpaid')  # Default is 'Unpaid'
    payment_method = db.Column(db.String(50), nullable=False)  # Payment method: 'PayOnline' or 'CashOnDelivery'
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # New date added field

    # User details
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_type = db.Column(db.String(50), nullable=False)  # e.g., Home, Office

    # Many-to-many relationship with Product
    products = db.relationship('Product', secondary=order_product, backref='orders')

    def __repr__(self):
        return f"<Order {self.id}>"
