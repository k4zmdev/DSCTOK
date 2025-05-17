import os
import re
import requests
import platform
import webbrowser
import tempfile
import time
from colorama import init, Fore, Style

init(autoreset=True)

ASCII_ART = r"""


 ________  ________  ________ _________  ________  ___  __            _____ ______   _______   ________   ___  ___     
|\   ___ \|\   ____\|\   ____\\___   ___\\   __  \|\  \|\  \         |\   _ \  _   \|\  ___ \ |\   ___  \|\  \|\  \    
\ \  \_|\ \ \  \___|\ \  \___\|___ \  \_\ \  \|\  \ \  \/  /|_       \ \  \\\__\ \  \ \   __/|\ \  \\ \  \ \  \\\  \   
 \ \  \ \\ \ \_____  \ \  \       \ \  \ \ \  \\\  \ \   ___  \       \ \  \\|__| \  \ \  \_|/_\ \  \\ \  \ \  \\\  \  
  \ \  \_\\ \|____|\  \ \  \____   \ \  \ \ \  \\\  \ \  \\ \  \       \ \  \    \ \  \ \  \_|\ \ \  \\ \  \ \  \\\  \ 
   \ \_______\____\_\  \ \_______\  \ \__\ \ \_______\ \__\\ \__\       \ \__\    \ \__\ \_______\ \__\\ \__\ \_______\
    \|_______|\_________\|_______|   \|__|  \|_______|\|__| \|__|        \|__|     \|__|\|_______|\|__| \|__|\|_______|
             \|_________|                                                                                              
                                                                                                                       
                                                                                                                      

"""

def print_header():
    print(Fore.BLUE + Style.BRIGHT + ASCII_ART)
    print(Fore.YELLOW + Style.BRIGHT + "🚀  https://github.com/k4zmdev/DSCTOK  🚀".center(115))
    print(Fore.CYAN + "-" * 120 + Style.RESET_ALL)

def get_discord_tokens():
    tokens = []
    system = platform.system()

    if system == "Windows":
        local_app = os.getenv('LOCALAPPDATA')
        roaming_app = os.getenv('APPDATA')
        paths = [
            os.path.join(roaming_app, 'Discord'),
            os.path.join(roaming_app, 'discordcanary'),
            os.path.join(roaming_app, 'discordptb'),
            os.path.join(local_app, 'Google', 'Chrome', 'User Data', 'Default'),
            os.path.join(local_app, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
            os.path.join(local_app, 'Yandex', 'YandexBrowser', 'User Data', 'Default'),
        ]
    elif system == "Linux":
        home = os.path.expanduser("~")
        paths = [
            os.path.join(home, '.config', 'discord'),
            os.path.join(home, '.config', 'discordcanary'),
            os.path.join(home, '.config', 'discordptb'),
            os.path.join(home, '.config', 'google-chrome', 'Default'),
        ]
    elif system == "Darwin":
        home = os.path.expanduser("~")
        paths = [
            os.path.join(home, 'Library', 'Application Support', 'discord'),
            os.path.join(home, 'Library', 'Application Support', 'discordcanary'),
            os.path.join(home, 'Library', 'Application Support', 'discordptb'),
            os.path.join(home, 'Library', 'Application Support', 'Google', 'Chrome', 'Default'),
        ]
    else:
        paths = []

    for path in paths:
        leveldb_path = os.path.join(path, 'Local Storage', 'leveldb')
        if not os.path.exists(leveldb_path):
            continue
        try:
            for filename in os.listdir(leveldb_path):
                if not filename.endswith(('.log', '.ldb')):
                    continue
                with open(os.path.join(leveldb_path, filename), errors='ignore') as f:
                    content = f.read()
                    tokens.extend(re.findall(r'mfa\.[\w-]{84}|[\w-]{24}\.[\w-]{6}\.[\w-]{27}', content))
        except Exception:
            pass

    return list(set(tokens))
    
def token_login_with_chrome(token):

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Discord Token Login</title>
</head>
<body>
    <script>
        window.localStorage.setItem('token', '{token}');
        window.location.href = "https://discord.com/app";
    </script>
    <h2>Logging in with token...</h2>
</body>
</html>
    """

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as tmpfile:
        tmpfile.write(html_content)
        tmp_file_path = tmpfile.name

    print("\033[92m🌐 Opening browser to log in with token...\033[0m")
    webbrowser.open(f"file://{tmp_file_path}")
    
    time.sleep(10)
    try:
        os.remove(tmp_file_path)
    except Exception:
        pass

def is_token_valid(token):
    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    return r.status_code == 200

def get_user_info(token):
    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

def get_user_guilds(token):
    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

def get_user_friends(token):
    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

def display_user_data(token):
    user = get_user_info(token)
    if not user:
        print(Fore.RED + "❌  Invalid token or failed to retrieve user info.\n")
        return

    print(Fore.GREEN + Style.BRIGHT + "🧑  USER INFORMATION\n" + Fore.RESET)
    print(f"{Fore.YELLOW}📧 Email: {Fore.WHITE}{user.get('email', 'N/A')}")
    print(f"{Fore.YELLOW}📞 Phone: {Fore.WHITE}{user.get('phone', 'N/A')}")
    print(f"{Fore.YELLOW}💳 Billing Card (via Nitro): {Fore.WHITE}N/A (not accessible via API)")
    nitro_status = "✅ Active" if user.get('premium_type', 0) > 0 else "❌ None"
    print(f"{Fore.YELLOW}🚀 Nitro: {Fore.WHITE}{nitro_status}")
    mfa_status = "✅ Enabled" if user.get('mfa_enabled', False) else "❌ Disabled"
    print(f"{Fore.YELLOW}🔐 MFA: {Fore.WHITE}{mfa_status}")
    print(f"{Fore.YELLOW}👤 Username: {Fore.WHITE}{user['username']}#{user['discriminator']}")
    displayname = user.get('global_name') or user['username']
    print(f"{Fore.YELLOW}🆔 Display Name: {Fore.WHITE}{displayname}")
    print(f"{Fore.YELLOW}🆔 ID: {Fore.WHITE}{user['id']}")

    print(Fore.CYAN + "\n" + "-" * 40)
    print("🔰  SERVER LIST (Only Owner)\n" + Fore.RESET)
    guilds = get_user_guilds(token)
    if guilds:
        owners = [g for g in guilds if g.get('owner')]
        if owners:
            for g in owners:
                print(f"  🏷️  {Fore.MAGENTA}{g['name']} {Fore.YELLOW}[OWNER]")
        else:
            print("  None")
    else:
        print(Fore.RED + "  Failed to fetch guilds.\n")

    print(Fore.CYAN + "\n" + "-" * 40)
    print("👥  FRIEND LIST\n" + Fore.RESET)
    friends = get_user_friends(token)
    if friends:
        for f in friends:
            if f.get('type') == 1:
                u = f.get('user', {})
                print(f"  👤 {Fore.GREEN}{u.get('username', 'N/A')}#{u.get('discriminator', 'N/A')} {Fore.WHITE}[{u.get('id', 'N/A')}]")
    else:
        print(Fore.RED + "  Failed to fetch friends.\n")

def change_status(token, status):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {
        "status": status
    }
    r = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=data)
    if r.status_code == 200:
        print(Fore.GREEN + "✅ Status updated successfully.")
    else:
        print(Fore.RED + "❌ Failed to update status.")

def send_dm(token, message):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    friends = get_user_friends(token)
    if friends:
        for friend in friends:
            if friend.get('type') == 1:
                user = friend.get('user', {})
                user_id = user.get('id')
                if user_id:
                    data = {
                        "recipient_id": user_id,
                        "content": message
                    }
                    r = requests.post("https://discord.com/api/v9/users/@me/channels", headers=headers, json=data)
                    if r.status_code == 200:
                        channel_id = r.json().get('id')
                        data = {
                            "content": message
                        }
                        r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=data)
                        if r.status_code == 200:
                            print(Fore.GREEN + f"✅ Message sent to {user.get('username')}#{user.get('discriminator')}")
                        else:
                            print(Fore.RED + f"❌ Failed to send message to {user.get('username')}#{user.get('discriminator')}")
                    else:
                        print(Fore.RED + f"❌ Failed to create DM channel with {user.get('username')}#{user.get('discriminator')}")
    else:
        print(Fore.RED + "❌ No friends found.")

def wait_return():
    input(Fore.CYAN + "\nPress Enter to return to the menu...")

def main():
    while True:
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        print_header()
        print(Fore.YELLOW + Style.BRIGHT + "Option:\n")
        print(f"{Fore.CYAN}🔑 (1) Get my token")
        print(f"{Fore.CYAN}🔍 (2) Check token")
        print(f"{Fore.CYAN}🔄 (3) Change status")
        print(f"{Fore.CYAN}🔐 (4) Token login")
        print(f"{Fore.CYAN}💬 (5) DM All")
        print(f"{Fore.CYAN}❌ (0) Exit\n")

        choice = input(Fore.WHITE + "[§] Choice : ").strip()
        tokens = get_discord_tokens()

        if not tokens:
            print(Fore.RED + "❌ No Discord tokens found on this machine.")
            wait_return()
            continue

        if choice == "1":
            token = tokens[0]
            if is_token_valid(token):
                print(Fore.MAGENTA + Style.BRIGHT + "\n🔑 Your Discord token:\n" + Fore.RESET)
                print(Fore.WHITE + token + "\n")
            else:
                print(Fore.RED + "❌ Your token is not valid.")
            wait_return()
        elif choice == "2":
            token = input(Fore.CYAN + "\nEnter the Discord token to check: " + Fore.WHITE).strip()
            if token:
                if is_token_valid(token):
                    print()
                    display_user_data(token)
                else:
                    print(Fore.RED + "❌ Invalid token.")
            else:
                print(Fore.RED + "❌ No token provided.")
            wait_return()
        elif choice == "4":
            token = input(Fore.CYAN + "\nEnter the Discord token: " + Fore.WHITE).strip()
            if token:
                if is_token_valid(token):
                    status = input(Fore.CYAN + "Enter the new status: " + Fore.WHITE).strip()
                    change_status(token, status)
                else:
                    print(Fore.RED + "❌ Invalid token.")
            else:
                print(Fore.RED + "❌ No token provided.")
            wait_return()
        elif choice == "5":
            token = input(Fore.CYAN + "\nEnter the Discord token to login: " + Fore.WHITE).strip()
            if token:
                if is_token_valid(token):
                    print(Fore.GREEN + "✅ Logged in successfully.")
                else:
                    print(Fore.RED + "❌ Invalid token.")
            else:
                print(Fore.RED + "❌ No token provided.")
            wait_return()
        elif choice == "6":
            token = input(Fore.CYAN + "\nEnter the Discord token: " + Fore.WHITE).strip()
            if token:
                if is_token_valid(token):
                    message = input(Fore.CYAN + "Enter the message to send: " + Fore.WHITE).strip()
                    send_dm(token, message)
                else:
                    print(Fore.RED + "❌ Invalid token.")
            else:
                print(Fore.RED + "❌ No token provided.")
            wait_return()
        elif choice == "3":
            print(Fore.GREEN + "\nBye! 👋")
            break
        else:
            print(Fore.RED + "❌ Invalid option. Try again.")
            wait_return()

if __name__ == "__main__":
    main()
