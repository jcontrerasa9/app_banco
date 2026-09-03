from flask import Flask, jsonify, request

from config import Config
from errors import AppError
from extensions import db, migrate
from services import cuenta_service


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    import models  # noqa: F401

    register_routes(app)
    register_error_handlers(app)

    return app


def register_routes(app):
    @app.get("/")
    def index():
        return {"status": "ok", "message": "API Flask funcionando"}

    @app.get("/api/cuentas")
    def list_cuentas():
        return jsonify(cuenta_service.list_cuentas())

    @app.get("/api/cuentas/<int:cuenta_id>")
    def get_cuenta(cuenta_id):
        return jsonify(cuenta_service.get_cuenta(cuenta_id))

    @app.post("/api/cuentas")
    def create_cuenta():
        data, status = cuenta_service.create_cuenta(request.get_json(silent=True))
        return jsonify(data), status

    @app.put("/api/cuentas/<int:cuenta_id>")
    def update_cuenta(cuenta_id):
        return jsonify(cuenta_service.update_cuenta(cuenta_id, request.get_json(silent=True)))

    @app.delete("/api/cuentas/<int:cuenta_id>")
    def delete_cuenta(cuenta_id):
        cuenta_service.delete_cuenta(cuenta_id)
        return "", 204


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(404)
    def handle_not_found(_error):
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def handle_internal_error(_error):
        return jsonify({"error": "Error interno del servidor"}), 500


app = create_app()