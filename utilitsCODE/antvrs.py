import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog,scrolledtext
from PIL import Image, ImageTk
from logtofile import log_to_file
from plyer import notification

viruses = []
names = ["Virus","Trojan32"]
name_virus = ""
def open_antv(actives_programs, root, lang, color, special_frames, start_time_,GlobalAlpha):
    actives_programs.append("Antivirus")
    global viruses, name_virus

    known_files = ["sh.dat", "t00r.dat", "001.dat"]

    log_to_file("Antivirus launch", start_time_=start_time_)

    def delete_vrs(path):
        total_path = path
        if os.path.exists(total_path):
            os.remove(total_path)
            messagebox.showinfo(lang['success'], lang["virus_deleted"])
        else:
            messagebox.showwarning(lang['warning'], lang['path_not_exists'])
    def scan_folder():
        viruses.clear()
        scanned_files_text.delete("1.0", END)

        folder_selected = os.getcwd()  # 📁 Текущая директория

        file_paths = []
        for dirpath, _, files in os.walk(folder_selected):
            for file in files:
                file_path = os.path.join(dirpath, file)
                file_paths.append(file_path)

        progress_bar.config(mode="determinate", maximum=len(file_paths))

        for i, path in enumerate(file_paths):
            scanned_files_text.insert(END, path + "\n")
            scanned_files_text.see(END)
            scanned_files_text.update()

            progress_bar['value'] = i
            roott.update_idletasks()

            if os.path.basename(path) in known_files:
                viruses.append(path)
                log_to_file(f"Virus (known file) found: {path}", start_time_=start_time_)

                try:
                    notification.notify(
                        title=lang["virus_detected"],
                        message=f"{lang['virus_detected']}: {path}",
                        timeout=5
                    )
                except Exception as e:
                    log_to_file(f"Notification error: {e}", level="error", start_time_=start_time_)

        if viruses:
            messagebox.showwarning(lang["virus_detected"], "\n".join(viruses))
            w = Toplevel(roott)
            w.attributes("-alpha", float(GlobalAlpha))
            w.title("Antivirus")
            w.geometry("600x300")
            vrs_type = ""
            if known_files[0] in viruses[0]:
                vrs_type = 'Malware'
            if known_files[1] in viruses[0]:
                vrs_type = 'Trojan32'
            if known_files[2] in viruses[0]:
                vrs_type = 'Trojan32'
            Label(w, text=f"{lang['virus_detected']}", font=("Arial", 13, "bold"), fg="black").pack()
            Label(w, text=f"{lang['vrs_path']}: {viruses[0]}", font=("Arial", 13, "bold"), fg="red").pack()
            Label(w, text=f"{lang['vrs_type']}: {vrs_type}", font=("Arial", 13, "bold"), fg="red").pack()
            ttk.Button(w, text=lang["delete_virus"], command=lambda: delete_vrs(viruses[0])).pack()
        else:
            messagebox.showinfo(lang["security"], lang["file_not_found"])
    def exit_program():
        log_to_file("Exiting antivirus", start_time_=start_time_)
        roott.destroy()

    # --- UI ---
    roott = Toplevel(root)
    roott.attributes("-alpha", float(GlobalAlpha))
    roott.title("Windoors Defender 52")
    roott.geometry("750x650")
    roott.configure(bg="#2C3E50")

    try:
        img = Image.open("icons/antivirus.png")
        icon_image = ImageTk.PhotoImage(img)
        roott.iconphoto(False, icon_image)
    except:
        pass

    style = ttk.Style()
    style.configure("Accent.TButton", font=("Arial", 12, "bold"), padding=6)

    frame = Frame(roott, bg="#2C3E50")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame, text=lang["defender"], font=("Arial", 16, "bold"),
              background="#2C3E50", foreground="white").pack(pady=10)

    ttk.Button(frame, text=lang["scan_folder"], style="Accent.TButton", command=scan_folder).pack(pady=10)

    scanned_files_text = scrolledtext.ScrolledText(frame, height=15, width=80, wrap="none")
    scanned_files_text.pack(pady=10, fill="both", expand=True)

    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
    progress_bar.pack(pady=10)

    ttk.Button(frame, text=lang["exit"], style="Accent.TButton", command=exit_program).pack(pady=10)

