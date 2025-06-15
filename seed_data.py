from app import app, db, Category, Product, User
from werkzeug.security import generate_password_hash

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create categories
        categories = [
            Category(name='Son môi', slug='son-moi'),
            Category(name='Dưỡng da', slug='duong-da'),
            Category(name='Làm sạch', slug='lam-sach'),
            Category(name='Chăm sóc tóc', slug='toc')
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        
        # Create admin user
        admin = User(
            name='Admin',
            contact='admin@loreal.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        
        # Create sample products
        products_data = [
            # Son môi
            {
                'name': "Son L'Oréal Paris Colour Riche Intense Volume Matte",
                'price': 300000,
                'description': "Thành phần chính: Chứa Hyaluronic Acid giúp dưỡng ẩm và làm đầy môi. Cách sử dụng: Thoa trực tiếp lên môi hoặc sử dụng cọ để tạo viền môi sắc nét. Công dụng: Mang lại màu sắc đậm nét, hiệu ứng nhung mịn, không làm khô môi.",
                'image_url': 'https://bomcosmetic.vn/wp-content/uploads/2021/12/son-li-muot-moi-l_oreal-paris-color-riche-moist-matte-mau-233.u2409.d20171022.t155354.412451.jpg',
                'category_id': 1,
                'stock_quantity': 50,
                'is_featured': True
            },
            {
                'name': "Son L'Oréal Paris Colour Riche Satin Lipstick",
                'price': 238000,
                'description': "Thành phần chính: Chứa Argan Oil và Vitamin E giúp dưỡng ẩm và làm mềm môi. Cách sử dụng: Thoa trực tiếp lên môi từ trung tâm ra ngoài. Công dụng: Mang lại màu sắc rực rỡ với độ bóng nhẹ, giúp môi mềm mại và không bị khô.",
                'image_url': 'https://bomcosmetic.vn/wp-content/uploads/2021/12/son-li-muot-moi-l_oreal-paris-color-riche-moist-matte-mau-233.u2409.d20171022.t155354.412451.jpg',
                'category_id': 1,
                'stock_quantity': 45,
                'is_featured': True
            },
            
            # Dưỡng da
            {
                'name': "Tinh Chất Dưỡng Ẩm L'Oréal Revitalift 1.5% Hyaluronic Acid Serum",
                'price': 357000,
                'description': "Thành phần chính: Chứa 1.5% Hyaluronic Acid với hai loại phân tử: Macro HA giúp cấp ẩm bề mặt và Micro HA thẩm thấu sâu, giúp da căng mướt và giảm nếp nhăn. Cách sử dụng: Thoa 2-3 giọt lên da sạch vào buổi sáng và tối trước bước kem dưỡng.",
                'image_url': 'https://cf.shopee.vn/file/a2dd412e5c28b0387c46d2417c968f30',
                'category_id': 2,
                'stock_quantity': 30,
                'is_featured': True
            },
            {
                'name': "Kem Chống Nắng L'Oréal UV Defender Matte & Fresh SPF50+ PA++++",
                'price': 299000,
                'description': "Thành phần chính: Chứa màng lọc quang phổ rộng Meroxyl SX/XL giúp bảo vệ da khỏi tia UVA và UVB. Cách sử dụng: Lắc đều trước khi sử dụng. Thoa một lượng vừa đủ lên mặt và cổ sau bước dưỡng da, trước khi ra nắng khoảng 15-20 phút.",
                'image_url': 'https://cf.shopee.vn/file/a2dd412e5c28b0387c46d2417c968f30',
                'category_id': 2,
                'stock_quantity': 40,
                'is_featured': True
            },
            
            # Làm sạch
            {
                'name': "Sữa Rửa Mặt Cấp Ẩm L'Oréal Revitalift Hyaluronic Acid Hydrating Gel-Cleanser",
                'price': 159000,
                'description': "Thành phần chính: Chứa Hyaluronic Acid và Glycerin giúp làm sạch nhẹ nhàng và cấp ẩm cho da. Cách sử dụng: Làm ướt mặt, lấy một lượng vừa đủ, tạo bọt và massage nhẹ nhàng, sau đó rửa sạch với nước.",
                'image_url': 'https://down-vn.img.susercontent.com/file/vn-11134207-7qukw-lfrdpg7idzhzb6',
                'category_id': 3,
                'stock_quantity': 60,
                'is_featured': True
            },
            {
                'name': "Nước Tẩy Trang L'Oréal Paris Revitalift Hyaluronic Acid Micellar Water 400ml",
                'price': 220000,
                'description': "Thành phần chính: Glycerin, Hexylene Glycol, Disodium Edta, Sodium Hyaluronate, Poloxamer 184. Công dụng: Làm sạch sâu lớp trang điểm và bụi bẩn; cấp ẩm cho da; giúp da căng mịn và tươi sáng; phù hợp cho da khô và da hỗn hợp.",
                'image_url': 'https://down-vn.img.susercontent.com/file/vn-11134207-7qukw-lfrdpg7idzhzb6',
                'category_id': 3,
                'stock_quantity': 35,
                'is_featured': True
            },
            
            # Chăm sóc tóc
            {
                'name': "Mặt nạ dưỡng tóc L'Oréal Paris Total Repair 5 Deep Repairing Mask",
                'price': 300000,
                'description': "Thành phần chính: Pro-Keratin và Ceramide. Công dụng: Phục hồi sâu, giúp tóc chắc khỏe và bóng mượt. Cách sử dụng: Sau khi gội, thoa lên tóc ướt, để trong 3-5 phút và xả sạch.",
                'image_url': 'https://myphamcacdai.vn/upload/products/large/myphamcacdai-dau-goi-phuc-hoi-toc-hu-ton-loreal-serie-expert-gold-quinoa-protein-absolut-repair-instant-resurfacing-shampoo-chinh-hang.png',
                'category_id': 4,
                'stock_quantity': 25,
                'is_featured': True
            },
            {
                'name': "Thuốc nhuộm tóc L'Oréal Paris Excellence Crème - 4.2 Plum Brown",
                'price': 749000,
                'description': "Thành phần chính: Pro-Keratin, Ceramide và Collagen. Công dụng: Phủ bạc hoàn hảo, màu sắc bền lâu và dưỡng tóc mềm mượt. Cách sử dụng: Trộn thuốc theo hướng dẫn, thoa đều lên tóc và để trong thời gian quy định, sau đó xả sạch.",
                'image_url': 'https://myphamcacdai.vn/upload/products/large/myphamcacdai-dau-goi-phuc-hoi-toc-hu-ton-loreal-serie-expert-gold-quinoa-protein-absolut-repair-instant-resurfacing-shampoo-chinh-hang.png',
                'category_id': 4,
                'stock_quantity': 20,
                'is_featured': True
            },
            
            # Additional products
            {
                'name': "Son L'Oréal Paris Chiffon Signature",
                'price': 359000,
                'description': "Son kem lì với chất son mịn mượt, nhẹ môi.",
                'image_url': 'https://bomcosmetic.vn/wp-content/uploads/2021/12/son-li-muot-moi-l_oreal-paris-color-riche-moist-matte-mau-233.u2409.d20171022.t155354.412451.jpg',
                'category_id': 1,
                'stock_quantity': 30,
                'is_featured': True
            },
            {
                'name': "Sữa Rửa Mặt L'Oréal Revitalift 100ml",
                'price': 155000,
                'description': "Thành phần chính: Chứa BHA và Glycerin giúp loại bỏ bụi bẩn, bã nhờn và lớp trang điểm.",
                'image_url': 'https://down-vn.img.susercontent.com/file/vn-11134207-7qukw-lfrdpg7idzhzb6',
                'category_id': 3,
                'stock_quantity': 55,
                'is_featured': True
            }
        ]
        
        for product_data in products_data:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        
        print("Database seeded successfully!")
        print(f"Created {len(categories)} categories")
        print(f"Created {len(products_data)} products")
        print("Admin user created: admin@loreal.com / admin123")

if __name__ == '__main__':
    seed_database()
