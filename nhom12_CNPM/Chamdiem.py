# ChamDiem.py
from Register import users
from Take_Quiz import mark_exam
from Cauhoi import QuestionManager

class CauHoi:
    def __init__(self, question, correct_answer, user_answer):
        self.question = question
        self.correct_answer = correct_answer
        self.user_answer = user_answer


def cham_diem(ds):
    if not ds:
        return 0
    dung = 0
    for ch in ds:
        if ch.user_answer.strip().lower() == ch.correct_answer.strip().lower():
            dung += 1
    return dung / len(ds) * 10


def xem_ket_qua(ds):
    print("\n========== KẾT QUẢ CHI TIẾT ==========")
    for i, ch in enumerate(ds, start=1):
        if ch.user_answer.strip().lower() == ch.correct_answer.strip().lower():
            print(f"Câu {i}: Đúng")
        else:
            print(f"Câu {i}: Sai (Đáp án đúng: {ch.correct_answer})")


def main():
    ds = []
    n = int(input("Nhập số lượng câu hỏi: "))
    for i in range(n):
        print(f"\n--- Câu hỏi {i + 1} ---")
        question = input("Nhập nội dung câu hỏi: ")
        user_answer = input("Nhập đáp án của bạn: ")
        correct_answer = input("Nhập đáp án đúng: ")
        ds.append(CauHoi(question, correct_answer, user_answer))

    diem = cham_diem(ds)
    print("\n=== KẾT QUẢ ===")
    so_cau_dung = int(diem / 10 * len(ds))
    print(f"Bạn trả lời đúng {so_cau_dung}/{len(ds)} câu.")
    print(f"Điểm của bạn: {diem:.2f}/10")
    xem_ket_qua(ds)


if __name__ == "__main__":
    main()