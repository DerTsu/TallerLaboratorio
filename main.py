from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:sBzi1zx8vzHzLWBghY1OTT2MQo0bb10d@dpg-cvffcdnnoe9s73bgstrg-a.oregon-postgres.render.com/db_g0q6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Receta
class Receta(db.Model):
    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    tiempo_preparacion = db.Column(db.Integer, nullable=True)  # en minutos
    dificultad = db.Column(db.String(20), nullable=True)  # fácil, media, difícil
    ingredientes = db.Column(db.Text, nullable=True)
    instrucciones = db.Column(db.Text, nullable=True)
    imagen_url = db.Column(db.String(200), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Receta {self.nombre}>'

# Crear todas las tablas
with app.app_context():
    db.create_all()

# Rutas de la aplicación
@app.route('/')
def index():
    recetas = Receta.query.all()
    return render_template('index.html', recetas=recetas)

@app.route('/receta/<int:id>')
def ver_receta(id):
    receta = Receta.query.get_or_404(id)
    return render_template('ver_receta.html', receta=receta)

@app.route('/receta/nueva', methods=['GET', 'POST'])
def nueva_receta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        tiempo_preparacion = request.form['tiempo_preparacion']
        dificultad = request.form['dificultad']
        ingredientes = request.form['ingredientes']
        instrucciones = request.form['instrucciones']
        imagen_url = request.form['imagen_url']
        
        nueva_receta = Receta(
            nombre=nombre,
            descripcion=descripcion,
            tiempo_preparacion=tiempo_preparacion,
            dificultad=dificultad,
            ingredientes=ingredientes,
            instrucciones=instrucciones,
            imagen_url=imagen_url
        )
        
        db.session.add(nueva_receta)
        db.session.commit()
        
        flash('Receta agregada exitosamente', 'success')
        return redirect(url_for('index'))
    
    return render_template('form_receta.html')

@app.route('/receta/editar/<int:id>', methods=['GET', 'POST'])
def editar_receta(id):
    receta = Receta.query.get_or_404(id)
    
    if request.method == 'POST':
        receta.nombre = request.form['nombre']
        receta.descripcion = request.form['descripcion']
        receta.tiempo_preparacion = request.form['tiempo_preparacion']
        receta.dificultad = request.form['dificultad']
        receta.ingredientes = request.form['ingredientes']
        receta.instrucciones = request.form['instrucciones']
        receta.imagen_url = request.form['imagen_url']
        
        db.session.commit()
        
        flash('Receta actualizada exitosamente', 'success')
        return redirect(url_for('ver_receta', id=receta.id))
    
    return render_template('form_receta.html', receta=receta)

@app.route('/receta/eliminar/<int:id>', methods=['POST'])
def eliminar_receta(id):
    receta = Receta.query.get_or_404(id)
    db.session.delete(receta)
    db.session.commit()
    
    flash('Receta eliminada exitosamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)