# Im in the chapter 11 of Lambda Coding :)

from flask import request, make_response, redirect, render_template, url_for, jsonify, request, session, flash
import requests
from app import create_app
from app.forms import LoginForm


app = create_app()
ESP32_IP = '192.168.1.6'
ESP32_PORT = 80

items = ['Im Valentin', 'Im interesting in to learn', 'I would like know more', 'I like your mom']



@app.route('/')
def home():
    return render_template('esp32.html')

@app.route("/index")
def index():
    user_ip_info = request.remote_addr
    response = make_response(redirect(url_for('show_info', _external=True))) 
    # response.set_cookie('user_ip_info', user_ip_info)
    session['user_ip_info'] = user_ip_info
    return response
   
# Jugando con la page :)
@app.route('/show_info_address')
def show_info():
    username = session.get('username')
    user_ip = session.get('user_ip_info')
    context = {
        'user_ip': user_ip,
        'items': items,
        # 'login_form': login_form,
        'username': username 
    }
    
        
    return render_template('ip_info.html', **context)

# Handing mistakes:

@app.errorhandler(404)
def not_found_endpoint(error):
    return render_template('404.html', error = error)
    

# Controlando el lugar ;)
@app.route('/control', methods=['POST', 'GET'])
def control():
    data = request.get_json()
    if not data or 'accion' not in data:
        return jsonify({"error": "Acción no especificada"}), 400

    accion = data['accion']
    url_esp32 = f"http://{ESP32_IP}:{ESP32_PORT}/accion"

    try:
        r = requests.post(url_esp32, json={"accion": accion}, timeout=3)
        if r.status_code == 200:
            return jsonify({"mensaje": f"Acción '{accion}' enviada al ESP32"})
        else:
            return jsonify({"error": f"ESP32 respondió con código {r.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": f"No se pudo conectar al ESP32: {str(e)}"}), 500

# Sensando el lugar ;)
@app.route('/datos', methods=['GET'])
def recibir_datos():
    global last_temp, last_hum
    temp = request.args.get('temp')
    hum = request.args.get('hum')
    if temp and hum:
        print(f"Temperatura: {temp} °C, Humedad: {hum} %")
        last_temp = temp
        last_hum = hum
        return "Datos recibidos"
    return "Faltan parámetros", 400

@app.route('/ver_datos')
def ver_datos():
    global last_temp, last_hum
    return render_template('ver_datos.html', temp = last_temp, hum = last_hum)

# @app.route('/api/datos')
# def api_datos():
#     global last_temp, last_hum
#     return render_template("ver_datos.html", temp=last_temp, hum=last_hum)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


