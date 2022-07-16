from datetime import datetime

# terminal color code
class Tcolors:
    RED   = '\033[1;31m' 
    BLUE  = '\033[1;34m'
    CYAN  = '\033[1;36m'
    GREEN = '\033[0;32m'
    RESET = '\033[0;0m'
    BOLD    = '\033[;1m'
    REVERSE = '\033[;7m'

class Logger:
    def __init__(self) -> None:
        pass
    
    def log(timestamp, klines):
        data = klines
        print(f"---------------------------------------------------------\n"  \
        f"{Tcolors.CYAN}[{datetime.fromtimestamp(timestamp / 1000)}]{Tcolors.RESET}\n\n" \
        f"{Tcolors.BLUE}Open price: {data['o']}{Tcolors.RESET}\n" \
        f"{Tcolors.BLUE}Close price: {data['c']}{Tcolors.RESET}\n" \
        f"{Tcolors.GREEN}High price: {data['h']}{Tcolors.RESET}\n" \
        f"{Tcolors.RED}Low price: {data['l']}{Tcolors.RESET}\n" \
        f"Base value volume: {data['v']}\n" \
        f"Number of trades: {data['n']}\n" \
        f"Quote asset volume: {data['q']}\n" \
        f"Taker buy base asset volume: {data['V']}\n" \
        f"Taker buy quote asset volume: {data['Q']}\n" \
        "---------------------------------------------------------\n")