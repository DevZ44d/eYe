import time
from colorama import Fore
logo = fr"""{Fore.RED}                           
                                                              
                      %%%%%%%%%%%%%%%%%%                      
                  %%%%@@@@@@@@@@@@@@@@@@%%%%                  
              @%%%@@@@@@@%%%%%%%%%%%@@@@@@@@%%%@              
           @%@@@@@@@@%%#########%%%#####%@@@@@@@@%@           
         @@@@@@@@@%%%%#%%###*====*###%%#%%%%@@@@@@@@@         
      @@@@@@@@@%%@@@@%%%%%#*=++++=*#%%%%%@@@@@%@@@@@@@@@      
     %@@@@@%%@@@@@@@@@%%%%%#=-++-=*%%%%%%@@@@@@@@%%@@@@%%     
     %%%%%%##%@@@@@@@@%%%%%%#****##%%%%%@@@@@@@@%#%%%%%%%     
         %%##%%%%%%%@@@%#%%%%%##%%%%%#%@@@%%%%%%%##%%         
               ####%%%%%%%##########%%%#%%%####               
                   ####%%%%%%#####%%%%%####                   
                       ###############%                       
                                                              
                                                                                                                   
"""

for _ in logo.splitlines():
    time.sleep(0.05)
    print(_)

def update_bot_file(token, chat_id):
    lines = []
    with open("src.py", 'r' , encoding="utf-8") as f:
        for line in f:
            if 'self.BOT_TOKEN =' in line:
                line = f'        self.BOT_TOKEN = "{token}"\n'
            elif 'self.CHAT_ID =' in line:
                line = f'        self.CHAT_ID = "{chat_id}"\n'
            lines.append(line)

    with open("src.py", 'w' , encoding="utf-8") as f:
        f.writelines(lines)

    print("- UpDated")

if __name__ == "__main__":
    token = input(f"{Fore.WHITE}[ {Fore.RED}* {Fore.WHITE}] Enter Your Token :{Fore.BLUE}~{Fore.RED}# ").strip()
    chat_id = input(f"{Fore.WHITE}[ {Fore.RED}* {Fore.WHITE}]Enter Your Id :{Fore.BLUE}~{Fore.RED}# ").strip()
    update_bot_file(token, chat_id)

