from datetime import datetime
from colorama import Fore, Back, Style, init

def print_info(s):
    print ("[" + Fore.CYAN + datetime.now().strftime('%H:%M:%S') + Style.RESET_ALL + "] [" + Fore.GREEN + "INFO" + Style.RESET_ALL + "] " + s)
def print_succ(s):
    print ("[" + Fore.CYAN + Style.BRIGHT + datetime.now().strftime('%H:%M:%S') + Style.RESET_ALL + "] [" + Fore.GREEN + Style.BRIGHT + "INFO" + Style.RESET_ALL + "] " + Style.BRIGHT + s + Style.RESET_ALL)
def print_warn(s):
    print ("[" + Fore.CYAN + datetime.now().strftime('%H:%M:%S') + Style.RESET_ALL + "] [" + Fore.YELLOW + Style.BRIGHT + "WARNING" + Style.RESET_ALL + "] " + s)
def print_errn(s):
    print ("[" + Fore.CYAN + datetime.now().strftime('%H:%M:%S') + Style.RESET_ALL + "] [" + Back.RED + Fore.WHITE + Style.BRIGHT + "CRITICAL" + Style.RESET_ALL + "] " + s)
def empty():
    print("")