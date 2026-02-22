import re
from collections import Counter, defaultdict
from datetime import datetime
import json
from tkinter import *
from PIL import Image, ImageTk
LOG_PATH = "syst_comp/system_log.log"

LOG_LINE_REGEX = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - "
    r"(?P<level>\w+) - \[(?P<sim_time>[\d.]+)\] - (?P<message>.+)"
)

Win = Tk()
Win.geometry("600x500")
Win.title("SVB Log Viewer")
Win.resizable(False, False)
image = Image.open("icons/log-format.png")
icon_image = ImageTk.PhotoImage(image)
Win.icon_img_ref = icon_image
Win.iconphoto(True, Win.icon_img_ref)
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

def print_report(report):
    Label(Win, text="📊 LOG ANALYSIS REPORT",font=("Arial",20,"bold"),fg="darkblue").pack()
    Label(Win, text="=" * 60).pack()
    Label(Win, text=f"Total log entries: {report['total_entries']}",font=("Arial",20,"bold")).pack()
    Label(Win, text="Log levels:",font=("Arial",20,)).pack()
    for level, count in report['levels'].items():
        if level == "SYSTEM":
            Label(Win, text=f"  {level}: {count}",font=("Arial",13,"bold"),fg = "blue").pack()
        elif level == "INFO":
            Label(Win, text=f"  {level}: {count}", font=("Arial", 13, "bold"),fg="blue").pack()
        elif level == "WARNING":
            Label(Win, text=f"  {level}: {count}", font=("Arial", 13, "bold"),fg="orange").pack()
        else:
            Label(Win, text=f"  {level}: {count}", font=("Arial", 13, "bold"),fg="red").pack()
    Label(Win, text=f"Simulated time range: {report['sim_time_range'][0]}s → {report['sim_time_range'][1]}s", font=("Arial", 13, "bold")).pack()
    Label(Win, text=f"Real time range: {report['real_time_range'][0]} → {report['real_time_range'][1]}", font=("Arial", 13, "bold")).pack()

def save_report(report, filename="log_report.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

# запуск анализа
logs = parse_log(LOG_PATH)
report = analyze(logs)
print_report(report)
save_report(report)

Win.mainloop()
