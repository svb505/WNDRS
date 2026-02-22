from logtofile import log_to_file

def load_balance(start_time_):
    log_to_file("load_balance", start_time_=start_time_)
    try:
        with open("bank/balance.bin", "rb") as f:

            return int.from_bytes(f.read(4), byteorder='little', signed=True)
    except FileNotFoundError:
        return 0
def save_balance(svb_coins,start_time_):
    log_to_file("save_balance", start_time_=start_time_)
    with open("bank/balance.bin", "wb") as f:
        f.write(svb_coins.to_bytes(4, byteorder='little', signed=True))