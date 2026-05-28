import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import textwrap

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(page_title="Generador CNSC Pro", layout="wide")
st.title("Automatización de Piezas socializaciones CNSC")

# ==========================================
# 2. CONFIGURACIÓN POR FORMATO
# ==========================================
FORMATOS = {
    "Post (Instagram)": {
        "archivo": "assets/PLANTILLA-EON-2026_POST.png", 
        "escala_alto": 900,  
        "coords": {
            "desc": (200, 1986),
            "ciudad": (350, 900),
            "dia": (2019, 1702),
            "ano": (2019, 1815),
            "hora": (540, 2516),
            "lugar": (1091, 2431),
            "direccion": (1091, 2517),
            "publico": (1623, 2330)
        },
        "ancho_caja_desc": 1900, # Ancho en píxeles
        "tamano_fuente_desc": 55,
        "tamano_fuente_ciudad": 80,
        "tamano_fuente_dia": 100,
        "tamano_fuente_ano": 55,
        "tamano_fuente_hora": 70,
        "tamano_fuente_lugar": 75,
        "tamano_fuente_direccion": 40,
        "ancho_caja_direccion": 921,
        "tamano_fuente_publico": 60
    },
    "Historia": {
        "archivo": "assets/PLANTILLA-EON-2026_HISTORIA.png",
        "escala_alto": 1200, 
        "coords": {
            "desc": (213, 2739),
            "ciudad": (459, 1200),
            "dia": (2029, 2375),
            "ano": (2029, 2489),
            "hora": (500, 3562),
            "lugar": (1072, 3487),
            "direccion": (1072, 3569),
            "publico": (1256, 3185)
        },
        "ancho_caja_desc": 1888, # Ancho en píxeles
        "tamano_fuente_desc": 65,
        "tamano_fuente_ciudad": 80,
        "tamano_fuente_dia": 120,
        "tamano_fuente_ano": 55,
        "tamano_fuente_hora": 80,
        "tamano_fuente_lugar": 80,
        "tamano_fuente_direccion": 45,
        "ancho_caja_direccion": 1000,
        "tamano_fuente_publico": 100
    }
}

# ==========================================
# 3. FUNCIONES DE PANELES 
# ==========================================


def obtener_fuente(estilo, tamano):
    fname = "assets/Montserrat-SemiBold.ttf" if estilo == "Bold" else "assets/Montserrat-Regular.ttf"
    try:
        return ImageFont.truetype(fname, tamano)
    except IOError:
        return ImageFont.load_default()

# ==========================================
# 4. BARRA LATERAL
# ==========================================
st.sidebar.subheader("1. Seleccionar Formatos")
st.sidebar.markdown("**Formatos a generar:**")
formatos_elegidos = []
for formato in FORMATOS.keys():
    if st.sidebar.checkbox(formato, value=True):
        formatos_elegidos.append(formato)

st.sidebar.subheader("2. Cargar Foto")
st.sidebar.markdown("Sube la foto de fondo de la ciudad.")
foto_ciudad_subida = st.sidebar.file_uploader("Sube Foto Ciudad", type=["png", "jpg", "jpeg"])

# ==========================================
# 5. LAYOUT Y LÓGICA
# ==========================================
col_controles, col_preview = st.columns([1, 1.2]) 

with col_controles:
    st.subheader("Datos y Controles")
    
    descripcion_txt = st.text_area("Texto Descripción", value="La CNSC te invita a participar en la socialización de las generalidades del proceso de selección en las modalidades de ascenso y abierto, así como las vacantes que se ofertan para personas con discapacidad.")

    municipio = st.text_area("Ciudad", placeholder="Ej: San Andrés\nIslas")
    
    with st.expander("🛠️ Ajustes de Ciudad por Formato"):
        tabs_ciu = st.tabs(["Post (Instagram)", "Historia"])
        defaults_ciu = {
            "Post (Instagram)": {"t": 100, "x": -20, "y": -650},
            "Historia": {"t": 136, "x": -40, "y": -709}
        }
        
        ajustes_ciudad = {}
        for i, fmt in enumerate(["Post (Instagram)", "Historia"]):
            d = defaults_ciu[fmt]
            with tabs_ciu[i]:
                c1, c2, c3 = st.columns(3)
                with c1:
                    t_ciu_off = st.number_input(f"Tamaño (±px)", value=d["t"], step=1, key=f"t_ciu_{fmt}")
                with c2:
                    x_ciu_off = st.number_input(f"Mover X (px)", value=d["x"], step=1, key=f"x_ciu_{fmt}")
                with c3:
                    y_ciu_off = st.number_input(f"Mover Y (px)", value=d["y"], step=1, key=f"y_ciu_{fmt}")
                ajustes_ciudad[fmt] = {"t": t_ciu_off, "x": x_ciu_off, "y": y_ciu_off}
                
    with st.expander("🖼️ Ajustes de Foto de Fondo"):
        tabs_foto = st.tabs(["Post (Instagram)", "Historia"])
        ajustes_foto = {}
        for i, fmt in enumerate(["Post (Instagram)", "Historia"]):
            with tabs_foto[i]:
                cf1, cf2, cf3 = st.columns(3)
                with cf1:
                    z_foto = st.slider("Zoom (%)", min_value=10, max_value=300, value=100, step=5, key=f"z_foto_{fmt}")
                with cf2:
                    x_foto = st.slider("Mover X (%)", min_value=-150, max_value=150, value=0, step=2, key=f"x_foto_{fmt}")
                with cf3:
                    y_foto = st.slider("Mover Y (%)", min_value=-150, max_value=150, value=0, step=2, key=f"y_foto_{fmt}")
                ajustes_foto[fmt] = {"zoom": z_foto / 100.0, "x": x_foto, "y": y_foto}
    
    st.markdown("---")
    st.markdown("**Datos fijos (Fecha, Hora, Lugar):**") 
    with st.container(border=True):
        st.markdown("📅 **Fecha**")
        c1, c2 = st.columns(2)
        with c1:
            dia_txt = st.text_input("Día", value="21 Y 22")
        with c2:
            ano_txt = st.text_input("Año (y mes)", value="de abril de 2026")
            
    hora_txt = st.text_input("Hora", value="9:00 am")
    lugar_txt = st.text_input("Lugar (Nombre)", value="SENA")
    direccion_txt = st.text_area("Dirección", value="Auditorio Centro de la Industria, la Empresa y los Servicios (CIES) Carrera 9 No. 68 - 50")
    publico_txt = st.text_input("Público Objetivo", value="Aforo limitado")

with col_preview:
    st.subheader("Ventana de Previsualización")
    
    if foto_ciudad_subida:
        if not formatos_elegidos:
            st.warning("⚠️ Selecciona al menos un formato en la barra lateral izquierda para comenzar.")
        else:
            img_ciudad_original = Image.open(foto_ciudad_subida).convert("RGBA")
            
            for formato in formatos_elegidos:
                config = FORMATOS[formato]
                st.markdown(f"### 🖼️ {formato}")
                
                try:
                    img_plantilla = Image.open(config["archivo"]).convert("RGBA")
                except FileNotFoundError:
                    st.error(f"⚠️ Error: No se encontró el archivo '{config['archivo']}' en la carpeta.")
                    continue
                
                img_ciudad = img_ciudad_original.copy()
                
                ancho_p, alto_p = img_plantilla.size
                lienzo = Image.new("RGBA", (ancho_p, alto_p), (255, 255, 255, 0))
                
                # Detectar el "hueco" transparente en la plantilla
                alpha = img_plantilla.split()[-1]
                mascara_hueco = alpha.point(lambda p: 255 if p < 128 else 0)
                bbox = mascara_hueco.getbbox()
                
                if bbox:
                    w_hueco = bbox[2] - bbox[0]
                    h_hueco = bbox[3] - bbox[1]
                    
                    ajuste_f = ajustes_foto.get(formato, {"zoom": 1.0, "x": 0, "y": 0})
                    zoom = ajuste_f["zoom"]
                    
                    img_w, img_h = img_ciudad.size
                    aspect_hueco = w_hueco / h_hueco
                    aspect_img = img_w / img_h
                    
                    if aspect_hueco > aspect_img:
                        crop_w = img_w
                        crop_h = img_w / aspect_hueco
                    else:
                        crop_w = img_h * aspect_hueco
                        crop_h = img_h
                        
                    crop_w /= zoom
                    crop_h /= zoom
                    
                    # El movimiento está en un rango de -150% a 150%
                    dx = (ajuste_f["x"] / 100.0) * (img_w / 2)
                    dy = (ajuste_f["y"] / 100.0) * (img_h / 2)
                    
                    cx = (img_w / 2) - dx
                    cy = (img_h / 2) - dy
                    
                    left = cx - crop_w / 2
                    upper = cy - crop_h / 2
                    right = cx + crop_w / 2
                    lower = cy + crop_h / 2
                    
                    foto_ajustada = img_ciudad.transform(
                        (w_hueco, h_hueco),
                        Image.EXTENT,
                        (left, upper, right, lower),
                        resample=Image.Resampling.BICUBIC
                    )
                    
                    lienzo.paste(foto_ajustada, (bbox[0], bbox[1]))
                else:
                    foto_ajustada = ImageOps.fit(img_ciudad, (ancho_p, alto_p), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                    lienzo.paste(foto_ajustada, (0, 0))
                lienzo = Image.alpha_composite(lienzo, img_plantilla)
                
                draw = ImageDraw.Draw(lienzo)
                
                def dibujar_parrafo(texto, coords, tam, col, est, ancho_w, justificar=True):
                    if tam > 0 and texto: 
                        font = obtener_fuente(est, tam)
                        inter = int(tam * 1.3) # Interlineado automático
                        # Envoltura de texto basada en píxeles respetando saltos manuales
                        lineas = []
                        for parrafo in texto.split('\n'):
                            palabras = parrafo.split()
                            linea_actual = ""
                            for palabra in palabras:
                                test_line = linea_actual + (" " if linea_actual else "") + palabra
                                if draw.textlength(test_line, font=font) <= ancho_w:
                                    linea_actual = test_line
                                else:
                                    if linea_actual:
                                        lineas.append(linea_actual)
                                    linea_actual = palabra
                            if linea_actual:
                                lineas.append(linea_actual)
                        
                        # Ancho máximo en píxeles para usar como referencia de justificación
                        max_pixel_width = max([draw.textlength(line, font=font) for line in lineas]) if lineas else 0
                        
                        curr_y = coords[1]
                        for i, line in enumerate(lineas):
                            es_ultima_linea = (i == len(lineas) - 1)
                            
                            # La última línea no se justifica o si justificar es falso
                            if es_ultima_linea or not justificar:
                                draw.text((coords[0], curr_y), line, font=font, fill=col)
                            else:
                                palabras = line.split()
                                if len(palabras) <= 1:
                                    draw.text((coords[0], curr_y), line, font=font, fill=col)
                                else:
                                    ancho_palabras = sum([draw.textlength(p, font=font) for p in palabras])
                                    espacio_sobrante = max_pixel_width - ancho_palabras
                                    espacio_entre_palabras = espacio_sobrante / (len(palabras) - 1)
                                    
                                    curr_x = coords[0]
                                    for palabra in palabras:
                                        draw.text((curr_x, curr_y), palabra, font=font, fill=col)
                                        curr_x += draw.textlength(palabra, font=font) + espacio_entre_palabras
                                        
                            curr_y += inter

                def dibujar_linea(texto, coords, tam, col, est, alineacion="left"):
                    if tam > 0 and texto:
                        font = obtener_fuente(est, tam)
                        x, y = coords
                        
                        lineas = str(texto).split('\n')
                        # Interlineado automático (1.1 veces el tamaño de la fuente para que quede compacto pero legible)
                        interlineado = int(tam * 1.1)
                        
                        for i, linea in enumerate(lineas):
                            ancho_texto = draw.textlength(linea, font=font)
                            nx = x
                            if alineacion == "right":
                                nx -= ancho_texto
                            elif alineacion == "center":
                                nx -= ancho_texto / 2
                                
                            draw.text((nx, y + (i * interlineado)), linea, font=font, fill=col)

                # --- DIBUJO FINAL ---
                coords_base = config["coords"]
                
                # 1. Descripción (Usa valores fijos sin opciones de edición)
                final_tamano = config["tamano_fuente_desc"]
                final_ancho = config["ancho_caja_desc"]
                dibujar_parrafo(descripcion_txt, coords_base["desc"], final_tamano, "#FFFFFF", "Regular", final_ancho)
                
                # 2. Ciudad + Ajuste X e Y dinámico
                ajuste_ciu = ajustes_ciudad.get(formato, {"t": 0, "x": 0, "y": 0})
                coord_ciu_x = coords_base["ciudad"][0] + ajuste_ciu["x"]
                coord_ciu_y = coords_base["ciudad"][1] + ajuste_ciu["y"]
                tam_ciu = config.get("tamano_fuente_ciudad", 80) + ajuste_ciu["t"]
                
                dibujar_linea(municipio.upper(), (coord_ciu_x, coord_ciu_y), tam_ciu, "#cffaff", "Bold", alineacion="left")
                
                # 3. Datos fijos 
                tam_dia_base = config.get("tamano_fuente_dia", 40)
                tam_ano_base = config.get("tamano_fuente_ano", 40)
                
                tam_hora = config.get("tamano_fuente_hora", 40)
                tam_lugar = config.get("tamano_fuente_lugar", 35)
                tam_dir = config.get("tamano_fuente_direccion", 25)
                ancho_dir = config.get("ancho_caja_direccion", 800)
                tam_pub = config.get("tamano_fuente_publico", 35)
                
                final_tam_dia = tam_dia_base
                final_tam_ano = tam_ano_base
                
                # Formatos que separan día y año
                dibujar_linea(dia_txt, coords_base["dia"], final_tam_dia, "#FFFFFF", "Bold", alineacion="right")
                dibujar_linea(ano_txt, coords_base["ano"], final_tam_ano, "#FFFFFF", "Regular", alineacion="right")
                dibujar_linea(hora_txt, coords_base["hora"], tam_hora, "#FFFFFF", "Bold")
                dibujar_linea(lugar_txt, coords_base["lugar"], tam_lugar, "#2caafb", "Bold")
                dibujar_parrafo(direccion_txt, coords_base["direccion"], tam_dir, "#FFFFFF", "Regular", ancho_dir, justificar=False)
                dibujar_linea(publico_txt, coords_base["publico"], tam_pub, "#FFFFFF", "Bold")

                st.image(lienzo, use_container_width=True)
                
                buf = io.BytesIO()
                lienzo.save(buf, format="PNG", optimize=True, dpi=(150, 150))
                
                prefijo = formato.split()[0]
                nombre_archivo = f"{prefijo}_{municipio}.png" if municipio else f"{prefijo}_cnsc.png"
                
                st.download_button(
                    label=f"💾 Descargar {formato} (PNG)", 
                    data=buf.getvalue(), 
                    file_name=nombre_archivo, 
                    mime="image/png",
                    key=f"dl_{formato}"
                )
                
                st.markdown("---")
    else:
        st.info("👈 Sube la foto de la ciudad en la barra lateral para ver la previsualización.")
