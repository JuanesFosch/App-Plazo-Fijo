from urllib.request import urlopen

import mechanicalsoup

url=mechanicalsoup.StatefulBrowser()

url.open ("https://www.bcra.gob.ar/Estadisticas/EstadisSitiopublico/")

url.follow_link()

url.page

#url.launch_browser()

url.page.find_all('tr')

url.select_form()

url.form.print_summary()



botón_ver = '<input border="0" id="btnAcept" name="btnAcept" src="../../Imagenes/Comunes/btnver.jpg" style="cursor: pointer;" type="image"/>'
checkbox_tasas="TreeView1n52CheckBox"

url["TreeView1n52CheckBox"] = "TreeView1t52"

#url.launch_browser()

"""
page = browser.get(url)

print(page)

html=page.soup

print(type(page.soup))

#print(html)

form = html.select("input")

#BUSCAR EN EL CÓDIGO FUENTE CADA CHECKBOX DEL FORM (IR BAJANDO POR LAS TREEVIEW), TIENEN NOMBRE E ID 

print(form)
"""

