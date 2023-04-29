
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

#print(driver)

#driver = webdriver.Chrome()

""" 
#Práctica de la librería Selenium

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title =driver.title

driver.implicitly_wait(30)
text_box = driver.find_element(by= By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
text_box.send_keys("Selenium")
text = driver.find_element(By.CSS_SELECTOR,"button")
click= driver.find_element(By.ID,value='my-check-2')
click.click()
#submit_button.click()
time.sleep(5)

"""

#-----------Inicio de la interacción con el sitio web.

driver.get("https://www.bcra.gob.ar/Estadisticas/EstadisSitiopublico/PreInicio.aspx")

title =driver.title

driver.implicitly_wait(30)

#Id de cada checkbox en la búsqueda por TreeView
id_ver="btnAcept"
id_tasas= "TreeView1n52CheckBox"
id_bancos="TreeView1n59CheckBox"
id_CER= "TreeView1n166CheckBox"
id_UVA= ""

# Números para la búsqueda por número de serie.
n_serie_bancos= 1222
n_serie_CER= 3540
n_serie_UVA=7913

# Valores para la búsqueda por texto.
valores_de_búsqueda={'bancos_privados':["Bancos Privados","listaSeries_ctl02_chkSeleccion"], # Texto y Id de cada checkbox.
                'CER':["CER","listaSeries_ctl32_chkSeleccion"],
                'UVA':["UVA","listaSeries_ctl02_chkSeleccion"]}

# Valores para insertar en los input de fecha.
f_desde="01/02/2023" # Deberían ser un campo 'Input'
f_hasta="01/03/2023"

# Si se busca por número de serie todos a la vez, las checkbox repiten los nombres, entonces no sería correcto.
# Hay que buscar por texto, y ahí es seguro el nombre de la checkbox que se genera. Los números de serie sirven para ubicar visualmente cada checkbox en el HTML.

#-------------Búsqueda por texto.---------------------

#--------Dataframe de Bancos Privados.
bancos = driver.find_element(by= By.ID, value="tBusqueda")
bancos.send_keys(valores_de_búsqueda['bancos_privados'][0])
ver_por_término= driver.find_element(By.ID,value="btnBuscar") 
ver_por_término.click()
check_bancos= driver.find_element(By.ID,value=valores_de_búsqueda['bancos_privados'][1])
check_bancos.click()
"""
# Búsqueda por número de serie
ver_por_número= driver.find_element(By.ID,value="btnBuscar") # Botón para entrar a la lista para buscar por número de serie
ver_por_número.click()
# Clickea las checkbox de cada número de serie.
check= driver.find_element(By.ID,value="listaSeries_ctl02_chkSeleccion")
check.click()
"""
#--------Aceptar selección
ver=driver.find_element(By.ID,value="btnAcept")
ver.click()

#-------Llenar campos de fecha
fecha_desde=driver.find_element(By.ID,value="fDesde")
fecha_desde.clear()
fecha_desde.send_keys(f_desde)

fecha_hasta=driver.find_element(By.ID,value="fHasta")
fecha_hasta.clear()
fecha_hasta.send_keys(f_hasta)

#------Aceptar selección de fecha
ultimo_ver=driver.find_element(By.ID,value="btnAcept")
beforePopup= driver.window_handles
#print(beforePopup)
ultimo_ver.click()


afterPopup = driver.window_handles
#print(afterPopup)

afterPopup.remove(afterPopup[0])
#print(afterPopup)
driver.switch_to.window(afterPopup[0])
print(driver.current_url)

#--------Busca la tabla donde están las columnas y filas con los datos.------

# Método usando 'Selenium'.
"""tabla= driver.find_element(By.ID,value='GrdResultados')

#---elemento 'th' es columna.
#---elemento 'tr' es fila.
columnas=[]
filas=[]
valores=[]

for column in tabla.find_elements(By.TAG_NAME,"th"):
        columnas.append(column.text)

for row in tabla.find_elements(By.TAG_NAME,"tr"):
        filas.append(row.text)
        
for value in tabla.find_elements(By.TAG_NAME,"td"):
        valores.append(value.text)"""
 
# Método usando 'requests' y 'read_html'.

req=requests.get(driver.current_url)
table = pd.read_html(req.text,attrs={'id':'GrdResultados'},encoding='utf-8')

df_bancos = table[0] # Este índice de la tabla de HTML es el DataFrame.
df_bancos.rename(columns={'Tasas de interés - Por depósitos - Series diarias - BADLAR - Tasas de interés por depósitos a plazo fijo de 30 a 35 días de plazo - Depósitos de más de un millón de pesos, en porcentaje nominal anual - Bancos privados': 'Badlar'}, inplace=True)

#-----Solucionar problemas de caracteres raros
df_bancos['Fecha']=df_bancos['Fecha'].str.encode('ascii', errors='ignore')
df_bancos['Badlar']=df_bancos['Badlar'].str.encode('ascii', errors='ignore')

df_bancos['Fecha']=df_bancos['Fecha'].str.decode("utf-8")
df_bancos['Badlar']=df_bancos['Badlar'].str.decode("utf-8")

# Limpieza y revisión del dataframe.
df_bancos.replace('&nbsp','',regex=True,inplace=True)
df_bancos.drop([0],inplace=True)
#print(df_bancos.head())
#print(df_bancos.info())

# Exportar como csv.
#df.to_csv('datos.csv',encoding='utf-8',index=False)
#time.sleep(5)

#--------DataFrame de CER----------------------------------------------------------

driver.get("https://www.bcra.gob.ar/Estadisticas/EstadisSitiopublico/PreInicio.aspx")

# Búsqueda por texto
cer = driver.find_element(by= By.ID, value="tBusqueda")
cer.send_keys(valores_de_búsqueda['CER'][0])
ver_por_término= driver.find_element(By.ID,value="btnBuscar") 
ver_por_término.click()
check_cer= driver.find_element(By.ID,value=valores_de_búsqueda['CER'][1])
check_cer.click()

#--------Aceptar selección
ver=driver.find_element(By.ID,value="btnAcept")
ver.click()

#-------Llenar campos de fecha
fecha_desde=driver.find_element(By.ID,value="fDesde")
fecha_desde.clear()
fecha_desde.send_keys(f_desde)
fecha_hasta=driver.find_element(By.ID,value="fHasta")
fecha_hasta.clear()
fecha_hasta.send_keys(f_hasta)

#------Aceptar selección de fecha
ultimo_ver=driver.find_element(By.ID,value="btnAcept")
beforePopup= driver.window_handles
ultimo_ver.click()
afterPopup = driver.window_handles
afterPopup.remove(afterPopup[0])
driver.switch_to.window(afterPopup[0])

#-----Busca la tabla donde están las columnas y filas con los datos.
# Método usando 'Selenium'.
"""
tabla= driver.find_element(By.ID,value='GrdResultados')

#---elemento 'th' es columna.
#---elemento 'tr' es fila.
columnas=[]
filas=[]
valores=[]

for column in tabla.find_elements(By.TAG_NAME,"th"):
        columnas.append(column.text)

for row in tabla.find_elements(By.TAG_NAME,"tr"):
        filas.append(row.text)
        
for value in tabla.find_elements(By.TAG_NAME,"td"):
        valores.append(value.text) """

# Método usando 'requests' y 'read_html'.

req=requests.get(driver.current_url)
table = pd.read_html(req.text,attrs={'id':'GrdResultados'},encoding='utf-8')

df_cer = table[0] # Este índice de la tabla de HTML es el DataFrame.
df_cer.rename(columns={'Tasas de interés - Tasas de interés y coeficientes de ajuste establecidos por el BCRA - Coeficiente de estabilización de referencia (CER), serie diaria': 'CER'}, inplace=True)

#-----Solucionar problemas de caracteres raros
df_cer['Fecha']=df_cer['Fecha'].str.encode('ascii', errors='ignore')
df_cer['CER']=df_cer['CER'].str.encode('ascii', errors='ignore')

df_cer['Fecha']=df_cer['Fecha'].str.decode("utf-8")
df_cer['CER']=df_cer['CER'].str.decode("utf-8")

# Limpieza y revisión del dataframe.
df_cer.replace('&nbsp','',regex=True,inplace=True)
df_cer.drop([0],inplace=True)
#print(df_cer.head())
#print(df_cer.info())

# Exportar como csv.
#df.to_csv('datos.csv',encoding='utf-8',index=False,del)
#time.sleep(5)

#--------DataFrame de UVA------------------------------------------------------------

driver.get("https://www.bcra.gob.ar/Estadisticas/EstadisSitiopublico/PreInicio.aspx")

# Búsqueda por texto
uva = driver.find_element(by= By.ID, value="tBusqueda")
uva.send_keys(valores_de_búsqueda['UVA'][0])
ver_por_término= driver.find_element(By.ID,value="btnBuscar") 
ver_por_término.click()
check_uva= driver.find_element(By.ID,value=valores_de_búsqueda['UVA'][1])
check_uva.click()

#--------Aceptar selección
ver=driver.find_element(By.ID,value="btnAcept")
ver.click()

#-------Llenar campos de fecha
fecha_desde=driver.find_element(By.ID,value="fDesde")
fecha_desde.clear()
fecha_desde.send_keys(f_desde)
fecha_hasta=driver.find_element(By.ID,value="fHasta")
fecha_hasta.clear()
fecha_hasta.send_keys(f_hasta)

#------Aceptar selección de fecha
ultimo_ver=driver.find_element(By.ID,value="btnAcept")
beforePopup= driver.window_handles
ultimo_ver.click()
afterPopup = driver.window_handles
afterPopup.remove(afterPopup[0])
driver.switch_to.window(afterPopup[0])

#-----Busca la tabla donde están las columnas y filas con los datos.
# Método usando 'Selenium'.
"""
tabla= driver.find_element(By.ID,value='GrdResultados')

#---elemento th='columna'
#---elemento tr='fila'
columnas=[]
filas=[]
valores=[]

for column in tabla.find_elements(By.TAG_NAME,"th"):
        columnas.append(column.text)

for row in tabla.find_elements(By.TAG_NAME,"tr"):
        filas.append(row.text)
        
for value in tabla.find_elements(By.TAG_NAME,"td"):
        valores.append(value.text) """

# Método usando 'requests' y 'read_html'.

req=requests.get(driver.current_url)
table = pd.read_html(req.text,attrs={'id':'GrdResultados'},encoding='utf-8')

df_uva = table[0] # Este índice de la tabla de HTML es el DataFrame.

#-----Solucionar problemas de caracteres raros
# En esto caso se hace antes de renombrar las columnas, porque los encabezados también traían caracteres raros.
df_uva.columns=df_uva.columns.str.encode('ascii',errors='ignore')
df_uva.columns=df_uva.columns.str.decode('utf-8')

df_uva.rename(columns={'Unidad de Valor Adquisitivo (UVA)- en pesos - base 31.3.2016=14.05': 'UVA'}, inplace=True)

df_uva['Fecha']=df_uva['Fecha'].str.encode('ascii', errors='ignore')
df_uva['UVA']=df_uva['UVA'].str.encode('ascii', errors='ignore')

df_uva['Fecha']=df_uva['Fecha'].str.decode("utf-8")
df_uva['UVA']=df_uva['UVA'].str.decode("utf-8")

# Limpieza y revisión del dataframe.
df_uva.replace('&nbsp','',regex=True,inplace=True)
df_uva.drop([0],inplace=True)
#print(df_uva.head())
#print(df_uva.info())
#print(df_uva)

# Exportar como csv.
#df_uva.to_csv('datos_uva.csv',encoding='utf-8',index=False)
#time.sleep(5)

#------------Unión de todos los Dataframe.

df_completo= df_bancos.set_index('Fecha').join([df_cer.set_index('Fecha'),df_uva.set_index('Fecha')])
#print(df_completo)
print(df_completo.head(15))
#print(df_completo.info())

# Exportar como csv. 
#df_completo.to_csv('datos_completo.csv',encoding='utf-8',index=True)

#fechas=pd.date_range(start="01/02/2023",end="01/03/2023",freq='D')
fechas1=pd.to_datetime([f_desde,f_hasta],format='%d/%m/%Y',errors='ignore')
fechas=pd.date_range(start=fechas1[0],end=fechas1[1],freq='D')

fec=pd.DataFrame(fechas,columns=['Fecha'])
fec['Fecha']=fec['Fecha'].dt.strftime('%d/%m/%Y')

df_completo= fec.set_index('Fecha').join([df_bancos.set_index('Fecha'),df_cer.set_index('Fecha'),df_uva.set_index('Fecha')])
#print(df_completo)
#df_completo.to_csv('datos_completo.csv',encoding='utf-8',index=True)
#print(fec)

#------------Carga a la base de datos.

# Credenciales para conectarse a la base.
hostname="localhost"
dbname="airbnb"
uname="root"
pwd=""

# Crea el 'engine' de SQLAlchemy para conectarse a la base de datos MySQL.
engine = create_engine("mysql+mysqlconnector://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=uname, pw=pwd))

# Convierte el dataframe a una tabla de sql.                                   
#df_completo.to_sql('tasas', engine, index=True)