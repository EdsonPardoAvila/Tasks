from datetime import date, timedelta


def easter_sunday(year):
    """Gregorian Easter (Meeus/Jones/Butcher)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def _next_monday(d):
    return d + timedelta(days=(7 - d.weekday()) % 7)


def colombian_holidays(year):
    """Lista de días festivos de Colombia para un año.

    Retorna [{date, title}] ordenado por fecha.
    Jueves/Viernes Santo van en su fecha; Ascensión, Corpus Christi y
    Sagrado Corazón se trasladan al lunes (práctica de puentes).
    """
    easter = easter_sunday(year)

    fixed = [
        (date(year, 1, 1), "Año Nuevo"),
        (date(year, 1, 6), "Día de los Reyes Magos"),
        (date(year, 3, 19), "Día de San José"),
        (date(year, 5, 1), "Día del Trabajo"),
        (date(year, 7, 20), "Día de la Independencia"),
        (date(year, 8, 7), "Batalla de Boyacá"),
        (date(year, 8, 15), "Asunción de la Virgen"),
        (date(year, 10, 12), "Día de la Raza"),
        (date(year, 11, 1), "Todos los Santos"),
        (date(year, 11, 11), "Independencia de Cartagena"),
        (date(year, 12, 8), "Inmaculada Concepción"),
        (date(year, 12, 25), "Navidad"),
    ]

    movable = [
        (easter - timedelta(days=3), "Jueves Santo"),
        (easter - timedelta(days=2), "Viernes Santo"),
        (_next_monday(easter + timedelta(days=39)), "Ascensión del Señor"),
        (_next_monday(easter + timedelta(days=60)), "Corpus Christi"),
        (_next_monday(easter + timedelta(days=68)), "Sagrado Corazón de Jesús"),
    ]

    holidays = fixed + movable
    holidays.sort(key=lambda item: item[0])
    return [{"date": d, "title": title} for d, title in holidays]


def holidays_as_events(start_year, end_year):
    """Festivos como eventos de FullCalendar en un rango de años."""
    events = []
    for year in range(start_year, end_year + 1):
        for h in colombian_holidays(year):
            events.append(
                {
                    "id": f"hol-{h['date'].isoformat()}",
                    "title": h["title"],
                    "start": h["date"].isoformat(),
                    "allDay": True,
                    "color": "#f1f5f9",
                    "textColor": "#475569",
                    "classNames": ["fc-holiday"],
                    "extendedProps": {
                        "holiday": True,
                        "description": "Día festivo en Colombia",
                    },
                }
            )
    events.sort(key=lambda e: e["start"])
    return events
