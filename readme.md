# Study Break Agent

**Student:** Anjee Tamang
**Course:** Artificial Intelligence, Semester V, Quest International College, Kathmandu
**Instructor:** Bimochan Raj Kunwar
**Assignment:** Dashain–Tihar Vacation Assignment, *Build an Intelligent Agent* (Agent B)
**File:** `Anjee_Tamang_agent.py`

---

## 1. What this project does

The Study Break Agent watches a student who is studying. It senses **how many minutes the student has studied without a break** and **how tired the student feels**, and then decides whether the student should **keep going**, take a **break**, or **sleep**.

A Tkinter window shows the student at a desk, the two sensor readings as bars, which rule fired, and the action the agent chose. The user changes the world with sliders and watches the agent react.

The program follows the same style as the lab apps (`temperature.py`, `vacuum.py`, `tihar_lights.py`): a plain-Python **backend** (the agent and its world) kept separate from the Tkinter **frontend** (drawing and user input).

---

## 2. Requirements and how to run

| Item | Detail |
|---|---|
| Python | 3.10 or newer (Python 3 with Tkinter) |
| Libraries | Only the standard library (`tkinter`, `sys`). Nothing to install with pip |
| Platform | Windows, macOS or Linux laptop. **Tkinter does not run in Google Colab** |

**Run the app**

```bash
python Anjee_Tamang_agent.py
```

On macOS or some Linux systems use `python3` instead of `python`.

**Run the backend tests (no window)**

```bash
python Anjee_Tamang_agent.py --test
```

This prints a table of test inputs, the expected action, the action the agent gave, and whether they match.

**If Tkinter is missing**
- Windows / macOS: reinstall Python from python.org (Tkinter is included in the standard installer).
- Ubuntu / Debian: `sudo apt install python3-tk`

---

## 3. PEAS description

PEAS (Performance measure, Environment, Actuators, Sensors) describes the task before any code is written.

| | Study Break Agent |
|---|---|
| **P**erformance measure | The student keeps studying while fresh, rests before getting exhausted, and does not study for long stretches without a break |
| **E**nvironment | A student at a desk: a study timer, a tiredness level, a book, tea and sleep |
| **A**ctuators | The decision shown on screen: `Keep going`, `Break`, `Sleep` (in the simulation these change the student's minutes and tiredness) |
| **S**ensors | Minutes studied since the last break, and tiredness level |

---

## 4. Percept, actions and rules

**Percept** (what the agent senses)

| Name | Range | Meaning |
|---|---|---|
| `minutes` | 0 to 180 | Minutes studied since the last break |
| `tiredness` | 0 to 100 | 0 = fresh, 100 = exhausted |

**Actions** (what the agent can do)

| Action | Meaning |
|---|---|
| `Keep going` | Continue studying |
| `Break` | Stop for a short rest (tea, stretch, walk) |
| `Sleep` | Stop studying and rest properly |

**Rules** (checked in this order; the first rule that matches wins)

| # | Condition | Action | Why |
|---|---|---|---|
| 1 | `tiredness > 80` | `Sleep` | The student is exhausted. This is the most urgent rule, so it is checked first |
| 2 | `minutes >= 50` | `Break` | A long session without stopping |
| 3 | `tiredness > 60` | `Break` | The student is getting tired even though the session is still short |
| 4 | none of the above | `Keep going` | Fresh and not studied for long |

**Thresholds** are named constants at the top of the backend, so they are easy to change:

```python
SLEEP_TIREDNESS = 80
BREAK_MINUTES = 50
BREAK_TIREDNESS = 60
```

### Why the rule order matters

The rules are checked from top to bottom. If Rule 2 came before Rule 1, a student with `minutes = 60` and `tiredness = 90` would get `Break` when `Sleep` is the better action. Putting the most urgent rule first fixes this.

---

## 5. Agent type

**Simple reflex agent.**

1. It chooses its action using **only the current percept** (minutes and tiredness right now) and condition–action rules.
2. It keeps **no memory** of earlier readings. For example, `minutes = 20, tiredness = 85` always gives `Sleep`, whatever happened before.
3. It has **no goal it plans for** and does not score outcomes, so it is not goal-based or utility-based.

A model-based version would remember earlier readings (like Program 4 in the lab) and ignore a single sudden spike in tiredness.

---

## 6. How the program is organised

The file has three sections, with no GUI code in the first two.

```
Anjee_Tamang_agent.py
├── 1. BACKEND LOGIC
│   ├── constants           SLEEP_TIREDNESS, BREAK_MINUTES, BREAK_TIREDNESS
│   ├── StudyBreakAgent     decide(minutes, tiredness) -> action
│   └── Environment         the world: minutes, tiredness, counters, apply(action)
├── 2. BACKEND TESTS        run_tests()  (python file.py --test)
└── 3. GUI (Tkinter)
    └── StudyBreakApp       window, sliders, drawing, the sense-decide-act loop
```

### The agent loop: sense → decide → act

```
   user moves a slider
          │
          ▼
   SENSE    on_change() reads minutes and tiredness from the sliders
          │
          ▼
   DECIDE   StudyBreakAgent.decide(minutes, tiredness)  ->  action
          │
          ▼
   DRAW     the window shows percept, rule, action and the student
          │
   user presses "Let the agent act" (or Space, or Auto mode)
          ▼
   ACT      Environment.apply(action) changes the world
          │
          └──► sliders update ──► SENSE again
```

### How each action changes the world (`Environment.apply`)

| Action | Minutes | Tiredness | Counter |
|---|---|---|---|
| `Keep going` | +5 (max 180) | +4 (max 100) | none |
| `Break` | reset to 0 | −25 (min 0) | `breaks` + 1 |
| `Sleep` | reset to 0 | set to 10 | `sleeps` + 1 |

---

## 7. Using the window

| Control | What it does |
|---|---|
| **Minutes studied** slider | Sets the minutes studied (0 to 180). The agent decides again at once |
| **Tiredness** slider | Sets the tiredness (0 to 100). The agent decides again at once |
| **Let the agent act** button (or **Space**) | Applies the agent's current action to the world for one step |
| **Auto mode** checkbox | The agent acts by itself every 0.7 seconds until you untick it |
| **F11** | Full screen on / off |
| **Esc** | Leave full screen |

**What you see on the canvas**

- The student at a desk. Eyes close and "Z z z" appears on `Sleep`; a tea cup appears on `Break`. The mouth goes from a smile to a flat line as tiredness rises.
- The big coloured text `ACTION: ...` (green = Keep going, amber = Break, red = Sleep).
- An explanation box with the percept, the rule that fired, and the action.
- Two bars (minutes and tiredness) with coloured lines at the thresholds (amber at 50 minutes, amber at 60 and red at 80 tiredness).
- Counters for breaks taken and sleeps.

### Window size: maximize, minimize and resize

- The window can be **minimized**, **maximized** and **resized** with the normal window buttons or by dragging the edges.
- The drawing **scales to fit** the window, keeping its proportions, and the text grows and shrinks with it.
- The window has a minimum size (700 × 580) so the controls are never cut off.
- Press **F11** for full screen and **Esc** to leave it.

---

## 8. Testing

Run `python Anjee_Tamang_agent.py --test`. The tests cover normal inputs and the **edge values**, where mistakes usually hide.

| # | Minutes | Tiredness | Expected | Why |
|---|---|---|---|---|
| 1 | 10 | 20 | Keep going | Fresh, short session |
| 2 | 49 | 60 | Keep going | Just below both Break limits |
| 3 | 50 | 20 | Break | Edge: exactly 50 minutes (`>=`) |
| 4 | 20 | 61 | Break | Edge: tiredness just above 60 |
| 5 | 20 | 80 | Break | Edge: 80 is **not** above 80, so not Sleep (Rule 3 gives Break) |
| 6 | 20 | 81 | Sleep | Edge: tiredness just above 80 |
| 7 | 120 | 90 | Sleep | Sleep rule beats the Break rule |

All seven cases give the expected action.

**Manual GUI check:** move each slider to the same values above and confirm the action text and rule box match the table.

---

## 9. Assignment checklist

| Requirement | Where in the program |
|---|---|
| Percept and actions named clearly | Module docstring, section 4 of this README |
| At least 3 rules | 4 rules in `StudyBreakAgent.decide`, each with a comment |
| Backend separate from GUI | `StudyBreakAgent` and `Environment` have no Tkinter code; `StudyBreakApp` only draws and takes input |
| GUI shows percept, action and state | Text, rule box, bars and the student drawing |
| User can change the world | Two sliders, the "Let the agent act" button, Space key, Auto mode |
| Tested on 5 or more inputs | `--test` runs 7 inputs, including edge values |
| Comments explain each rule | A comment above every rule in `decide` |
| Agent type note | Section 5 of this README |
| Optional extension | Auto mode, break and sleep counters |
| Runs with `python yourfile.py` | Yes |

---

## 10. Ideas for improving it

- **Memory (model-based):** remember the last few tiredness readings so one wrong reading does not trigger `Sleep`.
- **Time of day:** add a third percept so the agent suggests `Sleep` at night.
- **Utility-based version:** score each action (focus gained against tiredness added) and choose the best one.
- **Adjustable thresholds:** add sliders for the 50, 60 and 80 limits, like the threshold slider in `tihar_lights.py`.

---

## 11. Notes

- This is individual work for the Dashain–Tihar assignment. The structure follows the style of the lab examples, but the agent, rules, world and drawing are my own.
- The numbers (50 minutes, 60 and 80 tiredness) are design choices for this simulation, not medical advice.