from tkinter import *
from tkinter import ttk,messagebox
import os
import json
from datetime import datetime
from logtofile import log_to_file
from PIL import Image, ImageTk


def get_wifi_info(root,lang,start_time_):
    def refresh():
        w.destroy()
        get_wifi_info()
    def save_report():
        try:
            os.makedirs("wifi_reports", exist_ok=True)
            timestamp = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
            with open(f"wifi_reports/wifi_report_{timestamp}.json", "w", encoding="utf-8") as fjson:
                json.dump({
                    "SSID": ssid,
                    "Adapter": adapter_name,
                    "SignalStrength": signal_strength,
                    "ReceiveRate": receive_rate,
                    "RadioType": radio_type,
                    "ConnectionState": state,
                    "Frequency": frequency,
                    "Encryption": encryption,
                    "MACAddress": mac_address,
                    "IPAddress": ip_address,
                    "Profile": profile,
                    "NetworkType": network_type,
                    "TransmitRate": transmit_rate,
                    "ReceivePackets": receive_packets,
                    "TransmitPackets": transmit_packets
                }, fjson, ensure_ascii=False, indent=4)
            messagebox.showinfo(lang["success"], lang["datasaved"], parent=w)
        except Exception as e:
            messagebox.showinfo(lang["error"], lang["erwithsave"] + f": {e}", parent=w)

    log_to_file('Wifi info open', start_time_=start_time_)

    w = Toplevel(root)

    w.title(lang["wifiinfo"])
    w.geometry("600x500")
    img = Image.open("icons/interface/wifiinfo.png")
    icon_image = ImageTk.PhotoImage(img)
    w.iconphoto(False, icon_image)
    result = os.popen("netsh wlan show interfaces").read()
    ssid_index = result.find("SSID")
    ssid = result[ssid_index:].split("\n")[0].split(": ")[-1]
    signal_index = result.find("Signal")
    signal_strength = result[signal_index:].split("\n")[0].split(": ")[-1]
    frequency_index = result.find("Channel")
    frequency = result[frequency_index:].split("\n")[0].split(": ")[-1]
    encryption_index = result.find("Authentication")
    encryption = result[encryption_index:].split("\n")[0].split(": ")[-1]
    adapter_index = result.find("Name")
    adapter_name = result[adapter_index:].split("\n")[0].split(": ")[-1]
    mac_index = result.find("Physical address")
    mac_address = result[mac_index:].split("\n")[0].split(": ")[-1]
    ip_result = os.popen("ipconfig").read()
    ip_start = ip_result.find("IPv4")
    ip_address = ip_result[ip_start:].split("\n")[0].split(": ")[-1]
    rate_index = result.find("Receive rate (Mbps)")
    receive_rate = result[rate_index:].split("\n")[0].split(": ")[-1]
    radio_index = result.find("Radio type")
    radio_type = result[radio_index:].split("\n")[0].split(": ")[-1]
    state_index = result.find("State")
    state = result[state_index:].split("\n")[0].split(": ")[-1]
    profile_index = result.find("Profile")
    profile = result[profile_index:].split("\n")[0].split(": ")[-1]

    network_type_index = result.find("Network type")
    network_type = result[network_type_index:].split("\n")[0].split(": ")[-1]
    transmit_index = result.find("Transmit rate (Mbps)")
    transmit_rate = result[transmit_index:].split("\n")[0].split(": ")[-1]
    receive_packets_index = result.find("Receive packets")
    receive_packets = result[receive_packets_index:].split("\n")[0].split(": ")[-1]
    if not receive_packets:
        receive_packets = "N/D"
    transmit_packets_index = result.find("Transmit packets")
    transmit_packets = result[transmit_packets_index:].split("\n")[0].split(": ")[-1]
    if not transmit_packets:
        transmit_packets = "N/D"
    tree = ttk.Treeview(w, columns=("param", "value"), show='headings', height=7)
    tree.heading("param", text=lang['p'])
    tree.heading("value", text=lang["zn"])
    tree.pack(fill='both', expand=True)
    if "SSID" not in result:
        tree.insert("", "end", values=("SSID", lang["noconn"]))
        return
    else:
        tree.insert("", "end", values=("SSID", ssid))
    tree.insert("", "end", values=(lang['AdapterName'], adapter_name))
    tree.insert("", "end", values=(lang['SignalStrength'], signal_strength))
    tree.insert("", "end", values=(lang["ReceiveRate"], receive_rate + " Mbps"))
    tree.insert("", "end", values=(lang["RadioType"], radio_type))
    tree.insert("", "end", values=(lang["ConnectionState"], state))
    tree.insert("", "end", values=(lang['Frequency'], frequency + " MHz"))
    tree.insert("", "end", values=(lang['Encryption'], encryption))
    tree.insert("", "end", values=(lang["Profile"], profile))
    tree.insert("", "end", values=(lang["NetworkType"], network_type))
    tree.insert("", "end", values=(lang["TransmitRate"], transmit_rate + " Mbps"))
    tree.insert("", "end", values=(lang["ReceivePackets"], receive_packets))
    tree.insert("", "end", values=(lang["TransmitPackets"], transmit_packets))

    show_sensitive = BooleanVar(value=False)

    def toggle_sensitive():
        if show_sensitive.get():
            tree.item(mac_row, values=(lang['MACAddress'], mac_address))
            tree.item(ip_row, values=(lang['IPAddress'], ip_address))
        else:
            tree.item(mac_row, values=(lang['MACAddress'], "••••••••••••"))
            tree.item(ip_row, values=(lang['IPAddress'], "••••••••••••"))

    mac_row = tree.insert("", "end", values=(lang['MACAddress'], "••••••••••••"))
    ip_row = tree.insert("", "end", values=(lang['IPAddress'], "••••••••••••"))

    ttk.Checkbutton(w, text="👁️" + lang["show_hidden"], variable=show_sensitive, command=toggle_sensitive).pack(pady=5)
    ttk.Button(w, text="💾 " + lang["saveasf"], command=save_report).pack(pady=5)
    ttk.Button(w, text='🔁 ' + lang["refr"], command=refresh).pack(pady=10)
    log_to_file(f"$Adapter name:{adapter_name}", start_time_=start_time_)
    log_to_file(f"$SSID:{ssid}", start_time_=start_time_)
    log_to_file(f"$SignalStr{signal_strength}", start_time_=start_time_)
    log_to_file(f"$Freq:{frequency} MHz", start_time_=start_time_)
    log_to_file(f"$Encr:{encryption}", start_time_=start_time_)
    log_to_file(f"$Mac:{mac_address}", start_time_=start_time_)
    log_to_file(f"$IP:{ip_address}", start_time_=start_time_)
    log_to_file(f"$profile:{profile}", start_time_=start_time_)
    log_to_file(f"$ConnState:{state}", start_time_=start_time_)
    log_to_file(f"$RecRate:{receive_rate}", start_time_=start_time_)
    log_to_file(f"$RadioType:{radio_type}", start_time_=start_time_)
    log_to_file(f"$NetType:{network_type}", start_time_=start_time_)
    log_to_file(f"$TransRate:{transmit_rate}", start_time_=start_time_)
    log_to_file(f"$RecPack:{receive_packets}", start_time_=start_time_)
    log_to_file(f"$TransPack:{transmit_packets}", start_time_=start_time_)