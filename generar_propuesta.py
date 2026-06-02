from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Colores ──────────────────────────────────────────────
DARK   = colors.HexColor('#1a1714')
GOLD   = colors.HexColor('#c8962a')
CREAM  = colors.HexColor('#faf6ef')
CREAM2 = colors.HexColor('#f0e9dc')
RUST   = colors.HexColor('#9b3a2a')
GREY   = colors.HexColor('#5a4e46')
WHITE  = colors.white
BLUE   = colors.HexColor('#1a3a7a')

W, H = A4

# ── Estilos ──────────────────────────────────────────────
styles = getSampleStyleSheet()

def sty(name, **kwargs):
    base = kwargs.pop('parent', 'Normal')
    s = ParagraphStyle(name, parent=styles[base], **kwargs)
    return s

S = {
    'portada_brand': sty('portada_brand',
        fontSize=13, textColor=GOLD, alignment=TA_CENTER,
        spaceAfter=6, fontName='Helvetica-Bold', letterSpacing=4),
    'portada_title': sty('portada_title',
        fontSize=34, textColor=WHITE, alignment=TA_CENTER,
        spaceAfter=8, fontName='Helvetica-Bold', leading=40),
    'portada_sub': sty('portada_sub',
        fontSize=16, textColor=CREAM2, alignment=TA_CENTER,
        spaceAfter=6, fontName='Helvetica', leading=22),
    'portada_date': sty('portada_date',
        fontSize=10, textColor=GOLD, alignment=TA_CENTER,
        spaceAfter=4, fontName='Helvetica'),
    'portada_tag': sty('portada_tag',
        fontSize=13, textColor=CREAM2, alignment=TA_CENTER,
        fontName='Helvetica-Oblique'),

    'h1': sty('h1',
        fontSize=20, textColor=DARK, fontName='Helvetica-Bold',
        spaceBefore=18, spaceAfter=6, leading=26),
    'h2': sty('h2',
        fontSize=14, textColor=RUST, fontName='Helvetica-Bold',
        spaceBefore=14, spaceAfter=4, leading=18),
    'body': sty('body',
        fontSize=10.5, textColor=DARK, fontName='Helvetica',
        spaceAfter=5, leading=16, alignment=TA_JUSTIFY),
    'bullet': sty('bullet',
        fontSize=10.5, textColor=DARK, fontName='Helvetica',
        spaceAfter=4, leading=16, leftIndent=18, bulletIndent=4),
    'check': sty('check',
        fontSize=10.5, textColor=DARK, fontName='Helvetica',
        spaceAfter=3, leading=16, leftIndent=18),
    'callout': sty('callout',
        fontSize=10, textColor=GREY, fontName='Helvetica-Oblique',
        spaceAfter=6, leading=15, leftIndent=16, rightIndent=16,
        borderPadding=(8, 10, 8, 10), backColor=CREAM2,
        borderColor=GOLD, borderWidth=0),
    'footer': sty('footer',
        fontSize=7.5, textColor=GREY, alignment=TA_CENTER,
        fontName='Helvetica'),
    'num': sty('num',
        fontSize=11, textColor=DARK, fontName='Helvetica',
        spaceAfter=4, leading=16, leftIndent=18),
}


# ── Header / Footer ──────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(DARK)
    canvas.rect(0, H - 1.4*cm, W, 1.4*cm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(2*cm, H - 0.9*cm, 'ASBE')
    canvas.setFillColor(CREAM2)
    canvas.setFont('Helvetica', 8)
    canvas.drawRightString(W - 2*cm, H - 0.9*cm, 'Agencia de Servicios para el Sector de la Hostelería')
    # Gold line under header
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.5)
    canvas.line(0, H - 1.4*cm, W, H - 1.4*cm)
    # Footer
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.8*cm, W - 2*cm, 1.8*cm)
    canvas.setFillColor(GREY)
    canvas.setFont('Helvetica', 7)
    footer = 'ASBE · Agencia de Servicios para el Sector de la Hostelería · Málaga 2025 · sofia.beltran.calce@gmail.com'
    canvas.drawCentredString(W/2, 1.2*cm, footer)
    canvas.drawRightString(W - 2*cm, 1.2*cm, f'Pág. {doc.page}')
    canvas.restoreState()


def on_page_cover(canvas, doc):
    canvas.saveState()
    # Full dark background
    canvas.setFillColor(DARK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Gold top band
    canvas.setFillColor(GOLD)
    canvas.rect(0, H - 0.8*cm, W, 0.8*cm, fill=1, stroke=0)
    # Gold bottom band
    canvas.rect(0, 0, W, 0.8*cm, fill=1, stroke=0)
    # Subtle grid lines
    canvas.setStrokeColor(colors.HexColor('#2a2420'))
    canvas.setLineWidth(0.4)
    for x in range(0, int(W), 40):
        canvas.line(x, 0, x, H)
    for y in range(0, int(H), 40):
        canvas.line(0, y, W, y)
    # Center gold circle accent
    canvas.setFillColor(colors.HexColor('#c8962a22'))
    canvas.circle(W/2, H/2, 200, fill=1, stroke=0)
    canvas.restoreState()


# ── Documento ────────────────────────────────────────────
OUT = r'C:\Users\Usuario\Documents\Claude\Propuesta-Carta-PicnicSoho\Propuesta-PicnicSoho.pdf'

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    topMargin=2.4*cm, bottomMargin=2.4*cm,
)

story = []

# ═══════════════════════════════════════════════
# PORTADA
# ═══════════════════════════════════════════════
story.append(Spacer(1, 4.5*cm))
story.append(Paragraph('A S B E', S['portada_brand']))
story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width='60%', thickness=1.5, color=GOLD, spaceAfter=20, spaceBefore=4))
story.append(Paragraph('Propuesta de<br/>Carta Digital', S['portada_title']))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph('The PicNic · Soho · Málaga', S['portada_sub']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('Junio 2025', S['portada_date']))
story.append(HRFlowable(width='60%', thickness=1.5, color=GOLD, spaceAfter=20, spaceBefore=20))
story.append(Paragraph('"Una carta que vende por ti"', S['portada_tag']))
story.append(Spacer(1, 3*cm))
story.append(Paragraph('Presentada por', sty('tmp', fontSize=9, textColor=GREY, alignment=TA_CENTER, fontName='Helvetica')))
story.append(Paragraph('ASBE — Agencia de Servicios para el Sector de la Hostelería', sty('tmp2', fontSize=10, textColor=CREAM2, alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Paragraph('sofia.beltran.calce@gmail.com', sty('tmp3', fontSize=9, textColor=GOLD, alignment=TA_CENTER, fontName='Helvetica')))

story.append(PageBreak())

# ═══════════════════════════════════════════════
# SECCIÓN 1 — EL PROBLEMA
# ═══════════════════════════════════════════════
story.append(Paragraph('1. El problema actual', S['h1']))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=10))
story.append(Paragraph(
    'La carta actual de The PicNic está diseñada en formato de periódico denso, '
    'con texto pequeño y sin jerarquía visual. Esto genera problemas reales para el negocio:',
    S['body']))
story.append(Spacer(1, 0.2*cm))

problemas = [
    'Dificultad para que el cliente encuentre lo que busca',
    'Pérdida de oportunidades de venta cruzada',
    'Imagen poco acorde al nivel gastronómico del local',
    'Sin adaptación a móvil ni posibilidad de actualización rápida',
]
for p in problemas:
    story.append(Paragraph(f'&#x2022;  {p}', S['bullet']))

story.append(Spacer(1, 0.8*cm))

# ═══════════════════════════════════════════════
# SECCIÓN 2 — NUESTRA PROPUESTA
# ═══════════════════════════════════════════════
story.append(Paragraph('2. Nuestra propuesta: Carta Digital Web', S['h1']))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=10))
story.append(Paragraph(
    'Hemos desarrollado una carta digital completa, moderna y totalmente personalizada '
    'para The PicNic. Es una web accesible desde cualquier dispositivo mediante QR en mesa.',
    S['body']))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph('<b>¿Qué incluye?</b>', S['body']))
story.append(Spacer(1, 0.1*cm))

includes = [
    'Diseño elegante acorde a la identidad del local (colores, tipografía, estética)',
    'Todas las secciones organizadas: Desayunos, Bebidas, Tapas, Gourmet Burgers, Ensaladas & Wraps, Para Compartir, Dulces',
    'Descripciones completas de cada plato y precios actualizados',
    'Sección de Alérgenos integrada',
    'QR de mesa — uno para la carta y otro para reseñas en Google',
    'Adaptación perfecta a móvil, tablet y ordenador',
    'Alojada online (dominio propio o subdominio)',
]
for item in includes:
    story.append(Paragraph(f'<font color="#c8962a">&#10003;</font>  {item}', S['check']))

story.append(Spacer(1, 0.8*cm))

# ═══════════════════════════════════════════════
# SECCIÓN 3 — TODO ES EDITABLE
# ═══════════════════════════════════════════════
story.append(Paragraph('3. Todo es editable — es tuya para siempre', S['h1']))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=10))
story.append(Paragraph(
    'La carta está construida sobre tecnología web estándar, lo que significa que tienes control total:',
    S['body']))
story.append(Spacer(1, 0.2*cm))

editables = [
    '<b>Actualizar precios en minutos</b> — sin coste adicional',
    '<b>Añadir o eliminar platos</b> según temporada o disponibilidad',
    '<b>Cambiar fotos</b> cuando quieras',
    '<b>Sin apps, sin suscripciones</b> — es tuya para siempre',
]
for e in editables:
    story.append(Paragraph(f'&#x2022;  {e}', S['bullet']))

story.append(Spacer(1, 0.4*cm))
callout_text = (
    '<b>Recomendacion:</b> Anadir una fotografia propia de cada plato aumenta el ticket medio '
    'entre un 20% y un 30% segun estudios del sector. '
    'Podemos incluir sesion fotografica profesional en el paquete.'
)
story.append(Paragraph(callout_text, S['callout']))
story.append(Spacer(1, 0.5*cm))

# ═══════════════════════════════════════════════
# SECCIÓN 4 — QR MESAS
# ═══════════════════════════════════════════════
story.append(Paragraph('4. QR para las mesas', S['h1']))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=10))
story.append(Paragraph(
    'Se entregan dos códigos QR listos para imprimir y plastificar en cada mesa:',
    S['body']))
story.append(Spacer(1, 0.3*cm))

qr_data = [
    ['QR', 'Destino', 'Beneficio'],
    ['Ver la Carta', 'Carta digital online', 'El cliente navega el menú desde su móvil sin esperar'],
    ['Dejar Reseña', 'Google Reviews directo', 'Más reseñas = más visibilidad en Google Maps'],
]
qr_table = Table(qr_data, colWidths=[3.5*cm, 5.5*cm, 8*cm])
qr_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK),
    ('TEXTCOLOR', (0,0), (-1,0), GOLD),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CREAM2]),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 9),
    ('TEXTCOLOR', (0,1), (-1,-1), DARK),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0,1), (0,-1), RUST),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('PADDING', (0,0), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 0.5, CREAM2),
    ('LINEBELOW', (0,0), (-1,0), 2, GOLD),
]))
story.append(qr_table)
story.append(Spacer(1, 0.8*cm))

# ═══════════════════════════════════════════════
# SECCIÓN 5 — OPCIÓN PRO CON IA
# ═══════════════════════════════════════════════
story.append(PageBreak())
story.append(Paragraph('5. Opción PRO — Inteligencia Artificial integrada', S['h1']))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=10))
story.append(Paragraph(
    'Para los locales que quieren ir un paso más allá, ofrecemos la versión PRO con IA. '
    'Un chat con inteligencia artificial integrado en la carta donde el cliente puede:',
    S['body']))
story.append(Spacer(1, 0.2*cm))

ia_features = [
    'Preguntar qué platos tienen sin gluten, sin lactosa, veganos, etc.',
    'Pedir recomendaciones según su estado de ánimo o preferencias',
    'Conocer los ingredientes exactos de cada plato',
    '<b>Realizar su pedido directamente desde el chat</b>, sin necesidad de camarero',
]
for f in ia_features:
    story.append(Paragraph(f'&#x2022;  {f}', S['bullet']))

story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('<b>Beneficios para el negocio:</b>', S['body']))
story.append(Spacer(1, 0.1*cm))

ia_benefits = [
    'Reducción de tiempos de espera y mayor rotación de mesas',
    'Datos en tiempo real sobre qué platos se piden más',
    'Experiencia diferencial que fideliza al cliente y genera reseñas positivas',
    'Funciona 24/7 sin coste de personal adicional',
]
for b in ia_benefits:
    story.append(Paragraph(f'<font color="#c8962a">&#10003;</font>  {b}', S['check']))

story.append(Spacer(1, 0.4*cm))
story.append(Paragraph(
    'Esta opcion utiliza modelos de lenguaje de ultima generacion '
    '(Claude de Anthropic, el mismo modelo que usa ChatGPT Pro) '
    'integrados directamente en tu carta digital. '
    'Sin servidores complicados, sin mantenimiento tecnico por tu parte.',
    S['callout']))
story.append(Spacer(1, 0.8*cm))

# ═══════════════════════════════════════════════
# SECCIÓN 6 — INVERSIÓN
# ═══════════════════════════════════════════════
story.append(Paragraph('6. Inversión', S['h1']))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=10))

inv_data = [
    ['Paquete', 'Incluye', 'Precio'],
    ['Carta Digital Base',
     'Diseño personalizado + web online + 2 QR + 1 año de hosting',
     'Consultar'],
    ['Carta + Fotos',
     'Todo lo anterior + sesión fotográfica profesional de los platos',
     'Consultar'],
    ['PRO con IA',
     'Todo lo anterior + chat IA integrado + sistema de pedidos online',
     'Consultar'],
]
inv_table = Table(inv_data, colWidths=[4.5*cm, 8.5*cm, 3*cm])
inv_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK),
    ('TEXTCOLOR', (0,0), (-1,0), GOLD),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, CREAM2]),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0,1), (0,-1), DARK),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 9),
    ('TEXTCOLOR', (0,1), (-1,-1), DARK),
    ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (2,1), (2,-1), GOLD),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('PADDING', (0,0), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, CREAM2),
    ('LINEBELOW', (0,0), (-1,0), 2, GOLD),
    # Highlight PRO row
    ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#2a2420')),
    ('TEXTCOLOR', (0,3), (-1,3), CREAM2),
    ('FONTNAME', (0,3), (0,3), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0,3), (0,3), GOLD),
    ('TEXTCOLOR', (2,3), (2,3), GOLD),
]))
story.append(inv_table)
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph(
    '* Precios personalizados según necesidades del local. Sin cuotas mensuales en el paquete base.',
    sty('note', fontSize=8, textColor=GREY, fontName='Helvetica-Oblique')))
story.append(Spacer(1, 0.8*cm))

# ═══════════════════════════════════════════════
# SECCIÓN 7 — POR QUÉ ASBE
# ═══════════════════════════════════════════════
story.append(Paragraph('7. Por qué ASBE', S['h1']))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=10))
story.append(Paragraph(
    'ASBE es una agencia especializada en digitalización para el sector hostelero en Málaga. '
    'Trabajamos exclusivamente con restaurantes, cafeterías y bares para que la tecnología '
    'trabaje a su favor sin complicaciones técnicas.',
    S['body']))
story.append(Spacer(1, 0.3*cm))

asbe_points = [
    'Presencia local en Málaga — nos reunimos donde y cuando necesites',
    'Soporte en español, sin tecnicismos ni letra pequeña',
    'Entrega en 7 días laborables desde la aprobación',
    'Revisiones ilimitadas incluidas hasta tu total satisfacción',
    'Formación incluida: te enseñamos a editar tu carta en 5 minutos',
]
for a in asbe_points:
    story.append(Paragraph(f'<font color="#c8962a">&#10003;</font>  {a}', S['check']))

story.append(Spacer(1, 1*cm))

# ═══════════════════════════════════════════════
# PRÓXIMOS PASOS
# ═══════════════════════════════════════════════
story.append(Paragraph('Próximos pasos', S['h1']))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=10))

pasos = [
    'Revisamos juntos la carta y confirmamos platos, precios y secciones',
    'Sesión de fotos de los platos (opcional pero muy recomendada)',
    'Publicamos tu carta en línea con tu dominio o subdominio',
    'Te entregamos los QR listos para imprimir y poner en mesa',
    'Te explicamos cómo editarla tú mismo en menos de 5 minutos',
]
for i, p in enumerate(pasos, 1):
    story.append(Paragraph(f'<b>{i}.</b>  {p}', S['num']))

story.append(Spacer(1, 1.2*cm))

# CTA final
cta_data = [['¿Hablamos?   sofia.beltran.calce@gmail.com']]
cta_table = Table(cta_data, colWidths=[16.6*cm])
cta_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK),
    ('TEXTCOLOR', (0,0), (-1,-1), GOLD),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 13),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 18),
    ('BOTTOMPADDING', (0,0), (-1,-1), 18),
    ('LINEABOVE', (0,0), (-1,0), 2, GOLD),
    ('LINEBELOW', (0,-1), (-1,-1), 2, GOLD),
]))
story.append(cta_table)

# ═══════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════
doc.build(
    story,
    onFirstPage=on_page_cover,
    onLaterPages=on_page,
)
print(f'PDF generado: {OUT}')
