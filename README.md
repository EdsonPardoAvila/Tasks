# Proyecto Flask MVC

Estructura de carpetas en Python        .

## Estructura

```
port/
├── app/
│   ├── __init__.py      # Factory create_app()
│   ├── config.py        # Configuración por entorno
│   ├── extensions.py    # Extensiones (db, migrate)
│   ├── models/          # MODELO - capa de datos
│   ├── controllers/     # CONTROLADOR - Blueprints/rutas
│   └── views/           # VISTA - plantillas Jinja2
├── tests/               # Pruebas
├── run.py               # Punto de entrada
└── requirements.txt
```

## Uso

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python run.py
```

Servidor en http://127.0.0.1:5000

## Pruebas

```bash
python -m unittest discover tests
```

## Migraciones

```bash
flask --app run db init
flask --app run db migrate -m "mensaje"
flask --app run db upgrade
```
