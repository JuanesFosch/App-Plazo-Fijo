

#--------Dataframe de Bancos Privados.

#-------------Búsqueda por texto. (PUEDE SER UNA FUNCIÓN)-----
bancos = driver.find_element(by= By.ID, value="tBusqueda")
bancos.send_keys(valores_de_búsqueda['bancos_privados'][0])
ver_por_término= driver.find_element(By.ID,value="btnBuscar") 
ver_por_término.click()
check_bancos= driver.find_element(By.ID,value=valores_de_búsqueda['bancos_privados'][1])
check_bancos.click()

#--------Aceptar selección
ver=driver.find_element(By.ID,value="btnAcept")
ver.click()

#-------Llenar campos de fecha. (TIENE QUE SER UNA FUNCIÓN SÍ O SÍ)----
fecha_desde=driver.find_element(By.ID,value="fDesde")
fecha_desde.clear()
fecha_desde.send_keys(f_desde)

fecha_hasta=driver.find_element(By.ID,value="fHasta")
fecha_hasta.clear()
fecha_hasta.send_keys(f_hasta)

#------Aceptar selección de fecha. (TIENE QUE SER UNA FUNCIÓN SÍ O SÍ)----
ultimo_ver=driver.find_element(By.ID,value="btnAcept")
beforePopup= driver.window_handles
ultimo_ver.click()
afterPopup = driver.window_handles
afterPopup.remove(afterPopup[0])
driver.switch_to.window(afterPopup[0])

#--------Busca la tabla donde están las columnas y filas con los datos. (PUEDE SER UNA FUNCIÓN)--

# Método usando 'requests' y 'read_html'.

req=requests.get(driver.current_url)
table = pd.read_html(req.text,attrs={'id':'GrdResultados'},encoding='utf-8')

df_bancos = table[0] # Este índice de la tabla de HTML es el DataFrame.
df_bancos.rename(columns={'Tasas de interés - Por depósitos - Series diarias - BADLAR - Tasas de interés por depósitos a plazo fijo de 30 a 35 días de plazo - Depósitos de más de un millón de pesos, en porcentaje nominal anual - Bancos privados': 'Badlar'}, inplace=True)

#-----Solucionar problemas de caracteres raros. (PUEDE SER UNA FUNCIÓN)--
df_bancos['Fecha']=df_bancos['Fecha'].str.encode('ascii', errors='ignore')
df_bancos['Badlar']=df_bancos['Badlar'].str.encode('ascii', errors='ignore')

df_bancos['Fecha']=df_bancos['Fecha'].str.decode("utf-8")
df_bancos['Badlar']=df_bancos['Badlar'].str.decode("utf-8")

# Limpieza y revisión del dataframe. (TIENE QUE SER UNA FUNCIÓN SÍ O SÍ)----
df_bancos.replace('&nbsp','',regex=True,inplace=True)
df_bancos.drop([0],inplace=True)
#print(df_bancos.head())
#print(df_bancos.info())

# Exportar como csv.
#df.to_csv('datos.csv',encoding='utf-8',index=False)
#time.sleep(5)