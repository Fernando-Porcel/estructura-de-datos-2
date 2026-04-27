from flask import Blueprint, render_template, request, jsonify
from models.arbol_expresion import ArbolExpresion

arbol_bp = Blueprint('arbol', __name__)

@arbol_bp.route('/')
def index():
    return render_template('index.html')

@arbol_bp.route('/evaluar', methods=['POST'])
def evaluar():
    arbol = ArbolExpresion()
    data = request.get_json()
    expresion = data.get('expresion', '')

    try:
        arbol.construir(expresion)
        resultado = arbol.evaluar()
        return jsonify({
            'resultado': resultado,
            'arbol': arbol.arbol_diccionario()
        })
    except ValueError as e:
        return jsonify({'error': str(e)}) , 400
