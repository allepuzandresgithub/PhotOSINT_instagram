from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from colorama import Fore, Style, init

# Inicializa colorama
init(autoreset=True)

class UserSearch:
    def __init__(self, driver):
        self.driver = driver

    def search_user_by_url(self, username):
        try:
            # Formar la URL de búsqueda del usuario
            user_url = f"https://www.instagram.com/{username}/"
            self.driver.get(user_url)
            print(f"Buscando usuario: {username}")

            # Esperar a que la página cargue
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "@' + username + '")]'))
            # )
            print(Fore.GREEN + f"[*] Perfil cargado con éxito")
        except Exception as e:
            print(Fore.RED + f"Error al buscar el usuario: {e}")

    def search_user_from_input(self):
        username = input("Introduce el nombre de usuario: ")
        #self.search_user_by_url(username)
        return username


class Follow:
    def __init__(self, driver):
        self.driver = driver

    def check_if_private(self):
        try:
            private_text = "This account is private"
            private_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f'//*[text()="{private_text}"]'))
            )
            #print(Fore.RED + "La cuenta es privada")
            return True
        except:
            #print(Fore.GREEN + "La cuenta es pública")
            return False

    def follow_if_private(self):
        if self.check_if_private():
            try:
                follow_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Follow")]'))
                )
                follow_button.click()
                print(Fore.GREEN + "Solicitud de seguimiento enviada con éxito")
            except Exception as e:
                print(Fore.RED + f"Error al intentar seguir la cuenta: {e}")
        else:
            print(Fore.GREEN + "No necesitas seguir la cuenta porque es pública")
