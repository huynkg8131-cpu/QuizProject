import threading
import time
import queue
import random
import os
# ==================== QUIZ TAKING====================
class Exam:
  
    def __init__(self, student_name, questions, duration_seconds=30):
        self.student_name = student_name
        self.questions = questions # Danh sách câu hỏi
        self.duration = duration_seconds
        self.time_left = duration_seconds
        self.exam_over = False
        self.lock = threading.Lock() 
        
        self.student_answers = {} 

    def countdown_timer(self):
        while True:
            with self.lock:
                if self.exam_over or self.time_left <= 0:
                    break
                self.time_left -= 1
            time.sleep(1)

        with self.lock:
            if not self.exam_over:
                print("\nTime is up! Auto submitting the exam.")
                self.exam_over = True
                
    def get_input_with_timeout(self, prompt): # Đã bỏ tham số 'timeout' dư thừa
        """Lấy input từ người dùng trong khi luồng đếm ngược vẫn chạy."""
        q = queue.Queue()
        def temp_input():
            try:
                ans = input(prompt)
                q.put(ans)
            except EOFError:
                q.put(None)

        t = threading.Thread(target=temp_input)
        t.daemon = True
        t.start()

        while True:
            with self.lock:
                is_over = self.exam_over or self.time_left <= 0
                
            if is_over:
                return None
            
            try:
                ans = q.get(timeout=0.1) 
                return ans 
            except queue.Empty:
                pass
            
    def start_exam(self):
        print(f"\n=== Starting Exam for {self.student_name} ===")
        print(f"Time allowed: {self.duration} seconds\n")

        timer_thread = threading.Thread(target=self.countdown_timer)
        timer_thread.start()

        option_labels = ['A', 'B', 'C', 'D', 'E', 'F'] 
        
        for i, q in enumerate(self.questions, start=1):
            
            with self.lock:
                if self.exam_over:
                    print(f"\nExam stopped after Question {i-1}. Time ran out.")
                    break

            # HIỂN THỊ CÂU HỎI VÀ THỜI GIAN
            with self.lock:
                current_time_left = self.time_left
            print(f"\n--- Time Left: {current_time_left:02d} seconds ---") 
            print(f"Question {i} (ID: {q['id']}): {q['question']}")
            
            for j, opt_text in enumerate(q["options"]):
                label = option_labels[j]
                print(f"  {label}. {opt_text}")
            
            # LẤY CÂU TRẢ LỜI
            ans = self.get_input_with_timeout("Your answer (A, B, C, D) hoặc Enter để bỏ qua: ")

            user_input = ans if ans is not None else ""
            user_answer = user_input.strip().upper()

            # LƯU BÀI LÀM 
            self.student_answers[q['id']] = {
                'user_answer': user_answer, 
                'correct_answer': q['answer'], 
            }

            if ans is None or self.exam_over: 
                print("\nKết thúc nhận đáp án cho câu này (timeout/exam over).")
                break

        with self.lock:
            self.exam_over = True 
            
        timer_thread.join()

        print("\n==============================")
        print("Bài thi đã được nộp thành công.")
        print("==============================\n")
        
        return {
            'student_name': self.student_name,
            'total_questions': len(self.questions),
            'raw_answers': self.student_answers
        }




