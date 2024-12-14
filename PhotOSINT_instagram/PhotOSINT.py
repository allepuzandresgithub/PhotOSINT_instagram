import sys
import os
import time
import pickle
import getpass
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init
from modules.user_search import *
from modules.followers_list import *
from modules.following_list import *
from modules.follow_users_from_list import follow_users_from_list  # Importar la función desde el script

# Cabecera chula con arte ASCII
header = f"""
{Fore.GREEN}
  ▄▀▀▀▀▄  ▄▀▄▄▄▄   ▄▀▀▀█▄    ▄▀▀▄ ▀▄  ▄▀▀█▄▄   ▄▀▀▄▀▀▀▄
 █ █   ▐ █ █    ▌ █  ▄▀  ▀▄ █  █ █ █ █ ▄▀   █ █   █   █
    ▀▄   ▐ █      ▐ █▄▄▄▄   ▐  █  ▀█ ▐ █    █ ▐  █▀▀█▀
 ▀▄   █    █       █    ▐     █   █    █    █  ▄▀    █
  █▀▀▀    ▄▀▄▄▄▄▀  █        ▄▀   █    ▄▀▄▄▄▄▀ █     █
  ▐      █     ▐  █         █    ▐   █     ▐  ▐     ▐
         ▐        ▐         ▐        ▐     By All3_s3c
{Style.RESET_ALL}
"""

print(header)
init(autoreset=True)  # Colorama
gecko_path = 'driver/geckodriver'

if len(sys.argv) != 3:
    print(Fore.RED + "Uso: python main.py <tu_usuario> <usuario_a_buscar>")
    sys.exit(1)

login_username = sys.argv[1]
target_username = sys.argv[2]
login_password = getpass.getpass(prompt='Ingresa tu contraseña: ')

class Driver:
    def start_driver(self):

        options = Options()
        options.add_argument("--headless")  # Ejecuta en modo headless (sin interfaz gráfica)
        # options.headless = True  # Run in headless mode (without GUI)
        service = Service(gecko_path)
        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.get('https://instagram.com')
        return self.driver

d = Driver()

class Cookies:
    def load_cookies(self, driver, filepath):
        try:
            with open(filepath, 'rb') as cookiesfile:
                cookies = pickle.load(cookiesfile)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            print("[*] Cookies cargadas exitosamente.")
            return True
        except Exception as e:
            print(Fore.RED + f"Error al cargar las cookies: {e}")
            return False

    def save_cookies(self, driver, filepath):
        with open(filepath, 'wb') as filehandler:
            pickle.dump(driver.get_cookies(), filehandler)
        print("[*] Cookies guardadas exitosamente.")

c = Cookies()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        try:
            username_input = WebDriverWait(d.driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "username"))
            )
            username_input.send_keys(self.username)
            print(f"[*] Nombre de usuario añadido: {self.username}")
            
            passwd_input = WebDriverWait(d.driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "password"))
            )
            passwd_input.send_keys(self.password)
            print("[*] Contraseña añadida con éxito")

            login_button = WebDriverWait(d.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
            )
            d.driver.execute_script("arguments[0].click();", login_button)
            print(Fore.GREEN + "[*] Inicio de sesión correcto")
        except Exception as e:
            print(Fore.RED + f"Error al iniciar sesión: {e}")

n = User(login_username, login_password)

def main():
    print("[*] Starting driver....")
    driver = d.start_driver()
    driver.get('https://instagram.com')

    # Intentar cargar cookies
    if not c.load_cookies(driver, 'cookies.pkl'):
        # Si no se cargan las cookies, iniciar sesión
        n.login()
        # Guardar cookies después de iniciar sesión
        c.save_cookies(driver, 'cookies.pkl')
    else:
        driver.refresh()  # Refrescar después de cargar las cookies

    user_search = UserSearch(driver)  # Call the method to check if the account is private
    user_search.search_user_by_url(target_username)  # Asegúrate de buscar el usuario
    print("[*] Determinando si la cuenta es publica/privada")
    user_search = Follow(driver)  # Call the method to check if the account is private
    is_private = user_search.check_if_private()
    if is_private:
        print(Fore.RED + "La cuenta es privada.")
    else:
        print(Fore.GREEN + "La cuenta es pública.")
        followers_list = FollowersList(driver)
        followers = followers_list.get_followers(target_username)
        save_followers_to_file(followers, "followers_list.txt")

        following_list = FollowingList(driver)
        following = following_list.get_following(target_username)
        save_following_to_file(following, "following_list.txt")


    print("[*] Siguiendo a los usuarios...")
    # Llamar a la función para seguir usuarios desde la lista
    follow_users_from_list('followers_list.txt')
    follow_users_from_list('following_list.txt')

if __name__ == "__main__":
    main()

