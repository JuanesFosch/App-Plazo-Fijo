from selenium import webdriver #---------Webdriver es la funcionalidad principal de Selenium para interactuar con sitios web.
from selenium.webdriver.common.by import By #---------Importa el método 'By' para seleccionar atributos de los elementos HTML.
import time #---------Sirve para dar un intervalo de tiempo a las ventanas para que se mantengan abiertas.
import requests #---------Sirve para 'pedir' información, como la URL de un sitio.
import pandas as pd 
from sqlalchemy import create_engine #---------Sirve para exportar un DataFrame de Pandas a una base de datos MySQL.


#service = Service(executable_path="/path/to/chromedriver")
#print(service)

options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging']) # Esto se hace para que la ventana del navegador se mantenga abierta.

driver = webdriver.Chrome(options=options)

driver.get("https://www.idealista.pt/en/comprar-casas/lisboa/")
driver.implicitly_wait(30)
#req=requests.get(driver.current_url)

time.sleep(30)