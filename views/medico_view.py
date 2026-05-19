from flask import render_template

def list(medicos):
    return render_template('medicos/index.html', medicos=medicos)

def create():
    return render_template('medicos/create.html')

def edit(medico):
    return render_template('medicos/edit.html', medico=medico)

medico = {
    'list': list,
    'create': create,
    'edit': edit
}