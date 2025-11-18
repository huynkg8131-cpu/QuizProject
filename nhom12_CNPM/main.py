import threading
import time
import queue
import unittest

# ======================================================
#               MODULE 1 — QUẢN LÝ NGƯỜI DÙNG
# ======================================================

users = {}
exam_history={}

def register_user(username, password, email, role):
    if username in users:
        return "❌ Tên người dùng đã tồn tại."
    users[username] = {
        "password": password,
        "email": email,
        "role": role
    }
    return "✅ Đăng ký thành công!"

def login_user(username, password):
    if username not in users:
        return "❌ Không tìm thấy người dùng."
    if users[username]["password"] != password:
        return "❌ Sai mật khẩu."
    return f"🎉 Đăng nhập thành công! Xin chào {username}.", users[username]["role"]

def list_users(role):
    if role not in ["admin", "lecturer"]:
        return "❌ Bạn không có quyền xem danh sách."
    if not users:
        return "📭 Chưa có người dùng nào."
    output = "\n📋 DANH SÁCH NGƯỜI DÙNG:\n"
    for u, info in users.items():
        output += f"- {u} | {info['role']} | {info['email']}\n"
    return output

def delete_user(role, username):
    if role not in ["admin", "lecturer"]:
        return "❌ Bạn không có quyền xóa."
    if username in users:
        del users[username]
        return f" Đã xóa tài khoản {username}"
    return "❌ Không tìm thấy người dùng."

def update_user(role, username, new_email=None, new_password=None, new_role=None):
    if role not in ["admin", "lecturer"]:
        return "❌ Không có quyền cập nhật."
    if username not in users:
        return "❌ Không tìm thấy người dùng."
    if new_email: users[username]["email"] = new_email
    if new_password: users[username]["password"] = new_password
    if new_role: users[username]["role"] = new_role
    return "✏️ Cập nhật thành công!"
def add_user(role, username, password, email, user_role):
    if role != "admin":
        return "❌ Chỉ admin mới thêm người dùng."
    return register_user(username, password, email, user_role)


# ======================================================
#               MODULE 2 — QUẢN LÝ CÂU HỎI
# ======================================================

class Question:
    def __init__(self, qid, text, answers, correct_answer, level):
        self.qid = qid
        self.text = text
        self.answers = answers
        self.correct_answer = correct_answer
        self.level = level

class QuestionManager:
    def __init__(self):
        self.questions = {}
        self.next_id = 1

    def add_question(self, text, answers, correct_answer, level):
        q = Question(self.next_id, text, answers, correct_answer, level)
        self.questions[self.next_id] = q
        self.next_id += 1
        return q.qid

    def edit_question(self, qid, text=None, answers=None, correct_answer=None, level=None):
        if qid not in self.questions:
            return False
        q = self.questions[qid]
        if text: q.text = text
        if answers: q.answers = answers
        if correct_answer: q.correct_answer = correct_answer
        if level: q.level = level
        return True

    def delete_question(self, qid):
        if qid in self.questions:
            del self.questions[qid]
            return True
        return False


# ======================================================
#               MODULE 3 — LÀM BÀI THI
# ======================================================

class Exam:
  
    def __init__(self, student_name, questions, duration_seconds=30):
        self.student_name = student_name
        self.questions = questions
        self.duration = duration_seconds
        self.time_left = duration_seconds
        self.lock = threading.Lock()

        self.exam_over = False
        self.student_answers = {}

    def countdown(self):
        while self.time_left > 0 and not self.exam_over:
            time.sleep(1)
            with self.lock:
                self.time_left -= 1

        with self.lock:
            self.exam_over = True

    def input_timeout(self, prompt):
        q = queue.Queue()

        def read():
            try:
                q.put(input(prompt))
            except:
                q.put("")

        t = threading.Thread(target=read)
        t.daemon = True
        t.start()

        while True:
            if self.exam_over:
                return None
            try:
                return q.get(timeout=0.1)
            except queue.Empty:
                continue

    def start_exam(self):
        print(f"\n===== BẮT ĐẦU BÀI THI CHO: {self.student_name} =====")

        t = threading.Thread(target=self.countdown)
        t.start()

        labels = ["A", "B", "C", "D", "E", "F"]

        for q in self.questions:
            if self.exam_over:
                break

            print(f"\n⏳ Thời gian còn lại: {self.time_left} giây")
            print(f"ID {q['id']}: {q['question']}")

            for i, opt in enumerate(q["options"]):
                if i < len(labels):
                    print(f"  {labels[i]}. {opt}")
                else:
                    print(f"  {i+1}. {opt}")

            ans = self.input_timeout("Nhập đáp án: ")
            if ans is None:
                ans = ""

            # đảm bảo ans là str trước khi .upper()
            ans = (ans or "").upper().strip()

            self.student_answers[q["id"]] = {
                "correct": q["answer"],
                "user": ans
            }
        with self.lock:
            self.exam_over = True

        print("\n📤 BÀI THI ĐÃ ĐƯỢC NỘP\n")

        return self.student_answers


# ======================================================
#               MODULE 4 — CHẤM ĐIỂM
# ======================================================

def mark_exam(result):
    correct_count = 0
    total = len(result)
    for _, info in result.items():
        if info["user"] == info["correct"]:
            correct_count += 1
    score = correct_count / total * 10 if total else 0
    return score, correct_count

def save_exam_result(username, result, score, correct_count):
    """Lưu kết quả bài thi vào lịch sử"""
    if username not in exam_history:
        exam_history[username] = []
    
    exam_record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "correct": correct_count,
        "total": len(result),
        "details": result
    }
    
    exam_history[username].append(exam_record)
    return " Đã lưu kết quả bài thi!"

def view_exam_history(username):
    """Xem lịch sử bài thi"""
    if username not in exam_history or not exam_history[username]:
        return " Bạn chưa có lịch sử bài thi nào."
    
    output = f"\n LỊCH SỬ BÀI THI CỦA {username.upper()}:\n"
    output += "=" * 60 + "\n"
    
    for i, record in enumerate(exam_history[username], 1):
        output += f"\n Lần {i} - {record['date']}\n"
        output += f"    Điểm: {record['score']:.2f}/10\n"
        output += f"   ✅ Đúng: {record['correct']}/{record['total']} câu\n"
    
    return output
def view_exam_detail(username, exam_index):
    """Xem chi tiết một bài thi cụ thể"""
    if username not in exam_history or not exam_history[username]:
        return " Không có lịch sử bài thi."
    
    if exam_index < 1 or exam_index > len(exam_history[username]):
        return " Số thứ tự bài thi không hợp lệ."
    
    record = exam_history[username][exam_index - 1]
    
    output = f"\n CHI TIẾT BÀI THI LẦN {exam_index}\n"
    output += f" Thời gian: {record['date']}\n"
    output += f" Điểm số: {record['score']:.2f}/10\n"
    output += f"✅ Đúng: {record['correct']}/{record['total']} câu\n"
    output += "\n" + "=" * 60 + "\n"
    
    for qid, info in record['details'].items():
        status = "✅" if info['user'] == info['correct'] else "❌"
        output += f"\n{status} Câu {qid}: {info['question']}\n"
        output += f"   Đáp án đúng: {info['correct']}\n"
        output += f"   Bạn chọn: {info['user'] if info['user'] else '(Không trả lời)'}\n"
    
    return output
# ======================================================
#                  MENU CHÍNH
# ======================================================

def main_menu():
    qm = QuestionManager()
    current_role = None
    current_user = None

    while True:
        print("\n===== MENU CHÍNH =====")
        print("1. Đăng ký")
        print("2. Đăng nhập")
        print("3. Quản lý câu hỏi (admin/lecturer)")
        print("4. Làm bài thi")
        print("5. Xem lịch sử bài thi")
        print("6. Xem chi tiết bài thi")
        print("7. Quản lý người dùng (admin/lecturer)")
        print ("8. Thoát")


        choice = input("Chọn: ")

        # ĐĂNG KÝ
        if choice == "1":
            u = input("Username: ")
            p = input("Password: ")
            e = input("Email: ")
            r = input("Vai trò (student/lecturer/admin): ")
            print(register_user(u, p, e, r))

        # ĐĂNG NHẬP
        elif choice == "2":
            u = input("Tên đăng nhập: ")
            p = input("Mật khẩu: ")
            res = login_user(u, p)
            if isinstance(res, tuple):
                print(res[0])
                current_role = res[1]
                current_user = u
            else:
                print(res)

        # QUẢN LÝ CÂU HỎI
        elif choice == "3":
            if current_role not in ["admin", "lecturer"]:
                print("❌ Không có quyền.")
                continue

            while True:
                print("\n--- QUẢN LÝ CÂU HỎI ---")
                print("1. Thêm câu hỏi")
                print("2. Sửa câu hỏi")
                print("3. Xóa câu hỏi")
                print("4. Xem tất cả")
                print("5. Quay lại")

                c = input("Chọn: ")

                if c == "1":
                    text = input("Nội dung: ")
                    raw = input("Các đáp án (A,B,C,D): ")
                    ans = [x.strip() for x in raw.split(",")]
                    correct = input("Đáp án đúng (A/B/C/D): ").upper()
                    level = input("Mức độ: ")
                    qid = qm.add_question(text, ans, correct, level)
                    print(f"✔ Thêm câu hỏi ID {qid}")

                elif c == "2":
                    qid = int(input("ID cần sửa: "))
                    new_text = input("Nội dung mới: ")
                    raw = input("Đáp án mới (A,B,C...): ")
                    new_ans = [x.strip() for x in raw.split(",")] if raw else None
                    new_correct = input("Đáp án đúng mới: ")
                    lvl = input("Mức độ mới: ")
                    print("✔ Sửa thành công") if qm.edit_question(
                        qid, new_text or None, new_ans, new_correct or None, lvl or None
                    ) else print("❌ Không tìm thấy ID")

                elif c == "3":
                    qid = int(input("ID cần xóa: "))
                    print("✔ Đã xóa") if qm.delete_question(qid) else print("❌ Không tồn tại")

                elif c == "4":
                    for q in qm.questions.values():
                        print(f"\nID {q.qid}: {q.text}")
                        print("Đáp án:", q.answers)
                        print("Đúng:", q.correct_answer)
                        print("Level:", q.level)

                elif c == "5":
                    break

        # LÀM BÀI THI
        elif choice == "4":
            if not qm.questions:
                print("❌ Chưa có câu hỏi.")
                continue
            
            exam_questions = []
            for q in qm.questions.values():
                exam_questions.append({
                    "id": q.qid,
                    "question": q.text,
                    "options": q.answers,
                    "answer": q.correct_answer
                })
            
            exam = Exam(current_user or "Student", exam_questions, 30)
            result = exam.start_exam()
            score, correct = mark_exam(result)

            print(f"🎯 Bạn đúng {correct}/{len(result)}")
            print(f"⭐ Điểm: {score:.2f}/10")

        elif choice == "5":
            if not current_user:
                print("❌ Vui lòng đăng nhập trước.")
                continue
            print(view_exam_history(current_user))

        # XEM CHI TIẾT BÀI THI
        elif choice == "6":
            if not current_user:
                print("❌ Vui lòng đăng nhập trước.")
                continue
            
            print(view_exam_history(current_user))
            try:
                exam_num = int(input("\nNhập số thứ tự bài thi muốn xem chi tiết: "))
                print(view_exam_detail(current_user, exam_num))
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ.")
         elif choice=="7":
            if current_role != "admin":
                print("❌ Chỉ admin mới quản lý người dùng.")
                continue
            while True:
                print("\n--- QUẢN LÝ NGƯỜI DÙNG ---")
                print("1. Xem danh sách")
                print("2. Thêm người dùng")
                print("3. Cập nhật người dùng")
                print("4. Xóa người dùng")
                print("5. Quay lại")
                c=input("Chọn: ")
                if c=="1": print(list_users(current_role))
                elif c=="2":
                    u=input("Username: ")
                    p=input("Password: ")
                    e=input("Email: ")
                    r=input("Vai trò: ")
                    print(add_user(current_role,u,p,e,r))
                elif c=="3":
                    u=input("Tên người dùng cần cập nhật: ")
                    e=input("Email mới (bỏ trống nếu không đổi): ")
                    p=input("Mật khẩu mới (bỏ trống nếu không đổi): ")
                    r=input("Vai trò mới (bỏ trống nếu không đổi): ")
                    print(update_user(current_role,u,e or None,p or None,r or None))
                elif c=="4":
                    u=input("Tên người dùng cần xóa: ")
                    print(delete_user(current_role,u))
                elif c=="5":
                    break
                else: print("❌ Lựa chọn sai")
        #thoat
        elif choice == "8":
            print("Thoát...")
            break
        else:
            print("❌ Lựa chọn sai")

if __name__ == "__main__":
    main_menu()

