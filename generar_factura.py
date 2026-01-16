#!/usr/bin/env python3
"""
Script para generar factura de ANCLAJE SOLAR ENERGY S.A.S
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# Colores corporativos de ANCLAJE SOLAR ENERGY
COLOR_DORADO = colors.HexColor('#F5B301')  # Amarillo/dorado del sol
COLOR_AZUL = colors.HexColor('#1E5A8E')    # Azul de los paneles
COLOR_NEGRO = colors.HexColor('#2C2C2C')   # Negro del fondo
COLOR_GRIS = colors.HexColor('#6B6B6B')    # Gris para detalles


class FooterCanvas(canvas.Canvas):
    """Canvas personalizado para agregar pie de página automático"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_footer(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_footer(self, page_count):
        """Dibuja el pie de página en cada página"""
        page_width = letter[0]
        page_height = letter[1]
        
        # Línea decorativa dorada
        self.setStrokeColor(COLOR_DORADO)
        self.setLineWidth(3)
        self.line(40, 60, page_width - 40, 60)
        
        # Texto del pie de página
        self.setFont('Helvetica-Bold', 9)
        self.setFillColor(COLOR_AZUL)
        text1 = "Gracias por confiar en ANCLAJE SOLAR ENERGY"
        text_width1 = self.stringWidth(text1, 'Helvetica-Bold', 9)
        self.drawString((page_width - text_width1) / 2, 45, text1)
        
        self.setFont('Helvetica-Oblique', 8)
        self.setFillColor(COLOR_GRIS)
        text2 = "Energía limpia • Estabilidad • Futuro"
        text_width2 = self.stringWidth(text2, 'Helvetica-Oblique', 8)
        self.drawString((page_width - text_width2) / 2, 32, text2)


def generar_factura(
    logo_path=None,
    nit="",
    telefono="",
    correo="",
    cliente="",
    documento="",
    direccion="",
    fecha="",
    factura_no="",
    items=[],
    subtotal=0,
    iva=0,
    total=0
):
    """
    Genera una factura en PDF
    
    Args:
        logo_path: Ruta al archivo del logo (opcional)
        nit: NIT de la empresa
        telefono: Teléfono de la empresa
        correo: Correo de la empresa
        cliente: Nombre del cliente
        documento: Documento del cliente
        direccion: Dirección del cliente
        fecha: Fecha de la factura
        factura_no: Número de factura
        items: Lista de diccionarios con 'descripcion', 'cantidad', 'valor_unitario'
        subtotal: Subtotal de la factura
        iva: IVA de la factura
        total: Total a pagar
    """
    
    filename = f"factura_{factura_no or datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(
        filename, 
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=80  # Espacio extra para el pie de página
    )
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=COLOR_NEGRO,
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    empresa_style = ParagraphStyle(
        'EmpresaStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLOR_NEGRO,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )
    
    # Encabezado con logo y título
    header_data = []
    
    if logo_path and os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=1.5*inch, height=1.5*inch)
            title_para = Paragraph("<b>FACTURA DE VENTA</b>", title_style)
            header_data = [[img, title_para]]
            header_table = Table(header_data, colWidths=[2*inch, 4.5*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))
        except Exception as e:
            story.append(Paragraph("<b>FACTURA DE VENTA</b>", title_style))
    else:
        story.append(Paragraph("<b>FACTURA DE VENTA</b>", title_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Barra decorativa con colores corporativos  
    page_width = letter[0] - 80  # Ancho de página menos márgenes
    barra_data = [[""]]
    barra_table = Table(barra_data, colWidths=[page_width], rowHeights=[0.15*inch])
    barra_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_DORADO),
        ('LINEBELOW', (0, 0), (-1, -1), 2, COLOR_AZUL),
    ]))
    story.append(barra_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Información de la empresa en caja con fondo
    empresa_data = [
        [Paragraph("<b><font size=12 color='#1E5A8E'>ANCLAJE SOLAR ENERGY S.A.S</font></b>", empresa_style)],
        [Paragraph("<i>Energía Solar Fotovoltaica</i>", empresa_style)],
        [Paragraph(f"<b>NIT:</b> {nit}", empresa_style)],
        [Paragraph(f"<b>Teléfono:</b> {telefono}", empresa_style)],
        [Paragraph(f"<b>Correo:</b> {correo}", empresa_style)]
    ]
    
    empresa_table = Table(empresa_data, colWidths=[page_width])
    empresa_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9F9F9')),
        ('BOX', (0, 0), (-1, -1), 1.5, COLOR_AZUL),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(empresa_table)
    story.append(Spacer(1, 0.25*inch))
    
    # Información del cliente en dos columnas
    cliente_izq = [
        [Paragraph("<b>Cliente:</b>", empresa_style)],
        [Paragraph("<b>Documento:</b>", empresa_style)],
        [Paragraph("<b>Dirección:</b>", empresa_style)],
    ]
    
    cliente_der = [
        [Paragraph("<b>Fecha:</b>", empresa_style)],
        [Paragraph("<b>Factura No:</b>", empresa_style)],
        [Paragraph("", empresa_style)],  # Espacio vacío
    ]
    
    valores_izq = [
        [Paragraph(cliente, empresa_style)],
        [Paragraph(documento, empresa_style)],
        [Paragraph(direccion, empresa_style)],
    ]
    
    valores_der = [
        [Paragraph(fecha, empresa_style)],
        [Paragraph(f"<b><font color='#F5B301'>{factura_no}</font></b>", empresa_style)],
        [Paragraph("", empresa_style)],
    ]
    
    # Combinar las tablas - distribuir el ancho disponible
    col1_width = page_width * 0.30
    col2_width = page_width * 0.30
    col3_width = page_width * 0.20
    col4_width = page_width * 0.20
    
    tabla_izq = Table([[cliente_izq[i][0], valores_izq[i][0]] for i in range(3)], 
                      colWidths=[col1_width * 0.35, col1_width * 0.65])
    tabla_der = Table([[cliente_der[i][0], valores_der[i][0]] for i in range(3)], 
                      colWidths=[col2_width * 0.40, col2_width * 0.60])
    
    cliente_main = Table([[tabla_izq, tabla_der]], colWidths=[page_width * 0.53, page_width * 0.47])
    cliente_main.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAFAFA')),
        ('BOX', (0, 0), (-1, -1), 1.5, COLOR_DORADO),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(cliente_main)
    story.append(Spacer(1, 0.25*inch))
    
    # Tabla de items con diseño profesional
    items_data = [["Descripción", "Cantidad", "Valor Unitario", "Total"]]
    
    for item in items:
        descripcion = item.get('descripcion', '')
        tiene_iva = item.get('tiene_iva', False)
        
        # Agregar indicador de IVA si aplica
        if tiene_iva:
            descripcion = f"{descripcion} (+IVA)"
        
        items_data.append([
            descripcion,
            str(item.get('cantidad', '')),
            f"${item.get('valor_unitario', 0):,.2f}",
            f"${item.get('cantidad', 0) * item.get('valor_unitario', 0):,.2f}"
        ])
    
    # Distribuir columnas proporcionalmente
    items_table = Table(items_data, colWidths=[
        page_width * 0.45,  # Descripción
        page_width * 0.15,  # Cantidad
        page_width * 0.20,  # Valor Unitario
        page_width * 0.20   # Total
    ])
    items_table.setStyle(TableStyle([
        # Encabezado con colores corporativos
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_AZUL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Cuerpo de la tabla
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        
        # Filas alternadas
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
        
        # Bordes
        ('BOX', (0, 0), (-1, -1), 1.5, COLOR_AZUL),
        ('LINEBELOW', (0, 0), (-1, 0), 2, COLOR_DORADO),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
        
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    # Totales con diseño profesional (se agregarán juntos con la tabla)
    totales_style = ParagraphStyle(
        'TotalesStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_NEGRO,
        alignment=TA_RIGHT,
    )
    
    total_final_style = ParagraphStyle(
        'TotalFinalStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.white,
        alignment=TA_RIGHT,
        fontName='Helvetica-Bold'
    )
    
    totales_data = [
        ["Subtotal:", f"${subtotal:,.2f}"],
        ["IVA (19%):", f"${iva:,.2f}"],
    ]
    
    totales_table = Table(totales_data, colWidths=[1.5*inch, 1.5*inch])
    totales_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_NEGRO),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAFAFA')),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_GRIS),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    totales_table.hAlign = 'RIGHT'
    
    # Total a pagar destacado
    total_final_data = [["TOTAL A PAGAR:", f"${total:,.2f}"]]
    total_final_table = Table(total_final_data, colWidths=[1.5*inch, 1.5*inch])
    total_final_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_AZUL),
        ('BOX', (0, 0), (-1, -1), 2, COLOR_DORADO),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    total_final_table.hAlign = 'RIGHT'
    
    # Agrupar tabla de items con los totales para mantenerlos juntos
    items_y_totales = [
        items_table,
        Spacer(1, 0.2*inch),
        totales_table,
        Spacer(1, 0.1*inch),
        total_final_table
    ]
    
    story.append(KeepTogether(items_y_totales))
    
    # Generar PDF con pie de página automático
    doc.build(story, canvasmaker=FooterCanvas)
    print(f"✓ Factura generada: {filename}")
    return filename


def ejemplo_uso():
    """Ejemplo de cómo usar el generador de facturas"""
    
    items_ejemplo = [
        {
            'descripcion': 'Panel Solar 450W',
            'cantidad': 10,
            'valor_unitario': 850000,
            'tiene_iva': True
        },
        {
            'descripcion': 'Inversor 5kW',
            'cantidad': 1,
            'valor_unitario': 3500000,
            'tiene_iva': True
        },
        {
            'descripcion': 'Instalación y configuración',
            'cantidad': 1,
            'valor_unitario': 2000000,
            'tiene_iva': True
        }
    ]
    
    subtotal = sum(item['cantidad'] * item['valor_unitario'] for item in items_ejemplo)
    iva = sum(item['cantidad'] * item['valor_unitario'] * 0.19 for item in items_ejemplo if item.get('tiene_iva', False))
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
    
    generar_factura(
        logo_path=logo_path,
        nit="901.234.567-8",
        telefono="+57 300 123 4567",
        correo="ventas@anclajesolar.com",
        cliente="Juan Pérez García",
        documento="CC 1234567890",
        direccion="Calle 123 #45-67, Bogotá",
        fecha=datetime.now().strftime("%d/%m/%Y"),
        factura_no="001-2025",
        items=items_ejemplo,
        subtotal=subtotal,
        iva=iva,
        total=total
    )


if __name__ == "__main__":
    print("Generador de Facturas - ANCLAJE SOLAR ENERGY")
    print("=" * 50)
    ejemplo_uso()
