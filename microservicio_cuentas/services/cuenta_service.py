from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from errors import AppError, ConflictError, NotFoundError
from extensions import db
from models import Cuenta

REQUIRED_FIELDS = ("nombre", "apellido", "documento", "correo", "num_cuenta")
UPDATABLE_FIELDS = ("nombre", "apellido", "documento", "correo", "saldo", "num_cuenta")


def _validate_payload(data, *, partial=False):
    if not isinstance(data, dict):
        raise AppError("El cuerpo de la solicitud debe ser un objeto JSON")

    fields = UPDATABLE_FIELDS if partial else REQUIRED_FIELDS

    if not partial:
        missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
        if missing:
            raise AppError(f"Campos requeridos faltantes: {', '.join(missing)}")

    cleaned = {}
    for field in fields:
        if field not in data:
            continue

        value = data[field]
        if value is None or (isinstance(value, str) and not value.strip()):
            raise AppError(f"El campo '{field}' no puede estar vacío")

        if field == "saldo":
            try:
                cleaned[field] = Decimal(str(value))
            except (InvalidOperation, ValueError):
                raise AppError("El campo 'saldo' debe ser un número válido")
        else:
            cleaned[field] = str(value).strip()

    return cleaned


def list_cuentas():
    return [cuenta.to_dict() for cuenta in Cuenta.query.order_by(Cuenta.id).all()]


def get_cuenta(cuenta_id):
    cuenta = db.session.get(Cuenta, cuenta_id)
    if cuenta is None:
        raise NotFoundError("Cuenta no encontrada")
    return cuenta.to_dict()


def create_cuenta(data):
    payload = _validate_payload(data)

    cuenta = Cuenta(
        nombre=payload["nombre"],
        apellido=payload["apellido"],
        documento=payload["documento"],
        correo=payload["correo"],
        num_cuenta=payload["num_cuenta"],
        saldo=payload.get("saldo", Decimal("0.00")),
    )

    db.session.add(cuenta)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ConflictError("Ya existe una cuenta con ese documento, correo o número de cuenta")

    return cuenta.to_dict(), 201


def update_cuenta(cuenta_id, data):
    cuenta = db.session.get(Cuenta, cuenta_id)
    if cuenta is None:
        raise NotFoundError("Cuenta no encontrada")

    payload = _validate_payload(data, partial=True)
    if not payload:
        raise AppError("No se enviaron campos para actualizar")

    for field, value in payload.items():
        setattr(cuenta, field, value)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ConflictError("Ya existe una cuenta con ese documento, correo o número de cuenta")

    return cuenta.to_dict()


def delete_cuenta(cuenta_id):
    cuenta = db.session.get(Cuenta, cuenta_id)
    if cuenta is None:
        raise NotFoundError("Cuenta no encontrada")

    db.session.delete(cuenta)
    db.session.commit()