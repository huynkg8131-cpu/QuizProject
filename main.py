import unittest

# ============================
#   MODULE QUẢN LÝ CÂU HỎI
# ============================
"""
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

        if text is not None:
            q.text = text
        if answers is not None:
            q.answers = answers
        if correct_answer is not None:
            q.correct_answer = correct_answer
        if level is not None:
            q.level = level

        return True

    def delete_question(self, qid):
        if qid in self.questions:
            del self.questions[qid]
            return True
        return False

    def get_question(self, qid):
        return self.questions.get(qid)


# ============================
#   GIAO DIỆN CLI
# ============================

def show_menu():
    print("\n==============================")
    print(" QUIZ QUESTION MANAGER (CLI) ")
    print("==============================")
    print("1. Thêm câu hỏi")
    print("2. Sửa câu hỏi")
    print("3. Xóa câu hỏi")
    print("4. Xem tất cả câu hỏi")
    print("5. Thoát")
    print("==============================")


def run_cli():
    manager = QuestionManager()

    while True:
        show_menu()
        choice = input("Chọn chức năng: ")

        # -------- 1. Thêm câu hỏi --------
        if choice == "1":
            text = input("Nhập nội dung câu hỏi: ")

            raw_answers = input("Nhập các đáp án (cách nhau bởi dấu phẩy): ")
            answers = [a.strip() for a in raw_answers.split(",")]

            correct = input("Nhập đáp án đúng: ")
            level = input("Nhập mức độ (easy/medium/hard): ")

            qid = manager.add_question(text, answers, correct, level)
            print(f"✔ Đã thêm câu hỏi với ID = {qid}")

        # -------- 2. Sửa câu hỏi --------
        elif choice == "2":
            qid = int(input("Nhập ID câu hỏi muốn sửa: "))
            print("Để trống nếu không muốn thay đổi.")

            text = input("Nội dung mới: ")
            answers = input("Đáp án mới (A,B,C,...): ")
            correct = input("Đáp án đúng mới: ")
            level = input("Mức độ mới: ")

            text = text or None
            answers = [a.strip() for a in answers.split(",")] if answers else None
            correct = correct or None
            level = level or None

            if manager.edit_question(qid, text, answers, correct, level):
                print("✔ Sửa thành công")
            else:
                print("✘ Không tìm thấy câu hỏi")

        # -------- 3. Xóa câu hỏi --------
        elif choice == "3":
            qid = int(input("Nhập ID câu hỏi muốn xóa: "))
            if manager.delete_question(qid):
                print("✔ Đã xóa câu hỏi")
            else:
                print("✘ Không tìm thấy câu hỏi")

        # -------- 4. Hiển thị tất cả câu hỏi --------
        elif choice == "4":
            print("\n=== Danh sách câu hỏi ===")
            for q in manager.questions.values():
                print(f"ID: {q.qid}")
                print(f"Câu hỏi: {q.text}")
                print(f"Đáp án: {q.answers}")
                print(f"Đáp án đúng: {q.correct_answer}")
                print(f"Mức độ: {q.level}")
                print("-------------------------")

        # -------- 5. Thoát --------
        elif choice == "5":
            print("Thoát...")
            break

        else:
            print("Lựa chọn không hợp lệ!")


# ============================
#         UNIT TEST
# ============================

class TestQuestionManager(unittest.TestCase):

    def setUp(self):
        self.manager = QuestionManager()

    def test_add_question(self):
        qid = self.manager.add_question("2 + 2 = ?", ["1", "2", "3", "4"], "4", "easy")
        self.assertEqual(qid, 1)
        self.assertEqual(self.manager.get_question(1).text, "2 + 2 = ?")

    def test_edit_question(self):
        qid = self.manager.add_question("Thủ đô VN?", ["HN", "HCM"], "HN", "easy")
        self.manager.edit_question(qid, text="Thủ đô Việt Nam?", level="medium")
        q = self.manager.get_question(qid)
        self.assertEqual(q.text, "Thủ đô Việt Nam?")
        self.assertEqual(q.level, "medium")

    def test_delete_question(self):
        qid = self.manager.add_question("2 + 3 = ?", ["4", "5"], "5", "easy")
        result = self.manager.delete_question(qid)
        self.assertTrue(result)
        self.assertIsNone(self.manager.get_question(qid))


# ============================
#       ENTRY POINT
# ============================

if __name__ == "__main__":
    import sys

    if "--test" in sys.argv:
        unittest.main(argv=['ignored'], exit=False)
    else:
        run_cli()
"""