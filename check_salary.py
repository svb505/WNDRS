import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from check_ach import check_ach
from readandwrite_to_files import read_file, write_file
from save_and_load_balance import load_balance, save_balance
from server_statistick import update_file
from transactions import transactions


def check_salary(config,svb_coins,start_time_,lang):
    if os.path.exists("state/dat.cfg"):
        date_str = read_file("state/dat.cfg",'r').strip()

        try: date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError: date_obj = datetime.today().date()

        today = datetime.today().date()
        if date_obj <= today:
            with open("state/job.cfg", "r", encoding='utf-8') as f:
                for line in f:
                    key2, value1 = line.strip().split("=")
                    config[key2] = value1

            a = config.get("SALARY", "0")
            a = int(a)
            year = a * 12

            tax = (a / 100) * (13 if year < 5000000 else 15)
            net_salary = int(a - tax)

            svb_coins = load_balance(start_time_)
            svb_coins += net_salary
            transactions(f'+{net_salary} SVB Coins',start_time_)
            update_file("count_svbcoins.txt", int(net_salary))
            save_balance(svb_coins,start_time_)
            check_ach(svb_coins,start_time_,lang)

            next_month_date = datetime.today() + relativedelta(months=1)
            write_file('state/dat.cfg','w',next_month_date.strftime("%d.%m.%Y"))
            transactions(f"+{net_salary} SVB Coins {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",start_time_)
            messagebox.showinfo("", f"{lang['nach']} {net_salary} SVB Coins")