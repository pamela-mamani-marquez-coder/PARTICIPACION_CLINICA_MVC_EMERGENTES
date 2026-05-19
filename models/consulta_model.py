from database import db
from datetime import datetime

class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    diagnostico = db.Column(db.Text, nullable=False)
    tratamiento = db.Column(db.Text, nullable=False)
    
    # Claves foráneas (Relaciones 1-N)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    
    def __repr__(self):
        return f'<Consulta #{self.id} - {self.fecha.strftime("%d/%m/%Y")}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Consulta.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Consulta.query.get(id)
    
    @staticmethod
    def get_by_fecha(fecha_inicio, fecha_fin):
        return Consulta.query.filter(
            Consulta.fecha.between(fecha_inicio, fecha_fin)
        ).all()
    
    def update(self, diagnostico=None, tratamiento=None, fecha=None):
        if diagnostico: self.diagnostico = diagnostico
        if tratamiento: self.tratamiento = tratamiento
        if fecha: self.fecha = fecha
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()