from flask import Blueprint, request, jsonify
from .models import Product, Order, db, order_product
from .utils import upload_image_to_gcs
from google.cloud import storage
import os
import logging
from functools import wraps

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize GCS client
gcs_credentials_path = os.getenv('GCS_CREDENTIALS_PATH', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'strapi-385510-04a56795d885.json'))
bucket_name = os.getenv('GCS_BUCKET_NAME', 'cloudimagesbucket')

if not os.path.exists(gcs_credentials_path):
    raise ValueError(f"GCS credentials file not found at {gcs_credentials_path}")

try:
    storage_client = storage.Client.from_service_account_json(gcs_credentials_path)
    bucket = storage_client.bucket(bucket_name)
except Exception as e:
    logger.error(f"Failed to initialize GCS client: {str(e)}")
    raise

bp = Blueprint('api', __name__)

# Helper function to handle errors
def handle_errors(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    return wrapped

# Helper function to validate required fields
def validate_required_fields(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

# Product APIs (unchanged)
@bp.route('/products', methods=['GET'])
@handle_errors
def get_all_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock_count': p.stock_count,
        'image_url': p.image_url
    } for p in products])

@bp.route('/products/<int:product_id>', methods=['GET'])
@handle_errors
def get_one_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock_count': product.stock_count,
        'image_url': product.image_url
    })

@bp.route('/products', methods=['POST'])
@handle_errors
def create_product():
    data = request.form
    image_file = request.files.get('image')

    # Validate required fields
    required_fields = ['name', 'description', 'price', 'stock_count']
    validate_required_fields(data, required_fields)

    # Ensure stock_count is greater than 0
    stock_count = int(data['stock_count'])
    if stock_count <= 0:
        return jsonify({'error': 'Stock count must be greater than 0'}), 400

    # Create product without image URL first
    product = Product(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        stock_count=stock_count,
        image_url=None
    )
    db.session.add(product)
    db.session.commit()

    # Upload image to GCS if provided
    if image_file:
        logger.info(f"Image file received: {image_file.filename}")
        destination_blob_name = f"products/{product.id}"  # Use product ID as the image name
        try:
            image_url = upload_image_to_gcs(bucket, image_file, destination_blob_name)
            product.image_url = image_url
            db.session.commit()
            logger.info(f"Image uploaded successfully: {image_url}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to upload image to GCS: {str(e)}")
            return jsonify({'error': f'Failed to upload image to GCS: {str(e)}'}), 500

    logger.info(f"Product created successfully: {product.id}")
    return jsonify({'message': 'Product created', 'id': product.id}), 201

@bp.route('/products/<int:product_id>', methods=['PUT'])
@handle_errors
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.form
    image_file = request.files.get('image')

    if image_file:
        # Upload new image to GCS
        destination_blob_name = f"products/{product.id}"  # Use product ID as the image name
        try:
            image_url = upload_image_to_gcs(bucket, image_file, destination_blob_name)
            product.image_url = image_url
            logger.info(f"New image uploaded successfully: {image_url}")
        except Exception as e:
            logger.error(f"Failed to upload new image to GCS: {str(e)}")
            return jsonify({'error': f'Failed to upload new image to GCS: {str(e)}'}), 500

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = float(data.get('price', product.price))
    product.stock_count = int(data.get('stock_count', product.stock_count))
    db.session.commit()
    logger.info(f"Product updated successfully: {product.id}")
    return jsonify({'message': 'Product updated', 'id': product.id})

@bp.route('/products/<int:product_id>', methods=['DELETE'])
@handle_errors
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    logger.info(f"Product deleted successfully: {product_id}")
    return jsonify({'message': 'Product deleted', 'id': product_id})

# Order APIs
@bp.route('/orders', methods=['GET'])
@handle_errors
def get_all_orders():
    orders = Order.query.all()
    orders_data = []
    for order in orders:
        # Fetch products and quantities for the order
        order_products = db.session.execute(
            db.select(order_product).where(order_product.c.order_id == order.id)
        ).fetchall()

        products = []
        for op in order_products:
            product = Product.query.get(op.product_id)
            products.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock_count': product.stock_count,
                'image_url': product.image_url,
                'quantity': op.quantity
            })

        orders_data.append({
            'id': order.id,
            'status': order.status,
            'paid': order.paid,
            'payment_method': order.payment_method,
            'products': products
        })

    return jsonify(orders_data)

@bp.route('/orders/<int:order_id>', methods=['GET'])
@handle_errors
def get_one_order(order_id):
    order = Order.query.get_or_404(order_id)

    # Fetch products and quantities for the order
    order_products = db.session.execute(
        db.select(order_product).where(order_product.c.order_id == order.id)
    ).fetchall()

    products = []
    for op in order_products:
        product = Product.query.get(op.product_id)
        products.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock_count': product.stock_count,
            'image_url': product.image_url,
            'quantity': op.quantity
        })

    return jsonify({
        'id': order.id,
        'status': order.status,
        'paid': order.paid,
        'payment_method': order.payment_method,
        'products': products
    })

@bp.route('/orders', methods=['POST'])
@handle_errors
def create_order():
    data = request.json
    required_fields = ['products', 'payment_method']
    validate_required_fields(data, required_fields)

    # Validate payment method
    payment_method = data['payment_method']
    if payment_method not in ['PayOnline', 'CashOnDelivery']:
        return jsonify({'error': 'Invalid payment method'}), 400

    # Validate products and quantities
    products_data = data['products']  # List of {product_id, quantity}
    if not isinstance(products_data, list) or len(products_data) == 0:
        return jsonify({'error': 'Products must be a non-empty list'}), 400

    # Check stock for each product
    for item in products_data:
        product_id = item.get('product_id')
        quantity = item.get('quantity')
        if not product_id or not quantity:
            return jsonify({'error': 'Each product must have a product_id and quantity'}), 400

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': f'Product with ID {product_id} not found'}), 404

        if quantity > product.stock_count:
            return jsonify({'error': f'Product {product.name} is out of stock'}), 400

    # Create order
    order = Order(
        status='Pending',  # Default status
        paid='Unpaid',  # Default paid status
        payment_method=payment_method
    )
    db.session.add(order)
    db.session.commit()

    # Add products to the order and deduct stock
    for item in products_data:
        product_id = item['product_id']
        quantity = item['quantity']
        product = Product.query.get(product_id)

        # Add product to order
        db.session.execute(
            order_product.insert().values(order_id=order.id, product_id=product_id, quantity=quantity)
        )

        # Deduct stock
        product.stock_count -= quantity

    db.session.commit()
    logger.info(f"Order created successfully: {order.id}")
    return jsonify({'message': 'Order created', 'id': order.id}), 201

@bp.route('/orders/<int:order_id>', methods=['PUT'])
@handle_errors
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json

    # Validate status and payment rules
    if 'status' in data:
        new_status = data['status']
        if new_status not in ['Pending', 'Delivering', 'Completed']:
            return jsonify({'error': 'Invalid status'}), 400

        # Ensure order cannot be completed unless paid
        if new_status == 'Completed' and order.paid != 'Paid':
            return jsonify({'error': 'Order cannot be completed unless paid'}), 400

        # Ensure PayOnline orders cannot be delivered unless paid
        if new_status == 'Delivering' and order.payment_method == 'PayOnline' and order.paid != 'Paid':
            return jsonify({'error': 'PayOnline orders cannot be delivered unless paid'}), 400

        order.status = new_status

    if 'paid' in data:
        order.paid = data['paid']

    db.session.commit()
    logger.info(f"Order updated successfully: {order.id}")
    return jsonify({'message': 'Order updated', 'id': order.id})

@bp.route('/orders/<int:order_id>', methods=['DELETE'])
@handle_errors
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)

    # Only allow deletion if the order is in "Pending" state
    if order.status != 'Pending':
        return jsonify({'error': 'Order can only be deleted if it is in Pending state'}), 400

    # Fetch products and quantities for the order
    order_products = db.session.execute(
        db.select(order_product).where(order_product.c.order_id == order.id)
    ).fetchall()

    # Add back the quantities to the product stock
    for op in order_products:
        product = Product.query.get(op.product_id)
        product.stock_count += op.quantity

    # Delete the order
    db.session.delete(order)
    db.session.commit()
    logger.info(f"Order deleted successfully: {order_id}")
    return jsonify({'message': 'Order deleted', 'id': order_id})