# NUTRIA

repositorio para agente nutricional Nutria

## Descripción del Proyecto Nutria

Nutria es un innovador asistente nutricional desarrollado como un sistema multiagente, que aprovecha el poder de Semantic Kernel y Python para ofrecer recomendaciones personalizadas de nutrición basadas en inteligencia artificial.
Nuestro asistente combina varios agentes especializados que trabajan en conjunto para analizar preferencias alimenticias, restricciones dietéticas, objetivos de salud y patrones de consumo. Utilizando el framework de Semantic Kernel, Nutria puede comprender el lenguaje natural de los usuarios y proporcionar respuestas contextualizadas y personalizadas.
Nutria no solo recomienda alimentos, sino que aprende continuamente de las interacciones con el usuario para mejorar sus sugerencias con el tiempo. El sistema puede planificar comidas, sugerir alternativas saludables, calcular valores nutricionales y ayudar a los usuarios a mantener un estilo de vida equilibrado.
La arquitectura multiagente permite que diferentes componentes se especialicen en tareas específicas como análisis nutricional, planificación de comidas, educación al usuario y seguimiento de objetivos, todo integrado en una interfaz conversacional natural y accesible.

## Instrucciones de uso

- crea entorno virtual en python:

  ```bash
    py -m venv .venv
  ```

- instala dependencias:

  ```bash
    pip install -r requirements.txt
  ```

- crea un archivo .env tomando como base el archivo env.example y utiliza un token valido de github Models
- El proyecto se diseño usando openAI, asi que puedes utilizar el endpoint del archivo env.example o usar uno de azure por ejemplo, pero valida que el token ingresado sea valido

- ejecuta el punto de entrada:

  ```bash
    py api.py
  ```

- Disfruta

### Autor

Jose Luis Ojeda Polo

- Contacto: +57 3007730068
- Correo: <jlojeda0903@gmail.com>
- Correo corporativo: <joseojeda@seti.com.co>
- github: HannPark
