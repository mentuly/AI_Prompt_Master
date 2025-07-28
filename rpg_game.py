import random
import sqlite3
from prompt_tasks import get_random_task


class RPGPromptMaster:
    DB_FILE = "rpg_save.db"
    def __init__(self):
        self.conn = sqlite3.connect(self.DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.defeated_npcs = set()
        self.xp = 0
        self.rank = "Новачок"
        self.map = {
            "Ліс": False,
            "Поселення": False,
            "Гори": False,
            "Печера": False,
            "Вежа Майстра": False,
            "Річка": False,
            "Замок": False,
            "Ферма": False,
            "Руїни": False,
            "Порт": False
        }
        self.allowed_locations = ["Ліс"]
        self.start_game()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS player (
            xp INTEGER, rank TEXT
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS progress (
            npc TEXT, defeated INTEGER
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS unlocked (
            location TEXT
        )''')
        self.conn.commit()

    def save_game(self):
        self.cursor.execute('DELETE FROM player')
        self.cursor.execute('INSERT INTO player (xp, rank) VALUES (?, ?)', (self.xp, self.rank))
        self.cursor.execute('DELETE FROM progress')
        for npc in self.defeated_npcs:
            self.cursor.execute('INSERT INTO progress (npc, defeated) VALUES (?, 1)', (npc,))
        self.cursor.execute('DELETE FROM unlocked')
        for loc in self.allowed_locations:
            self.cursor.execute('INSERT INTO unlocked (location) VALUES (?)', (loc,))
        self.conn.commit()

    def load_game(self):
        self.cursor.execute('SELECT xp, rank FROM player')
        row = self.cursor.fetchone()
        if row:
            self.xp, self.rank = row
        self.cursor.execute('SELECT npc FROM progress')
        self.defeated_npcs = set(npc for (npc,) in self.cursor.fetchall())
        self.cursor.execute('SELECT location FROM unlocked')
        self.allowed_locations = [loc for (loc,) in self.cursor.fetchall()] or ["Ліс"]

    def start_game(self):
        self.load_game()
        self.show_intro()
        self.intro_teacher()
        while True:
            print("\nОберіть дію:")
            print("1. Переглянути карту")
            print("2. Подорожувати")
            print("3. Вийти")
            main_choice = input("Ваш вибір: ")
            if main_choice == "1":
                self.show_map()
                continue
            elif main_choice == "2":
                self.show_map()
                command = input("Куди вирушити? (напиши назву локації або 'вихід'): ")
                if command.lower() == "вихід":
                    print("До зустрічі, майбутній Легендо Промптів!")
                    self.save_game()
                    break
                elif command in self.map:
                    if command in self.allowed_locations:
                        self.enter_location(command)
                    else:
                        print(f"Вас не пускають до '{command}'. Ви ще не готові.")
                else:
                    print("Такої локації не існує.")
            elif main_choice == "3":
                print("До зустрічі!")
                self.save_game()
                break

    def show_intro(self):
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                   AI PROMPT MASTER RPG                       ║
║                                                              ║
║           Welcome to the World of Promptia!                  ║
║     Train your mind. Defeat vague ideas. Win battles.        ║
║               Become a Prompt Legend!                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

    def intro_teacher(self):
        print("\n👨‍🏫 Вчитель: Вітаю, шукачу знань! Світ Промптів сповнений випробувань.\n")
        print("Щоб стати Легендою Промптів, ти маєш подорожувати цим світом, зустрічати наставників і перемагати НПС!")
        print("Ось мапа твоїх пригод. Почни з Лісу. Збирай досвід і відкривай нові місця!\n")

    def show_map(self):
        print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
║      Ліс — Поселення — Гори               Ферма —     Руїни           ║
║       |             |                          |         |            ║
║     Річка      Печера                         Порт       Замок        ║
║                       |                                     |         ║
║                    Вежа Майстра                            ???        ║
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        print("=== Стан карти ===")
        for location in self.map:
            access = "✅" if location in self.allowed_locations else "🔒"
            print(f"{access} {location}")
        print(f"\n🔹 Ваш XP: {self.xp} | Ранг: {self.rank}")

    def enter_location(self, location):
        print(f"🏞️ Ви входите в '{location}'...")
        npc_lookup = {
            "Ліс": ("Промпт-Початківець", 15),
            "Поселення": ("Промпт-Майстер", 30),
            "Гори": ("Синтаксис-Вартовий", 45),
            "Ферма": ("Кома-Кентавр", 60),
            "Печера": ("Семантик-Тінь", 90),
            "Руїни": ("Фрагмент-Древній", 120),
            "Порт": ("Формат-Навігатор", 180),
            "Замок": ("Аргумент-Лорд", 240),
            "Вежа Майстра": ("Лорд Промптів", 270)
        }
        if location in npc_lookup:
            name, xp_value = npc_lookup[location]
            self.npc_battle(name, xp_value)

    def evaluate_prompt(self, prompt):
        score = 0
        feedback = []
        if len(prompt) > 100: score += 2
        else: feedback.append("Зробіть промпт детальнішим.")
        if any(word in prompt.lower() for word in ["історія", "поясни", "генеруй", "код"]):
            score += 2
        else: feedback.append("Додайте ключові слова (наприклад: створити, поясни, придумай).")
        if prompt.endswith("."): score += 1
        else: feedback.append("Завершіть думку крапкою.")
        return score, " ".join(feedback) if feedback else "Чудовий промпт!"

    def npc_battle(self, npc_name, npc_xp):
        if npc_name in self.defeated_npcs:
            print(f"🔁 Ви вже перемогли {npc_name}. Хочете пройти реванш без нагород?")
            choice = input("Натисніть 'так' для реваншу або 'ні' для пропуску: ").strip().lower()
            if choice != "так":
                return
            else:
                npc_xp = 0

        print(f"⚔️ {npc_name} має {npc_xp} XP.")
        task = get_random_task()
        print(f"Завдання: {task}")
        prompt = input("Напишіть свій промпт для битви та натисніть Enter: ")
        if prompt.strip().lower() == "idk":
            print("🔓 Чит-режим активовано. Ви автоматично виграли бій!")
            user_score = 10
            feedback = "(Чит-код активований — перемога без оцінки.)"
        else:
            user_score, feedback = self.evaluate_prompt(prompt)

        # оцінка вже зроблена вище, повтор не потрібен

        if npc_xp <= 50:
            npc_score = 1
        elif npc_xp <= 100:
            npc_score = 2
        elif npc_xp <= 200:
            npc_score = 3
        elif npc_xp <= 400:
            npc_score = 4
        else:
            npc_score = 5

        print(f"Ваша оцінка: {user_score}, {npc_name}: {npc_score}")

        if user_score >= npc_score:
            print(f"🎉 Ви перемогли {npc_name} та отримали {npc_xp} XP!")
            if npc_name not in self.defeated_npcs:
                self.defeated_npcs.add(npc_name)
                self.xp += npc_xp
            self.update_rank()
            print(f"💡 Порада для вдосконалення: {feedback}")
            if self.xp >= 15 and "Поселення" not in self.allowed_locations:
                self.allowed_locations.append("Поселення")
            if self.xp >= 45 and "Гори" not in self.allowed_locations:
                self.allowed_locations.append("Гори")
            if self.xp >= 90 and "Печера" not in self.allowed_locations:
                self.allowed_locations.append("Печера")
            if self.xp >= 150 and "Ферма" not in self.allowed_locations:
                self.allowed_locations.append("Ферма")
            if self.xp >= 240 and "Руїни" not in self.allowed_locations:
                self.allowed_locations.append("Руїни")
            if self.xp >= 360 and "Порт" not in self.allowed_locations:
                self.allowed_locations.append("Порт")
            if self.xp >= 540 and "Замок" not in self.allowed_locations:
                self.allowed_locations.append("Замок")
            if self.xp >= 780 and "Вежа Майстра" not in self.allowed_locations:
                self.allowed_locations.append("Вежа Майстра")
        else:
            print("😞 Ви програли. Але зможете спробувати ще раз пізніше!")
            print(f"💡 Порада: {feedback}")

    def update_rank(self):
        prev_rank = self.rank
        if len(self.defeated_npcs) == 9:
            self.rank = "Легенда Промптів"
        elif self.xp >= 1000:
            self.rank = "Майстер Промптів"
        elif self.xp >= 500:
            self.rank = "Учень Майстра"
        elif self.xp >= 200:
            self.rank = "Учень"
        if self.rank != prev_rank:
            if self.rank == "Легенда Промптів":
                print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║     🏆 Вітаємо! Ви стали Легендою Промптів! 🏆                     ║
║                                                                    ║
║  Ви перемогли всіх NPC, пройшли усі пригоди й стали майстром!     ║
║   Тепер ваші промпти — еталон для цілих поколінь шукачів знань.   ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")
                while True:
                    choice = input("🔁 Бажаєте почати гру спочатку? (так/ні): ").strip().lower()
                    if choice == "так":
                        self.__init__()
                        return
                    elif choice == "ні":
                        print("👋 Дякуємо за гру в AI Prompt Master RPG!")
                        self.save_game()
                        exit()
                    else:
                        print("Будь ласка, оберіть 'так' або 'ні'.")
            print(f"🏅 Ваш ранг оновлено: {self.rank}")
        else:
            print(f"🔸 Ви отримали XP. Поточний XP: {self.xp}")