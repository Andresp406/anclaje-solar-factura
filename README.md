# 🌞 ANCLAJE SOLAR ENERGY - Generador de Facturas

Aplicación web para generar facturas profesionales en PDF.

## 🚀 Despliegue en Railway

### Opción 1: Desde GitHub (Recomendado)

1. Sube este proyecto a un repositorio GitHub
2. Ve a [Railway.app](https://railway.app/)
3. Click en "Start a New Project"
4. Click en "Deploy from GitHub repo"
5. Selecciona tu repositorio
6. ¡Railway desplegará automáticamente!

### Opción 2: Desde Railway CLI

```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# O con curl
bash <(curl -fsSL cli.new)

# 2. Login
railway login

# 3. Inicializar proyecto
cd /home/apenagos/deta-app
railway init

# 4. Desplegar
railway up
```

## ✨ Características

- ✅ Generación de facturas en PDF con diseño profesional
- ✅ Formulario web interactivo
- ✅ IVA opcional por item (toggle)
- ✅ Cálculo automático de totales
- ✅ Logo corporativo incluido
- ✅ Pie de página automático en PDFs
- ✅ Diseño responsive

## 🛠️ Tecnologías

- **Backend**: Flask
- **PDF**: ReportLab
- **Hosting**: Railway (plan gratuito)
- **Frontend**: HTML/CSS/JavaScript vanilla

## 📝 Uso Local

```bash
pip install -r requirements.txt
python main.py
```

Abre http://localhost:5000

## 📦 Estructura del Proyecto

```
deta-app/
├── main.py                      # Entry point
├── app_factura.py              # App Flask principal
├── generar_factura.py          # Generador de PDFs
├── logo_anclaje.jpeg           # Logo corporativo
├── templates/                  # Templates HTML
│   └── formulario_factura.html
├── requirements.txt            # Dependencias Python
├── Procfile                    # Config para Railway
├── runtime.txt                 # Versión de Python
└── README.md                   # Esta documentación
```

## 🎯 Plan Gratuito de Railway

- ✅ 500 horas/mes de ejecución
- ✅ $5 USD de crédito mensual
- ✅ HTTPS automático
- ✅ Deploy desde GitHub
- ✅ Sin tarjeta de crédito inicial

## 📄 Licencia

© 2025 ANCLAJE SOLAR ENERGY S.A.S
