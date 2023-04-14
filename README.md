### App-Plazo-Fijo

Este es un proyecto de Web Scraping para obtener los datos de las tasas de interés del BCRA para los plazos fijos, y de la cotización del dólar. 
La idea es traer los datos históricos y actualizarlos todos los días, para crear una comparación entre las dos formas de inversión.
La página web del BCRA no es muy amigable para el usuario y tampoco tiene una API, por lo que es difícil consultar este tipo de datos.

Con Selenium y Pandas pude recolectar los datos y crear un conjunto de datos que se pueden exportar en formatos cómodos y así poder visualizarlos.

Lo siguiente es crear con Django una aplicación web con estas visualizaciones.

