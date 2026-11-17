"""
Anjee_Tamang_agent.py  -  Study Break Agent (a SIMPLE REFLEX AGENT)

Student : Anjee Tamang
Agent   : B. Study break agent
Course  : Artificial Intelligence, Semester V - Quest International College

    sense (minutes studied, tiredness)  ->  decide (rules)  ->  Keep going / Break / Sleep

Percept : minutes studied without a break (0-180) and tiredness (0-100)
Actions : "Keep going", "Break", "Sleep"
Type    : simple reflex agent (decides from the CURRENT percept only, no memory)

Run:    python Anjee_Tamang_agent.py          (needs Python 3 with Tkinter)
Test:   python Anjee_Tamang_agent.py --test   (runs the backend tests, no window)

Controls
    Minutes slider      set how long the student has studied without a break
    Tiredness slider    set how tired the student feels
    "Let the agent act" the agent's action is applied to the world (one step)
    "Auto mode"         the agent keeps acting by itself, step after step
"""
import sys
import tkinter as tk

# --------------------------------------------------------------------------
# 1. BACKEND LOGIC  (no GUI code in this section)
# --------------------------------------------------------------------------

# Thresholds used by the rules. Kept as named constants so the rules are easy
# to read and to change.
SLEEP_TIREDNESS = 80      # above this the student is exhausted -> Sleep
BREAK_MINUTES = 50        # studied this long (or more) without a break -> Break
BREAK_TIREDNESS = 60      # above this the student is tired -> Break


class StudyBreakAgent:
    """The agent program: percept (minutes, tiredness) in, action out."""

    def decide(self, minutes, tiredness):
        # Rule 1: very tired (tiredness > 80). Rest properly: Sleep.
        # This rule is checked FIRST because it is the most urgent one.
        if tiredness > SLEEP_TIREDNESS:
            return "Sleep"

        # Rule 2: studied 50 minutes or more without stopping. Take a Break.
        if minutes >= BREAK_MINUTES:
            return "Break"

        # Rule 3: getting tired (tiredness > 60) even though the session is
        # still short. Take a Break before it gets worse.
        if tiredness > BREAK_TIREDNESS:
            return "Break"

        # Rule 4: fresh and not studied for long. Keep going.
        return "Keep going"


class Environment:
    """The world: a student who studies, gets tired, and can rest."""

    def __init__(self):
        self.minutes = 20          # minutes studied since the last break (0-180)
        self.tiredness = 30        # tiredness, 0 (fresh) to 100 (exhausted)
        self.action = "Keep going" # last action chosen by the agent
        self.breaks = 0            # score counter: how many breaks were taken
        self.sleeps = 0            # score counter: how many times the student slept

    def apply(self, action):
        """Change the world according to the agent's action (one time step)."""
        self.action = action
        if action == "Keep going":
            # Studying 5 more minutes makes the student a little more tired.
            self.minutes = min(180, self.minutes + 5)
            self.tiredness = min(100, self.tiredness + 4)
        elif action == "Break":
            # A short break resets the study timer and lowers tiredness.
            self.minutes = 0
            self.tiredness = max(0, self.tiredness - 25)
            self.breaks += 1
        elif action == "Sleep":
            # Sleep resets the timer and makes the student fresh again.
            self.minutes = 0
            self.tiredness = 10
            self.sleeps += 1


# --------------------------------------------------------------------------
# 2. BACKEND TESTS  (run with:  python Anjee_Tamang_agent.py --test)
# --------------------------------------------------------------------------

def run_tests():
    """Check the agent on different inputs, including the edge values."""
    agent = StudyBreakAgent()
    # (minutes, tiredness, expected action)
    cases = [
        (10, 20, "Keep going"),   # fresh and short session
        (49, 60, "Keep going"),   # just below both Break limits
        (50, 20, "Break"),        # edge: exactly 50 minutes -> Break
        (20, 61, "Break"),        # edge: tiredness just above 60 -> Break
        (20, 80, "Break"),        # edge: 80 is NOT above 80, so not Sleep
        (20, 81, "Sleep"),        # edge: tiredness just above 80 -> Sleep
        (120, 90, "Sleep"),       # Sleep rule beats the Break rule
    ]
    print(f"{'minutes':>8} {'tired':>6}  {'expected':<11} {'agent gave':<11} ok?")
    for minutes, tired, expected in cases:
        got = agent.decide(minutes, tired)
        print(f"{minutes:>8} {tired:>6}  {expected:<11} {got:<11} {'Yes' if got == expected else 'NO'}")


# --------------------------------------------------------------------------
# 3. GUI  (drawing and user input)
# --------------------------------------------------------------------------

# Colour palette
BG, PANEL, INK, MUTED = "#0B1F3A", "#132B4D", "#E6EEF8", "#9FB4D1"
TEAL, AMBER, RED, GREEN = "#00A7A0", "#F2A33A", "#E5484D", "#3DD68C"

# One colour per action so the user can see the decision at a glance
ACTION_COLOUR = {"Keep going": GREEN, "Break": AMBER, "Sleep": RED}


class StudyBreakApp:
    AUTO_MS = 700              # time between steps in Auto mode
    W, H = 640, 330            # canvas size

    def __init__(self, root):
        self.root = root
        self.env = Environment()
        self.agent = StudyBreakAgent()

        root.title("Study Break Agent - Anjee Tamang")
        root.configure(bg=BG)
        root.resizable(True, True)
        root.minsize(700, 580)
        self.fullscreen = False
        root.bind("<F11>", self.toggle_fullscreen)
        root.bind("<Escape>", lambda e: self.toggle_fullscreen(leave=True))

        # --- titles ---
        tk.Label(root, text="Study Break Agent  (simple reflex)", bg=BG, fg=INK,
                 font=("Helvetica", 16, "bold")).pack(pady=(10, 0))
        tk.Label(root, text="percept: minutes studied + tiredness   →   rules   →   "
                            "action: Keep going / Break / Sleep",
                 bg=BG, fg=MUTED, font=("Helvetica", 10)).pack()

        # --- drawing area (must exist before the sliders call on_change) ---
        self.canvas = tk.Canvas(root, width=self.W, height=self.H, bg=PANEL, highlightthickness=0)
        self.canvas.pack(padx=12, pady=10, fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw())

        # --- controls: the user changes the world here ---
        box = tk.Frame(root, bg=BG)
        box.pack(pady=(0, 6))

        tk.Label(box, text="Minutes studied", bg=BG, fg=INK).grid(row=0, column=0, sticky="e", padx=6)
        self.minutes_slider = tk.Scale(box, from_=0, to=180, orient="horizontal", length=300,
                                       command=self.on_change, bg=BG, fg=INK,
                                       troughcolor=PANEL, highlightthickness=0)
        self.minutes_slider.set(self.env.minutes)
        self.minutes_slider.grid(row=0, column=1)

        tk.Label(box, text="Tiredness (0-100)", bg=BG, fg=INK).grid(row=1, column=0, sticky="e", padx=6)
        self.tired_slider = tk.Scale(box, from_=0, to=100, orient="horizontal", length=300,
                                     command=self.on_change, bg=BG, fg=INK,
                                     troughcolor=PANEL, highlightthickness=0)
        self.tired_slider.set(self.env.tiredness)
        self.tired_slider.grid(row=1, column=1)

        # Button: let the agent's chosen action change the world
        tk.Button(box, text="Let the agent act", command=self.step, width=18,
                  bg=PANEL, fg=INK, activebackground=TEAL, activeforeground=INK,
                  relief="flat").grid(row=0, column=2, padx=14)

        # Checkbox: Auto mode (optional extension)
        self.auto_var = tk.BooleanVar(value=False)
        tk.Checkbutton(box, text="Auto mode (agent acts by itself)", variable=self.auto_var,
                       command=self.on_auto_toggle, bg=BG, fg=INK, selectcolor=PANEL,
                       activebackground=BG, activeforeground=INK).grid(row=1, column=2, padx=14)

        tk.Label(root, text="Keys: Space = let the agent act", bg=BG, fg=MUTED,
                 font=("Helvetica", 10)).pack(pady=(0, 10))
        root.bind("<space>", lambda e: self.step())

        self.on_change()           # first sense -> decide -> draw

    def toggle_fullscreen(self, _event=None, leave=False):
        """Toggle full-screen view; Escape always returns to windowed view."""
        self.fullscreen = False if leave else not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    # ----- user input -----
    def on_change(self, *_):
        """The user moved a slider: SENSE the new world and DECIDE again."""
        self.env.minutes = self.minutes_slider.get()      # SENSE
        self.env.tiredness = self.tired_slider.get()
        self.env.action = self.agent.decide(self.env.minutes, self.env.tiredness)   # DECIDE
        self.draw()

    def step(self):
        """ACT: apply the agent's action to the world, then sense again."""
        self.env.apply(self.env.action)                   # ACT
        self.minutes_slider.set(self.env.minutes)         # show the new world on the sliders
        self.tired_slider.set(self.env.tiredness)
        self.on_change()                                  # SENSE + DECIDE again

    def on_auto_toggle(self):
        """Start the auto loop when the checkbox is ticked."""
        if self.auto_var.get():
            self.auto_tick()

    def auto_tick(self):
        """Auto mode: act, then schedule the next step while the box is ticked."""
        if self.auto_var.get():
            self.step()
            self.root.after(self.AUTO_MS, self.auto_tick)

    # ----- drawing -----
    def draw(self):
        c, env = self.canvas, self.env
        c.delete("all")
        action = env.action
        colour = ACTION_COLOUR[action]

        # --- the student at a desk (left side) ---
        c.create_rectangle(30, 230, 330, 250, fill="#6B4A2B", outline="")          # desk top
        c.create_rectangle(50, 250, 62, 310, fill="#4A3320", outline="")           # desk legs
        c.create_rectangle(298, 250, 310, 310, fill="#4A3320", outline="")
        c.create_rectangle(110, 205, 190, 230, fill="#D8DEE9", outline="#6B7A99")  # open book
        c.create_line(150, 205, 150, 230, fill="#6B7A99")
        c.create_rectangle(140, 150, 180, 205, fill="#3F6FD8", outline="")         # body
        c.create_oval(130, 95, 190, 155, fill="#F1C7A0", outline="")               # head
        if action == "Sleep":                                                      # eyes closed + Zzz
            c.create_line(144, 122, 156, 122, width=2)
            c.create_line(164, 122, 176, 122, width=2)
            c.create_text(215, 90, text="Z z z", fill=INK, font=("Helvetica", 16, "bold"))
        else:                                                                      # eyes open
            c.create_oval(145, 117, 153, 125, fill="black")
            c.create_oval(167, 117, 175, 125, fill="black")
        # mouth: smile when fresh, flat when tired
        if env.tiredness > SLEEP_TIREDNESS:
            c.create_line(150, 142, 170, 142, width=2)
        elif env.tiredness > BREAK_TIREDNESS:
            c.create_line(150, 142, 170, 140, width=2)
        else:
            c.create_arc(148, 128, 172, 148, start=200, extent=140, style="arc", width=2)
        if action == "Break":                                                      # tea cup on the desk
            c.create_rectangle(250, 205, 280, 230, fill="#E8D8B8", outline="")
            c.create_oval(276, 210, 292, 224, outline="#E8D8B8", width=3)
            c.create_text(265, 192, text="~ ~", fill=MUTED)

        # --- readouts and rule explanation (right side) ---
        c.create_text(370, 22, anchor="w", fill=colour, font=("Helvetica", 24, "bold"),
                      text=f"ACTION: {action}")
        c.create_text(370, 62, anchor="w", fill=INK, font=("Helvetica", 12),
                      text=f"Minutes studied: {env.minutes}    Tiredness: {env.tiredness}")
        c.create_text(370, 92, anchor="nw", fill=INK, font=("Consolas", 10),
                      text=f"percept : minutes = {env.minutes}, tired = {env.tiredness}\n"
                           f"rule    : {self.which_rule()}\n"
                           f"action  : {action}")

        # --- bars: sensor value against the agent's thresholds ---
        self.draw_bar(370, 170, "Minutes studied", env.minutes, 180, [(BREAK_MINUTES, AMBER)])
        self.draw_bar(370, 220, "Tiredness", env.tiredness, 100,
                      [(BREAK_TIREDNESS, AMBER), (SLEEP_TIREDNESS, RED)])

        # --- score counters ---
        c.create_text(370, 285, anchor="w", fill=MUTED, font=("Helvetica", 11),
                      text=f"Breaks taken: {env.breaks}     Sleeps: {env.sleeps}")

    def which_rule(self):
        """Return a short text saying which rule fired (for the explanation box)."""
        m, t = self.env.minutes, self.env.tiredness
        if t > SLEEP_TIREDNESS:
            return f"R1: tired {t} > {SLEEP_TIREDNESS}  -> Sleep"
        if m >= BREAK_MINUTES:
            return f"R2: minutes {m} >= {BREAK_MINUTES} -> Break"
        if t > BREAK_TIREDNESS:
            return f"R3: tired {t} > {BREAK_TIREDNESS}  -> Break"
        return "R4: no rule above fired -> Keep going"

    def draw_bar(self, x, y, label, value, maximum, marks):
        """Draw one horizontal bar with threshold marks (value / maximum)."""
        c, width = self.canvas, 240
        c.create_text(x, y - 12, anchor="w", text=label, fill=MUTED, font=("Helvetica", 9))
        c.create_rectangle(x, y, x + width, y + 18, outline=MUTED)
        c.create_rectangle(x + 1, y + 1, x + 1 + (width - 2) * value / maximum, y + 17,
                           fill=TEAL, outline="")
        for threshold, colour in marks:                     # vertical line for each threshold
            tx = x + width * threshold / maximum
            c.create_line(tx, y - 5, tx, y + 23, fill=colour, width=3)


def main():
    root = tk.Tk()
    StudyBreakApp(root)
    root.mainloop()


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()          # backend only: no window needed
    else:
        main()
