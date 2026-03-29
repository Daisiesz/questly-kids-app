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
        self.root.geometry("1150x750")
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
                "goals": {"weekly": [], "monthly": [], "annual": []},
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
        # Header
        header = tk.Frame(self.root, bg="#ff6bcb", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🌟 Questly", font=("Comic Sans MS", 32, "bold"), bg="#ff6bcb", fg="white").pack(side="left", padx=30)
        tk.Label(header, text="for SuperKids 4–12", font=("Arial", 18), bg="#ff6bcb", fg="white").pack(side="left", padx=10)

        self.points_label = tk.Label(header, text=f"⭐ {self.data['points']}", font=("Arial", 22, "bold"), bg="#ff6bcb", fg="yellow")
        self.points_label.pack(side="right", padx=40)

        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=15)

        self.home_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.home_tab, text="🏠 Home")

        self.goals_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.goals_tab, text="🎯 My Goals")

        self.monthly_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.monthly_tab, text="📅 Monthly Plans")

        self.daily_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.daily_tab, text="✅ Daily Quests")

        self.break_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.break_tab, text="⏰ Break Time")

        self.journal_tab = ttk.Frame(self.notebook)      # Only daily journal
        self.notebook.add(self.journal_tab, text="📖 E-Journal")

        self.gratitude_tab = ttk.Frame(self.notebook)    # Separate Gratitude tab
        self.notebook.add(self.gratitude_tab, text="❤️ Gratitude")

        self.create_home_tab()
        self.create_goals_tab()
        self.create_monthly_tab()
        self.create_daily_tab()
        self.create_break_tab()
        self.create_journal_tab()
        self.create_gratitude_tab()

    # ==================== ONBOARDING ====================
    def show_onboarding_if_needed(self):
        if self.data.get("profile") is None:
            self.onboard_win = tk.Toplevel(self.root)
            self.onboard_win.title("Welcome to Questly!")
            self.onboard_win.geometry("520x680")
            self.onboard_win.configure(bg="#fce7f3")
            self.onboard_win.grab_set()

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

    # ==================== HOME TAB ====================
    def create_home_tab(self):
        tk.Label(self.home_tab, text="Good morning, superstar! Ready for adventures? 🌈", 
                 font=("Comic Sans MS", 26, "bold"), bg="#a5f3fc").pack(pady=40)
        
        btn_frame = tk.Frame(self.home_tab, bg="#a5f3fc")
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="🚀 Start Today's Quest", font=("Arial", 16, "bold"), bg="#10b981", fg="white", width=25, height=2,
                  command=self.start_day).pack(side="left", padx=15)
        tk.Button(btn_frame, text="🌅 Get Morning Affirmation", font=("Arial", 16, "bold"), bg="#8b5cf6", fg="white", width=25, height=2,
                  command=self.show_morning_affirmation).pack(side="left", padx=15)

    # ==================== GOALS TAB ====================
    def create_goals_tab(self):
        tk.Label(self.goals_tab, text="🎯 My Big Goals", font=("Comic Sans MS", 24, "bold")).pack(pady=20)

        tk.Label(self.goals_tab, text="Weekly Goals", font=("Arial", 14, "bold")).pack(anchor="w", padx=40, pady=(10,5))
        self.weekly_entry = tk.Entry(self.goals_tab, font=("Arial", 12), width=60)
        self.weekly_entry.pack(padx=40, pady=5)
        tk.Button(self.goals_tab, text="Add Weekly Goal", bg="#ec4899", fg="white", command=self.add_weekly_goal).pack(pady=5)

        tk.Label(self.goals_tab, text="Monthly Goals", font=("Arial", 14, "bold")).pack(anchor="w", padx=40, pady=(20,5))
        self.monthly_entry = tk.Entry(self.goals_tab, font=("Arial", 12), width=60)
        self.monthly_entry.pack(padx=40, pady=5)
        tk.Button(self.goals_tab, text="Add Monthly Goal", bg="#ec4899", fg="white", command=self.add_monthly_goal).pack(pady=5)

        tk.Label(self.goals_tab, text="Annual Goals (Big Dreams)", font=("Arial", 14, "bold")).pack(anchor="w", padx=40, pady=(20,5))
        self.annual_entry = tk.Entry(self.goals_tab, font=("Arial", 12), width=60)
        self.annual_entry.pack(padx=40, pady=5)
        tk.Button(self.goals_tab, text="Add Annual Goal", bg="#ec4899", fg="white", command=self.add_annual_goal).pack(pady=5)

        self.goals_display = tk.Frame(self.goals_tab, bg="white")
        self.goals_display.pack(fill="both", expand=True, padx=40, pady=20)
        self.refresh_goals_display()

    def add_weekly_goal(self):
        goal = self.weekly_entry.get().strip()
        if goal:
            self.data["goals"]["weekly"].append(goal)
            self.save_data()
            self.weekly_entry.delete(0, tk.END)
            self.refresh_goals_display()

    def add_monthly_goal(self):
        goal = self.monthly_entry.get().strip()
        if goal:
            self.data["goals"]["monthly"].append(goal)
            self.save_data()
            self.monthly_entry.delete(0, tk.END)
            self.refresh_goals_display()

    def add_annual_goal(self):
        goal = self.annual_entry.get().strip()
        if goal:
            self.data["goals"]["annual"].append(goal)
            self.save_data()
            self.annual_entry.delete(0, tk.END)
            self.refresh_goals_display()

    def refresh_goals_display(self):
        for widget in self.goals_display.winfo_children():
            widget.destroy()
        tk.Label(self.goals_display, text="Your Current Goals:", font=("Arial", 14, "bold")).pack(anchor="w", pady=10)

        for period, goals in self.data["goals"].items():
            if goals:
                tk.Label(self.goals_display, text=period.capitalize() + " Goals:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20)
                for g in goals:
                    tk.Label(self.goals_display, text="• " + g, font=("Arial", 11)).pack(anchor="w", padx=40)

    def show_morning_affirmation(self):
        if not self.data["goals"]["weekly"] and not self.data["goals"]["monthly"]:
            messagebox.showinfo("Morning Affirmation", "You are brave, kind, and capable of amazing things! 🌟")
            return

        affirmations = []
        for goal in self.data["goals"]["weekly"][:2]:
            affirmations.append(f"You are getting closer to your goal: {goal}")
        for goal in self.data["goals"]["monthly"][:1]:
            affirmations.append(f"Keep going! Your monthly dream '{goal}' is possible.")

        msg = "🌅 Good morning!\n\n" + "\n\n".join(affirmations[:3])
        messagebox.showinfo("Morning Affirmation", msg)

    # ==================== DAILY QUESTS ====================
    def create_daily_tab(self):
        tk.Label(self.daily_tab, text="Today’s Epic Quests ✨", font=("Comic Sans MS", 24, "bold")).pack(pady=20)
        btn_frame = tk.Frame(self.daily_tab)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Get Smart Suggestions from Goals", bg="#10b981", fg="white", 
                  command=self.suggest_from_goals).pack(side="left", padx=10)
        tk.Button(btn_frame, text="+ Add Custom Quest", bg="#ec4899", fg="white", 
                  command=self.add_custom_quest).pack(side="left", padx=10)

        self.daily_list = tk.Frame(self.daily_tab, bg="white")
        self.daily_list.pack(fill="both", expand=True, padx=30, pady=10)
        self.refresh_daily()

    def suggest_from_goals(self):
        suggestions = []
        for goal in self.data["goals"]["weekly"][:2]:
            suggestions.append(f"Work on: {goal}")
        for goal in self.data["goals"]["monthly"][:1]:
            suggestions.append(f"Step toward: {goal}")
        if not suggestions:
            suggestions = ["Practice something new today", "Help someone at home"]
        
        for sug in suggestions:
            self.data["daily_quests"].append({"text": sug, "completed": False})
        self.save_data()
        self.refresh_daily()
        messagebox.showinfo("Smart Suggestions", "Added goal-based quests for you!")

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
        self.save_data()
        self.points_label.config(text=f"⭐ {self.data['points']}")

    # ==================== MONTHLY PLANS ====================
    def create_monthly_tab(self):
        tk.Label(self.monthly_tab, text="Big Monthly Dreams 📅", font=("Comic Sans MS", 24, "bold")).pack(pady=20)
        tk.Button(self.monthly_tab, text="+ Add New Monthly Goal", font=("Arial", 12), bg="#ec4899", fg="white",
                  command=self.add_monthly_plan).pack(pady=10)
        self.monthly_list = tk.Frame(self.monthly_tab, bg="white")
        self.monthly_list.pack(fill="both", expand=True, padx=30, pady=10)
        self.refresh_monthly()

    def add_monthly_plan(self):
        title = simpledialog.askstring("New Goal", "What is your big dream this month?")
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

    # ==================== BREAK TIME ====================
    def create_break_tab(self):
        tk.Label(self.break_tab, text="Need a break, superstar? 🧘", font=("Comic Sans MS", 24, "bold")).pack(pady=40)
        self.timer_label = tk.Label(self.break_tab, text="45:00", font=("Arial", 48, "bold"), fg="#14b8a6")
        self.timer_label.pack(pady=30)
        tk.Button(self.break_tab, text="Start 45-min Focus Timer", font=("Arial", 14), bg="#14b8a6", fg="white",
                  command=self.start_focus_timer).pack(pady=10)

    def start_focus_timer(self):
        messagebox.showinfo("Timer", "Focus timer started! (Demo version)")

    def start_day(self):
        messagebox.showinfo("Adventure Time!", "Your day has officially started! Go complete some quests!")

    # ==================== E-JOURNAL TAB ====================
    def create_journal_tab(self):
        tk.Label(self.journal_tab, text="📖 My E-Journal", font=("Comic Sans MS", 24, "bold")).pack(pady=15)

        tk.Button(self.journal_tab, text="🔔 Morning Reminder: Record in Journal", bg="#8b5cf6", fg="white", 
                  font=("Arial", 12), command=self.morning_journal_reminder).pack(pady=8)

        tk.Button(self.journal_tab, text="🌙 Evening Reminder: Gratitude Time", bg="#f97316", fg="white", 
                  font=("Arial", 12), command=self.evening_gratitude_reminder).pack(pady=8)

        tk.Label(self.journal_tab, text="Write about your day:", font=("Arial", 14, "bold")).pack(anchor="w", padx=40, pady=(25,5))
        self.journal_text = tk.Text(self.journal_tab, height=14, font=("Arial", 12), wrap="word")
        self.journal_text.pack(fill="x", padx=40, pady=10)

        tk.Button(self.journal_tab, text="Save Journal Entry ✨", bg="#ec4899", fg="white", font=("Arial", 14),
                  command=self.save_journal).pack(pady=15)

    def morning_journal_reminder(self):
        messagebox.showinfo("Morning Reminder", 
            "🌞 Good morning! Time to write in your E-Journal.\n\nWhat are you looking forward to today?")

    def evening_gratitude_reminder(self):
        messagebox.showinfo("Evening Reminder", 
            "🌙 Evening time!\nIt's gratitude time.\n\nWhat 3 things made you happy today?")

    def save_journal(self):
        text = self.journal_text.get("1.0", tk.END).strip()
        if text:
            today = datetime.now().strftime("%Y-%m-%d")
            self.data["journal"][today] = text
            self.save_data()
            messagebox.showinfo("Saved", "Journal entry saved successfully! 📖")

    # ==================== SEPARATE GRATITUDE TAB ====================
    def create_gratitude_tab(self):
        tk.Label(self.gratitude_tab, text="❤️ 3 Things I'm Grateful For Today", 
                 font=("Comic Sans MS", 24, "bold")).pack(pady=30)

        tk.Label(self.gratitude_tab, text="1.", font=("Arial", 14, "bold")).pack(anchor="w", padx=60, pady=(10,5))
        self.grat1 = tk.Text(self.gratitude_tab, height=4, font=("Arial", 12), wrap="word")
        self.grat1.pack(fill="x", padx=60, pady=5)

        tk.Label(self.gratitude_tab, text="2.", font=("Arial", 14, "bold")).pack(anchor="w", padx=60, pady=(15,5))
        self.grat2 = tk.Text(self.gratitude_tab, height=4, font=("Arial", 12), wrap="word")
        self.grat2.pack(fill="x", padx=60, pady=5)

        tk.Label(self.gratitude_tab, text="3.", font=("Arial", 14, "bold")).pack(anchor="w", padx=60, pady=(15,5))
        self.grat3 = tk.Text(self.gratitude_tab, height=4, font=("Arial", 12), wrap="word")
        self.grat3.pack(fill="x", padx=60, pady=5)

        tk.Button(self.gratitude_tab, text="Save Gratitude ❤️", bg="#10b981", fg="white", font=("Arial", 16, "bold"),
                  command=self.save_gratitude).pack(pady=40)

    def save_gratitude(self):
        g1 = self.grat1.get("1.0", tk.END).strip()
        g2 = self.grat2.get("1.0", tk.END).strip()
        g3 = self.grat3.get("1.0", tk.END).strip()
        
        if g1 and g2 and g3:
            today = datetime.now().strftime("%Y-%m-%d")
            self.data["gratitude"][today] = [g1, g2, g3]
            self.save_data()
            messagebox.showinfo("Gratitude Saved", "Thank you for recording what makes you happy ❤️")
            
            # Clear fields
            self.grat1.delete("1.0", tk.END)
            self.grat2.delete("1.0", tk.END)
            self.grat3.delete("1.0", tk.END)
        else:
            messagebox.showwarning("Incomplete", "Please fill all three gratitude items ❤️")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = QuestlyApp()
    app.run()