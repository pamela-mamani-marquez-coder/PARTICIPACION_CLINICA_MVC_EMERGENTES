from flask import render_template

def list(pacientes):
    return render_template('pacientes/index.html', pacientes=pacientes)

def create():
    return render_template('pacientes/create.html')

def edit(paciente):
    return render_template('pacientes/edit.html', paciente=paciente)

paciente = {
    'list': list,
    'create': create,
    'edit': edit
}