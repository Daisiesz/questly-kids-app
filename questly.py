import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import random

class QuestlyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Questly - Kids Adventure Planner 🌟")
        self.root.geometry("1100x720")
        self.root.configure(bg="#a5f3fc")

        self.data_file = "questly_data.json"
        self.load_data()

        self.create_widgets()
        self.show_onboarding_if_needed()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "profile": None,
                "interests": [],
                "monthly_plans": [],
                "daily_quests": [],
                "points": 125,
                "streak": 4,
                "completed_today": 0,
                "journal": {},
                "gratitude": {}
            }

    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def create_widgets(self):
        header = tk.Frame(self.root, bg="#ff6bcb", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🌟 Questly", font=("Comic Sans MS", 32, "bold"), bg="#ff6bcb", fg="white").pack(side="left", padx=30)
        tk.Label(header, text="for SuperKids 4–12", font=("Arial", 18), bg="#ff6bcb", fg="white").pack(side="left", padx=10)

        self.points_label = tk.Label(header, text=f"⭐ {self.data['points']}", font=("Arial", 22, "bold"), bg="#ff6bcb", fg="yellow")
        self.points_label.pack(side="right", padx=40)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)

        self.home_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.home_tab, text="🏠 Home")

        self.monthly_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.monthly_tab, text="📅 Monthly Plans")

        self.daily_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.daily_tab, text="✅ Daily Quests")

        self.break_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.break_tab, text="⏰ Break Time")

        self.journal_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.journal_tab, text="📖 Journal")

        self.create_home_tab()
        self.create_monthly_tab()
        self.create_daily_tab()
        self.create_break_tab()
        self.create_journal_tab()

    def create_home_tab(self):
        tk.Label(self.home_tab, text="Welcome back, superstar! 🌈", font=("Comic Sans MS", 28, "bold"), bg="#a5f3fc").pack(pady=60)
        btn_frame = tk.Frame(self.home_tab, bg="#a5f3fc")
        btn_frame.pack(pady=30)
        tk.Button(btn_frame, text="🚀 START TODAY’S QUEST!", font=("Arial", 16, "bold"), bg="#10b981", fg="white", width=25, height=2,
                  command=self.start_day).pack(side="left", padx=20)
        tk.Button(btn_frame, text="✨ Surprise Me!", font=("Arial", 16, "bold"), bg="#ec4899", fg="white", width=20, height=2,
                  command=self.get_random_prompt).pack(side="left", padx=20)

    def create_monthly_tab(self):
        tk.Label(self.monthly_tab, text="Big Monthly Dreams 📅", font=("Comic Sans MS", 24, "bold")).pack(pady=20)
        tk.Button(self.monthly_tab, text="+ Add New Monthly Goal", font=("Arial", 12), bg="#ec4899", fg="white",
                  command=self.add_monthly_plan).pack(pady=10)
        self.monthly_list = tk.Frame(self.monthly_tab, bg="white")
        self.monthly_list.pack(fill="both", expand=True, padx=30, pady=10)
        self.refresh_monthly()

    def create_daily_tab(self):
        tk.Label(self.daily_tab, text="Today’s Epic Quests ✨", font=("Comic Sans MS", 24, "bold")).pack(pady=20)
        btn_frame = tk.Frame(self.daily_tab)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Get Smart Suggestions", bg="#10b981", fg="white", command=self.suggest_daily_tasks).pack(side="left", padx=10)
        tk.Button(btn_frame, text="+ Add Custom Quest", bg="#ec4899", fg="white", command=self.add_custom_quest).pack(side="left", padx=10)

        self.daily_list = tk.Frame(self.daily_tab, bg="white")
        self.daily_list.pack(fill="both", expand=True, padx=30, pady=10)
        self.refresh_daily()

    def create_break_tab(self):
        tk.Label(self.break_tab, text="Need a break, superstar? 🧘", font=("Comic Sans MS", 24, "bold")).pack(pady=40)
        self.timer_label = tk.Label(self.break_tab, text="45:00", font=("Arial", 48, "bold"), fg="#14b8a6")
        self.timer_label.pack(pady=30)
        tk.Button(self.break_tab, text="Start 45-min Focus Timer", font=("Arial", 14), bg="#14b8a6", fg="white",
                  command=self.start_focus_timer).pack(pady=10)
        tk.Button(self.break_tab, text="I need a break NOW!", font=("Arial", 14), bg="#f59e0b", fg="white",
                  command=self.give_break_suggestion).pack(pady=10)

    def create_journal_tab(self):
        tk.Label(self.journal_tab, text="Today's Journal 📖", font=("Comic Sans MS", 20)).pack(pady=10)
        self.journal_text = tk.Text(self.journal_tab, height=8, font=("Arial", 12))
        self.journal_text.pack(fill="x", padx=40, pady=10)
        tk.Button(self.journal_tab, text="Save My Story ✨", bg="#ec4899", fg="white", font=("Arial", 12),
                  command=self.save_journal).pack(pady=8)

        tk.Label(self.journal_tab, text="3 Things I'm Grateful For ❤️", font=("Comic Sans MS", 20)).pack(pady=20)
        self.grat1 = tk.Entry(self.journal_tab, font=("Arial", 12))
        self.grat1.pack(fill="x", padx=60, pady=5)
        self.grat2 = tk.Entry(self.journal_tab, font=("Arial", 12))
        self.grat2.pack(fill="x", padx=60, pady=5)
        self.grat3 = tk.Entry(self.journal_tab, font=("Arial", 12))
        self.grat3.pack(fill="x", padx=60, pady=5)

        tk.Button(self.journal_tab, text="Save Gratitude ❤️", bg="#10b981", fg="white", font=("Arial", 12),
                  command=self.save_gratitude).pack(pady=20)

    def show_onboarding_if_needed(self):
        if self.data["profile"] is None:
            self.onboard_win = tk.Toplevel(self.root)
            self.onboard_win.title("Welcome to Questly!")
            self.onboard_win.geometry("520x680")
            self.onboard_win.configure(bg="#fce7f3")

            tk.Label(self.onboard_win, text="Hi superstar! 🌈", font=("Comic Sans MS", 24, "bold"), bg="#fce7f3").pack(pady=20)
            tk.Label(self.onboard_win, text="Let's make this YOUR adventure!", font=("Arial", 14), bg="#fce7f3").pack(pady=5)

            tk.Label(self.onboard_win, text="What's your awesome name?", font=("Arial", 12, "bold"), bg="#fce7f3").pack(anchor="w", padx=40)
            self.name_entry = tk.Entry(self.onboard_win, font=("Arial", 16), width=35)
            self.name_entry.pack(pady=8, padx=40)

            tk.Label(self.onboard_win, text="How old are you? (4-12)", font=("Arial", 12, "bold"), bg="#fce7f3").pack(anchor="w", padx=40, pady=(20,5))
            self.age_entry = tk.Entry(self.onboard_win, font=("Arial", 16), width=10)
            self.age_entry.pack(pady=8, padx=40)

            tk.Label(self.onboard_win, text="What do you LOVE doing? (check as many as you want)", 
                     font=("Arial", 12, "bold"), bg="#fce7f3").pack(anchor="w", padx=40, pady=(30,10))

            self.interest_vars = {}
            interests = ["Drawing / Art 🎨", "Music / Piano 🎹", "Swimming 🏊", "Animals / Farm 🐮", 
                        "Cars 🚗", "Reading 📚", "Crafts 🧶", "Sports ⚽", "Exploring 🌍"]

            frame = tk.Frame(self.onboard_win, bg="#fce7f3")
            frame.pack(pady=10, padx=40)
            for i, interest in enumerate(interests):
                var = tk.BooleanVar()
                self.interest_vars[interest] = var
                cb = tk.Checkbutton(frame, text=interest, variable=var, font=("Arial", 11), bg="#fce7f3", anchor="w")
                cb.grid(row=i//2, column=i%2, sticky="w", padx=20, pady=6)

            tk.Button(self.onboard_win, text="COMPLETE & START ADVENTURE! 🚀", 
                      font=("Arial", 16, "bold"), bg="#ec4899", fg="white", height=2,
                      command=self.complete_onboarding).pack(pady=40, fill="x", padx=60)

    def complete_onboarding(self):
        name = self.name_entry.get().strip() or "SuperKid"
        try:
            age = int(self.age_entry.get())
            if age < 4 or age > 12:
                messagebox.showwarning("Age", "Please enter age between 4 and 12")
                return
        except:
            age = 8

        selected = [k for k, v in self.interest_vars.items() if v.get()]

        self.data["profile"] = {"name": name, "age": age}
        self.data["interests"] = selected
        self.save_data()
        self.onboard_win.destroy()
        messagebox.showinfo("Welcome!", f"Hi {name}! Ready for adventures? 🌟")
        self.refresh_all()

    def refresh_all(self):
        self.points_label.config(text=f"⭐ {self.data['points']}")

    def start_day(self):
        messagebox.showinfo("Let's Go!", "Today’s adventure started! Have fun!")

    def get_random_prompt(self):
        prompts = ["Feed the cows 🐮", "Practice swimming 🏊", "Draw your dream house 🎨", "Learn a new song 🎹"]
        prompt = random.choice(prompts)
        if messagebox.askyesno("Surprise Idea", f"{prompt}\nAdd to daily quests?"):
            self.data["daily_quests"].append({"text": prompt, "completed": False})
            self.save_data()
            self.refresh_daily()

    def add_monthly_plan(self):
        title = simpledialog.askstring("New Goal", "What is your big monthly dream?")
        if title:
            self.data["monthly_plans"].append({"title": title, "emoji": "🌟", "progress": 20})
            self.save_data()
            self.refresh_monthly()

    def refresh_monthly(self):
        for widget in self.monthly_list.winfo_children():
            widget.destroy()
        for plan in self.data["monthly_plans"]:
            f = tk.Frame(self.monthly_list, bg="#fce7f3", relief="ridge", bd=2)
            f.pack(fill="x", pady=8, padx=20)
            tk.Label(f, text=plan["emoji"] + " " + plan["title"], font=("Arial", 14, "bold"), bg="#fce7f3").pack(anchor="w", padx=15, pady=10)

    def suggest_daily_tasks(self):
        suggestions = ["Feed the cows and give them hugs 🐮", "Practice swimming like a dolphin 🏊", "Draw a rainbow 🎨", "Help wash the car 🚗"]
        for sug in random.sample(suggestions, min(3, len(suggestions))):
            self.data["daily_quests"].append({"text": sug, "completed": False})
        self.save_data()
        self.refresh_daily()
        messagebox.showinfo("Added!", "3 fun quests added for today!")

    def add_custom_quest(self):
        text = simpledialog.askstring("New Quest", "What quest do you want to add today?")
        if text:
            self.data["daily_quests"].append({"text": text, "completed": False})
            self.save_data()
            self.refresh_daily()

    def refresh_daily(self):
        for widget in self.daily_list.winfo_children():
            widget.destroy()
        for i, quest in enumerate(self.data["daily_quests"]):
            var = tk.BooleanVar(value=quest.get("completed", False))
            cb = tk.Checkbutton(self.daily_list, text=quest["text"], variable=var, font=("Arial", 12),
                                command=lambda idx=i, v=var: self.toggle_quest(idx, v))
            cb.pack(anchor="w", padx=40, pady=6)

    def toggle_quest(self, idx, var):
        self.data["daily_quests"][idx]["completed"] = var.get()
        if var.get():
            self.data["points"] += 15
            self.data["completed_today"] += 1
        self.save_data()
        self.refresh_all()

    def start_focus_timer(self):
        messagebox.showinfo("Timer", "Focus timer started! (Demo: alert in 5 seconds)")
        self.root.after(5000, lambda: messagebox.showinfo("Great job!", "Time for a creative break! 🎨"))

    def give_break_suggestion(self):
        suggestions = ["Draw with crayons 🎨", "Dance to your favorite song 💃", "Go outside and find flowers 🌸"]
        messagebox.showinfo("Break Idea", random.choice(suggestions))

    def save_journal(self):
        text = self.journal_text.get("1.0", tk.END).strip()
        if text:
            today = datetime.now().strftime("%Y-%m-%d")
            self.data["journal"][today] = text
            self.save_data()
            messagebox.showinfo("Saved", "Your journal entry is saved! 📖")

    def save_gratitude(self):
        g1 = self.grat1.get().strip()
        g2 = self.grat2.get().strip()
        g3 = self.grat3.get().strip()
        if g1 and g2 and g3:
            today = datetime.now().strftime("%Y-%m-%d")
            self.data["gratitude"][today] = [g1, g2, g3]
            self.save_data()
            messagebox.showinfo("Gratitude Saved", "Thank you for sharing what makes you happy ❤️")
            self.grat1.delete(0, tk.END)
            self.grat2.delete(0, tk.END)
            self.grat3.delete(0, tk.END)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = QuestlyApp()
    app.run()