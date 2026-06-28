import os
import sys
import time
import json
import random
import getpass
import shutil
from datetime import datetime

class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_CYAN = "\033[46m"

SAVE_FILE = "terminalos_v3_save.json"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_size():
    return shutil.get_terminal_size((80, 24))

def load_state():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"files": {}, "username": "user"}

def save_state(state):
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except:
        pass

def print_centered(text, color=C.WHITE):
    w = get_size().columns
    lines = text.split('\n')
    for line in lines:
        padding = max(0, (w - len(line)) // 2)
        print(f"{' ' * padding}{color}{line}{C.RESET}")

def boot_sequence():
    clear()
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    
    logo = [
        "  ████████╗███████╗██████╗ ███╗   ███╗",
        "  ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║",
        "     ██║   █████╗  ██████╔╝██╔████╔██║",
        "     ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║",
        "     ██║   ███████╗██║  ██║██║ ╚═╝ ██║",
        "     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝"
    ]
    
    print_centered("TerminalOS v3.0", C.BRIGHT_CYAN)
    print()
    for line in logo:
        print_centered(line, C.BRIGHT_GREEN)
        time.sleep(0.15)
    print()
    
    steps = [
        "Initializing kernel",
        "Mounting virtual filesystem",
        "Loading drivers",
        "Starting network services",
        "Checking user credentials",
        "Preparing desktop environment"
    ]
    
    for i, step in enumerate(steps):
        pct = int((i + 1) / len(steps) * 100)
        filled = (pct // 10)
        bar = "█" * filled + "░" * (10 - filled)
        sys.stdout.write("\r" + C.BRIGHT_YELLOW + f" [{bar}] {pct}% " + C.WHITE + step + "..." + " " * 10)
        sys.stdout.flush()
        time.sleep(random.uniform(0.3, 0.8))
    
    print("\n")
    print_centered("Boot complete!", C.BRIGHT_CYAN)
    time.sleep(0.8)
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def fake_login():
    clear()
    w = get_size().columns
    print("\n" * 3)
    print_centered("╔══════════════════════════════╗", C.BRIGHT_CYAN)
    print_centered("║       TerminalOS Login       ║", C.BRIGHT_CYAN)
    print_centered("╚══════════════════════════════╝", C.BRIGHT_CYAN)
    print("\n")
    
    username = input(C.BRIGHT_YELLOW + "  Username: " + C.BRIGHT_WHITE)
    password = getpass.getpass(C.BRIGHT_YELLOW + "  Password: " + C.BRIGHT_WHITE)
    
    print()
    print_centered("Authenticating...", C.BRIGHT_GREEN)
    time.sleep(1)
    
    if not username:
        username = "guest"
        
    print_centered(f"Welcome, {username}!", C.BRIGHT_CYAN)
    time.sleep(1.2)
    return username

def draw_header(title):
    w = get_size().columns
    print(C.BRIGHT_CYAN + "┌" + "─" * (w - 2) + "┐")
    title_str = f" {title} "
    padding = (w - len(title_str)) // 2
    print("│" + " " * padding + C.BRIGHT_YELLOW + C.BOLD + title_str + C.RESET + C.BRIGHT_CYAN + " " * (w - padding - len(title_str)) + "│")
    print("└" + "─" * (w - 2) + "┘" + C.RESET)

def file_manager(state):
    while True:
        clear()
        draw_header("📁 FILE MANAGER")
        print()
        
        if not state["files"]:
            print(C.BRIGHT_RED + "  [ No files found ]\n")
        else:
            print(f"  {C.BRIGHT_YELLOW}{'NAME':<25}{'SIZE (bytes)':<15}")
            print(f"  {C.WHITE}{'─' * 40}")
            for name, content in state["files"].items():
                print(f"  {C.BRIGHT_GREEN}{name:<25}{C.WHITE}{len(content):<15}")
            print()
            
        print(C.BRIGHT_CYAN + "  [1] " + C.WHITE + "Create File")
        print(C.BRIGHT_CYAN + "  [2] " + C.WHITE + "Delete File")
        print(C.BRIGHT_CYAN + "  [3] " + C.WHITE + "Open File")
        print(C.BRIGHT_RED   + "  [4] " + C.WHITE + "Back to Desktop")
        print()
        
        choice = input(C.BRIGHT_YELLOW + "  > " + C.BRIGHT_WHITE).strip()
        
        if choice == "1":
            name = input(C.BRIGHT_CYAN + "  File name: " + C.BRIGHT_WHITE).strip()
            if not name:
                continue
            if name in state["files"]:
                print(C.BRIGHT_RED + "  File already exists!")
                time.sleep(1)
                continue
            print(C.BRIGHT_BLACK + "  (Type ':wq' on a new line to save and exit)")
            lines = []
            while True:
                line = input(C.WHITE + "  > " + C.BRIGHT_WHITE)
                if line.strip() == ":wq":
                    break
                lines.append(line)
            state["files"][name] = "\n".join(lines)
            save_state(state)
            print(C.BRIGHT_GREEN + "  File saved successfully!")
            time.sleep(1)
            
        elif choice == "2":
            name = input(C.BRIGHT_CYAN + "  File name to delete: " + C.BRIGHT_WHITE).strip()
            if name in state["files"]:
                del state["files"][name]
                save_state(state)
                print(C.BRIGHT_GREEN + "  File deleted!")
            else:
                print(C.BRIGHT_RED + "  File not found!")
            time.sleep(1)
            
        elif choice == "3":
            name = input(C.BRIGHT_CYAN + "  File name to open: " + C.BRIGHT_WHITE).strip()
            if name in state["files"]:
                clear()
                draw_header(f"📄 {name}")
                print()
                print(C.BRIGHT_WHITE + state["files"][name])
                print()
                input(C.BRIGHT_BLACK + "  Press Enter to continue..." + C.RESET)
            else:
                print(C.BRIGHT_RED + "  File not found!")
                time.sleep(1)
                
        elif choice == "4":
            break

def notepad(state):
    clear()
    draw_header("📝 NOTEPAD")
    print()
    name = input(C.BRIGHT_CYAN + "  Enter note name: " + C.BRIGHT_WHITE).strip()
    if not name:
        return
        
    if name not in state["files"]:
        state["files"][name] = ""
        
    clear()
    draw_header(f"📝 NOTEPAD - {name}")
    print(C.BRIGHT_BLACK + "  (Type ':wq' to save, ':q' to discard)")
    print()
    
    if state["files"][name]:
        print(C.BRIGHT_BLUE + "  --- Current Content ---")
        for line in state["files"][name].split("\n"):
            print(C.WHITE + "  " + line)
        print(C.BRIGHT_BLUE + "  -----------------------")
        
    print(C.BRIGHT_GREEN + "  Enter new text (append mode):")
    lines = state["files"][name].split("\n") if state["files"][name] else []
    
    while True:
        line = input(C.WHITE + "  > " + C.BRIGHT_WHITE)
        if line.strip() == ":wq":
            break
        if line.strip() == ":q":
            return
        lines.append(line)
        
    state["files"][name] = "\n".join(lines)
    save_state(state)
    print(C.BRIGHT_GREEN + "  Note saved!")
    time.sleep(1)

def terminal_shell(state, username):
    clear()
    print(C.BRIGHT_GREEN + "TerminalOS Shell v3.0 (tsh)")
    print(C.WHITE + "Type 'help' for available commands.\n")
    
    while True:
        try:
            cmd = input(f"{C.BRIGHT_CYAN}{username}@terminalos{C.WHITE}:~$ " + C.BRIGHT_WHITE).strip()
        except EOFError:
            break
            
        if not cmd:
            continue
            
        parts = cmd.split(" ", 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command == "help":
            print(C.BRIGHT_YELLOW + "  Available commands:")
            print(C.WHITE + "  help       - Show this help")
            print("  echo       - Print text")
            print("  date       - Show current date/time")
            print("  clear      - Clear screen")
            print("  ls/list    - List files")
            print("  cat        - View file content")
            print("  whoami     - Show current user")
            print("  sysinfo    - Show system info")
            print("  hack       - Run hack simulation")
            print("  matrix     - Matrix rain effect")
            print("  exit       - Return to desktop")
            
        elif command == "echo":
            print(C.BRIGHT_WHITE + args)
            
        elif command == "date":
            print(C.BRIGHT_WHITE + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
        elif command == "clear":
            clear()
            
        elif command in ["ls", "list"]:
            if not state["files"]:
                print(C.BRIGHT_RED + "  (empty)")
            else:
                for name in state["files"]:
                    print(C.BRIGHT_GREEN + "  " + name)
                    
        elif command == "cat":
            if args.strip() in state["files"]:
                print(C.BRIGHT_WHITE + state["files"][args.strip()])
            else:
                print(C.BRIGHT_RED + "  File not found")
                
        elif command == "whoami":
            print(C.BRIGHT_WHITE + username)
            
        elif command == "sysinfo":
            print(C.BRIGHT_CYAN + "  OS: TerminalOS v3.0")
            print(C.WHITE + f"  User: {username}")
            print("  CPU: simulated @ 3.2GHz")
            print("  RAM: 8192 MB")
            
        elif command == "hack":
            run_hack_sequence()
            
        elif command == "matrix":
            matrix_rain(5)
            clear()
            
        elif command == "sudo":
            if args.strip().lower() == "matrix":
                print(C.BRIGHT_GREEN + "  Granted root access.")
                time.sleep(0.5)
                matrix_rain(8)
                clear()
            elif args.strip().lower() == "hack":
                print(C.BRIGHT_GREEN + "  Granted root access.")
                time.sleep(0.5)
                run_hack_sequence()
            else:
                print(C.BRIGHT_RED + f"  sudo: unknown command '{args}'")
                
        elif command == "exit":
            break
            
        else:
            print(C.BRIGHT_RED + f"  tsh: command not found: {command}")

def run_hack_sequence():
    clear()
    print(C.BRIGHT_RED + C.BOLD + "  INITIATING HACK SEQUENCE..." + C.RESET)
    time.sleep(0.5)
    
    targets = ["192.168.1.1", "10.0.0.5", "172.16.0.1", "8.8.8.8", "127.0.0.1"]
    
    for t in targets:
        print(C.BRIGHT_YELLOW + f"\n  Scanning target: {t}")
        time.sleep(0.4)
        for _ in range(random.randint(2, 5)):
            port = random.randint(1, 65535)
            status = random.choice(["OPEN", "CLOSED", "FILTERED"])
            color = C.BRIGHT_GREEN if status == "OPEN" else C.BRIGHT_RED
            print(f"    Port {port}: {color}{status}{C.RESET}")
            time.sleep(0.1)
            
    print(C.BRIGHT_RED + "\n  Bypassing firewall..." + C.RESET)
    time.sleep(1.5)
    print(C.BRIGHT_GREEN + C.BOLD + "  ACCESS GRANTED!" + C.RESET)
    print(C.BRIGHT_CYAN + "  Root privileges obtained.")
    time.sleep(1.5)
    input(C.BRIGHT_BLACK + "\n  Press Enter to continue..." + C.RESET)

def matrix_rain(duration=5):
    clear()
    w, h = get_size()
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()
    
    chars = "01ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ"
    drops = [0] * w
    start = time.time()
    
    try:
        while time.time() - start < duration:
            for i in range(w):
                if random.random() > 0.75:
                    ch = random.choice(chars)
                    color = C.BRIGHT_WHITE if random.random() > 0.9 else C.GREEN
                    if drops[i] < h:
                        sys.stdout.write(f"\033[{drops[i]+1};{i+1}H{color}{ch}")
                    drops[i] += 1
                    if drops[i] > h + random.randint(0, 5):
                        drops[i] = 0
            sys.stdout.flush()
            time.sleep(0.05)
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

def system_info(username):
    clear()
    draw_header("ℹ️ SYSTEM INFORMATION")
    print()
    
    logo = [
        "       _____       ",
        "      /     \\      ",
        "     | () () |     ",
        "      \\  ^  /      ",
        "       |||||       ",
        "       |||||       "
    ]
    
    info = [
        f"{C.BRIGHT_YELLOW}user{C.WHITE}@{C.BRIGHT_YELLOW}terminalos",
        "-----------------",
        f"{C.BRIGHT_CYAN}OS{C.WHITE}: TerminalOS v3.0",
        f"{C.BRIGHT_CYAN}Host{C.WHITE}: CLI Workstation",
        f"{C.BRIGHT_CYAN}Kernel{C.WHITE}: 5.15.0-cli",
        f"{C.BRIGHT_CYAN}Uptime{C.WHITE}: 1 hour, 5 mins",
        f"{C.BRIGHT_CYAN}Packages{C.WHITE}: 42 (tsh)",
        f"{C.BRIGHT_CYAN}Shell{C.WHITE}: tsh 3.0",
        f"{C.BRIGHT_CYAN}Resolution{C.WHITE}: {get_size().columns}x{get_size().lines}",
        f"{C.BRIGHT_CYAN}CPU{C.WHITE}: Virt @ 3.2GHz",
        f"{C.BRIGHT_CYAN}Memory{C.WHITE}: 256MB / 2048MB",
    ]
    
    for i in range(max(len(logo), len(info))):
        left = logo[i] if i < len(logo) else " " * 19
        right = info[i] if i < len(info) else ""
        print(f"  {C.BRIGHT_CYAN}{left}  {right}")
        
    print()
    input(C.BRIGHT_BLACK + "  Press Enter to continue..." + C.RESET)

def guess_number():
    clear()
    draw_header("🎲 GUESS THE NUMBER")
    print()
    target = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    
    print(C.BRIGHT_CYAN + "  I'm thinking of a number between 1 and 100.")
    print(C.BRIGHT_YELLOW + f"  You have {max_attempts} attempts.\n")
    
    while attempts < max_attempts:
        try:
            guess = input(C.BRIGHT_YELLOW + f"  Attempt {attempts+1}/{max_attempts}: " + C.BRIGHT_WHITE).strip()
            guess = int(guess)
        except ValueError:
            print(C.BRIGHT_RED + "  Please enter a valid number.")
            continue
            
        attempts += 1
        
        if guess == target:
            print(C.BRIGHT_GREEN + C.BOLD + f"\n  🎉 Correct! You guessed it in {attempts} attempts!" + C.RESET)
            break
        elif guess < target:
            diff = target - guess
            hint = "Very low!" if diff > 20 else "Low!"
            print(C.BRIGHT_MAGENTA + f"  {hint}")
        else:
            diff = guess - target
            hint = "Very high!" if diff > 20 else "High!"
            print(C.BRIGHT_MAGENTA + f"  {hint}")
            
    if attempts >= max_attempts and guess != target:
        print(C.BRIGHT_RED + f"\n  Game over! The number was {target}.")
        
    input(C.BRIGHT_BLACK + "\n  Press Enter to continue..." + C.RESET)

def hangman():
    clear()
    draw_header("绞刑架 HANGMAN")
    print()
    words = ["terminal", "python", "hacker", "matrix", "system", "kernel", "binary", "crypto"]
    word = random.choice(words).upper()
    guessed = set()
    attempts = 6
    
    stages = [
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
          ---
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / 
          ---
        """,
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |      
          ---
        """,
        """
           --------
           |      |
           |      O
           |     \\|
           |      |
           |      
          ---
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |      
          ---
        """,
        """
           --------
           |      |
           |      O
           |      
           |      
           |      
          ---
        """,
        """
           --------
           |      |
           |      
           |      
           |      
           |      
          ---
        """
    ]
    
    while attempts > 0:
        clear()
        draw_header("绞刑架 HANGMAN")
        print()
        print(C.BRIGHT_RED + stages[attempts])
        print()
        
        display = " ".join([c if c in guessed else "_" for c in word])
        print(C.BRIGHT_CYAN + "  Word: " + C.BRIGHT_WHITE + display)
        print(C.BRIGHT_YELLOW + "  Guessed: " + C.WHITE + " ".join(sorted(guessed)))
        print()
        
        if "_" not in display:
            print(C.BRIGHT_GREEN + C.BOLD + "  🎉 You win!" + C.RESET)
            break
            
        try:
            letter = input(C.BRIGHT_YELLOW + "  Guess a letter: " + C.BRIGHT_WHITE).strip().upper()
        except EOFError:
            break
            
        if len(letter) != 1 or not letter.isalpha():
            print(C.BRIGHT_RED + "  Invalid input.")
            time.sleep(0.8)
            continue
            
        if letter in guessed:
            print(C.BRIGHT_MAGENTA + "  Already guessed.")
            time.sleep(0.8)
            continue
            
        guessed.add(letter)
        
        if letter not in word:
            attempts -= 1
            print(C.BRIGHT_RED + "  Wrong!")
            time.sleep(0.8)
            
    if attempts == 0:
        clear()
        draw_header("绞刑架 HANGMAN")
        print()
        print(C.BRIGHT_RED + stages[0])
        print(C.BRIGHT_RED + f"\n  Game over! The word was: {word}")
        
    input(C.BRIGHT_BLACK + "\n  Press Enter to continue..." + C.RESET)

def games_menu():
    while True:
        clear()
        draw_header("🎮 GAMES")
        print()
        print(C.BRIGHT_CYAN + "  [1] " + C.WHITE + "Guess the Number")
        print(C.BRIGHT_CYAN + "  [2] " + C.WHITE + "Hangman")
        print(C.BRIGHT_RED   + "  [3] " + C.WHITE + "Back to Desktop")
        print()
        
        choice = input(C.BRIGHT_YELLOW + "  > " + C.BRIGHT_WHITE).strip()
        
        if choice == "1":
            guess_number()
        elif choice == "2":
            hangman()
        elif choice == "3":
            break

def desktop(state, username):
    while True:
        clear()
        w = get_size().columns
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        draw_header("TerminalOS Desktop")
        
        print()
        print(C.BRIGHT_CYAN + "  ┌─────────────────────────────────────────────┐")
        print(C.BRIGHT_CYAN + "  │" + C.RESET + f"  {C.BRIGHT_GREEN}User:{C.WHITE} {username:<33}" + C.BRIGHT_CYAN + "│")
        print(C.BRIGHT_CYAN + "  │" + C.RESET + f"  {C.BRIGHT_GREEN}Time:{C.WHITE} {now:<33}" + C.BRIGHT_CYAN + "│")
        print(C.BRIGHT_CYAN + "  │" + C.RESET + f"  {C.BRIGHT_GREEN}Files:{C.WHITE} {len(state['files']):<33}" + C.BRIGHT_CYAN + "│")
        print(C.BRIGHT_CYAN + "  └─────────────────────────────────────────────┘")
        print()
        
        print(C.BRIGHT_YELLOW + "  [1] " + C.BRIGHT_WHITE + "File Manager")
        print(C.BRIGHT_YELLOW + "  [2] " + C.BRIGHT_WHITE + "Notepad")
        print(C.BRIGHT_YELLOW + "  [3] " + C.BRIGHT_WHITE + "Terminal Shell")
        print(C.BRIGHT_YELLOW + "  [4] " + C.BRIGHT_WHITE + "System Info")
        print(C.BRIGHT_YELLOW + "  [5] " + C.BRIGHT_WHITE + "Games")
        print(C.BRIGHT_YELLOW + "  [6] " + C.BRIGHT_WHITE + "Matrix Rain (Easter Egg)")
        print(C.BRIGHT_RED   + "  [7] " + C.BRIGHT_WHITE + "Shutdown")
        print()
        
        choice = input(C.BRIGHT_CYAN + "  Select option> " + C.BRIGHT_WHITE).strip()
        
        if choice == "1":
            file_manager(state)
        elif choice == "2":
            notepad(state)
        elif choice == "3":
            terminal_shell(state, username)
        elif choice == "4":
            system_info(username)
        elif choice == "5":
            games_menu()
        elif choice == "6":
            matrix_rain(6)
        elif choice == "7":
            clear()
            print()
            print_centered("Shutting down TerminalOS...", C.BRIGHT_RED)
            for i in range(10, 0, -1):
                bar = "█" * i + "░" * (10 - i)
                pct = (10 - i) * 10
                sys.stdout.write("\r" + C.BRIGHT_RED + f"  [{bar}] {pct}%  " + C.RESET)
                sys.stdout.flush()
                time.sleep(0.2)
            print("\n")
            print_centered("Goodbye!", C.BRIGHT_CYAN)
            time.sleep(1)
            clear()
            break
        else:
            print(C.BRIGHT_RED + "  Invalid option!")
            time.sleep(0.8)

def main():
    try:
        state = load_state()
        boot_sequence()
        username = fake_login()
        state["username"] = username
        save_state(state)
        desktop(state, username)
    except KeyboardInterrupt:
        clear()
        print(C.BRIGHT_RED + "\nTerminalOS interrupted. Goodbye!" + C.RESET)
        sys.exit(0)

if __name__ == "__main__":
    main()