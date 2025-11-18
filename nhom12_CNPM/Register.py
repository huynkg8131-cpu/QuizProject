# Khởi tạo dữ liệu người dùng
users = {}

# Đăng ký người dùng mới
def register_user(username, password, email, role):
    if username in users:
        return "❌ Tên người dùng đã tồn tại."
    users[username] = {
        "password": password,
        "email": email,
        "role": role
    }
    return "✅ Đăng ký thành công!"

# Đăng nhập người dùng
def login_user(username, password):
    if username not in users:
        return "❌ Không tìm thấy người dùng."
    if users[username]["password"] != password:
        return "❌ Sai mật khẩu."
    return f"✅ Đăng nhập thành công! Xin chào {username}.", users[username]["role"]

# Xem danh sách người dùng (chỉ admin và lecturer)
def list_users(current_role):
    if current_role not in ["admin", "lecturer"]:
        print("❌ Bạn không có quyền xem danh sách người dùng.")
        return
    if not users:
        print("📭 Chưa có người dùng nào.")
        return
    print("📋 Danh sách người dùng:")
    for username, info in users.items():
        print(f"- {username} ({info['role']}) - {info['email']}")

# Xóa người dùng (chỉ admin và lecturer)
def delete_user(current_role, username):
    if current_role not in ["admin", "lecturer"]:
        return "❌ Bạn không có quyền xóa người dùng."
    if username in users:
        del users[username]
        return f"🗑️ Đã xóa người dùng: {username}"
    return "❌ Không tìm thấy người dùng."

# Cập nhật thông tin người dùng (chỉ admin và lecturer)
def update_user(current_role, username, new_email=None, new_password=None, new_role=None):
    if current_role not in ["admin", "lecturer"]:
        return "❌ Bạn không có quyền cập nhật thông tin người dùng."
    if username not in users:
        return "❌ Không tìm thấy người dùng."
    if new_email:
        users[username]["email"] = new_email
    if new_password:
        users[username]["password"] = new_password
    if new_role:
        users[username]["role"] = new_role
    return f"✏️ Thông tin người dùng {username} đã được cập nhật."

# Giao diện dòng lệnh đơn giản
if __name__ == "__main__":
    print("🔐 Hệ thống quản lý người dùng")
    print("1. Đăng ký\n2. Đăng nhập\n3. Xem danh sách\n4. Cập nhật\n5. Xóa\n6. Thoát")

    current_user_role = None

    while True:
        choice = input("\n Chọn chức năng (1-6): ")

        if choice == "1":
            u = input("Tên người dùng: ")
            p = input("Mật khẩu: ")
            e = input("Email: ")
            r = input("Vai trò (student/lecturer/admin): ")
            print(register_user(u, p, e, r))

        elif choice == "2":
            u = input("Tên người dùng: ")
            p = input("Mật khẩu: ")
            login_result = login_user(u, p)
            if isinstance(login_result, tuple):
                print(login_result[0])
                current_user_role = login_result[1]
            else:
                print(login_result)

        elif choice == "3":
            if current_user_role is None:
                print("❌ Vui lòng đăng nhập trước.")
            else:
                list_users(current_user_role)

        elif choice == "4":
            if current_user_role is None:
                print("❌ Vui lòng đăng nhập trước.")
            else:
                u = input("Tên người dùng cần cập nhật: ")
                e = input("Email mới (bỏ trống nếu không đổi): ")
                p = input("Mật khẩu mới (bỏ trống nếu không đổi): ")
                r = input("Vai trò mới (bỏ trống nếu không đổi): ")
                print(update_user(current_user_role, u, e or None, p or None, r or None))

        elif choice == "5":
            if current_user_role is None:
                print("❌ Vui lòng đăng nhập trước.")
            else:
                u = input("Tên người dùng cần xóa: ")
                print(delete_user(current_user_role, u))

        elif choice == "6":
            print("👋 Tạm biệt!")
            break

        else:
            print("❗ Lựa chọn không hợp lệ.")