from logtofile import log_system
from readandwrite_to_files import read_file

def set_region(lang,start_time_):
    try:
        reg = read_file("syst_comp/region.cfg", 'r').strip()
    except:
        reg = "usa"

    if reg == "usa":
        reg = lang["usa"]
        log_system("Region SET 'USA'",start_time_)
    elif reg == "netherlans":
        reg = lang["netherlans"]
        log_system("Region SET 'NETHERLANDS'",start_time_)
    elif reg == "france":
        reg = lang["france"]
        log_system("Region SET 'FRANCE'",start_time_)
    elif reg == "russia":
        reg = lang["russia"]
        log_system("Region SET 'RUSSIA'",start_time_)
    elif reg == "hungry":
        reg = lang["hungry"]
        log_system("Region SET 'HUNGRY'",start_time_)
    elif reg == "italia":
        reg = lang["italia"]
        log_system("Region SET 'ITALIA'",start_time_)
    elif reg == "canada":
        reg = lang["canada"]
        log_system("Region SET 'CANADA'",start_time_)
    else:
        reg = lang['australia']
        log_system("Region SET 'AUSTRALIA'",start_time_)
    return reg