import requests
import random
import string
import threading
import urllib3
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# Generate a random subdomain
def random_subdomain():
    return ''.join(random.choices(string.ascii_lowercase, k=8))

# List of common User-Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
]

# CORS scanning function
def check_cors(url, save_file):
    headers = {
        "Origin": f"https://{random_subdomain()}.{url.split('//')[-1]}",
        "User-Agent": random.choice(USER_AGENTS),
    }
    methods = ["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"]

    print(Fore.YELLOW + f"[*] Scanning: {url}")

    for method in methods:
        try:
            response = requests.request(method, url, headers=headers, timeout=5, verify=False)
            cors_origin = response.headers.get("Access-Control-Allow-Origin", "")
            cors_credentials = response.headers.get("Access-Control-Allow-Credentials", "")
            allow_methods = response.headers.get("Access-Control-Allow-Methods", "")

            if cors_origin and (cors_origin == headers["Origin"] or cors_origin == "*") and cors_credentials.lower() == "true":
                print(Fore.RED + f"[!] Potential CORS Misconfiguration: {url}")
                print(Fore.CYAN + f"    Access-Control-Allow-Origin: {cors_origin}")
                print(Fore.CYAN + f"    Access-Control-Allow-Credentials: {cors_credentials}")
                print(Fore.CYAN + f"    Allowed Methods: {allow_methods}")

                if save_file:
                    with open(save_file, "a") as f:
                        f.write(f"{url} | Origin: {cors_origin} | Methods: {allow_methods}\n")
                break

        except requests.exceptions.RequestException as e:
            print(Fore.LIGHTBLACK_EX + f"[-] Error scanning {url}: {e}")

# Main function
def main():
    print(Fore.MAGENTA + "\n╔══════════════════════════╗")
    print(Fore.MAGENTA + "║  CORS Misconfig Scanner  ║")
    print(Fore.MAGENTA + "║     Made by Spector-Sec  ║")
    print(Fore.MAGENTA + "╚══════════════════════════╝\n")

    choice = input("Scan single URL (1) or multiple URLs from file (2): ").strip()
    save_option = input("Save vulnerable URLs to a file? (yes/no): ").strip().lower()
    save_file = "vulnerable_urls.txt" if save_option == "yes" else None

    if choice == "1":
        url = input("Enter URL: ").strip()
        if not url.startswith("http"):
            print(Fore.RED + "[!] Invalid URL format! Use http:// or https://")
            return
        check_cors(url, save_file)

    elif choice == "2":
        file_path = input("Enter file path (urls.txt): ").strip()
        try:
            with open(file_path, "r") as f:
                urls = [line.strip() for line in f if line.strip()]

            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(lambda url: check_cors(url, save_file), urls)

        except FileNotFoundError:
            print(Fore.RED + "[!] File not found!")

    else:
        print(Fore.RED + "[!] Invalid choice!")

if __name__ == "__main__":
    main()
