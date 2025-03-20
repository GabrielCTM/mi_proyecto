from flask import Flask, render_template, request
import rule_engine

app = Flask(__name__)

# Definir reglas correctamente como lista de tuplas
rules_text = [
    ("puntuacion_crediticia > 750", -10),
    ("puntuacion_crediticia >= 600 and puntuacion_crediticia <= 750", 5),
    ("puntuacion_crediticia < 600", 15),

    ("ingresos_mensuales > 3 * cuota_prestamo", -10),
    ("ingresos_mensuales >= 1.5 * cuota_prestamo and ingresos_mensuales <= 3 * cuota_prestamo", 5),
    ("ingresos_mensuales < 1.5 * cuota_prestamo", 15),

    ("deuda_ingreso < 0.30", -5),
    ("deuda_ingreso > 0.50", 15),
    ("deuda_ingreso >= 0.30 and deuda_ingreso <= 0.50", 5),

    ("tipo_empleo == 'fijo_5_anios'", -5),
    ("tipo_empleo == 'temporal'", 10),
    ("tipo_empleo != 'fijo_5_anios' and tipo_empleo != 'temporal'", 5),

    ("garantias == 'propiedad'", -5),
    ("garantias == 'aval_bajo_valor'", 5),
    ("garantias == 'sin_garantías'", 10),

    ("historial_prestamos == 'sin_retrasos'", -5),
    ("historial_prestamos == 'impagos'", 15),
    ("historial_prestamos != 'sin_retrasos' and historial_prestamos != 'impagos'", 5)
]

# Convertimos las reglas en objetos Rule de rule-engine
rules = [(rule_engine.Rule(condition), valor) for condition, valor in rules_text]

def calcular_riesgo(datos_cliente):
    puntaje = 0
    contexto = datos_cliente.copy()

    # Aplicar cada regla sobre los datos del cliente
    for rule, valor in rules:
        if rule.matches(contexto):
            puntaje += valor

    nivel = "Bajo" if puntaje < 10 else "Moderado" if puntaje < 30 else "Alto"
    return {"puntaje": puntaje, "nivel": nivel}

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        cliente = {
            "puntuacion_crediticia": int(request.form["puntuacion_crediticia"]),
            "ingresos_mensuales": int(request.form["ingresos_mensuales"]),
            "cuota_prestamo": int(request.form["cuota_prestamo"]),
            "deuda_ingreso": float(request.form["deuda_ingreso"]),
            "tipo_empleo": request.form["tipo_empleo"],
            "garantias": request.form["garantias"],
            "historial_prestamos": request.form["historial_prestamos"],
        }

        resultado = calcular_riesgo(cliente)

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)