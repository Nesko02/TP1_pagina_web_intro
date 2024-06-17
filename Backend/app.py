from flask import Flask, jsonify
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



if __name__ == '__main__':
    app.run(debug=True, port=5000)

