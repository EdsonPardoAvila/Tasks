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

## 8. Estilo flat/minimalista con desenfoque en modales

**Fecha:** 18/11/2026

Se aplicó un estilo flat/minimalista a los modales con desenfoque moderado del fondo:

- **Overlay:** tinte más suave `rgba(0,0,0,0.25)` + `backdrop-filter: blur(5px)` (con prefijo `-webkit-` para Safari).
- **Modal flat:** sombra reducida (`0 8px 24px rgba(0,0,0,0.08)`), borde de 1px `var(--border)` en lugar de profundidad por sombra.
- **Animación plana:** fade de opacidad sin desplazamiento.
- Aplica a ambos modales (formulario y confirmación); el overlay del sidebar no cambió.

**Archivos:** `app/views/static/css/style.css`, `historial.md`.

---

## 9. Paleta pastel multicolor en botones

**Fecha:** 18/11/2026

Se aplicaron tonos pastel a los botones y se registró una paleta multicolor como variables del diseño (estilo flat coherente con el cambio anterior):

### Paleta pastel (variables en `:root`)

| Color | Fondo | Texto | Hover |
|---|---|---|---|
| Azul | `#dbeafe` | `#1d4ed8` | `#bfdbfe` |
| Verde | `#dcfce7` | `#15803d` | `#bbf7d0` |
| Ámbar | `#fef3c7` | `#b45309` | `#fde68a` |
| Rosa | `#ffe4e6` | `#be123c` | `#fecdd3` |
| Violeta | `#ede9fe` | `#6d28d9` | `#ddd6fe` |

### Aplicación en botones

| Clase | Uso | Pastel |
|---|---|---|
| `.btn-primary` | "+ Nuevo usuario", "Crear/Guardar" | Azul |
| `.btn-danger` | icono Eliminar (tabla) | Rosa |
| `.btn-danger-solid` | confirmación "Eliminar" | Rosa marcado (`#fecdd3` / `#9f1239`, hover `#fda4af`) |
| `.btn` | "Cancelar" | Neutro (sin cambio) |
| `.btn-success` | utilitaria (nueva) | Verde |
| `.btn-warning` | utilitaria (nueva) | Ámbar |
| `.btn-info` | utilitaria (nueva) | Violeta |

**Archivos:** `app/views/static/css/style.css`, `historial.md`.

---

## 10. Módulo calendario

**Fecha:** 19/11/2026

Se creó el módulo calendario con vista mensual y modelo `Event` listo para futuros eventos y tareas:

- **Modelo** `Event` (`app/models/event.py`, tabla `events`): title, description, start, end, all_day, color, created_at. Sin UI de creación aún.
- **Blueprint** `calendar` (`app/controllers/calendar.py`, prefijo `/calendar`):
  - `GET /calendar/` — vista del calendario.
  - `GET /calendar/api/events` — JSON `[]` (feed preparado para FullCalendar).
- **Vista** `calendar/index.html`: FullCalendar v6 por CDN (`fullcalendar@6.1.21` + locale `es`), vistas mes/semana/día, toolbar en español, `firstDay: 1` (lunes).
- **Sidebar**: enlace "Calendario" en `base.html`.
- **CSS**: estilos `#calendar` / `.fc` con variables del tema (borde, botones pastel azul, hoy resaltado).
- **Blueprint registrado** en `create_app()`.
- **3 pruebas nuevas**: página `/calendar/`, API `events` vacía, enlace en sidebar (10 en total).
- Modelo `Task` (separado) queda para una entrega futura, junto con el CRUD de eventos.

**Archivos:** `app/models/event.py`, `app/models/__init__.py`, `app/controllers/calendar.py`, `app/views/calendar/index.html`, `app/__init__.py`, `app/views/base.html`, `app/views/static/css/style.css`, `tests/test_app.py`, `historial.md`.

---

## 11. Paleta del calendario y CRUD de eventos

**Fecha:** 19/11/2026

Se ajustó FullCalendar a la paleta pastel del proyecto y se implementó el CRUD completo de eventos:

### Paleta
- Variables CSS de `#calendar .fc` mapeadas a los tokens del tema (`--border`, `--accent-soft`, pastel azul para botones/eventos, rosa para el indicador "ahora").
- Eventos con fondo pastel + `textColor` oscuro (mapa `PALETTE` en el controller) para mantener contraste legible.
- Estilos flat: celdas de hoy con `--accent-soft`, cabecera con `--bg`, eventos con radio 6px, fin de semana atenuado.
- Swatches de color en el modal (5 colores pastel) y soporte de `textarea`/`select` en `.form-group`.

### CRUD de eventos
| Método | Ruta | Acción |
|---|---|---|
| GET | `/calendar/api/events` | Feed JSON de FullCalendar desde la BD |
| POST | `/calendar/events/` | Crear (validación + PRG) |
| POST | `/calendar/events/<id>` | Actualizar |
| POST | `/calendar/events/<id>/delete` | Eliminar (confirm modal) |

- Validación: título y inicio obligatorios; fin ≥ inicio; color fuera de paleta → default `#dbeafe`.
- `all_day`: normaliza a medianoche; el feed usa fechas `YYYY-MM-DD` con `end` exclusivo de FullCalendar.
- **Modal** `#event-modal` en `calendar/index.html`: título, descripción, todo el día (alterna `date`/`datetime-local`), inicio/fin, swatches de color.
- **`calendar.js`**: init FullCalendar, `dateClick` → modal de creación (09:00–10:00), `eventClick` → edición con botón Eliminar (`data-confirm`), botón "+ Nuevo evento".
- **10 pruebas nuevas** (19 en total): crear, validación, actualizar, eliminar, 404, formato `all_day`, color inválido, modal en página.

**Archivos:** `app/controllers/calendar.py`, `app/views/calendar/index.html`, `app/views/static/js/calendar.js`, `app/views/static/css/style.css`, `tests/test_app.py`, `historial.md`.

---

## 12. Mejora de diseño del modal de eventos

**Fecha:** 19/11/2026

Se rediseñó el modal (también aplica al de usuarios) con foco en scroll, tamaño y responsividad:

- **Estructura flex:** `.modal` es columna con `max-height: min(92vh, 720px)`; header y footer fijos, `.modal-body` con `overflow-y: auto` y scrollbar sutil del tema.
- **Tamaño:** `max-width` de 440px → 480px; en móvil `100%` / `95vh` y overlay con menos padding.
- **Organización del form:** sección "Periodo" con cabecera (etiqueta + checkbox "Todo el día") e Inicio/Fin en grid de 2 columnas (`.form-period` / `.period-header` / `.form-row`); colores al final; en ≤768px las fechas se apilan.
- **Footer responsivo:** `flex-wrap`, "Eliminar" a la izquierda (`btn-delete-left`); en ≤480px botones en columna full-width.
- **Tests:** 19 OK (sin cambios en lógica).

**Archivos:** `app/views/static/css/style.css`, `app/views/calendar/index.html`, `historial.md`.

---

## 13. Dropdown de acciones del evento

**Fecha:** 19/11/2026

Se separó el flujo de acciones del evento del modal de crear/editar:

- **Crear:** el modal de form ya **no** tiene botón "Eliminar" (no hay nada que borrar).
- **Clic en un evento:** ya no abre edición directa; muestra un **dropdown** (`#event-dropdown`) junto al cursor con:
  - **Ver más** → modal de solo lectura (`#event-detail-modal`): título, periodo formateado (`Intl` es) y descripción.
  - **Editar** → modal form existente en modo edición (solo Cancelar | Guardar).
  - **Eliminar** → reutiliza `#confirm-modal` de `base.html` vía `#event-delete-form` (`data-confirm`).
- Dropdown: cerrar con clic fuera, `ESC` o scroll; posicionado sin salirse del viewport; ítem danger en rosa pastel.
- **Tests:** 19 OK (página exige dropdown y detalle, y `assertNotIn` de `event-delete-btn`).

**Archivos:** `app/views/calendar/index.html`, `app/views/static/js/calendar.js`, `app/views/static/css/style.css`, `tests/test_app.py`, `historial.md`.

---

## 14. Fix dropdown y mejora visual del calendario

**Fecha:** 19/11/2026

### Bug fix: dropdown al clickear un evento
- **Causa:** el mismo click burbujeaba al listener de `document` y cerraba el dropdown recién abierto (parpadeo / no aparecía).
- **Fix:** `stopPropagation()` + `preventDefault()` en `eventClick`; guardia temporal de 150 ms en el handler de `document`; no cerrar si el click fue dentro de `.fc-event`.

### Más eventos por día
- `dayMaxEvents: 3`: hasta 3 eventos por celda y link nativo **"+N más"** (popover de FullCalendar).

### Diseño visual
- Toolbar: título 1.2rem semibold, botones pastel con focus ring, grupos de vistas con radio limpio.
- Cabeceras de día: uppercase, letter-spacing, muted.
- Celdas: hover sutil en número, hoy resaltado, días de otro mes atenuados.
- Eventos: radio 6px, font-weight 500, hover con leve elevación; estilo del link "+N más" y del popover.
- Vista semana/día: slots, eje de horas y "ahora" (rosa) con la paleta del tema.
- Lista: bordes/radius del tema.

### Responsive
- ≤768px: toolbar en 2 filas (título centrado arriba), botones/celdas/eventos más compactos.
- ≤480px: se oculta el botón "Día" del toolbar; celdas y eventos aún más compactos.

**Archivos:** `app/views/static/js/calendar.js`, `app/views/static/css/style.css`, `historial.md`.

---

## 15. Días festivos de Colombia

**Fecha:** 19/11/2026

Se agregaron los días festivos de Colombia al calendario, con estilo propio:

- **`app/holidays.py`:** `easter_sunday()` (Meeus/Jones/Butcher) + `colombian_holidays(year)` → 17 festivos/año (12 fijos + Jueves/Viernes Santo + Ascensión, Corpus Christi y Sagrado Corazón trasladados al lunes). `holidays_as_events()` los convierte en eventos de FullCalendar.
- **API** `GET /calendar/api/events`: lee `start`/`end` de FullCalendar, genera festivos del rango de años y los mezcla con los eventos de BD (ordenados por fecha).
- **Estilo:** neutro slate (`#f1f5f9` / `#475569`) + borde izquierdo `#94a3b8` y clase `.fc-holiday` — distinto de los 5 colores de eventos, dentro del tema flat.
- **Clic en festivo:** abre el modal de detalle en solo lectura (sin dropdown Editar/Eliminar).
- **Tests:** 22 en total (festivos 2026, presencia en API, no rompen eventos de usuario, feed "vacío" = sin eventos de usuario pero con festivos).

**Archivos:** `app/holidays.py`, `app/controllers/calendar.py`, `app/views/static/js/calendar.js`, `app/views/static/css/style.css`, `tests/test_app.py`, `historial.md`.

---

## Estado actual del proyecto

```
port/
├── app/
│   ├── __init__.py          # Factory + static_folder + db.create_all()
│   ├── config.py            # dev / test / prod
│   ├── extensions.py        # db, migrate
│   ├── holidays.py          # festivos Colombia + Pascua
│   ├── models/              # User, Event
│   ├── controllers/         # main, user (CRUD), calendar (CRUD + festivos)
│   └── views/               # base.html, main/, user/, calendar/, static/css, static/js
├── tests/                   # 22 pruebas
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

**Servidor:** http://127.0.0.1:5000 — rutas: `/`, `/users/`, `/calendar/`.
