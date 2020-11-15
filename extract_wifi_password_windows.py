import subprocess
import pandas as pd
from time import sleep
import os


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

production = {'ID': [i + 1 for i in range(len(wifi_list))], 'Wifi Name': [line for line in wifi_list],
              'Wifi Password': [line for line in password_list]}

df = pd.DataFrame(production)
print()
print(df)

with open('html_template.txt', 'r') as f:
    html = f.read()

while True:
    try:
        x = input('\nDo you want to save the output? [yes / no]: ')
        title = 'Wifi_Passwords'
        if x.casefold() == 'yes'.casefold():
            # Create Html Page
            final_title = title + '.html'
            with open(final_title, 'w') as f:
                f.write(html.format(table=df.to_html(classes=('table', 'table-hover', 'table-dark'), index=False)))

            df.to_excel(title + '.xlsx', index=False)
            print(f'The file has been saved successfully under name: {final_title}')
            sleep(3)
            print(f'Opening "{final_title}" in 3 seconds...')
            sleep(1)
            for i in range(3, 0, -1):
                sleep(1)
                print(i)
            sleep(2)
            os.system(final_title)
            break

        elif x.casefold() == 'no'.casefold():
            print('Have a good day! ^-^')

            break
        else:
            print('Wrong choice Try again')
    except Exception as e:
        print('Error!', e)
