import subprocess
import pandas as pd

command1 = ['netsh', 'wlan', 'show', 'profile']
data = subprocess.check_output(command1).decode('utf-8').splitlines()
wifi_list = [line.strip().split(':')[1] for line in data if "All User Profile" in line]
wifi_list = [line.strip() for line in wifi_list]

command2 = ['netsh', 'wlan', 'show', 'profile', '', 'key=clear']
password_list = []
for wifi in wifi_list:
    command2[4] = wifi
    results = subprocess.check_output(command2).decode('utf-8').splitlines()
    results = [line.strip().split(':')[1] for line in results if "Key Content" in line]
    results = [line.strip() for line in results]
    password_list.append(results[0])

production = {'Wifi Name': [line for line in wifi_list], 'Wifi Password': [line for line in password_list]}

df = pd.DataFrame(production)
print(df)

