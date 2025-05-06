#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import math
import operator
import sys


# Avaluador segur d’expressions
_OPERADORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_FUNCIONS = {
    # trigonometria (radiants)
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    # logaritmes
    "log": math.log10,
    "ln": math.log,
    # arrels, potències i constants
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "pi": math.pi,
    "e": math.e,
}

class SafeEval(ast.NodeVisitor):
    """Avaluador molt restringit, sense `eval` ni riscos d’injecció."""
    def __init__(self, mem_value: float):
        super().__init__()
        self.names = {"mem": mem_value, **_FUNCIONS}

    # Números sencers o flotants
    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Constant no permesa")

    # Nom (variable o funció)
    def visit_Name(self, node):
        if node.id in self.names:
            return self.names[node.id]
        raise NameError(f"Nom no permès: {node.id}")

    # Operadors binaris
    def visit_BinOp(self, node):
        op_type = type(node.op)
        if op_type in _OPERADORS:
            return _OPERADORS[op_type](self.visit(node.left), self.visit(node.right))
        raise TypeError(f"Operador no permès: {op_type}")

    # Operadors unaris (+x, -x)
    def visit_UnaryOp(self, node):
        op_type = type(node.op)
        if op_type in _OPERADORS:
            return _OPERADORS[op_type](self.visit(node.operand))
        raise TypeError(f"Operador unari no permès: {op_type}")

    # Crida de funció
    def visit_Call(self, node):
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return func(*args)

    # Puntuació de l’arbre: Expression → body
    def visit_Expression(self, node):
        return self.visit(node.body)

def safe_eval(expr: str, mem_value: float = 0.0) -> float:
    """Avalua `expr` amb els operadors i funcions permeses."""
    expr = expr.replace("^", "**")
    arbre = ast.parse(expr, mode="eval")
    return SafeEval(mem_value).visit(arbre.body)

def demana_numero(prompt: str) -> float:
    """
    Demana un nombre fins que l’usuari escriu una entrada vàlida.
    Retorna float perquè la divisió i els decimals funcionin de manera natural.
    """
    while True:
        entrada = input(prompt)
        try:
            return float(entrada.replace(",", "."))
        except ValueError:
            print("➜ Entrada invàlida: has d’escriure un número.")


def demana_opcio(prompt: str, min_opcio: int, max_opcio: int) -> int:
    """
    Demana una opció dins d’un rang; torna-la a demanar mentre sigui incorrecta.
    """
    while True:
        entrada = input(prompt)
        if entrada.isdigit():
            opcio = int(entrada)
            if min_opcio <= opcio <= max_opcio:
                return opcio
        print(f"➜ Opció no vàlida. Introdueix un número entre {min_opcio} i {max_opcio}.")

def comprova_operacio(prompt: str) -> bool:
    """
    Comprova si la operació és vàlida
    """



def calculadora_basica() -> None:
    """
    Bucle principal de la calculadora bàsica.
    """
    while True:
        print("\nQuina operació vols realitzar?")
        print("1. Sumar")
        print("2. Restar")
        print("3. Multiplicar")
        print("4. Dividir")
        print("5. Sortir")

        opcio = demana_opcio("Opció ➜ ", 1, 5)

        if opcio == 5:
            print("Fins aviat!")
            break

        num1 = demana_numero("\nEscriu el primer número: ")
        num2 = demana_numero("Escriu el segon número: ")

        if opcio == 1:
            resultat = num1 + num2
            signe = "+"
        elif opcio == 2:
            resultat = num1 - num2
            signe = "-"
        elif opcio == 3:
            resultat = num1 * num2
            signe = "x"
        elif opcio == 4:
            if num2 == 0:
                print("Error: no es pot dividir entre 0.")
                continue
            resultat = num1 / num2
            signe = "÷"

        # Mostra resultat sense zeros finals innecessaris
        if num1.is_integer():
            num1 = int(num1)

        if num2.is_integer():
            num2 = int(num2)

        if resultat.is_integer():
            resultat = int(resultat)

        print(f"{num1} {signe} {num2} = {resultat}")

def calculadora_intermitja() -> None:
    print("\n--- Mode INTERMIG ---")
    print("Escriu expressions amb + - * / ^ (potència), parèntesis i funcions:")
    print("   sin(), cos(), tan(), sqrt(), log() [base 10], ln() [naturals]")
    print("· Ordres de memòria: M+, M-, MR, MC")
    print("· Escriu 'sortir' per acabar.\n")

    memoria = 0.0
    ultim_resultat = 0.0

    while True:
        entrada = input(">>> ").strip()

        # Comandes especials (case-insensitive)
        ent_upper = entrada.upper()

        if ent_upper in ("SORTIR", "EXIT", "QUIT"):
            print("Tancant calculadora intermèdia…")
            break
        elif ent_upper == "MR":
            print(f"Memòria = {memoria}")
            ultim_resultat = memoria
            continue
        elif ent_upper == "MC":
            memoria = 0.0
            print("Memòria esborrada.")
            continue
        elif ent_upper == "M+":
            memoria += ultim_resultat
            print(f"Memòria = {memoria}")
            continue
        elif ent_upper == "M-":
            memoria -= ultim_resultat
            print(f"Memòria = {memoria}")
            continue

        # Avaluar expressió
        try:
            resultat = safe_eval(entrada, memoria)
            ultim_resultat = resultat
            resultat = int(resultat) if resultat.is_integer() else resultat
            print(f"= {resultat}")
        except Exception as e:
            print(f"⚠️  Error de sintaxi o funció desconeguda: {e}")


def main() -> None:
    print("------------------------------------")
    print(" Benvingut/da a la teva Calculadora ")
    print("------------------------------------")

    print("\nQuina calculadora vols utilitzar?")
    print("1. Bàsica")
    print("2. Millorada")
    tipus = demana_opcio("Opció ➜ ", 1, 2)

    if tipus == 1:
        calculadora_basica()
    elif tipus == 2:
        calculadora_intermitja()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterromput per l’usuari. Fins aviat!")
        sys.exit(0)
