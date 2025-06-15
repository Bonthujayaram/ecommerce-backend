from app import app, db
from models import Product
from seed_data import PRODUCTS

def reset_database():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Add all products from seed_data
        for product_data in PRODUCTS:
            product = Product(
                id=product_data['id'],
                name=product_data['name'],
                category=product_data['category'],
                price=product_data['price'],
                description=product_data['description'],
                image_url=product_data['image_url'],
                rating=product_data['rating'],
                stock_quantity=product_data['stock_quantity'],
                brand=product_data['brand']
            )
            db.session.add(product)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Database reset and seeded successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {str(e)}")

if __name__ == "__main__":
    reset_database() 