from flask import Blueprint, request, redirect, url_for, flash, make_response, send_file
from datetime import datetime, date
import csv
import io
from fpdf import FPDF
from models.consulta_model import Consulta
from models.medico_model import Medico
from models.paciente_model import Paciente
from views import consulta_view

consulta_bp = Blueprint('consulta', __name__, url_prefix='/consultas')

@consulta_bp.route('/')
def index():
    consultas = Consulta.get_all()
    return consulta_view['list'](consultas)

@consulta_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        medico_id = request.form.get('medico_id')
        paciente_id = request.form.get('paciente_id')
        diagnostico = request.form.get('diagnostico', '').strip()
        tratamiento = request.form.get('tratamiento', '').strip()
        fecha_str = request.form.get('fecha')
        
        if not medico_id or not paciente_id or not diagnostico or not tratamiento:
            flash('⚠️ Todos los campos son obligatorios', 'warning')
            return consulta_view['create']()
        
        try:
            
            if fecha_str:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            else:
                fecha = date.today()
            
            consulta = Consulta(
                medico_id=medico_id, 
                paciente_id=paciente_id, 
                diagnostico=diagnostico, 
                tratamiento=tratamiento, 
                fecha=fecha
            )
            consulta.save()
            flash('✅ Consulta registrada exitosamente', 'success')
            return redirect(url_for('consulta.index'))
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'danger')
            return consulta_view['create']()
    
    return consulta_view['create']()

@consulta_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    consulta = Consulta.get_by_id(id)
    if not consulta:
        flash('❌ Consulta no encontrada', 'danger')
        return redirect(url_for('consulta.index'))
    
    if request.method == 'POST':
        diagnostico = request.form.get('diagnostico', '').strip()
        tratamiento = request.form.get('tratamiento', '').strip()
        fecha_str = request.form.get('fecha')
        
        try:
            fecha = None
            if fecha_str:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            consulta.update(diagnostico=diagnostico, tratamiento=tratamiento, fecha=fecha)
            flash('✅ Consulta actualizada', 'success')
            return redirect(url_for('consulta.index'))
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'danger')
    
    return consulta_view['edit'](consulta)

@consulta_bp.route('/delete/<int:id>')
def delete(id):
    consulta = Consulta.get_by_id(id)
    if not consulta:
        flash('❌ Consulta no encontrada', 'danger')
        return redirect(url_for('consulta.index'))
    
    try:
        consulta.delete()
        flash('✅ Consulta eliminada', 'success')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'danger')
    
    return redirect(url_for('consulta.index'))

# 🎁 EXTRA: Filtro de consultas por fecha
@consulta_bp.route('/filtrar', methods=['GET', 'POST'])
def filtrar():
    if request.method == 'POST':
        fecha_inicio_str = request.form.get('fecha_inicio')
        fecha_fin_str = request.form.get('fecha_fin')
        
        if fecha_inicio_str and fecha_fin_str:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                consultas = Consulta.get_by_fecha(fecha_inicio, fecha_fin)
                flash(f'🔍 Mostrando consultas del {fecha_inicio_str} al {fecha_fin_str}', 'info')
                return consulta_view['list'](consultas, filtro=True)
            except Exception as e:
                flash(f'❌ Error: {str(e)}', 'danger')
    
    return consulta_view['filtrar']()

#  CLASE PDF PERSONALIZADA
class ClinicaPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'CLINICA MEDICA - REPORTE', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

# 📄 EXTRA 2: Exportar consultas a PDF
@consulta_bp.route('/exportar/consultas/pdf')
def exportar_consultas_pdf():
    try:
        consultas = Consulta.get_all()
        
        pdf = ClinicaPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Título
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f'Reporte de Consultas - {date.today().strftime("%d/%m/%Y")}', 0, 1, 'C')
        pdf.ln(3)
        
        # Encabezados de tabla
        pdf.set_fill_color(220, 220, 220)
        pdf.set_font('Arial', 'B', 9)
        headers = ['ID', 'Fecha', 'Médico', 'Paciente', 'Diagnóstico']
        col_widths = [10, 20, 40, 40, 80]
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 7, header, 1, 0, 'C', True)
        pdf.ln()
        
        # Datos
        pdf.set_font('Arial', '', 8)
        for c in consultas:
            # Manejo de texto largo en diagnóstico
            diagnostico = c.diagnostico[:40] + "..." if len(c.diagnostico) > 40 else c.diagnostico
            
            pdf.cell(col_widths[0], 6, str(c.id), 1, 0, 'C')
            pdf.cell(col_widths[1], 6, c.fecha.strftime('%d/%m/%Y'), 1, 0, 'C')
            pdf.cell(col_widths[2], 6, c.medico.nombre[:25], 1, 0, 'L')
            pdf.cell(col_widths[3], 6, c.paciente.nombre[:25], 1, 0, 'L')
            pdf.cell(col_widths[4], 6, diagnostico, 1, 0, 'L')
            pdf.ln()
        
        # Guardar y enviar
        filename = f'consultas_{date.today().strftime("%Y%m%d")}.pdf'
        pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
        
        response = make_response(pdf_output)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        flash('✅ Reporte de consultas exportado a PDF', 'success')
        return response
        
    except Exception as e:
        flash(f'❌ Error al exportar PDF: {str(e)}', 'danger')
        return redirect(url_for('consulta.index'))

# 📄 Exportar médicos a PDF
@consulta_bp.route('/exportar/medicos/pdf')
def exportar_medicos_pdf():
    try:
        medicos = Medico.get_all()
        
        pdf = ClinicaPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f'Reporte de Médicos - {date.today().strftime("%d/%m/%Y")}', 0, 1, 'C')
        pdf.ln(3)
        
        pdf.set_fill_color(220, 220, 220)
        pdf.set_font('Arial', 'B', 9)
        headers = ['ID', 'Nombre', 'Especialidad', 'Teléfono', 'Correo']
        col_widths = [10, 45, 40, 30, 65]
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 7, header, 1, 0, 'C', True)
        pdf.ln()
        
        pdf.set_font('Arial', '', 8)
        for m in medicos:
            pdf.cell(col_widths[0], 6, str(m.id), 1, 0, 'C')
            pdf.cell(col_widths[1], 6, m.nombre[:28], 1, 0, 'L')
            pdf.cell(col_widths[2], 6, m.especialidad[:25], 1, 0, 'L')
            pdf.cell(col_widths[3], 6, m.telefono or '-', 1, 0, 'C')
            pdf.cell(col_widths[4], 6, m.correo[:35], 1, 0, 'L')
            pdf.ln()
        
        filename = f'medicos_{date.today().strftime("%Y%m%d")}.pdf'
        pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
        
        response = make_response(pdf_output)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        flash('✅ Reporte de médicos exportado', 'success')
        return response
        
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'danger')
        return redirect(url_for('medico.index'))

# 📄 Exportar pacientes a PDF
@consulta_bp.route('/exportar/pacientes/pdf')
def exportar_pacientes_pdf():
    try:
        pacientes = Paciente.get_all()
        
        pdf = ClinicaPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f'Reporte de Pacientes - {date.today().strftime("%d/%m/%Y")}', 0, 1, 'C')
        pdf.ln(3)
        
        pdf.set_fill_color(220, 220, 220)
        pdf.set_font('Arial', 'B', 9)
        headers = ['ID', 'Nombre', 'Edad', 'Teléfono', 'Dirección']
        col_widths = [10, 50, 15, 30, 85]
        
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 7, header, 1, 0, 'C', True)
        pdf.ln()
        
        pdf.set_font('Arial', '', 8)
        for p in pacientes:
            pdf.cell(col_widths[0], 6, str(p.id), 1, 0, 'C')
            pdf.cell(col_widths[1], 6, p.nombre[:30], 1, 0, 'L')
            pdf.cell(col_widths[2], 6, str(p.edad), 1, 0, 'C')
            pdf.cell(col_widths[3], 6, p.telefono or '-', 1, 0, 'C')
            pdf.cell(col_widths[4], 6, p.direccion[:45] or '-', 1, 0, 'L')
            pdf.ln()
        
        filename = f'pacientes_{date.today().strftime("%Y%m%d")}.pdf'
        pdf_output = pdf.output(dest='S').encode('latin-1', 'ignore')
        
        response = make_response(pdf_output)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        flash('✅ Reporte de pacientes exportado', 'success')
        return response
        
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'danger')
        return redirect(url_for('paciente.index'))