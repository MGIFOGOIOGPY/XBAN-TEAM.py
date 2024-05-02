import socket
import threading
import select
import os
import random
import re
import sys
import time
import pyfiglet
from colorama import Fore

SOCKS_VERSION = 5

class Proxy:
    def __init__(self):
        self.username = "username"
        self.password = "password"
        self.packet = b''
        self.sendmode = 'client-0-'

    def handle_client(self, connection):
        version, nmethods = connection.recv(2)
        methods = self.get_available_methods(nmethods, connection)

        if 2 not in set(methods):
            connection.close()
            return

        connection.sendall(bytes([SOCKS_VERSION, 2]))

        if not self.verify_credentials(connection):
            return

        version, cmd, _, address_type = connection.recv(4)

        if address_type == 1:
            address = socket.inet_ntoa(connection.recv(4))
        elif address_type == 3:
            domain_length = connection.recv(1)[0]
            address = connection.recv(domain_length)
            address = socket.gethostbyname(address)
            name = socket.gethostname()

        port = int.from_bytes(connection.recv(2), 'big', signed=False)
        port2 = port

        try:
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((address, port))
            bind_address = remote.getsockname()
            addr = int.from_bytes(socket.inet_aton(bind_address[0]), 'big', signed=False)
            port = bind_address[1]
            reply = b''.join([
                bytes([5, 0, 0, 1]),
                socket.inet_aton(addr),
                port.to_bytes(2, 'big')
            ])
        except Exception as e:
            reply = self.generate_failed_reply(address_type, 5)
        
        connection.sendall(reply)
        self.botdev(connection, remote, port)

    def generate_failed_reply(self, address_type, error_number):
        return b''.join([
            bytes([5, error_number, 0, address_type]),
            bytes([0, 0, 0, 0]),
            bytes([0, 0])
        ])

    def verify_credentials(self, connection):
        version = ord(connection.recv(1))

        username_len = ord(connection.recv(1))
        username = connection.recv(username_len).decode('utf-8')

        password_len = ord(connection.recv(1))
        password = connection.recv(password_len).decode('utf-8')

        if username == self.username and password == self.password:
            response = bytes([version, 0])
            connection.sendall(response)
            return True
        else:
            response = bytes([version, 0xFF])
            connection.sendall(response)
            connection.close()
            return False

    def get_available_methods(self, nmethods, connection):
        methods = []
        for i in range(nmethods):
            methods.append(ord(connection.recv(1)))
        return methods

    def run(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen()

        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=self.handle_client, args=(conn,))
            t.start()

    def botdev(self, client, remote, port):
        while True:
            r, _, _ = select.select([client, remote], [], [])
            if client in r:
                pass
            else:
                pass

    @staticmethod
    def print_center(text):
        columns = os.get_terminal_size().columns
        print(text.center(columns))

    @staticmethod
    def print_commands_ar():
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}\n" * 10)
        Proxy.print_center(f"{Fore.BLUE}1- زيادة مستوى اللاعب")
        Proxy.print_center(f"{Fore.BLUE}2- إرسال رسائل مزعجة")
        Proxy.print_center(f"{Fore.BLUE}3- الانضمام إلى الفريق بشكل مخفي")
        Proxy.print_center(f"{Fore.BLUE}4- مقبرة فري فاير")
        Proxy.print_center(f"{Fore.BLUE}5- معلومات اللاعب")
        Proxy.print_center(f"{Fore.BLUE}6- سبام (أمر التنفيذ: #Cmd)")
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}{Fore.RESET}")

    @staticmethod
    def print_commands_en():
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}\n" * 10)
        Proxy.print_center(f"{Fore.GREEN}1- Increase player level")
        Proxy.print_center(f"{Fore.GREEN}2- Spam messages")
        Proxy.print_center(f"{Fore.GREEN}3- Join the team secretly")
        Proxy.print_center(f"{Fore.GREEN}4- Free Fire Graveyard")
        Proxy.print_center(f"{Fore.GREEN}5- Player Information")
        Proxy.print_center(f"{Fore.GREEN}6- Spam (Command Execution: #Cmd)")
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}{Fore.RESET}")

    @staticmethod
    def print_commands_fr():
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}\n" * 10)
        Proxy.print_center(f"{Fore.CYAN}1- Augmenter le niveau du joueur")
        Proxy.print_center(f"{Fore.CYAN}2- Envoyer des messages de spam")
        Proxy.print_center(f"{Fore.CYAN}3- Rejoindre l'équipe en secret")
        Proxy.print_center(f"{Fore.CYAN}4- Cimetière de Free Fire")
        Proxy.print_center(f"{Fore.CYAN}5- Informations sur le joueur")
        Proxy.print_center(f"{Fore.CYAN}6- Spam (Exécution de commande : #Cmd)")
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}{Fore.RESET}")

    @staticmethod
    def print_commands_zh():
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}\n" * 10)
        Proxy.print_center(f"{Fore.YELLOW}1- 增加玩家等级")
        Proxy.print_center(f"{Fore.YELLOW}2- 发送垃圾信息")
        Proxy.print_center(f"{Fore.YELLOW}3- 秘密加入团队")
        Proxy.print_center(f"{Fore.YELLOW}4- 自由之火墓地")
        Proxy.print_center(f"{Fore.YELLOW}5- 玩家信息")
        Proxy.print_center(f"{Fore.YELLOW}6- 垃圾邮件（命令执行：#Cmd）")
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}{Fore.RESET}")

    @staticmethod
    def print_player_info_ar():
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}\n" * 10)
        Proxy.print_center(f"{Fore.BLUE}يتم جلب معلومات اللاعب هنا...")
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}{Fore.RESET}")

    @staticmethod
    def print_player_info_en():
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}\n" * 10)
        Proxy.print_center(f"{Fore.GREEN}Player information is being retrieved here...")
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}{Fore.RESET}")

    @staticmethod
    def print_player_info_fr():
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}\n" * 10)
        Proxy.print_center(f"{Fore.CYAN}Les informations du joueur sont récupérées ici...")
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}{Fore.RESET}")

    @staticmethod
    def print_player_info_zh():
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}\n" * 10)
        Proxy.print_center(f"{Fore.YELLOW}玩家信息正在这里获取...")
        Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}{Fore.RESET}")

if __name__ == "__main__":
    # Enter password
    password = input(f"{Fore.CYAN}Enter the password (ادخل كلمة المرور): {Fore.RESET}")
    
    Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}\n")
    Proxy.print_center(f"{Fore.MAGENTA}Ahlan fi bot @XBAN_vip_bot")
    Proxy.print_center(f"{Fore.YELLOW}127.0.0.1\n")
    Proxy.print_center(f"{Fore.YELLOW}{'#' * 40}{Fore.RESET}")

    Proxy.print_center(f"{Fore.YELLOW}   welcome, {Fore.MAGENTA}XBAN TEAM X FREE FIRE{Fore.YELLOW} in the game")
    text = pyfiglet.figlet_format(f"{Fore.GREEN}XBAN LVL{Fore.RESET}")
    Proxy.print_center(text)

    # Choose language
    language = input(f"{Fore.BLUE}Choose language (اختر اللغة) [ar/en/fr/zh]: {Fore.RESET}")

    if language.lower() == 'ar':
        Proxy.print_commands_ar()
    elif language.lower() == 'en':
        Proxy.print_commands_en()
    elif language.lower() == 'fr':
        Proxy.print_commands_fr()
    elif language.lower() == 'zh':
        Proxy.print_commands_zh()
    else:
        print(f"{Fore.RED}Invalid language! لغة غير صالحة!{Fore.RESET}")

    # Enter player ID
    player_id = input(f"{Fore.CYAN}Enter your player ID (ادخل رقم اللاعب الخاص بك): {Fore.RESET}")
    Proxy.print_center(f"{Fore.CYAN}Your player ID (رقم اللاعب الخاص بك): {player_id}{Fore.RESET}")

    # Setting up proxy server
    proxy = Proxy()
    proxy.run('localhost', 3000)
