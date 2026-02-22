from readandwrite_to_files import write_file
import os
from logtofile import log_to_file

def transactions(data,start_time_):
    if os.path.exists("syst_comp/transactions_hst.cache"):
        try:
            write_file("syst_comp/transactions_hst.cache","a",f"{data}\n")
        except Exception as e:
            log_to_file(str(e),level = "error",start_time_=start_time_)
    else:
        try:
            write_file("syst_comp/transactions_hst.cache","w",f"{data}\n")
        except Exception as e:
                log_to_file(str(e), level="error", start_time_=start_time_)