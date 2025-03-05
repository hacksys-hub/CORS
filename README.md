# CORS
Cross-Origin Resource Sharing (CORS) is a security mechanism that allows web applications to make requests across different domains. However, misconfigured CORS policies can lead to severe security vulnerabilities, allowing attackers to steal sensitive data, perform unauthorized actions, and escalate privileges.
This repository provides in-depth knowledge, exploitation techniques, and PoCs to help ethical hackers and security researchers identify and exploit insecure CORS implementations.





![1](https://github.com/user-attachments/assets/ec2a819a-5fdf-4427-850e-276b262150f9)


# USES

 python3 cors/cors-exploit.py -h
usage: cors-exploit.py [-h] -d DOMAIN -t TARGET [-c COOKIE]

CLI-Based CORS Exploitation Tool

options:
  -h, --help           show this help message and exit
  -d, --domain DOMAIN  Attacker-controlled free domain
  -t, --target TARGET  Target URL to exploit
  -c, --cookie COOKIE  Session cookie (optional)

# SPECORS.PY
This tool helps security researchers detect **CORS misconfigurations** in web applications. It performs **fast, multi-threaded scanning** using multiple HTTP methods to identify security risks that allow unauthorized access.

Features:
---------
✔ Scans single URLs or bulk URLs from a file (`urls.txt`).  
✔ Uses **GET, POST, OPTIONS, PUT, DELETE, PATCH** for accurate detection.  
✔ Checks headers like `Access-Control-Allow-Origin`, `Credentials`, and `Methods`.  
✔ **Multi-threaded scanning** for speed and efficiency.  
✔ **Saves vulnerable URLs** for further analysis.  
✔ **Colorful UI** for an improved user experience.  

Usage:
------
1️⃣ Run the script and choose **single URL** or **multiple URLs from a file**.  
2️⃣ The tool will **automatically scan for CORS vulnerabilities**.  
3️⃣ If vulnerabilities are found, they will be **displayed in red** and optionally saved to a file.  

Made by Spector-Sec 🚀



