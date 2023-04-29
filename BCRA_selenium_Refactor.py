from selenium import webdriver #---------Webdriver es la funcionalidad principal de Selenium para interactuar con sitios web.
from selenium.webdriver.common.by import By #---------Importa el método 'By' para seleccionar atributos de los elementos HTML.
import time #---------Sirve para dar un intervalo de tiempo a las ventanas para que se mantengan abiertas.
import requests #---------Sirve para 'pedir' información, como la URL de un sitio.
import pandas as pd 
from sqlalchemy import create_engine #---------Sirve para exportar un DataFrame de Pandas a una base de datos MySQL.


#------HABRÍA QUE HACER UN BUCLE PARA QUE BUSQUE TODAS LAS POSIBILIDADES POR TEXTO: BANCOS, UVA Y CER.----
#----LA FECHA VA A SER SIEMPRE LA MISMA.-----
#----------HABRÍA QUE HACER OTRO BUCLE PARA QUE BUSQUE LA TABLA (QUE ES SIEMPRE LA MISMA) PERO QUE RENOMBRE SEGÚN CATEGORÍA-----
#----EL OTRO BUCLE ES DE AGARRAR CADA DF, FORMATEARLO E IMPRIMIRLO----



options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging']) # Esto se hace para que la ventana del navegador se mantenga abierta.

driver = webdriver.Chrome(options=options)


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
términos_de_búsqueda={'bancos_privados':["Bancos Privados","listaSeries_ctl02_chkSeleccion"], # Texto y Id de cada checkbox.
                'CER':["CER","listaSeries_ctl32_chkSeleccion"],
                'UVA':["UVA","listaSeries_ctl02_chkSeleccion"]}

# Valores para insertar en los input de fecha.
f_desde="01/02/2023" # Deberían ser un campo 'Input'
f_hasta="01/03/2023"

nombres_columnas= {"bancos_original": 'Tasas de interés - Por depósitos - Series diarias - BADLAR - Tasas de interés por depósitos a plazo fijo de 30 a 35 días de plazo - Depósitos de más de un millón de pesos, en porcentaje nominal anual - Bancos privados' 
            , "bancos_nuevo": 'Badlar',
            "cer_original": 'Tasas de interés - Tasas de interés y coeficientes de ajuste establecidos por el BCRA - Coeficiente de estabilización de referencia (CER), serie diaria',
            "cer_nuevo": 'CER',
            "uva_original": 'Unidad de Valor Adquisitivo (UVA)- en pesos - base 31.3.2016=14.05',
            "uva_nuevo": 'UVA' }


# Si se busca por número de serie todos a la vez, las checkbox repiten los nombres, entonces no sería correcto.
# Hay que buscar por texto, y ahí es seguro el nombre de la checkbox que se genera. Los números de serie sirven para ubicar visualmente cada checkbox en el HTML.

#--------Dataframe de Bancos Privados.

#-------------Búsqueda por término. (PUEDE SER UNA FUNCIÓN)-----
"""
bancos = driver.find_element(by= By.ID, value="tBusqueda")
bancos.send_keys(términos_de_búsqueda['bancos_privados'][0])
ver_por_término= driver.find_element(By.ID,value="btnBuscar") 
ver_por_término.click()
check_bancos= driver.find_element(By.ID,value=términos_de_búsqueda['bancos_privados'][1])
check_bancos.click() """


def búsqueda_por_texto(término):
    """Busca el campo para ingresar términos para la búsqueda e ingresa el término"""
    categoría=driver.find_element(by= By.ID, value="tBusqueda")
    categoría.send_keys(términos_de_búsqueda[f'{término}'][0])
    ver_por_término= driver.find_element(By.ID,value="btnBuscar") 
    ver_por_término.click()
    check_categoría= driver.find_element(By.ID,value=términos_de_búsqueda[f'{término}'][1])
    check_categoría.click()


búsqueda_por_texto('bancos_privados')

#--------Aceptar selección---(PODRÍA SER UNA FUNCIÓN PARA TODOS LOS CLICKEOS)
ver=driver.find_element(By.ID,value="btnAcept")
ver.click()

#-------Llenar campos de fecha. (TIENE QUE SER UNA FUNCIÓN SÍ O SÍ)----
"""
fecha_desde=driver.find_element(By.ID,value="fDesde")
fecha_desde.clear()
fecha_desde.send_keys(f_desde)

fecha_hasta=driver.find_element(By.ID,value="fHasta")
fecha_hasta.clear()
fecha_hasta.send_keys(f_hasta)  """

def selección_fecha(desde,hasta):
    """Busca el campo para ingresar fechas e ingresa las fechas"""
    fecha_desde=driver.find_element(By.ID,value="fDesde")
    fecha_desde.clear()
    fecha_desde.send_keys(desde)

    fecha_hasta=driver.find_element(By.ID,value="fHasta")
    fecha_hasta.clear()
    fecha_hasta.send_keys(hasta)

selección_fecha(f_desde,f_hasta)
#------Aceptar selección de fecha. (TIENE QUE SER UNA FUNCIÓN SÍ O SÍ)----
"""
ultimo_ver=driver.find_element(By.ID,value="btnAcept")
beforePopup= driver.window_handles
ultimo_ver.click()
afterPopup = driver.window_handles
afterPopup.remove(afterPopup[0])
driver.switch_to.window(afterPopup[0]) """

def aceptar_fecha(botón):
    """Acepta la selección de fecha anterior"""
    ultimo_ver=driver.find_element(By.ID,value=f"{botón}")
    #beforePopup= driver.window_handles
    ultimo_ver.click()
    afterPopup = driver.window_handles    # Pasa de controlar la ventana abierta a controlar la ventana que se abre después de clickear.
    afterPopup.remove(afterPopup[0])
    driver.switch_to.window(afterPopup[0])


aceptar_fecha("btnAcept")

#--------Busca la tabla donde están las columnas y filas con los datos. (PUEDE SER UNA FUNCIÓN)--

# Método usando 'requests' y 'read_html'.
"""
req=requests.get(driver.current_url)
table = pd.read_html(req.text,attrs={'id':'GrdResultados'},encoding='utf-8')

df_categoría = table[0] # Este índice de la tabla de HTML es el DataFrame.
df_categoría.rename(columns={'Tasas de interés - Por depósitos - Series diarias - BADLAR - Tasas de interés por depósitos a plazo fijo de 30 a 35 días de plazo - Depósitos de más de un millón de pesos, en porcentaje nominal anual - Bancos privados': 'Badlar'}, inplace=True)
"""

def busca_tabla(nombre_original,nombre_nuevo):
    """Busca la tabla donde están las columnas y filas con los datos. Renombra las columnas"""
    req=requests.get(driver.current_url)
    table = pd.read_html(req.text,attrs={'id':'GrdResultados'},encoding='utf-8')
    df_categoría = table[0] # Este índice de la tabla de HTML es el DataFrame.
    df_categoría.rename(columns={f"{nombre_original}" : f"{nombre_nuevo}"}, inplace=True)
    return df_categoría

for value in nombres_columnas.values():
    print(value)
    #df_categoría= busca_tabla(value,value)
    #print(df_categoría)

#---TENDRÍA QUE HACER UNA LISTA DE LOS QUE YA SE PASARON O ALGO ASÍ---

#-----Solucionar problemas de caracteres raros. (PUEDE SER UNA FUNCIÓN)--TENER EN CUENTA EL CASO LOS NOMBRES DE COLUMNAS DE UVA---
#---TIENE QUE DEVOLVER 3 DF POR SEPARADO, PARA TRATARLOS DESPUES Y JUNTARLOS---
def formatos(df_categoría):
    #Solucionar problemas de caracteres raros

    df_categoría['Fecha']=df_categoría['Fecha'].str.encode('ascii', errors='ignore')

    if df_categoría.columns[1] == 'Badlar':
        df_categoría['Badlar']=df_categoría['Badlar'].str.encode('ascii', errors='ignore')
    elif df_categoría.columns[1] == 'UVA':
        df_categoría['UVA']=df_categoría['UVA'].str.encode('ascii', errors='ignore')
    elif df_categoría.columns[1] == 'CER':
        df_categoría['CER']=df_categoría['CER'].str.encode('ascii', errors='ignore')

    df_categoría['Fecha']=df_categoría['Fecha'].str.decode("utf-8")

    if df_categoría.columns[1] == 'Badlar':
        df_categoría['Badlar']=df_categoría['Badlar'].str.decode("utf-8")
    if df_categoría.columns[1] == 'CER':
        df_categoría['CER']=df_categoría['CER'].str.decode("utf-8")
    if df_categoría.columns[1] == 'CER':
        df_categoría['CER']=df_categoría['CER'].str.decode("utf-8")
    df_categoría.replace('&nbsp','',regex=True,inplace=True)
    df_categoría.drop([0],inplace=True)
# Limpieza y revisión del dataframe. (TIENE QUE SER UNA FUNCIÓN SÍ O SÍ)----

print(df_categoría.head())
print(df_categoría.info())
    


formatos(df_categoría) """
# Exportar como csv.
#df.to_csv('datos.csv',encoding='utf-8',index=False)
#time.sleep(5)






"""
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

"""
