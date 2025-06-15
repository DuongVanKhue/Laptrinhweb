# L'Oreal Paris Website - Full Stack Application

Ứng dụng web bán mỹ phẩm L'Oreal Paris được xây dựng với Flask (Backend) và HTML/CSS/JavaScript (Frontend).

## 🚀 Tính năng chính

### Frontend
- Trang chủ với banner và sản phẩm nổi bật
- Danh sách sản phẩm với tìm kiếm, lọc và phân trang
- Chi tiết sản phẩm
- Giỏ hàng và thanh toán
- Đăng nhập/Đăng ký
- Trang liên hệ
- Trang giới thiệu thương hiệu

### Backend API
- Authentication (đăng ký, đăng nhập, quên mật khẩu)
- Quản lý sản phẩm và danh mục
- Giỏ hàng và đơn hàng
- Hệ thống liên hệ
- Phân quyền Admin/User

## 📋 Yêu cầu hệ thống

- Python 3.7+
- Flask và các dependencies trong requirements.txt

## 🛠️ Cài đặt và chạy

### 1. Clone hoặc tải project về

### 2. Cài đặt dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Khởi tạo database và dữ liệu mẫu
\`\`\`bash
python seed_data.py
\`\`\`

### 4. Chạy ứng dụng
\`\`\`bash
python run.py
\`\`\`

### 5. Truy cập website
- Website: http://localhost:5000
- Admin login: admin@loreal.com / admin123

## 📊 Cấu trúc Database

### Tables:
- **users**: Thông tin người dùng
- **categories**: Danh mục sản phẩm  
- **products**: Sản phẩm
- **cart_items**: Giỏ hàng
- **orders**: Đơn hàng
- **order_items**: Chi tiết đơn hàng
- **contact**: Tin nhắn liên hệ

## 🔧 API Endpoints

### Authentication
- `POST /api/register` - Đăng ký
- `POST /api/login` - Đăng nhập
- `POST /api/logout` - Đăng xuất
- `POST /api/forgot-password` - Quên mật khẩu

### Products
- `GET /api/products` - Danh sách sản phẩm
- `GET /api/products/<id>` - Chi tiết sản phẩm
- `GET /api/products/featured` - Sản phẩm nổi bật

### Cart
- `GET /api/cart` - Xem giỏ hàng
- `POST /api/cart/add` - Thêm vào giỏ
- `PUT /api/cart/update/<id>` - Cập nhật số lượng
- `DELETE /api/cart/remove/<id>` - Xóa khỏi giỏ

### Orders
- `POST /api/orders` - Tạo đơn hàng

### Other
- `POST /api/contact` - Gửi tin nhắn liên hệ
- `GET /api/categories` - Danh sách danh mục
- `GET /api/user` - Thông tin user hiện tại

## 👤 Tài khoản mặc định

**Admin:**
- Email: admin@loreal.com
- Password: admin123

## 📁 Cấu trúc thư mục

\`\`\`
loreal-website/
├── app.py              # Main Flask application
├── run.py              # Application runner
├── seed_data.py        # Database seeding script
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
├── templates/         # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── products.html
│   ├── cart.html
│   └── ...
└── loreal_store.db    # SQLite database (auto-generated)
\`\`\`

## 🔒 Bảo mật

- Mật khẩu được hash bằng Werkzeug
- Session-based authentication
- CORS protection
- Input validation và sanitization

## 🎨 Giao diện

- Responsive design
- Modern UI/UX
- Smooth animations và transitions
- Mobile-friendly

## 📝 Ghi chú

- Database sử dụng SQLite cho development
- Có thể chuyển sang PostgreSQL/MySQL cho production
- Session được lưu trữ server-side
- Images sử dụng external URLs

## 🚀 Deployment

Để deploy lên production:

1. Thay đổi SECRET_KEY trong app.py
2. Cấu hình database production
3. Set DEBUG=False
4. Sử dụng WSGI server như Gunicorn

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng kiểm tra:
- Python version >= 3.7
- Tất cả dependencies đã được cài đặt
- Database đã được khởi tạo bằng seed_data.py
- Port 5000 không bị conflict

## 📄 License

MIT License - Tự do sử dụng cho mục đích học tập và thương mại.
"# Laptrinhweb" 
