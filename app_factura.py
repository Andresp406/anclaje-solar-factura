#!/usr/bin/env python3
"""
Aplicación web para generar facturas de ANCLAJE SOLAR ENERGY
"""

from flask import Flask, render_template, request, send_file, jsonify
from datetime import datetime
import os
import sys

# Importar la función de generación de facturas
from generar_factura import generar_factura

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anclaje-solar-energy-2025'

@app.route('/')
def index():
    """Página principal con el formulario"""
    return render_template('formulario_factura.html')

@app.route('/generar', methods=['POST'])
def generar():
    """Procesar el formulario y generar la factura"""
    try:
        # Obtener datos del formulario
        nit = request.form.get('nit', '')
        telefono = request.form.get('telefono', '')
        correo = request.form.get('correo', '')
        cliente = request.form.get('cliente', '')
        documento = request.form.get('documento', '')
        direccion = request.form.get('direccion', '')
        fecha_input = request.form.get('fecha', '')
        
        # Convertir fecha de YYYY-MM-DD a DD/MM/YYYY
        if fecha_input:
            try:
                fecha_obj = datetime.strptime(fecha_input, '%Y-%m-%d')
                fecha = fecha_obj.strftime('%d/%m/%Y')
            except:
                fecha = fecha_input
        else:
            fecha = datetime.now().strftime("%d/%m/%Y")
        
        factura_no = request.form.get('factura_no', '')
        
        # Obtener items de la factura
        items = []
        descripcion_items = request.form.getlist('descripcion[]')
        cantidad_items = request.form.getlist('cantidad[]')
        valor_items = request.form.getlist('valor_unitario[]')
        tiene_iva_items = request.form.getlist('tiene_iva[]')
        
        for i, (desc, cant, valor) in enumerate(zip(descripcion_items, cantidad_items, valor_items)):
            if desc and cant and valor:
                # Verificar si este item tiene IVA (el checkbox envía "1" si está marcado)
                tiene_iva = str(i) in tiene_iva_items or (i < len(tiene_iva_items) and tiene_iva_items[i] == '1')
                items.append({
                    'descripcion': desc,
                    'cantidad': int(cant),
                    'valor_unitario': float(valor),
                    'tiene_iva': tiene_iva
                })
        
        # Calcular totales considerando IVA por item
        subtotal = sum(item['cantidad'] * item['valor_unitario'] for item in items)
        iva = sum(item['cantidad'] * item['valor_unitario'] * 0.19 for item in items if item.get('tiene_iva', False))
        total = subtotal + iva
        
        # Ruta del logo - usar ruta relativa para Deta
        posibles_logos = [
            'logo_anclaje.jpeg',
            'logo.png', 
            'logo_anclaje.png', 
            'anclaje_logo.png',
            '/home/apenagos/Escritorio/papa/logo_anclaje.jpeg'  # Fallback local
        ]
        logo_path = None
        for logo in posibles_logos:
            if os.path.exists(logo):
                logo_path = logo
                break
        
        # Generar factura
        archivo_pdf = generar_factura(
            logo_path=logo_path,
            nit=nit,
            telefono=telefono,
            correo=correo,
            cliente=cliente,
            documento=documento,
            direccion=direccion,
            fecha=fecha,
            factura_no=factura_no,
            items=items,
            subtotal=subtotal,
            iva=iva,
            total=total
        )
        
        # Enviar el archivo PDF
        return send_file(
            archivo_pdf,
            as_attachment=True,
            download_name=f'factura_{factura_no}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calcular_total', methods=['POST'])
def calcular_total():
    """Endpoint para calcular totales en tiempo real"""
    try:
        data = request.json
        items = data.get('items', [])
        
        subtotal = sum(item['cantidad'] * item['valor_unitario'] for item in items)
        iva = subtotal * 0.19
        total = subtotal + iva
        
        return jsonify({
            'subtotal': subtotal,
            'iva': iva,
            'total': total
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("=" * 60)
    print("Generador de Facturas - ANCLAJE SOLAR ENERGY")
    print("=" * 60)
    print("\nServidor iniciado en: http://localhost:5000")
    print("Presiona Ctrl+C para detener el servidor\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
