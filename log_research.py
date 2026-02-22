import re
from collections import Counter, defaultdict
from datetime import datetime
import json
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

LOG_PATH = "syst_comp/system_log.log"

LOG_LINE_REGEX = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - "
    r"(?P<level>\w+) - \[(?P<sim_time>[\d.]+)\] - (?P<message>.+)"
)

def parse_log(filepath):
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            match = LOG_LINE_REGEX.match(line)
            if match:
                data = match.groupdict()
                data["datetime"] = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S,%f")
                data["sim_time"] = float(data["sim_time"])
                entries.append(data)
    return entries

def analyze(entries):
    level_counts = Counter(e["level"] for e in entries)
    messages_by_level = defaultdict(list)
    sim_times = [e["sim_time"] for e in entries]
    timestamps = [e["datetime"] for e in entries]

    for e in entries:
        messages_by_level[e["level"]].append(e["message"])

    report = {
        "total_entries": len(entries),
        "levels": dict(level_counts),
        "errors": messages_by_level.get("ERROR", []),
        "warnings": messages_by_level.get("WARNING", []),
        "sim_time_range": (min(sim_times), max(sim_times)) if sim_times else (0, 0),
        "real_time_range": (
            timestamps[0].strftime("%Y-%m-%d %H:%M:%S") if timestamps else "",
            timestamps[-1].strftime("%Y-%m-%d %H:%M:%S") if timestamps else "",
        ),
    }

    return report


def show_details(entry):
    top = Toplevel()
    top.title("Log Entry Details")
    top.geometry("600x350")

    text = Text(top, wrap=WORD, font=("Consolas", 11), bg="#1e1e1e", fg="white")
    text.pack(expand=True, fill=BOTH)

    # Подсветка
    for level in ["INFO", "WARNING", "ERROR", "SYSTEM", "DEBUG", "TRACE"]:
        text.tag_config(f"level_{level}", foreground="blue")  # серый по умолчанию

    # А потом переопредели основные:
    text.tag_config("level_INFO", foreground="#569CD6")
    text.tag_config("level_WARNING", foreground="#DCDCAA")
    text.tag_config("level_ERROR", foreground="#F44747")
    text.tag_config("level_SYSTEM", foreground="#00C896")

    def insert_tagged(label, value, tag=None):
        text.insert(END, f"{label}: ", ("label",))
        text.insert(END, f"{value}\n", tag)

    insert_tagged("Timestamp", entry["datetime"], "timestamp")  # fix: use 'datetime'
    insert_tagged("Level", entry["level"], f"level_{entry['level']}")
    insert_tagged("Sim Time", entry["sim_time"], "simtime")
    text.insert(END, "Message:\n", ("label",))
    text.insert(END, entry["message"], ())

    text.config(state=DISABLED)


    # Вставка текста с подсветкой
    def insert_tagged(label, value, tag=None):
        text.insert(END, f"{label}: ", ("label",))
        text.insert(END, f"{value}\n", tag)

    insert_tagged("Timestamp", entry["timestamp"], "timestamp")
    insert_tagged("Level", entry["level"], f"level_{entry['level']}")
    insert_tagged("Sim Time", entry["sim_time"], "simtime")
    text.insert(END, "Message:\n", ("label",))
    text.insert(END, entry["message"], ())

    text.config(state=DISABLED)


def log_search_tool(entries):
    def filter_logs(*args):
        keyword = search_var.get().lower()
        level = level_var.get()
        tree.delete(*tree.get_children())
        for i, entry in enumerate(entries):
            if (keyword in entry["message"].lower()) and (level == "ALL" or entry["level"] == level):
                tree.insert(
                    "",
                    "end",
                    iid=str(i),
                    values=(entry["timestamp"], entry["level"], entry["message"][:80]),
                    tags=(entry["level"],)
                )

    def on_double_click(event):
        item_id = tree.selection()
        if item_id:
            entry = entries[int(item_id[0])]
            show_details(entry)

    root = Tk()
    root.title("🔍 Log Search Tool")
    root.geometry("800x600")

    try:
        img = Image.open("icons/interface/research.png").resize((32, 32))
        root.iconphoto(True, ImageTk.PhotoImage(img))
    except:
        pass

    # Controls
    top_frame = Frame(root)
    top_frame.pack(fill=X, padx=10, pady=5)

    ttk.Label(top_frame, text="🔍 Search:", font=("Arial", 10)).pack(side=LEFT)
    search_var = StringVar()
    search_entry = Entry(top_frame, textvariable=search_var, width=30)
    search_entry.pack(side=LEFT, padx=5)

    ttk.Label(top_frame, text="📁 Level:", font=("Arial", 10)).pack(side=LEFT, padx=(20, 5))
    level_var = StringVar(value="ALL")
    level_menu = ttk.Combobox(top_frame, textvariable=level_var, values=["ALL", "INFO", "WARNING", "ERROR", "SYSTEM"])
    level_menu.pack(side=LEFT)
    level_menu.bind("<<ComboboxSelected>>", filter_logs)

    ttk.Button(top_frame, text="🔄 Update", command=filter_logs).pack(side=LEFT, padx=10)

    # Treeview
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True)

    columns = ("timestamp", "level", "message")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.heading("timestamp", text="⏱ Время")
    tree.heading("level", text="⚠️ Уровень")
    tree.heading("message", text="💬 Сообщение")

    tree.column("timestamp", width=150)
    tree.column("level", width=80, anchor="center")
    tree.column("message", width=520)
    tree.tag_configure("INFO", foreground="blue")
    tree.tag_configure("WARNING", foreground="orange")
    tree.tag_configure("ERROR", foreground="red")
    tree.tag_configure("SYSTEM", foreground="darkblue")

    vsb = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=vsb.set)
    vsb.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)

    tree.bind("<Double-1>", on_double_click)

    filter_logs()
    root.mainloop()

# Основной запуск
entries = parse_log(LOG_PATH)
report = analyze(entries)
save_report = lambda r: json.dump(r, open("log_report.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
save_report(report)

log_search_tool(entries)
