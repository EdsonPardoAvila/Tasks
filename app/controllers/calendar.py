from datetime import datetime, time, timedelta

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for

from app.extensions import db
from app.holidays import holidays_as_events
from app.models import Event

bp = Blueprint("calendar", __name__, url_prefix="/calendar")

PALETTE = {
    "#dbeafe": "#1d4ed8",
    "#dcfce7": "#15803d",
    "#fef3c7": "#b45309",
    "#ffe4e6": "#be123c",
    "#ede9fe": "#6d28d9",
}

DEFAULT_COLOR = "#dbeafe"


@bp.route("/")
def index():
    return render_template("calendar/index.html")


def _parse_dt(value):
    if not value:
        return None
    for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def _serialize_event(event):
    data = {
        "id": event.id,
        "title": event.title,
        "description": event.description or "",
        "allDay": event.all_day,
        "color": event.color or DEFAULT_COLOR,
        "textColor": PALETTE.get(event.color or DEFAULT_COLOR, "#1d4ed8"),
    }
    if event.all_day:
        data["start"] = event.start.date().isoformat()
        if event.end and event.end.date() != event.start.date():
            data["end"] = (event.end.date() + timedelta(days=1)).isoformat()
    else:
        data["start"] = event.start.isoformat()
        if event.end:
            data["end"] = event.end.isoformat()
    return data


@bp.route("/api/events")
def api_events():
    events = Event.query.order_by(Event.start).all()
    payload = [_serialize_event(e) for e in events]

    start_arg = request.args.get("start", "")
    end_arg = request.args.get("end", "")
    start_year = datetime.now().year - 1
    end_year = datetime.now().year + 1
    for arg, attr in ((start_arg, "start"), (end_arg, "end")):
        parsed = _parse_dt(arg[:10]) if arg else None
        if parsed:
            if attr == "start":
                start_year = parsed.year
            else:
                end_year = parsed.year
    if start_year > end_year:
        start_year, end_year = end_year, start_year

    payload.extend(holidays_as_events(start_year, end_year))
    payload.sort(key=lambda e: e.get("start", ""))
    return jsonify(payload)


def _read_form():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip() or None
    color = request.form.get("color", DEFAULT_COLOR)
    if color not in PALETTE:
        color = DEFAULT_COLOR
    all_day = request.form.get("all_day") == "on"
    start = _parse_dt(request.form.get("start", ""))
    end = _parse_dt(request.form.get("end", ""))

    errors = []
    if not title:
        errors.append("El título es obligatorio.")
    if not request.form.get("start"):
        errors.append("La fecha de inicio es obligatoria.")
    elif start is None:
        errors.append("La fecha de inicio no es válida.")
    if request.form.get("end") and end is None:
        errors.append("La fecha de fin no es válida.")
    if start and end and end < start:
        errors.append("El fin no puede ser anterior al inicio.")

    if all_day and start:
        start = datetime.combine(start.date(), time.min)
        if end:
            end = datetime.combine(end.date(), time.min)
            if end < start:
                end = start

    return {
        "title": title,
        "description": description,
        "color": color,
        "all_day": all_day,
        "start": start,
        "end": end,
    }, errors


@bp.route("/events/", methods=["POST"])
def create():
    data, errors = _read_form()
    if errors:
        flash(" ".join(errors), "error")
        return redirect(url_for("calendar.index"))

    event = Event(**data)
    db.session.add(event)
    db.session.commit()
    flash("Evento creado correctamente.", "success")
    return redirect(url_for("calendar.index"))


@bp.route("/events/<int:event_id>", methods=["POST"])
def update(event_id):
    event = db.session.get(Event, event_id) or abort(404)
    data, errors = _read_form()
    if errors:
        flash(" ".join(errors), "error")
        return redirect(url_for("calendar.index"))

    for key, value in data.items():
        setattr(event, key, value)
    db.session.commit()
    flash("Evento actualizado correctamente.", "success")
    return redirect(url_for("calendar.index"))


@bp.route("/events/<int:event_id>/delete", methods=["POST"])
def delete(event_id):
    event = db.session.get(Event, event_id) or abort(404)
    db.session.delete(event)
    db.session.commit()
    flash("Evento eliminado.", "success")
    return redirect(url_for("calendar.index"))
