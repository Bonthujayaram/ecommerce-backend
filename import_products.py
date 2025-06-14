import json
from models import db, Product
from app import app
from flask import request, jsonify

def import_products():
    with app.app_context():
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
            for p in products:
                product = Product(
                    name=p['name'],
                    category=p['category'],
                    price=p['price'],
                    image_url=p['image_url'],
                    rating=p['rating']
                )
                db.session.add(product)
            db.session.commit()
        print('Products imported!')

@app.route('/products/search')
def search_products():
    query = request.args.get('q', '').lower()
    products = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) |
        (Product.description.ilike(f'%{query}%')) |
        (Product.category.ilike(f'%{query}%')) |
        (Product.brand.ilike(f'%{query}%'))
    ).all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products/category/<category>')
def get_products_by_category(category):
    products = Product.query.filter(Product.category.ilike(category)).all()
    return jsonify([p.to_dict() for p in products])

if __name__ == '__main__':
    import_products()

