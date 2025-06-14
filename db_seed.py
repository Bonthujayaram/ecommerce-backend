from models import db, Product
from app import app  # Ensure app.py initializes Flask & db
import random

def seed_products():
    with app.app_context():
        db.drop_all()  # Delete existing tables (optional)
        db.create_all()

        categories = ['shirts', 'laptop', 'mobile', 'books', 'fashion', 'electronics', 'home', 'sports', 'accessories']
        brands = ["Levi's", 'Nike', 'Samsung', 'Apple', 'HP', 'Puma', 'Sony', 'Adidas', 'Realme']
        products = []

        category_image_map = {
            'shirts': [
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1589998059171-30b864430f16?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1598032895397-20bc4281b6d6?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1576566588028-4147f3848f16?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1591195857868-392e2e0ebfa9?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1601333143550-36eb63eb3670?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1519864600265-abb23847ef2c?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=1",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=2",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=3",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=4",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=5",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=6",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=7"
            ],
            'laptop': [
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1541807084-5c52b6b3ad08?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1542393545-10f5cde2c810?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1496181133206-80ce9b88a0a6?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1531297484008-4e3a6a88d8f7?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1516383740770-cb320d80d96c?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&sig=1",
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&sig=2",
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&sig=3",
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&sig=4",
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&sig=5",
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&sig=6",
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&sig=7",
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&sig=8",
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&sig=9"
            ],
            'mobile': [
                "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1512499617640-c2f999098c01?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1567581935881-3e7d8b0d4e53?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1605773527850-7db7f93e6f9e?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1510878933023-e2e3e3c7114a?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1512941930350-8c0565f98ed1?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1544244015-6a2b829ea718?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1510557887715-379e466ce3b8?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1505156868547-9b49f4df4e04?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1516726817505-f5ed4d61081f?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1606761568499-6d2451b23c66?w=300&h=300&fit=crop"
            ],
            'books': [
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1464983953574-0892a716854b?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1491841573634-28140fc7ced7?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1524578271613-d550e5e5c167?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1516979187457-637b7a7d4292?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1528050793636-71eb9b2ed4e4?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1509266272358-7701c7ac8c85?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1513001900722-370f803f498d?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=300&fit=crop&sig=1",
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=300&fit=crop&sig=2",
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=300&fit=crop&sig=3",
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=300&fit=crop&sig=4",
                "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=300&h=300&fit=crop&sig=5"
            ],
            'fashion': [
                "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1539109136881-3be0616b15a6?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1483985988355-763728e1935b?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1529958030586-3aae4ca485ff?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1495385794356-15371f348c31?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=6",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=7",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop&sig=8"
            ],
            'electronics': [
                "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1518770660439-4636190af475?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1504707748692-419802cf939d?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1498049794561-4ab15d5b87d9?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1518291344630-4857135ec6eb?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1558089687-0f3e662486f5?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1516321497487-e288fb19713f?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1517430816045-df4b7de11d1d?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1533227268428-f9ed0900fb3b?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=300&h=300&fit=crop&sig=1",
                "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=300&h=300&fit=crop&sig=2",
                "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=300&h=300&fit=crop&sig=3"
            ],
            'home': [
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1513694203232-7e429f7a7b0e?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1495314736024-fa1c8b6bd385?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1513161454946-9e5904a6c563?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1492889971304-ac16ab3a568a?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1501183638620-5d4f7d7d4b7f?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=300&h=300&fit=crop&sig=1",
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=300&h=300&fit=crop&sig=2",
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=300&h=300&fit=crop&sig=3",
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=300&h=300&fit=crop&sig=4",
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=300&h=300&fit=crop&sig=5",
                "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=300&h=300&fit=crop&sig=6"
            ],
            'sports': [
                "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1505843279827-4b2b0c44a0a0?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1552674605-48b258eb7c09?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1517838277536-f60e7c6ad4b7?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1530549380692-3b033c6f3dc8?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1507398941214-572c25e4d7dc?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1518611012118-696072aa6fa6?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1471295253337-3ceaaedca402?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1495556650867-99590bb98c34?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1519058082700-6d27f0b270e7?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=300&h=300&fit=crop&sig=1",
                "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=300&h=300&fit=crop&sig=2",
                "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=300&h=300&fit=crop&sig=3",
                "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=300&h=300&fit=crop&sig=4",
                "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=300&h=300&fit=crop&sig=5",
                "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=300&h=300&fit=crop&sig=6"
            ],
            'accessories': [
                "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1522312346375-6e8b7a6a66f9?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1514327605112-b887c0e61c0a?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1506152983158-b4a74a01c721?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1502982720700-bfff8f170760?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1519643381402-22cdbd2ec730?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1504192010706-8bd53d26a529?w=300&h=300&fit=crop",
                "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=300&h=300&fit=crop&sig=1",
                "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=300&h=300&fit=crop&sig=2"
            ]
        }

        for i in range(1, 101):
            category = random.choice(categories)
            brand = random.choice(brands)
            name = f"{brand} {category.capitalize()} {i}"
            price = round(random.uniform(199.99, 99999.99), 2)
            images = category_image_map.get(category, [])
            if images and len(images) > 0:
                image_url = images.pop(0)
            else:
                # Fallback: always generate a unique Unsplash image for this product
                image_url = f"https://source.unsplash.com/300x300/?{category},{brand},{i}"
            rating = round(random.uniform(3.0, 5.0), 1)
            stock = random.randint(5, 50)
            desc = f"This is a high-quality {category} by {brand}."

            product = Product(
                name=name,
                category=category,
                price=price,
                image_url=image_url,
                rating=rating,
                stock_quantity=stock,
                brand=brand,
                description=desc
            )
            products.append(product)

        db.session.add_all(products)
        db.session.commit()
        print("✅ 100 mock products with images added to the database!")

if __name__ == '__main__':
    seed_products()
