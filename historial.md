# Historial de desarrollo

Línea de tiempo del desarrollo del proyecto **Flask MVC** (18/11/2026).

---

## 1. Estructura MVC con Flask

**Fecha:** 18/11/2026

Se creó la estructura de carpetas del proyecto siguiendo el patrón Modelo-Vista-Controlador:

- **Modelo** (`app/models/`) — capa de datos con SQLAlchemy.
- **Controlador** (`app/controllers/`) — Blueprints y rutas.
- **Vista** (`app/views/`) — plantillas Jinja2.

Detalles:

- Factory pattern con `create_app()` en `app/__init__.py`.
- Configuración por entorno (development/testing/production) en `app/config.py`.
- Extensiones (`db`, `migrate`) en `app/extensions.py`.
- Modelo de ejemplo `User` (id, username, email).
- Blueprints `main` (`/`) y `user` (`/users/`).
- Punto de entrada `run.py`, `requirements.txt`, `.gitignore` y `README.md`.
- Entorno virtual `venv` con Flask, Flask-SQLAlchemy y Flask-Migrate.
- 2 pruebas iniciales pasando; servidor verificado en `/` (HTTP 200).

**Archivos creados:** `run.py`, `requirements.txt`, `.gitignore`, `README.md`, `app/__init__.py`, `app/config.py`, `app/extensions.py`, `app/models/*`, `app/controllers/*`, `app/views/*`, `tests/*`.

---

## 2. Vista con Navbar y Sidebar

**Fecha:** 18/11/2026

Se reemplazó el index por un layout con barra de navegación fija y barra lateral:

- Tema minimalista claro: navbar blanca, sidebar con enlaces e iconos SVG.
- CSS (`app/views/static/css/style.css`) con CSS Grid/Fixed layout y variables de color.
- JS (`app/views/static/js/main.js`): toggle del sidebar en móvil (hamburguesa + overlay) y enlace activo según la URL.
- Responsive: en pantallas < 768px el sidebar se oculta.

Ajustes necesarios:

- `static_folder="views/static"` en `create_app()` para servir los estáticos.
- `db.create_all()` al arrancar para crear las tablas (corrige error 500 en `/users/`).

**Archivos modificados:** `app/__init__.py`, `app/views/base.html`, `app/views/main/index.html`, `app/views/static/css/style.css`, `app/views/static/js/main.js`.

---

## 3. Definición de rutas

**Fecha:** 18/11/2026

Se aclaró que las rutas se definen en los controladores (Blueprints):

- `app/controllers/main.py` — ruta `/`.
- `app/controllers/user.py` — prefijo `/users/`.
- Registro en `app/__init__.py` con `app.register_blueprint(...)`.

---

## 4. CRUD de usuarios

**Fecha:** 18/11/2026

Se implementó el CRUD completo con vistas HTML y validación mínima:

| Método | Ruta | Acción |
|---|---|---|
| GET | `/users/` | Listado (tabla) |
| GET | `/users/new` | Formulario crear |
| POST | `/users/` | Crear |
| GET | `/users/<id>/edit` | Formulario editar |
| POST | `/users/<id>` | Actualizar |
| POST | `/users/<id>/delete` | Eliminar |

Detalles:

- Vistas `user/list.html` (tabla + estado vacío) y `user/form.html` (crear/editar reutilizado).
- Flash messages para feedback, patrón PRG (redirect tras POST), 404 si el id no existe.
- Confirmación de borrón con `data-confirm` en JS.
- Estilos de tabla, formulario y botones en `style.css`.
- 6 pruebas unitarias (crear, editar, eliminar, 404, listado).
- Flujo completo verificado con curl (302 en cada POST, listado y 404).

**Archivos:** `app/controllers/user.py` (reescrito), `app/views/user/list.html`, `app/views/user/form.html`, `app/views/base.html`, `app/views/static/css/style.css`, `app/views/static/js/main.js`, `tests/test_app.py`.

---

## 5. Notyf + iconos en botones

**Fecha:** 18/11/2026

Se sustituyeron las alertas HTML por notificaciones toast y se mejoró la UI de la tabla:

- **Notyf v3** (CDN jsdelivr): `notyf.min.css` y `notyf.min.js` en `base.html`.
- Los flash messages se envían como JSON oculto (`#flash-messages`) y `main.js` los muestra con `notyf.success()` / `notyf.error()` (3s, esquina superior derecha).
- Botones **Editar** (icono lápiz) y **Eliminar** (icono papelera) solo con iconos SVG, accesibles con `title`/`aria-label`.
- Nueva clase `.btn-icon`; eliminados estilos huérfanos `.alert` y `.flashes`.

**Archivos:** `app/views/base.html`, `app/views/static/js/main.js`, `app/views/static/css/style.css`, `app/views/user/list.html`.

---

## 6. Formularios como modales

**Fecha:** 18/11/2026

Los formularios de crear y editar dejaron de ser páginas separadas para convertirse en un modal dentro del listado:

- **Modal único** en `user/list.html`: overlay + diálogo con título, formulario (username, email) y pie de acciones.
- Botón **"+ Nuevo usuario"** abre el modal vacío (acción = `POST /users/`).
- Icono **Editar** lo abre precargado con `data-id`, `data-username` y `data-email` (acción = `POST /users/<id>`).
- Cierre por ✕, botón Cancelar, clic en el overlay y tecla `ESC`.
- **Eliminadas** las rutas `GET /users/new` y `GET /users/<id>/edit` y el archivo `user/form.html`.
- Errores de validación: redirect al listado + Notyf (modal cerrado).
- Nuevos estilos `.modal-overlay`, `.modal`, `.modal-header/body/footer`; eliminado `.form-card`.
- 7 pruebas unitarias (nueva: presencia del modal; 404 ahora vía `POST /users/999`).

**Archivos:** `app/controllers/user.py`, `app/views/user/list.html`, `app/views/static/js/main.js`, `app/views/static/css/style.css`, `tests/test_app.py`; eliminado `app/views/user/form.html`.

---

## 7. Modal de confirmación para eliminar

**Fecha:** 18/11/2026

Se sustituyó el `window.confirm()` nativo por un modal de confirmación propio:

- **Modal genérico** `#confirm-modal` en `base.html` (`role="alertdialog"`): título, mensaje, Cancelar y botón **Eliminar** en rojo sólido (`.btn-danger-solid`).
- `main.js`: al enviar un `form[data-confirm]` se abre el modal; al confirmar se marca `dataset.confirmed` y se envía el form (sin bucle). Cierre por ✕, Cancelar, overlay y `ESC`.
- Estilos `.modal-confirm` (380px) y `.btn-danger-solid`.
- Test ampliado para exigir `confirm-modal` en el listado (7 pruebas).

**Archivos:** `app/views/base.html`, `app/views/static/js/main.js`, `app/views/static/css/style.css`, `tests/test_app.py`.

---

## Estado actual del proyecto

```
port/
├── app/
│   ├── __init__.py          # Factory + static_folder + db.create_all()
│   ├── config.py            # dev / test / prod
│   ├── extensions.py        # db, migrate
│   ├── models/              # User
│   ├── controllers/         # main (CRUD rutas), user (CRUD completo)
│   └── views/               # base.html, main/, user/, static/css, static/js
├── tests/                   # 7 pruebas
├── run.py
├── requirements.txt
├── .gitignore
├── README.md
└── historial.md             # este archivo
```

**Ejecutar:**

```bash
venv\Scripts\activate
python run.py
```

**Pruebas:**

```bash
python -m unittest discover tests
```

**Servidor:** http://127.0.0.1:5000 — rutas: `/`, `/users/`, `/users/new`.
