from database import db

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(150))
    telefono = db.Column(db.String(20))
    
    # Relación 1-N: Un paciente tiene muchas consultas
    consultas = db.relationship('Consulta', backref='paciente', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Paciente {self.nombre} ({self.edad} años)>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Paciente.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Paciente.query.get(id)
    
    def update(self, nombre=None, edad=None, direccion=None, telefono=None):
        if nombre: self.nombre = nombre
        if edad: self.edad = edad
        if direccion: self.direccion = direccion
        if telefono: self.telefono = telefono
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()