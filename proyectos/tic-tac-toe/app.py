# main.py
from flask import Flask, render_template, request, session, jsonify
from controllers.game_controller import ControladorJuego

app = Flask(__name__)
app.secret_key = 'clave-de-desarrollo-cambiar-en-produccion'

controlador = ControladorJuego()


@app.route('/')
def inicio():
    return render_template('tablero.html')


@app.route('/api/nueva', methods=['POST'])
def nueva_partida():
    datos = request.get_json(silent=True) or {}
    modo = datos.get('modo', ControladorJuego.MODO_HUMANO)
    dificultad = datos.get('dificultad', 'dificil')

    try:
        estado = controlador.nueva_partida(modo, dificultad)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400

    session['estado'] = estado
    return jsonify(estado)


@app.route('/api/jugar', methods=['POST'])
def jugar():
    estado = session.get('estado')
    if estado is None:
        return jsonify({'error': 'No hay una partida en curso'}), 400

    datos = request.get_json(silent=True) or {}
    estado = controlador.jugar(estado, datos.get('fila'), datos.get('columna'))

    session['estado'] = estado
    return jsonify(estado)


@app.route('/api/estado')
def estado_actual():
    return jsonify(session.get('estado'))


if __name__ == '__main__':
    app.run(debug=True)