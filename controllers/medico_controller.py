from flask import Blueprint, request, redirect, url_for, flash
from models.medico_model import Medico
from views import medico_view

medico_bp = Blueprint('medico', __name__, url_prefix='/medicos')

@medico_bp.route('/')
def index():
    medicos = Medico.get_all()
    return medico_view['list'](medicos)

@medico_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        especialidad = request.form.get('especialidad', '').strip()
        telefono = request.form.get('telefono', '').strip()
        correo = request.form.get('correo', '').strip()
        
        if not nombre or not especialidad or not correo:
            flash('⚠️ Nombre, especialidad y correo son obligatorios', 'warning')
            return medico_view['create']()
        
        try:
            medico = Medico(nombre=nombre, especialidad=especialidad, telefono=telefono, correo=correo)
            medico.save()
            flash('✅ Médico registrado exitosamente', 'success')
            return redirect(url_for('medico.index'))
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'danger')
            return medico_view['create']()
    
    return medico_view['create']()

@medico_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    medico = Medico.get_by_id(id)
    if not medico:
        flash('❌ Médico no encontrado', 'danger')
        return redirect(url_for('medico.index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        especialidad = request.form.get('especialidad', '').strip()
        telefono = request.form.get('telefono', '').strip()
        correo = request.form.get('correo', '').strip()
        
        try:
            medico.update(nombre=nombre, especialidad=especialidad, telefono=telefono, correo=correo)
            flash('✅ Médico actualizado', 'success')
            return redirect(url_for('medico.index'))
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'danger')
    
    return medico_view['edit'](medico)

@medico_bp.route('/delete/<int:id>')
def delete(id):
    medico = Medico.get_by_id(id)
    if not medico:
        flash('❌ Médico no encontrado', 'danger')
        return redirect(url_for('medico.index'))
    
    try:
        medico.delete()
        flash('✅ Médico eliminado', 'success')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'danger')
    
    return redirect(url_for('medico.index'))