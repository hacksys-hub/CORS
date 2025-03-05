import requests
import random
import string
import threading
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

def random_subdomain():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

def check_cors(url, save_file):
    headers = {
        "Origin": f"https://{random_subdomain()}.{url.split('//')[-1]}"
    }
    methods = ["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"]
    
    print(Fore.YELLOW + f"[*] Scanning: {url}")
    
    for method in methods:
        try:
            response = requests.request(method, url, headers=headers, timeout=5, verify=False)
            access_control_origin = response.headers.get("Access-Control-Allow-Origin", "")
            access_control_credentials = response.headers.get("Access-Control-Allow-Credentials", "")
            vary_header = response.headers.get("Vary", "")
            allow_methods = response.headers.get("Access-Control-Allow-Methods", "")
            
            if access_control_origin and (access_control_origin == headers["Origin"] or access_control_origin == "*") and access_control_credentials.lower() == "true":
                print(Fore.RED + f"[!] Potential CORS Misconfiguration: {url}")
                print(Fore.CYAN + f"    Access-Control-Allow-Origin: {access_control_origin}")
                print(Fore.CYAN + f"    Access-Control-Allow-Credentials: {access_control_credentials}")
                print(Fore.CYAN + f"    Access-Control-Allow-Methods: {allow_methods}")
                print(Fore.CYAN + f"    Vary: {vary_header}")
                
                if save_file:
                    with open(save_file, "a") as f:
                        f.write(f"{url} | Origin: {access_control_origin} | Methods: {allow_methods}\n")
                break
            
        except requests.exceptions.RequestException as e:
            print(Fore.LIGHTBLACK_EX + f"[-] Error scanning {url}: {e}")

def main():
    print(Fore.MAGENTA + "Made by Spector-Sec")
    
    choice = input("Scan single URL (1) or multiple URLs from file (2): ")
    save_option = input("Save vulnerable URLs to a file? (yes/no): ").strip().lower()
    save_file = "vulnerable_urls.txt" if save_option == "yes" else None
    
    if choice == "1":
        url = input("Enter URL: ")
        check_cors(url, save_file)
    elif choice == "2":
        file_path = input("Enter file path (urls.txt): ")
        try:
            with open(file_path, "r") as f:
                urls = [line.strip() for line in f.readlines()]
                threads = []
                for url in urls:
                    t = threading.Thread(target=check_cors, args=(url, save_file))
                    threads.append(t)
                    t.start()
                
                for t in threads:
                    t.join()
        except FileNotFoundError:
            print(Fore.RED + "[!] File not found!")
    else:
        print(Fore.RED + "[!] Invalid choice!")

if __name__ == "__main__":
    main()
