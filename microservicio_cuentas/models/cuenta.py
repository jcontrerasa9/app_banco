from datetime import datetime, timezone
from decimal import Decimal

from extensions import db


class Cuenta(db.Model):
    __tablename__ = "cuentas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(30), nullable=False, unique=True, index=True)
    correo = db.Column(db.String(150), nullable=False, unique=True, index=True)
    saldo = db.Column(db.Numeric(15, 2), nullable=False, default=Decimal("0.00"))
    num_cuenta = db.Column(db.String(50), nullable=False, unique=True, index=True)
    fecha = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return (
            f"<Cuenta id={self.id} "
            f"documento={self.documento} "
            f"cuenta={self.num_cuenta}>"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "documento": self.documento,
            "correo": self.correo,
            "saldo": float(self.saldo),
            "num_cuenta": self.num_cuenta,
            "fecha": self.fecha.isoformat() if self.fecha else None,
        }