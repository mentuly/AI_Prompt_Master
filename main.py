# ШІ я використовував тільки щоб він мені росказав як краще до нього звертатись, це ви можете наглядно побачити з 80 до 105 строки

import json
import os
from prompt_tasks import get_random_task, get_random_task_coding
from rpg_game import RPGPromptMaster

USER_DATA_FILE = "user_data.json"

class PromptTrainer:
    def __init__(self):
        self.user_data = self.load_data()
        self.main_menu()

    def load_data(self):
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as f:
                return json.load(f)
        return {"history": [], "score": 0, "achievements": []}

    def save_data(self):
        with open(USER_DATA_FILE, "w") as f:
            json.dump(self.user_data, f, indent=2)

    def main_menu(self):
        while True:
            print("\n=== AI Prompt Master ===")
            print("0. RPG Mode")
            print("1. Навчання")
            print("2. Творчість")
            print("3. Кодування")
            print("4. Анти-промпт")
            print("5. Битва промптів")
            print("6. Переглянути статистику")
            print("7. Вийти")
            choice = input("Оберіть режим: ")

            if choice == "0":
                RPGPromptMaster()
            elif choice == "1":
                self.run_mode("Навчання")
            elif choice == "2":
                self.run_mode("Творчість")
            elif choice == "3":
                self.coding("Кодування")
            elif choice == "4":
                self.anti_prompt()
            elif choice == "5":
                self.prompt_battle()
            elif choice == "6":
                self.show_stats()
            elif choice == "7":
                break
            else:
                print("Невірний вибір.")
    
    def coding(self, mode):
        print(f"\n=== Режим: {mode} ===")
        task = get_random_task_coding()
        print(f"Завдання: {task}")
        prompt = input("Введіть свій промпт: ")
        score, feedback = self.evaluate_prompt(prompt)
        self.user_data["score"] += score
        self.user_data["history"].append({
            "mode": mode,
            "prompt": prompt,
            "score": score,
            "task": task
        })
        self.save_data()
        print(f"Оцінка: {score} балів")
        print(f"Порада: {feedback}")

    def run_mode(self, mode):
        print(f"\n=== Режим: {mode} ===")
        task = get_random_task()
        print(f"Завдання: {task}")
        prompt = input("Введіть свій промпт: ")
        score, feedback = self.evaluate_prompt(prompt)
        self.user_data["score"] += score
        self.user_data["history"].append({
            "mode": mode,
            "prompt": prompt,
            "score": score,
            "task": task
        })
        self.save_data()
        print(f"Оцінка: {score} балів")
        print(f"Порада: {feedback}")

    def evaluate_prompt(self, prompt):
        score = 0
        feedback = []
        if len(prompt) > 100:
            score += 2
        else:
            feedback.append("Зробіть промпт детальнішим.")
        if any(word in prompt.lower() for word in ["історія", "поясни", "генеруй", "код", "згенеруй"]):
            score += 2
        else:
            feedback.append("Додайте ключові слова (наприклад: створити, поясни, придумай).")
        if prompt.endswith("."):
            score += 1
        else:
            feedback.append("Завершіть думку крапкою.")
        return score, " ".join(feedback) if feedback else "Чудовий промпт!"

    def anti_prompt(self):
        print("\n=== Анти-промпт ===")
        bad_prompts = [
            "Напиши твір",
            "Зроби домашку",
            "Розкажи щось",
            "Створи щось цікаве",
            "Напиши код",
            "Дай відповідь",
            "Поясни тему"
        ]
        print("Погані приклади промптів:")
        for bp in bad_prompts:
            print(f"❌ {bp}")
        print("\nСпробуйте переробити один з них, щоб він став чітким і цікавим.")
        prompt = input("Ваш варіант: ")
        score, feedback = self.evaluate_prompt(prompt)
        print(f"Оцінка: {score} | {feedback}")

    def prompt_battle(self):
        print("\n=== Битва промптів ===")
        p1 = input("Гравець 1, введіть промпт: ")
        p2 = input("Гравець 2, введіть промпт: ")
        s1, _ = self.evaluate_prompt(p1)
        s2, _ = self.evaluate_prompt(p2)
        print(f"Результати: Гравець 1 — {s1}, Гравець 2 — {s2}")
        if s1 > s2:
            print("Переможець: Гравець 1")
        elif s2 > s1:
            print("Переможець: Гравець 2")
        else:
            print("Нічия!")

    def show_stats(self):
        print("\n=== Статистика ===")
        print(f"Загальний рахунок: {self.user_data['score']}")
        print("Історія промптів:")
        for item in self.user_data["history"][-5:]:
            print(f"[{item['mode']}] {item['prompt']} — {item['score']} балів | Завдання: {item.get('task', '—')}")

if __name__ == "__main__":
    PromptTrainer()