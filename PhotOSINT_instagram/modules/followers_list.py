from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init
import time

# Inicializa colorama
init(autoreset=True)

class FollowersList:
    def __init__(self, driver):
        self.driver = driver

    def get_followers(self, username):
        try:
            # Formar la URL de seguidores del usuario
            user_url = f"https://www.instagram.com/{username}/"
            self.driver.get(user_url)
            print("Obteniendo seguidores...")

            # Hacer clic en el enlace de seguidores
            followers_link = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/followers/")]'))
            )
            followers_link.click()

            # Esperar a que la lista de seguidores se cargue
            followers_panel = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@role="dialog"]'))
            )

            # Desplazarse por la lista de seguidores
            followers = []
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", followers_panel)
            while True:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_panel)
                time.sleep(2)
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", followers_panel)
                if new_height == last_height:
                    break
                last_height = new_height

            followers_elements = self.driver.find_elements(By.XPATH, '//a[@href and contains(@href, "/")]')
            for element in followers_elements:
                follower = element.get_attribute('href').split('/')[-2]
                if follower not in followers:
                    followers.append(follower)
                    print(Fore.BLUE + f"Seguidor obtenido: {follower}")  # Mostrar seguidor obtenido

            #print(Fore.GREEN + "Lista de seguidores obtenida con éxito")
            return followers
        except Exception as e:
            print(Fore.RED + f"Error al obtener la lista de seguidores: {e}")
            return []

def save_followers_to_file(followers, filename="followers_list.txt"):
    try:
        followers = followers[35:] #Elimina las 10 primeras lineas
        with open(filename, 'w') as file:
            for follower in followers:
                file.write(follower + "\n")
                #print(Fore.YELLOW + f"Guardando seguidor: {follower}")  # Mostrar seguidor guardado
        print(Fore.GREEN + f"Seguidores guardados en {filename}")
    except Exception as e:
        print(Fore.RED + f"Error al guardar seguidores en el archivo: {e}")

