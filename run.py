import os
from flask import Flask, request, session, redirect, url_for, flash, make_response
from datetime import date
from controllers import medico_controller, paciente_controller, consulta_controller
from database import db

# ============================================
# INICIALIZACIÓN DE LA APLICACIÓN
# ============================================
app = Flask(__name__)

# Configuración para local y Render
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "sqlite:///clinica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or "clinica_secret_2026_render"

# Inicializar SQLAlchemy
db.init_app(app)

# Registrar Blueprints
app.register_blueprint(medico_controller)
app.register_blueprint(paciente_controller)
app.register_blueprint(consulta_controller)

# ============================================
# CONTEXT PROCESSOR (Para navbar activo)
# ============================================
@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path.startswith(path) else ''
    return dict(is_active=is_active)

# ============================================
# RUTA PRINCIPAL - HOME ESTILIZADO
# ============================================
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clínica Médica - Sistema de Gestión</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
            }
            .hero-section {
                padding: 60px 20px;
                text-align: center;
                color: white;
            }
            .hero-title {
                font-size: 3.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                animation: fadeInDown 1s ease;
            }
            .hero-subtitle {
                font-size: 1.3rem;
                margin-bottom: 3rem;
                opacity: 0.95;
                animation: fadeInUp 1s ease;
            }
            .menu-cards {
                display: flex;
                justify-content: center;
                gap: 30px;
                flex-wrap: wrap;
                margin: 40px 0;
            }
            .card-menu {
                background: white;
                border-radius: 15px;
                padding: 30px 40px;
                text-decoration: none;
                color: #333;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
                min-width: 200px;
                animation: fadeIn 1.2s ease;
            }
            .card-menu:hover {
                transform: translateY(-10px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.3);
                color: #333;
                text-decoration: none;
            }
            .card-menu i {
                font-size: 3rem;
                margin-bottom: 15px;
                display: block;
            }
            .card-menu.medicos i { color: #667eea; }
            .card-menu.pacientes i { color: #764ba2; }
            .card-menu.consultas i { color: #f093fb; }
            .card-menu h3 {
                margin: 0;
                font-size: 1.3rem;
                font-weight: 600;
            }
            .footer-credit {
                margin-top: 60px;
                padding: 20px;
                text-align: center;
                color: rgba(255,255,255,0.8);
                font-size: 0.9rem;
                animation: fadeIn 1.5s ease;
            }
            .footer-credit strong {
                color: white;
                font-weight: 600;
            }
            @keyframes fadeInDown {
                from { opacity: 0; transform: translateY(-30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @media (max-width: 768px) {
                .hero-title { font-size: 2.5rem; }
                .menu-cards { flex-direction: column; align-items: center; }
            }
        </style>
    </head>
    <body>
        <div class="hero-section">
            <h1 class="hero-title">
                <i class="bi bi-heart-pulse me-3"></i>Clínica Médica
            </h1>
            <p class="hero-subtitle">Sistema de Gestión con Flask + SQLAlchemy</p>
            
            <div class="menu-cards">
                <a href="/medicos" class="card-menu medicos">
                    <i class="bi bi-person-badge"></i>
                    <h3>Médicos</h3>
                </a>
                <a href="/pacientes" class="card-menu pacientes">
                    <i class="bi bi-people"></i>
                    <h3>Pacientes</h3>
                </a>
                <a href="/consultas" class="card-menu consultas">
                    <i class="bi bi-calendar-check"></i>
                    <h3>Consultas</h3>
                </a>
            </div>
            
            <div class="footer-credit">
                <p>Elaborado por la Univ. <strong>PAMELA MAMANI MARQUEZ</strong></p>
                <p class="mb-0"><small>Gestión Académica 2026</small></p>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

# ============================================
# RUTA DE LOGOUT (Cerrar Sesión)
# ============================================
@app.route("/logout")
def logout():
    """Cerrar sesión y limpiar datos de usuario"""
    session.clear()
    flash('👋 Sesión cerrada correctamente. ¡Hasta pronto!', 'info')
    return redirect(url_for('home'))

# ============================================
# RUTA PARA INICIALIZAR BASE DE DATOS (Render)
# ============================================
@app.route("/init-db")
def init_db_route():
    """Inicializar la base de datos con datos de prueba"""
    from models.medico_model import Medico
    from models.paciente_model import Paciente
    from models.consulta_model import Consulta
    
    with app.app_context():
        db.create_all()
        
        # Solo crear datos si no existen
        if not Medico.query.first():
            # Crear médico de prueba
            doctor = Medico(
                nombre="Dr. Mario Torrez",
                especialidad="Medicina General",
                telefono="777-1234",
                correo="mario@clinica.com"
            )
            db.session.add(doctor)
            
            # Crear paciente de prueba
            paciente = Paciente(
                nombre="Pamela Mamani",
                edad=22,
                direccion="Av. Principal #123",
                telefono="666-5678"
            )
            db.session.add(paciente)
            db.session.commit()
            
            # Crear consulta de prueba (relacionada)
            consulta = Consulta(
                fecha=date.today(),
                diagnostico="Control médico rutinario",
                tratamiento="Reposo y vitaminas",
                medico_id=doctor.id,
                paciente_id=paciente.id
            )
            db.session.add(consulta)
            db.session.commit()
            
            return """
            <div style="text-align:center; padding: 50px; font-family: sans-serif;">
                <h1 style="color:#28a745;">✅ Base de datos creada exitosamente</h1>
                <p>Se han creado: 1 Médico, 1 Paciente y 1 Consulta de prueba.</p>
                <a href="/" style="display:inline-block; margin-top:20px; padding:10px 20px; background:#667eea; color:white; text-decoration:none; border-radius:5px;">Ir al Inicio</a>
            </div>
            """
        else:
            return """
            <div style="text-align:center; padding: 50px; font-family: sans-serif;">
                <h1 style="color:#17a2b8;">ℹ️ La base de datos ya existe</h1>
                <p>Los datos de prueba ya fueron creados anteriormente.</p>
                <a href="/" style="display:inline-block; margin-top:20px; padding:10px 20px; background:#667eea; color:white; text-decoration:none; border-radius:5px;">Ir al Inicio</a>
            </div>
            """

# ============================================
# EJECUCIÓN DE LA APLICACIÓN
# ============================================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Base de datos 'clinica.db' lista en 'instance/'")

    app.run(debug=True, host='0.0.0.0', port=5000)