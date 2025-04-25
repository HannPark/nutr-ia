# NUTRIA

repositorio para agente nutricional Nutria

nutr_ia/
├── config/
│   ├── __init__.py
│   ├── app_config.py            # Configuración general de la aplicación
│   └── openai_config.py         # Configuración de las APIs de OpenAI
├── agents/
│   ├── __init__.py
│   ├── base_agent.py            # Clase base para todos los agentes
│   ├── consultant_agent.py      # Agente Consultor
│   ├── nutritionist_agent.py    # Agente Nutriólogo
│   └── searcher_agent.py        # Agente Buscador
├── models/
│   ├── __init__.py
│   ├── patient_data.py          # Modelo de datos del paciente
│   ├── diagnosis.py             # Modelo de diagnóstico nutricional
│   └── diet_plan.py             # Modelo del plan de dieta
├── skills/
│   ├── __init__.py
│   ├── consultant_skills/       # Skills específicos del Agente Consultor
│   ├── nutritionist_skills/     # Skills específicos del Agente Nutriólogo
│   └── searcher_skills/         # Skills específicos del Agente Buscador
├── utils/
│   ├── __init__.py
│   ├── json_validator.py        # Validación de estructuras JSON
│   └── image_processor.py       # Procesamiento de imágenes (screenshots)
├── main.py                      # Punto de entrada de la aplicación
└── requirements.txt             # Dependencias del proyecto
