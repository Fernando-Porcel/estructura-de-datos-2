from models.nodo_expresion import Nodo

class ArbolExpresion:
    def __init__(self):
        self.__raiz = None

    def construir(self, expresion):
        tokens = self._tokenizar(expresion)
        postfija = self._infija_posfija(tokens)
        self._construir_arbol(postfija)

    def _tokenizar(self, expresion):
        tokens = []
        numero = ''
        operadores = {'+', '-', '*', '/', '^'}
        parentesis = {'(', ')'}

        for i, letra in enumerate(expresion):

            if letra.isdigit() or letra == '.':
                 numero += letra

            elif letra in operadores or letra in parentesis:
                if numero:
                    tokens.append(float(numero) if '.' in numero else int(numero))
                    numero = ''

                if letra == '-':
                    es_unario = (
                        len(tokens) == 0 or
                        tokens[-1] == '('
                    )

                    if es_unario:
                        if i + 1 < len(expresion) and (expresion[i+1].isdigit() or expresion[i+1] == '.'):
                            numero = '-'
                        else:
                            tokens.append(-1)
                            tokens.append('*')
                    else:
                         tokens.append('-')
                         
                elif letra == '(' and len(tokens) != 0 and (tokens[-1] not in operadores and tokens[-1] != '('):
                    tokens.append('*')
                    tokens.append(letra)
                else:
                     tokens.append(letra)
            else:
                 raise ValueError(f"Sintaxis error")

        if numero:
            tokens.append(float(numero) if '.' in numero else int(numero))

        return tokens

    def _infija_posfija(self, tokens):
        salida = []
        pila = []
        
        for token in tokens:
            if isinstance(token, (int, float)):
                salida.append(token)

            elif token == '(':
                pila.append('(')

            elif token == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())

                if not pila:
                    raise ValueError("Cierre descolgado")
                pila.pop()
            
            else:
                while pila and self._prioridad(pila[-1]) >= self._prioridad(token):
                    salida.append(pila.pop())
                pila.append(token)

        while pila:
            op = pila.pop()
            if op == '(':
                raise ValueError("Cierre descolgado")
            salida.append(op)

        return salida

    def _prioridad(self, operador):
        if operador == '^': return 4
        if operador in "*/": return 3
        if operador in "+-": return 2
        if operador == '(': return 1

    def _construir_arbol(self, lista_postfija):
        pila_nodos  = []

        for token in lista_postfija:
            if isinstance(token, (int, float)):
                pila_nodos.append(Nodo(token))

            else:
                if len(pila_nodos) < 2:
                    raise ValueError(f"Sintaxis error")

                nodo_operador = Nodo(token)

                nodo_operador.derecho = pila_nodos.pop()
                nodo_operador.izquierdo = pila_nodos.pop()

                pila_nodos.append(nodo_operador)

        if len(pila_nodos) != 1:
            raise ValueError("Sintaxis error")
        
        self.__raiz = pila_nodos.pop()

    def evaluar(self):
        if self.__raiz is None:
            return '0'

        return self._evaluar_recursivo(self.__raiz)
    
    def _evaluar_recursivo(self, nodo):
        if nodo.es_hoja():
            return nodo.valor
        
        numero_izq = self._evaluar_recursivo(nodo.izquierdo)
        numero_der = self._evaluar_recursivo(nodo.derecho)

        return self._calcular(numero_izq, numero_der, nodo.valor)
    
    def _calcular(self, numero_izq, numero_der, operador):
        if operador == '+':
            return numero_izq + numero_der
        elif operador == '-':
            return numero_izq - numero_der
        elif operador == '*':
            return numero_izq * numero_der
        elif operador == '/':
            if numero_der != 0: 
                return numero_izq / numero_der
            else:
                raise ValueError("No se puede dividir por 0")
        elif operador == '^':
            return numero_izq ** numero_der

    def vaciar(self):
        self.__raiz = None

    def arbol_diccionario(self):
        return self._arbol_diccionario_recursivo(self.__raiz)

    def _arbol_diccionario_recursivo(self, nodo):
        if nodo is None:
            return None

        return {
            'valor': nodo.valor,
            'izquierdo': self._arbol_diccionario_recursivo(nodo.izquierdo),
            'derecho': self._arbol_diccionario_recursivo(nodo.derecho)
        }