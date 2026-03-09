from tkinter import *
from tkinter import filedialog
import re
from PIL import Image, ImageTk
from logtofile import log_to_file
from play_sound import play_sound

LANGUAGES = {
    "Python": {
        "icon": "icons/file_icons/py.png",
        "ext": "*.py",
        "rules": {
            "kw": (r"\b(def|class|if|else|elif|for|while|return|import|from|as|try|except|with|lambda|pass|break|continue)\b", "#569CD6"),
            "str": (r'"[^"\n]*"|\'[^\']*\'', "#CE9178"),
            "com": (r"#.*", "gray"),
            "num": (r"\b\d+(\.\d+)?\b", "#B5CEA8"),
        }
    },
    "C++": {
        "icon": "icons/file_icons/cpp.png",
        "ext": "*.cpp",
        "rules": {
            "kw": (r"\b(int|float|double|char|bool|void|class|struct|public|private|protected|return|if|else|for|while|switch|case|namespace|using|new|delete|const|static|virtual|override)\b", "#569CD6"),
            "prep": (r"#include|#define", "#C586C0"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+\b", "#B5CEA8"),
        }
    },
    "C": {
        "icon": "icons/file_icons/c.png",
        "ext": "*.c",
        "rules": {
            "kw": (r"\b(int|float|double|char|void|return|if|else|for|while|switch|case|struct|typedef|static)\b", "#569CD6"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+\b", "#B5CEA8"),
        }
    },
    "C#": {
        "icon": "icons/file_icons/cs.png",
        "ext": "*.cs",
        "rules": {
            "kw": (r"\b(class|interface|public|private|protected|static|void|int|double|bool|string|return|if|else|for|while|switch|case|foreach|new|this|using|namespace|try|catch|finally|throw)\b", "#569CD6"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+(\.\d+)?\b", "#B5CEA8"),
        }
    },
    "Ruby": {
        "icon": "icons/file_icons/ruby.png",
        "ext": "*.rb",
        "rules": {
            "kw": (r"\b(def|class|module|if|else|elsif|unless|while|until|for|in|do|end|return|yield|self|true|false|nil)\b", "#569CD6"),
            "str": (r'"[^"\n]*"|\'[^\']*\'', "#CE9178"),
            "com": (r"#.*", "gray"),
            "num": (r"\b\d+(\.\d+)?\b", "#B5CEA8"),
        }
    },
    "Swift": {
        "icon": "icons/file_icons/swift.png",
        "ext": "*.swift",
        "rules": {
            "kw": (r"\b(class|struct|enum|protocol|func|let|var|if|else|for|while|return|import|guard|switch|case|break|continue)\b", "#569CD6"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+(\.\d+)?\b", "#B5CEA8"),
        }
    },
    "Go": {
        "icon": "icons/file_icons/go.png",
        "ext": "*.go",
        "rules": {
            "kw": (r"\b(func|package|import|return|if|else|for|range|struct|interface|type|var|const|go|defer|select|switch|case)\b", "#569CD6"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+(\.\d+)?\b", "#B5CEA8"),
        }
    },
    "Dart": {
        "icon": "icons/file_icons/dart.png",
        "ext": "*.dart",
        "rules": {
            "kw": (r"\b(class|extends|implements|import|void|int|double|var|final|const|return|if|else|for|while|switch|case|new|this)\b", "#569CD6"),
            "str": (r'"[^"\n]*"|\'[^\']*\'', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+(\.\d+)?\b", "#B5CEA8"),
        }
    },
    "Kotlin": {
        "icon": "icons/file_icons/kotlin.png",
        "ext": "*.kt",
        "rules": {
            "kw": (r"\b(fun|class|object|interface|val|var|if|else|when|for|while|return|import|package|this|super|is|in)\b", "#569CD6"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+(\.\d+)?\b", "#B5CEA8"),
        }
    },
    "Java": {
        "icon": "icons/file_icons/java.png",
        "ext": "*.java",
        "rules": {
            "kw": (r"\b(class|interface|public|private|protected|static|void|int|double|boolean|return|if|else|for|while|new|this|extends|implements)\b", "#569CD6"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+\b", "#B5CEA8"),
        }
    },
    "JavaScript": {
        "icon": "icons/file_icons/js.png",
        "ext": "*.js",
        "rules": {
            "kw": (r"\b(let|const|var|function|class|return|if|else|for|while|new|this|import|export)\b", "#569CD6"),
            "str": (r'"[^"\n]*"|\'[^\']*\'|`[^`]*`', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+(\.\d+)?\b", "#B5CEA8"),
        }
    },
    "TypeScript": {
        "icon": "icons/file_icons/ts.png",
        "ext": "*.ts",
        "rules": {
            "kw": (r"\b(let|const|interface|type|class|implements|extends|return|if|else|for|while|import|export)\b", "#569CD6"),
            "str": (r'"[^"\n]*"|\'[^\']*\'|`[^`]*`', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+\b", "#B5CEA8"),
        }
    },
    "HTML": {
        "icon": "icons/file_icons/html.png",
        "ext": "*.html",
        "rules": {
            "tag": (r"</?\w+[^>]*>", "#569CD6"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "com": (r"<!--.*?-->", "gray"),
        }
    },
    "CSS": {
        "icon": "icons/file_icons/css.png",
        "ext": "*.css",
        "rules": {
            "kw": (r"\b(color|background|width|height|margin|padding|display|flex|grid|position)\b", "#C586C0"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "num": (r"\b\d+px\b", "#B5CEA8"),
            "com": (r"/\*[\s\S]*?\*/", "gray"),
        }
    },
    "SQL": {
        "icon": "icons/file_icons/sql.png",
        "ext": "*.sql",
        "rules": {
            "kw": (r"\b(SELECT|FROM|WHERE|INSERT|UPDATE|DELETE|CREATE|TABLE|DROP|JOIN|ON|GROUP|ORDER|BY|LIMIT)\b", "#569CD6"),
            "str": (r"'[^']*'", "#CE9178"),
            "num": (r"\b\d+\b", "#B5CEA8"),
            "com": (r"--.*", "gray"),
        }
    },
    "PHP": {
        "icon": "icons/file_icons/php.png",
        "ext": "*.php",
        "rules": {
            "kw": (r"\b(function|class|public|private|protected|return|if|else|foreach|while|new|echo)\b", "#569CD6"),
            "var": (r"\$\w+", "#9CDCFE"),
            "str": (r'"[^"\n]*"|\'[^\']*\'', "#CE9178"),
            "com": (r"//.*|#.*|/\*[\s\S]*?\*/", "gray"),
        }
    },
    "Rust": {
        "icon": "icons/file_icons/rust.png",
        "ext": "*.rs",
        "rules": {
            "kw": (r"\b(fn|let|mut|struct|enum|impl|trait|pub|use|match|if|else|for|while|loop|return)\b", "#569CD6"),
            "str": (r'"[^"\n]*"', "#CE9178"),
            "com": (r"//.*|/\*[\s\S]*?\*/", "gray"),
            "num": (r"\b\d+\b", "#B5CEA8"),
        }
    },
}

def open_main_ide_menu(actives_programs,root,lang,state_sound,errors,volume,start_time_,GlobalAlpha):
    actives_programs.append("Main ide")
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    log_to_file("Main ide launched",start_time_ = start_time_)
    main_ide_window = Toplevel(root)
    main_ide_window.attributes('-alpha',float(GlobalAlpha))
    main_ide_window.attributes('-topmost', True)
    img = Image.open("icons/ide universal.png")
    icon_image = ImageTk.PhotoImage(img)
    main_ide_window.iconphoto(False, icon_image)
    main_ide_window.title("IDE Language Selection")
    main_ide_window.geometry("700x750")
    main_ide_window.config(bg="black")

    Label(main_ide_window, text=lang["enter_langue"], font=("Helvetica", 16), fg="white", bg="black").pack(pady=20,
                                                                                                           side="top")
    Button(main_ide_window, text="C++", width=20, command=lambda:create_ide("C++",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="C#", width=20, command=lambda:create_ide("C#",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="C", width=20, command=lambda:create_ide("C",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="SQL", width=20, command=lambda:create_ide("SQL",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="Python", width=20, command=lambda:create_ide("Python",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="Swift", width=20, command=lambda:create_ide("Swift",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5,
                                                                                                      side="top")
    Button(main_ide_window, text="Kotlin", width=20, command=lambda:create_ide("Kotlin",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5,
                                                                                                        side="top")
    Button(main_ide_window, text="Dart", width=20, command=lambda:create_ide("Dart",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="TypeScript", width=20, command=lambda:create_ide("TypeScript",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5,
                                                                                                        side="top")
    Button(main_ide_window, text="JavaScript", width=20, command=lambda:create_ide("JavaScript",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5,
                                                                                                       side="top")
    Button(main_ide_window, text="HTML/CSS", width=20, command=lambda:create_ide("HTML",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5,
                                                                                                            side="top")
    Button(main_ide_window, text="PHP", width=20, command=lambda:create_ide("PHP",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="Java", width=20, command=lambda:create_ide("Java",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="Ruby", width=20, command=lambda:create_ide("Ruby",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="GO", width=20, command=lambda:create_ide("GO",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")
    Button(main_ide_window, text="Rust", width=20, command=lambda:create_ide("Rust",actives_programs,root,lang,state_sound,errors,volume,start_time_), bg="#2b2b2b", fg="white").pack(pady=5, side="top")

    Button(main_ide_window, text=lang["exit"], command=main_ide_window.destroy, bg="#660000", fg="white").pack(
        pady=20, side="top")
def create_ide(language,actives_programs, root, lang,state_sound, volume, start_time_, GlobalAlpha):

    cfg = LANGUAGES[language]

    actives_programs.append(language)
    play_sound("sound//click.mp3", volume, state_sound, start_time_)
    log_to_file(f"{language} IDE launched", start_time_=start_time_)

    win = Toplevel(root)
    win.title(f"{language} IDE")
    win.geometry("900x600")
    win.config(bg="black")
    win.attributes("-alpha", float(GlobalAlpha))

    icon = ImageTk.PhotoImage(Image.open(cfg["icon"]))
    win.iconphoto(False, icon)

    text = Text(win, bg="black", fg="white",
                insertbackground="white",
                font=("Courier New", 12))
    text.pack(fill="both", expand=True)

    # MENU
    menu = Menu(win)
    win.config(menu=menu)
    fm = Menu(menu, tearoff=0)
    menu.add_cascade(label=lang["file"], menu=fm)

    def open_file():
        path = filedialog.askopenfilename(filetypes=[(language, cfg["ext"])])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                text.delete("1.0", END)
                text.insert("1.0", f.read())
            highlight()

    def save_file():
        path = filedialog.asksaveasfilename(defaultextension=cfg["ext"])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text.get("1.0", END))

    fm.add_command(label=lang["open"], command=open_file)
    fm.add_command(label=lang["save"], command=save_file)
    fm.add_separator()
    fm.add_command(label=lang["exit"], command=win.destroy)

    # HIGHLIGHT
    for tag, (_, color) in cfg["rules"].items():
        text.tag_config(tag, foreground=color)

    def highlight(event=None):
        content = text.get("1.0", END)
        for tag in cfg["rules"]:
            text.tag_remove(tag, "1.0", END)

        for tag, (pattern, _) in cfg["rules"].items():
            for m in re.finditer(pattern, content, re.IGNORECASE):
                text.tag_add(tag,
                             f"1.0 + {m.start()} chars",
                             f"1.0 + {m.end()} chars")

    text.bind("<KeyRelease>", highlight)
    highlight()