from flask import render_template
from datetime import date
from models.medico_model import Medico
from models.paciente_model import Paciente

def list(consultas, filtro=False):
    return render_template('consultas/index.html', consultas=consultas, filtro=filtro)

def create():
    medicos = Medico.get_all()
    pacientes = Paciente.get_all()
    today = date.today().strftime('%Y-%m-%d')  
    return render_template('consultas/create.html', medicos=medicos, pacientes=pacientes, today=today)

def edit(consulta):
    medicos = Medico.get_all()
    pacientes = Paciente.get_all()
    return render_template('consultas/edit.html', consulta=consulta, medicos=medicos, pacientes=pacientes)

def filtrar():
    return render_template('consultas/filtrar.html')

consulta = {
    'list': list,
    'create': create,
    'edit': edit,
    'filtrar': filtrar
}