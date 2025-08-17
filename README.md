# IA_NotasFeedBack

## Descripción

IA_NotasFeedBack es una aplicación web que gestiona estudiantes y sus notas, proporcionando feedback personalizado usando Inteligencia Artificial.
El proyecto está dividido en frontend (Vue 3) y backend (Django REST Framework), donde el backend se encarga de exponer un endpoint seguro que interactúa con la API de IA para generar recomendaciones según las notas de los estudiantes.

Esta app se desarrolló como prueba técnica para USAMEDIC, enfocándose en la integración de IA de manera funcional y segura.

## Tecnologías utilizadas

Frontend: Vue 3, Composition API, Vite
Backend: Python 3.13, Django 5.2, Django REST Framework
IA: OpenAI GPT-4o 
Control de versiones: Git & GitHub

## Requisitos previos

-Node.js >= 20.x
-npm >= 10.x
-Python >= 3.13
-Virtualenv para Python
-Cuenta y API Key de OpenAI (u otro proveedor de IA), La key se adjuntara por correo


## Configuración del backend
1)Crear y activar un entorno virtual:
      python -m venv venv
2) Para la instalacion del backend apoyarse del archivo requirements.txt, que se encuentra en la carpeta del backend:
      pip install -r requirements.txt
3)Crear un archivo .env en IA_NotasFeedBack_Backend/backend/ con el API Key:
      OPENAI_API_KEY="el api key"
4)Aplicar migraciones
      python manage.py migrate
5)Ejecutar el servidor
      python manage.py runserver
      El backend estará disponible en: http://127.0.0.1:8000/

## Configuración del frontend
Primero posicionarse en la carpeta IA_NotasFeedBack_Frontend, ingresar y luego:
1)Instalar dependencias:
      npm install
2)Ejecutar servidor de desarrollo:
      npm run dev
3)Abrir la aplicación en el navegador:
      http://localhost:5173
