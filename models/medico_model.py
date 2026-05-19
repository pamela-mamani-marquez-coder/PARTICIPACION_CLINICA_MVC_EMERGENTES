from database import db

class Medico(db.Model):
    __tablename__ = 'medicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relación 1-N: Un médico tiene muchas consultas
    consultas = db.relationship('Consulta', backref='medico', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Medico {self.nombre} - {self.especialidad}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Medico.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Medico.query.get(id)
    
    def update(self, nombre=None, especialidad=None, telefono=None, correo=None):
        if nombre: self.nombre = nombre
        if especialidad: self.especialidad = especialidad
        if telefono: self.telefono = telefono
        if correo: self.correo = correo
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()