# /app/products/routes.py
from flask import Blueprint, render_template, request, redirect, url_for

products_bp = Blueprint('products', __name__)

# In-memory product storage (to simulate a database)
products = [
    {"id": 1, "name": "Product 1", "price": 100, "description": "Description of Product 1"},
    {"id": 2, "name": "Product 2", "price": 200, "description": "Description of Product 2"}
]

# List all products
@products_bp.route('/')
def list_products():
    return render_template('products.html', products=products)

# View product details
@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    # Find product by ID
    product = next((prod for prod in products if prod['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    return "Product not found", 404

# Create product
@products_bp.route('/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        product_id = len(products) + 1  # Simulate auto-incrementing ID
        products.append({
            "id": product_id,
            "name": name,
            "price": price,
            "description": description
        })
        return redirect(url_for('products.list_products'))  # Redirect to list all products
    return render_template('create_product.html')

# Edit product
@products_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = next((prod for prod in products if prod['id'] == product_id), None)
    if not product:
        return "Product not found", 404

    if request.method == 'POST':
        product['name'] = request.form['name']
        product['price'] = request.form['price']
        product['description'] = request.form['description']
        return redirect(url_for('products.product_detail', product_id=product_id))  # Redirect to product details

    return render_template('edit_product.html', product=product)

# Delete product
@products_bp.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    global products
    products = [prod for prod in products if prod['id'] != product_id]  # Remove the product by ID
    return redirect(url_for('products.list_products'))  # Redirect to list all products
