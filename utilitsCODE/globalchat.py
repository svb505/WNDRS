from datetime import datetime
from send_email import send_email
import threading
import time
import customtkinter as ctk
import tkinter.messagebox as mb
from tkinter import simpledialog
from stream_chat import StreamChat
import os
from load_env import load_env
import sys
from logtofile import log_to_file

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

load_env()

username = None
is_admin = False
stop_event = threading.Event()
API_KEY = os.getenv("CHAT_API")
API_SECRET = os.getenv('CHAT_SECRET_API')
GLOBAL_CHANNEL_ID = "global"
POLL_INTERVAL = 1.0
ADMIN_USERNAME = os.getenv("CHAT_ADMIN")

def chat_win(root,lang,email,start_time_,GlobalAlpha):
    client = StreamChat(api_key=API_KEY, api_secret=API_SECRET)
    def ensure_global_channel():
        channel = client.channel("messaging", GLOBAL_CHANNEL_ID, {"name": "Global Chat"})
        try:
            channel.create(ADMIN_USERNAME)
        except:
            pass
        return channel
    channel = ensure_global_channel()
    def handle_event(etype,target,reason,admin = "SVBdev"):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not email:
            return

        if etype == "banned":
            subject = lang["chat:you_are_banned"]
            html = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto;">
                  <h2 style="color: #d9534f;">{lang["chat:account_banned"]}</h2>
                  <p style="font-size: 16px; color: #555;">
                    {lang["your_acc_has_been"]} <b>{lang["banned"]}</b> {lang["admin"]} <b>{admin}</b>.
                  </p>
                  <p style="color: #888;">{lang['reason']}: {reason}</p>
                  <p style="color: #888;">{lang["date_and_time"]}: {current_time}</p>
                  <p style="color: #888;">{lang["obr_v_pod"]}</p>
                </div>
              </body>
            </html>
            """
            send_email(to=email, subject=subject, html=html)
        elif etype == "muted":
            subject = lang["chat:muted"]
            html = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto;">
                  <h2 style="color: #f0ad4e;">{lang["muted_in_chat"]}</h2>
                  <p style="font-size: 16px; color: #555;">
                   {lang["your_acc_has_been"]} <b>{lang["muted"]}</b> {lang["admin"]} <b>{admin}</b>.
                  </p>
                <p style="color: #888;">{lang['reason']}: {reason}</p>
                  <p style="color: #888;">{lang["date_and_time"]}: {current_time}</p>
                  <p style="color: #888;">{lang["mute_inf"]}</p>
                </div>
              </body>
            </html>
            """
            send_email(to=email, subject=subject, html=html)
        elif etype == "kicked":
            subject = lang["chat:you_has_been_kicked"]
            html = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 6px rgba(0,0,0,0.1); max-width: 500px; margin: auto;">
                  <h2 style="color: #5bc0de;">{lang['you_kicked']}</h2>
                  <p style="font-size: 16px; color: #555;">
                    {lang["your_acc_has_been"]} <b>{lang["kicked2"]}</b> {lang["admin"]} <b>{admin}</b>.
                  </p>
                 <p style="color: #888;">{lang['reason']}: NULL</p>
                  <p style="color: #888;">{lang["date_and_time"]}: {current_time}</p>
                  <p style="color: #888;">{lang["kick_inf"]}</p>
                </div>
              </body>
            </html>
            """
            send_email(to=email, subject=subject, html=html)
    try:
        log_to_file(f"[INFO] Subscribe to events StreamChat actived",start_time_ = start_time_)
    except Exception as e:
        log_to_file(f"[ERROR] Failed to subscribe to events: {e}", level = "error",start_time_=start_time_)
    def join_chat():
        global username, is_admin
        u = username_entry.get().strip()
        if not u:
            mb.showwarning(lang['error'], lang["enter_name_chat"],parent = Win)
            return
        username = u
        is_admin = (username == ADMIN_USERNAME)

        try:
            client.upsert_user({"id": username, "name": username, "role": "admin" if is_admin else "user"})
            client.create_token(username)
            channel.add_members([username])
        except Exception as e:
            mb.showerror(lang["error"], str(e),parent = Win)
            return

        login_frame.pack_forget()
        chat_frame.pack(fill="both", expand=True)
        set_admin_controls(is_admin)

        threading.Thread(target=poll_loop, daemon=True).start()
    def get_channel_members():
        try:
            state = channel.query(state=True)
            members = [m.get("user", {}).get("id", "") for m in state.get("members", [])]
            return members
        except Exception:
            return []
    def poll_loop():
        while not stop_event.is_set():
            try:
                fetch_and_render()
            except:
                pass
            time.sleep(POLL_INTERVAL)
    def fetch_and_render():
        res = channel.query(state=True, watch=False, messages={"limit": 50})
        msgs = res.get("messages", [])
        members = [m.get("user", {}).get("id", "unknown") for m in res.get("members", [])]
        render_messages(msgs)
        render_members(members)
    def render_messages(msgs):
        messages_box.configure(state="normal")
        messages_box.delete("1.0", "end")
        for msg in msgs:
            user = msg.get("user", {}).get("id", "system")
            text = msg.get("text", "")
            ts = msg.get("created_at", "")[:19].replace("T", " ")
            messages_box.insert("end", f"[{ts}] {user}: {text}\n")
        messages_box.configure(state="disabled")
        messages_box.yview_moveto(1.0)
    def render_members(members):
        members_box.configure(state="normal")
        members_box.delete("1.0", "end")
        for m in members:
            members_box.insert("end", f"{m}\n")
        members_box.configure(state="disabled")
    def send_message():
        text = input_entry.get().strip()
        if not text:
            return
        try:
            client.upsert_user({"id": username, "name": username})
            channel.add_members([username])

            channel.send_message({"text": text}, username)

            input_entry.delete(0, "end")
        except Exception as e:
            mb.showerror(lang["error"], str(e),parent = Win)
    def kick_user():
        if not is_admin:
            mb.showwarning(lang['no_rules'], lang["no_admin"],parent = Win)
            return
        target = target_entry.get().strip()
        if not target:
            mb.showwarning(lang['error'], lang['enter_name_for_kick'],parent = Win)
            return
        try:
            channel.remove_members([target])
            mb.showinfo(lang['success'], f"{lang['user_chat']} {target} {lang['kicked']}",parent = Win)
        except Exception as e:
            mb.showerror(lang["error"], str(e),parent = Win)
    def ban_user():
        if not is_admin:
            mb.showwarning(lang['no_rules'], lang["no_admin"],parent = Win)
            return
        target = target_entry.get().strip()
        if not target:
            mb.showwarning(lang['error'], lang['enter_name_for_ban'],parent = Win)
            return
        minutes = simpledialog.askinteger("Ban", lang["ban_minutes"], initialvalue=60,parent = Win)
        reason = simpledialog.askstring("Ban", lang["enter_reason"],parent = Win)
        if minutes is None:
            return
        try:
            client.ban_user(target, user_id=username, timeout=minutes if minutes > 0 else None)
            mb.showinfo(lang['success'],
                        f"{lang['user_chat']} {target} {lang['ban_for']} {minutes} {lang['min_utes']}",parent = Win)
        except Exception as e:
            mb.showerror(lang['error'], str(e),parent = Win)
        handle_event("banned",target,reason)
    def mute_user():
        if not is_admin:
            mb.showwarning(lang['no_rules'], lang["mute_for_admin!"],parent = Win)
            return
        target = target_entry.get().strip()
        if not target:
            mb.showwarning(lang['error'], lang["enter_name_for_mute"],parent = Win)
            return
        minutes = simpledialog.askinteger("Mute", lang["ban_minutes"], initialvalue=60,parent = Win)
        reason = simpledialog.askstring("Ban", lang["enter_reason"],parent = Win)
        if minutes is None:
            return
        try:
            client.mute_user(target, timeout=minutes if minutes > 0 else None)
            mb.showinfo(lang["success"],
                        f"{lang['user_chat']} {target} {lang['mute_for']} {minutes} {lang['min_utes']}",parent = Win)
        except Exception as e:
            mb.showerror(lang['error'], str(e),parent = Win)
        handle_event("muted",target,reason)
    def promote_user():
        if not is_admin:
            mb.showwarning(lang["no_rules"], lang["promote_for_admin!"],parent = Win)
            return
        target = target_entry.get().strip()
        if not target:
            mb.showwarning(lang["error"], lang['enter_name_for_uv'],parent = Win)
            return
        try:
            client.upsert_user({"id": target, "role": "moderator"})
            mb.showinfo(lang['success'], f"{lang['user_chat']} {target} {lang['aremoder']}",parent = Win)
        except Exception as e:
            mb.showerror(lang['error'], str(e),parent = Win)
        handle_event("kicked", target,"NULL")
    def set_admin_controls(visible):
        state = "normal" if visible else "disabled"
        for w in (target_entry, kick_btn, ban_btn, mute_btn, promote_btn):
            w.configure(state=state)
    def on_close():
        stop_event.set()
        Win.destroy()
    ctk.set_appearance_mode("Dark")
    Win = ctk.CTkToplevel(root)
    Win.attributes("-alpha",float(GlobalAlpha))
    Win.title(lang["globalchat"])
    Win.geometry("800x600")
    Win.attributes('-topmost',True)

    login_frame = ctk.CTkFrame(Win)
    login_frame.pack(fill="both", expand=True)
    ctk.CTkLabel(login_frame, text=lang['enter_username']).pack(pady=12)
    username_entry = ctk.CTkEntry(login_frame, placeholder_text="username")
    username_entry.pack(pady=8)
    login_btn = ctk.CTkButton(login_frame, text=lang['voyti'], command=join_chat)
    login_btn.pack(pady=8)

    chat_frame = ctk.CTkFrame(Win)

    left = ctk.CTkFrame(chat_frame)
    left.pack(side="left", fill="both", expand=True, padx=8, pady=8)
    messages_box = ctk.CTkTextbox(left, width=500, height=420)
    messages_box.pack(fill="both", expand=True)
    messages_box.configure(state="disabled")
    input_entry = ctk.CTkEntry(left, placeholder_text=lang["sms..."])
    input_entry.pack(fill="x", pady=6)
    send_btn = ctk.CTkButton(left, text=lang['send-chat'], command=send_message)
    send_btn.pack(pady=4)

    right = ctk.CTkFrame(chat_frame, width=240)
    right.pack(side="right", fill="y", padx=8, pady=8)
    ctk.CTkLabel(right, text=lang['uchast']).pack(pady=(4, 6))
    members_box = ctk.CTkTextbox(right, width=220, height=200)
    members_box.pack()
    members_box.configure(state="disabled")

    ctk.CTkLabel(right, text=lang["moderation"]).pack(pady=(12, 6))
    target_entry = ctk.CTkEntry(right, placeholder_text="username")
    target_entry.pack(pady=4)
    kick_btn = ctk.CTkButton(right, text=lang["kick"], command=kick_user)
    kick_btn.pack(fill="x", pady=3)
    ban_btn = ctk.CTkButton(right, text=lang['ban'], command=ban_user)
    ban_btn.pack(fill="x", pady=3)
    mute_btn = ctk.CTkButton(right, text=lang["mute--"], command=mute_user)
    mute_btn.pack(fill="x", pady=3)
    promote_btn = ctk.CTkButton(right, text=lang['promote'], command=promote_user)
    promote_btn.pack(fill="x", pady=3)

    set_admin_controls(False)

    Win.protocol("WM_DELETE_WINDOW", on_close)