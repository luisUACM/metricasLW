Dashboard de métricas para programación y diseño

Una plataforma web que calcula métricas a partir de una o varias clases en python, 
todas centradas en la mejora de la programación de dichas clases. 
Mostradas de manera visual en formato de dasshboard.
Desarrollado en Python con Flask, Plotly y Bootstrap

Desarrollado por:
■ Luis Alberto Juárez Calderón
■ Wendy Ruiz Soto

Para correr la aplicación ejecutar el archivo wsgi.py

El proyecto se organiza de la siguiente manera:

src/__init__.py --> Archivo de creación y configuración para Flask
src/routes --> Contiene los archivos de las rutas de la plataforma web
src/templates --> Contiene las vistas html de la plataforma web
src/static --> Contiene imágenes, css y js necesarios para los templates
src/uploads --> Almacena el código del usuario en el archivo Clases.py
src/utils --> Contiene archivos y clases de la lógica y funcionamiento del programa

Dependencias:
Los siguientes paquetes deberán ser instalados para poder ejecutar el programa:
♦ Flask        3.0.2
♦ plotly       5.19.0
♦ numpy        1.26.4
♦ networkx     3.2.1
