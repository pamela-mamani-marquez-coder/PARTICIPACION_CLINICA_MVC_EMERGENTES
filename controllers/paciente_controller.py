from flask import Blueprint, request, redirect, url_for, flash
from models.paciente_model import Paciente
from views import paciente_view

paciente_bp = Blueprint('paciente', __name__, url_prefix='/pacientes')

@paciente_bp.route('/')
def index():
    pacientes = Paciente.get_all()
    return paciente_view['list'](pacientes)

@paciente_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        edad = request.form.get('edad', '').strip()
        direccion = request.form.get('direccion', '').strip()
        telefono = request.form.get('telefono', '').strip()
        
        if not nombre or not edad:
            flash('⚠️ Nombre y edad son obligatorios', 'warning')
            return paciente_view['create']()
        
        try:
            paciente = Paciente(nombre=nombre, edad=int(edad), direccion=direccion, telefono=telefono)
            paciente.save()
            flash('✅ Paciente registrado exitosamente', 'success')
            return redirect(url_for('paciente.index'))
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'danger')
            return paciente_view['create']()
    
    return paciente_view['create']()

@paciente_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    paciente = Paciente.get_by_id(id)
    if not paciente:
        flash('❌ Paciente no encontrado', 'danger')
        return redirect(url_for('paciente.index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        edad = request.form.get('edad', '').strip()
        direccion = request.form.get('direccion', '').strip()
        telefono = request.form.get('telefono', '').strip()
        
        try:
            paciente.update(nombre=nombre, edad=int(edad) if edad else None, direccion=direccion, telefono=telefono)
            flash('✅ Paciente actualizado', 'success')
            return redirect(url_for('paciente.index'))
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'danger')
    
    return paciente_view['edit'](paciente)

@paciente_bp.route('/delete/<int:id>')
def delete(id):
    paciente = Paciente.get_by_id(id)
    if not paciente:
        flash('❌ Paciente no encontrado', 'danger')
        return redirect(url_for('paciente.index'))
    
    try:
        paciente.delete()
        flash('✅ Paciente eliminado', 'success')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'danger')
    
    return redirect(url_for('paciente.index'))