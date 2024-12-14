import time
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from colorama import Fore

# Ruta al driver de geckodriver
gecko_path = 'driver/geckodriver'

class Driver:
    def start_driver(self):

        options = Options()
        options.add_argument("--headless") # Ejecuta en modo headless (sin interfaz gráfica)
        service = Service(gecko_path)
        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.get('https://instagram.com')
        return self.driver

d = Driver()

def load_cookies(driver, filepath):
    try:
        with open(filepath, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                driver.add_cookie(cookie)
        #print("[*] Cookies cargadas exitosamente {2}.")
    except Exception as e:
        print(Fore.RED + f"Error al cargar las cookies: {e}")

# Función para seguir usuarios desde una lista
def follow_users_from_list(file_path):
    driver = d.start_driver()
    # Cargar cookies antes de navegar a Instagram
    load_cookies(driver, 'cookies.pkl')
    driver.refresh()

    try:
        with open(file_path, 'r') as file:
            users = file.readlines()
        for user in users:
            user = user.strip()
            driver.get(f'https://instagram.com/{user}')
            try:
                follow_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "_acan") and contains(@class, "_acap") and contains(@class, "_acas") and contains(@class, "_aj1-") and contains(@class, "_ap30")]'))
                )
                follow_button.click()
                print(Fore.YELLOW + f"[*] Siguiendo a {user}")
                time.sleep(1)
            except Exception as e:
                print(Fore.WHITE + f"[*] La solicitud ya fue enviada a {user}")
    except Exception as e:
        print(Fore.RED + f"Error al leer el archivo: {e}")

