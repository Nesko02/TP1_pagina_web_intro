from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/productos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Auto(db.Model):
    __tablename__ = 'autos'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    kilometros = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    foto_url = db.Column(db.String(255))

class Opinion(db.Model):
    __tablename__ = 'opiniones'
    id = db.Column(db.Integer, primary_key=True)
    auto_id = db.Column(db.Integer, db.ForeignKey('autos.id'), nullable=False)
    opinion = db.Column(db.Text, nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    estrellas = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['GET'])
def get_autos():
    autos = Auto.query.all()
    return jsonify([{
        'id': auto.id,
        'marca': auto.marca,
        'modelo': auto.modelo,
        'kilometros': auto.kilometros,
        'precio': str(auto.precio),
        'foto_url': auto.foto_url
    } for auto in autos])

@app.route('/info_autos/<id>', methods=['GET'])
def get_auto_detalle(id):
    auto = Auto.query.get(id)
    if auto is None:
        return None
    return jsonify({
        'id': auto.id,
        'marca': auto.marca,
        'modelo': auto.modelo,
        'kilometros': auto.kilometros,
        'precio': str(auto.precio),
        'foto_url': auto.foto_url
    })

@app.route('/actualizar_auto/<id>', methods=['PUT'])
def actualizar_auto(id):
    data = request.json
    auto = Auto.query.get(id)
    if not auto:
        return jsonify({'error': 'Auto no encontrado'}), 404

    auto.marca = data.get('marca', auto.marca)
    auto.modelo = data.get('modelo', auto.modelo)
    auto.kilometros = data.get('kilometros', auto.kilometros)
    auto.precio = data.get('precio', auto.precio)

    db.session.commit()

    return jsonify({'mensaje': 'Auto actualizado correctamente'})

@app.route('/agregar_auto', methods=['POST'])
def agregar_auto():
    data = request.json
    nuevo_auto = Auto(
        marca=data['marca'],
        modelo=data['modelo'],
        kilometros=data['kilometros'],
        precio=data['precio'],
        foto_url=data['foto_url']
    )
    db.session.add(nuevo_auto)
    db.session.commit()

    return jsonify({'mensaje': 'Auto agregado correctamente', 'id': nuevo_auto.id})

@app.route('/eliminar_auto/<id>', methods=['DELETE'])
def eliminar_auto(id):
    auto = Auto.query.get(id)
    if not auto:
        return jsonify({'error': 'Auto no encontrado'}), 404

    db.session.delete(auto)
    db.session.commit()

    return jsonify({'mensaje': 'Auto eliminado correctamente'})


@app.route('/opiniones/<auto_id>', methods=['GET'])
def get_opiniones(auto_id):
    opiniones = Opinion.query.filter_by(auto_id=auto_id).all()
    return jsonify([{
        'id': opinion.id,
        'auto_id': opinion.auto_id,
        'opinion': opinion.opinion,
        'autor': opinion.autor,
        'estrellas': opinion.estrellas
    } for opinion in opiniones])

@app.route('/opiniones_generales', methods=['GET'])
def get_todas_opiniones():
    autos = Auto.query.all()
    data = []
    for auto in autos:
        opiniones = Opinion.query.filter_by(auto_id=auto.id).all()
        opiniones_data = [{
            'id': opinion.id,
            'opinion': opinion.opinion,
            'autor': opinion.autor,
            'estrellas': opinion.estrellas
        } for opinion in opiniones]
        data.append({
            'auto_id': auto.id,
            'marca': auto.marca,
            'modelo': auto.modelo,
            'opiniones': opiniones_data
        })
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True, port=5000)

