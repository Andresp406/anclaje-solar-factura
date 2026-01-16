# 📧 Guía: Automatizar envío de facturas con n8n

## 🎯 Objetivo
Enviar automáticamente cada factura generada por email y WhatsApp usando n8n.

## 📋 Paso 1: Crear Workflow en n8n

### 1.1 Accede a tu cuenta n8n Cloud
- Ve a https://app.n8n.cloud/
- Inicia sesión con tu cuenta

### 1.2 Crea un nuevo workflow
1. Click en **"Create new workflow"**
2. Nómbralo: **"Envío Automático de Facturas"**

## 🔧 Paso 2: Configurar Nodos en n8n

### Nodo 1: Webhook (Trigger)

1. **Agregar nodo Webhook:**
   - Click en **"+"** → Busca **"Webhook"**
   - Configura:
     - **HTTP Method**: `POST`
     - **Path**: `factura-generada`
     - **Authentication**: `None` (o Header Auth si quieres seguridad)

2. **Copiar URL del Webhook:**
   - n8n te dará una URL como: `https://tu-instancia.app.n8n.cloud/webhook/factura-generada`
   - **Guárdala**, la necesitarás para Railway

### Nodo 2: Decodificar PDF de Base64

1. **Agregar nodo Code:**
   - Click en **"+"** → Busca **"Code"**
   - Modo: `Run Once for All Items`
   - Código:

```javascript
const items = $input.all();

return items.map(item => {
  const pdfData = item.json.pdf_base64;
  const pdfFilename = item.json.pdf_filename;
  
  return {
    json: item.json,
    binary: {
      data: {
        data: pdfData,
        mimeType: 'application/pdf',
        fileName: pdfFilename,
        fileExtension: 'pdf'
      }
    }
  };
});
```

### Nodo 3: IF - Verificar si hay Email

1. **Agregar nodo IF:**
   - Click en **"+"** → Busca **"IF"**
   - Condición:
     - **Value 1**: `{{ $json.email_cliente }}`
     - **Operation**: `is not empty`

### Nodo 4: Enviar Email (rama TRUE)

1. **Agregar nodo Gmail/Send Email:**
   - Conecta desde la salida **TRUE** del IF
   - Click en **"+"** → Busca **"Gmail"** o **"Send Email"**
   
2. **Configurar Gmail:**
   - **Operation**: `Send`
   - **To**: `={{ $json.email_cliente }}`
   - **Subject**: `Factura {{ $json.factura_no }} - ANCLAJE SOLAR ENERGY`
   - **Message**: 
   ```
   Hola {{ $json.cliente }},

   Adjunto encontrarás tu factura No. {{ $json.factura_no }}.

   Detalle:
   - Fecha: {{ $json.fecha }}
   - Subtotal: ${{ $json.subtotal }}
   - IVA: ${{ $json.iva }}
   - Total: ${{ $json.total }}

   Gracias por tu preferencia.

   ANCLAJE SOLAR ENERGY
   Energía limpia • Estabilidad • Futuro
   ```
   - **Attachments**: `Binary Property` → `data`

3. **Conectar cuenta Gmail:**
   - Click en **"Create New Credential"**
   - Sigue el proceso OAuth de Google

### Nodo 5: IF - Verificar si hay WhatsApp

1. **Agregar otro nodo IF:**
   - Condición:
     - **Value 1**: `{{ $json.telefono_cliente }}`
     - **Operation**: `is not empty`

### Nodo 6: Enviar WhatsApp (rama TRUE)

#### Opción A: WhatsApp Cloud API (Oficial de Meta)

1. **Agregar nodo HTTP Request:**
   - **Method**: `POST`
   - **URL**: `https://graph.facebook.com/v18.0/TU_PHONE_ID/messages`
   - **Authentication**: `Generic Credential Type` → `Header Auth`
     - Header Name: `Authorization`
     - Header Value: `Bearer TU_TOKEN_DE_WHATSAPP`
   - **Body Content Type**: `JSON`
   - **Body**:
   ```json
   {
     "messaging_product": "whatsapp",
     "to": "{{ $json.telefono_cliente }}",
     "type": "document",
     "document": {
       "link": "URL_DEL_PDF_TEMPORAL",
       "caption": "Factura {{ $json.factura_no }} - ANCLAJE SOLAR ENERGY"
     }
   }
   ```

#### Opción B: Twilio WhatsApp (Más fácil)

1. **Agregar nodo Twilio:**
   - Busca **"Twilio"**
   - **Resource**: `Message`
   - **Operation**: `Send`
   - **From**: `whatsapp:+14155238886` (número de Twilio)
   - **To**: `whatsapp:{{ $json.telefono_cliente }}`
   - **Message**: 
   ```
   Hola {{ $json.cliente }}! 📄
   
   Tu factura {{ $json.factura_no }} ha sido generada.
   
   Total: ${{ $json.total }}
   
   La factura PDF llegará a tu email.
   
   ANCLAJE SOLAR ENERGY ☀️
   ```

#### Opción C: Evolution API (Recomendado - Sin límites)

1. **Agregar nodo HTTP Request:**
   - **Method**: `POST`
   - **URL**: `https://tu-evolution-api.com/message/sendMedia`
   - **Headers**:
     - `Content-Type`: `application/json`
     - `apikey`: `TU_API_KEY`
   - **Body**:
   ```json
   {
     "number": "{{ $json.telefono_cliente }}",
     "mediaBase64": "{{ $json.pdf_base64 }}",
     "fileName": "{{ $json.pdf_filename }}",
     "caption": "Factura {{ $json.factura_no }} - ANCLAJE SOLAR ENERGY"
   }
   ```

## 🔐 Paso 3: Configurar Variable de Entorno en Railway

1. **Ve a Railway Dashboard:**
   - https://railway.app/
   - Selecciona tu proyecto **"anclaje-solar-factura"**

2. **Agregar Variable de Entorno:**
   - Click en **"Variables"**
   - Click en **"+ New Variable"**
   - **Name**: `N8N_WEBHOOK_URL`
   - **Value**: `https://tu-instancia.app.n8n.cloud/webhook/factura-generada`
   - Click **"Add"**

3. **Redesplegar:**
   - Railway redesplegará automáticamente con la nueva variable

## 🧪 Paso 4: Probar el Sistema

### 4.1 Activar Workflow en n8n
1. En n8n, click en **"Execute Workflow"** (botón de play arriba)
2. El webhook quedará escuchando

### 4.2 Generar Factura de Prueba
1. Ve a tu app: https://web-production-612f3.up.railway.app/
2. Llena el formulario:
   - Datos del cliente
   - **Email**: Tu email de prueba
   - **WhatsApp**: Tu número de prueba (+57 XXX XXX XXXX)
3. Genera la factura

### 4.3 Verificar
- ✅ Deberías recibir el PDF por email
- ✅ Deberías recibir mensaje por WhatsApp
- ✅ En n8n verás la ejecución en el historial

## 📊 Workflow Visual (Resumen)

```
[Webhook] → [Decodificar PDF] → [IF Email?]
                                      ├─ TRUE → [Enviar Gmail]
                                      └─ FALSE → (no hace nada)
                                   
                                 → [IF WhatsApp?]
                                      ├─ TRUE → [Enviar WhatsApp]
                                      └─ FALSE → (no hace nada)
```

## 🔧 Configuraciones Adicionales Opcionales

### Guardar Facturas en Google Drive

1. **Agregar nodo Google Drive:**
   - Después de "Decodificar PDF"
   - **Operation**: `Upload`
   - **File**: Binary Data → `data`
   - **Folder**: Selecciona carpeta de Drive
   - **File Name**: `{{ $json.pdf_filename }}`

### Notificar a Slack

1. **Agregar nodo Slack:**
   - **Operation**: `Post Message`
   - **Channel**: `#facturas`
   - **Text**: 
   ```
   Nueva factura generada! 🎉
   Cliente: {{ $json.cliente }}
   No: {{ $json.factura_no }}
   Total: ${{ $json.total }}
   ```

### Guardar en Base de Datos

1. **Agregar nodo MySQL/PostgreSQL/Airtable:**
   - Guarda: cliente, factura_no, total, fecha
   - Para reportes y análisis

## 🚨 Solución de Problemas

### Email no llega:
- Verifica credenciales de Gmail
- Revisa spam
- Confirma que `email_cliente` no esté vacío

### WhatsApp no llega:
- Verifica número con código de país (+57)
- Confirma que WhatsApp API esté configurada
- Revisa logs de n8n

### Webhook no responde:
- Verifica que workflow esté ACTIVO en n8n
- Confirma URL en Railway
- Revisa logs de Railway: `railway logs`

## 📝 Notas Importantes

1. **Seguridad**: Considera agregar autenticación al webhook (Header Auth)
2. **Límites**: 
   - Gmail: 500 emails/día
   - WhatsApp Meta: Requiere Business Account verificada
   - Twilio WhatsApp: Números pre-aprobados para pruebas
3. **Costos**:
   - n8n Cloud: Plan gratuito hasta 5,000 ejecuciones/mes
   - Gmail: Gratis
   - WhatsApp Meta: Gratis hasta 1,000 conversaciones/mes
   - Twilio: $0.005 por mensaje

## 🎉 ¡Listo!

Tu sistema de facturación ahora envía automáticamente:
- ✅ PDF por email
- ✅ Notificación por WhatsApp
- ✅ Sin intervención manual

---

**ANCLAJE SOLAR ENERGY**  
*Energía limpia • Estabilidad • Futuro*
