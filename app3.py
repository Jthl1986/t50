import pandas as pd
import streamlit as st
import requests
import streamlit.components.v1 as components
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import feedparser
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import lxml
import plotly.graph_objects as go
import numpy as np
#from streamlit_lottie import st_lottie

st.set_page_config(page_title="AgroAppCredicoop",page_icon="🌱",layout="wide") 

arrenda = 0

#OCULTAR FUENTE GITHUB
hide_github_link = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_github_link, unsafe_allow_html=True)

def layout_centrado():
    st.markdown("""
        <style>
            /* Apuntamos al contenedor principal */
            .main .block-container {
                max-width: 800px !important;
                /* Agregamos padding arriba para que no se "coma" el contenido */
                padding-top: 5rem !important; 
                padding-bottom: 5rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            /* Esto asegura que el header de Streamlit (donde está el menú) 
               no tape el título de tu app */
            [data-testid="stHeader"] {
                background: rgba(0,0,0,0);
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

#PARA ABRIR GOOGLEMAPS
def abrir_google_maps():
    # Coordenadas de ejemplo (puedes cambiarlas por las que necesites)
    latitud = -34.62125
    longitud = -58.42810
    url_maps = f"https://www.google.com/maps?q={latitud},{longitud}"

    # Enlace a Google Maps
    st.write(f"[Google Maps]({url_maps})")

    
def css():
    # CSS to inject contained in a string
    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

#LOTTIE
#def load_lottieurl(url: str):
#    r = requests.get(url)
#    if r.status_code != 200:
#        return None
#    return r.json()

#VALORES DE MANTENIMIENTO
valorminc = 75700 #valor minimo cosecha
valormaxc = 122000 #valor maximo cosecha
valors = 60000 #valor referencia siembra

#CARGA RINDES HISTÓRICOS
url = "https://raw.githubusercontent.com/Jthl1986/T1/main/Estimaciones11.csv"
dfr = pd.read_csv(url, encoding='ISO-8859-1', sep=';')


# VALUACION HACIENDA
def app():
    st.title("🐮 Valuación de hacienda")
    left, right = st.columns(2)
    left.write("Completar:")
    form = left.form("template_form")
    tipo = form.selectbox('Ingrese tipo de hacienda: ', ["Ternero             ", "Novillito       ", "Ternera             ", "Vaquillona        ", "Vaca                "])
    cantidad = form.number_input("Ingrese cantidad de cabezas: ", step=1)
    peso = form.number_input("Ingrese peso: ", step=1)
    submit = form.form_submit_button("Ingresar")
    df=pd.read_html('https://www.monasterio-tattersall.com/precios-hacienda') #leo la tabla de la página
    hacienda = df[0] 
    categoria = hacienda.Categoría 
    promedio = hacienda.Promedio
    tabla = pd.DataFrame({'categoria':categoria,'promedio':promedio}) #creo un dataframe con categoria y promedio
    ternero=tabla[0:6] 
    novillito=tabla[7:11]
    ternera=tabla[13:18]
    vaquillona=tabla[18:21]
    vaca=tabla[36:37]  
    fecha= "Semana: 26/01/2026 al 02/01/2026" #(tabla[37:38].values)[0][0] #el predeterminado es 25:26 #"Semana: 09/06/2025 al 13/06/2025"
    ternero160=int(ternero.promedio[2][2:6])
    ternero180=int(ternero.promedio[3][2:6])
    ternero200=int(ternero.promedio[4][2:6])
    ternero230=int(ternero.promedio[5][2:6])
    novillo260=int(novillito.promedio[7][2:6])
    novillo300=int(novillito.promedio[8][2:6])
    ternera150=int(ternera.promedio[14][2:6])
    ternera170=int(ternera.promedio[15][2:6])
    ternera190=int(ternera.promedio[16][2:6])
    ternera210=int(ternera.promedio[17][2:6])
    vaquillona250=int(vaquillona.promedio[18][2:6])
    vaquillona290=int(vaquillona.promedio[18][2:6])
    vaquillona291=int(vaquillona.promedio[18][2:6])
    vacas= 982634 #int(vaca.promedio[22][2:8])
    def constructor():
        def valores():
            if tipo == 'Ternero             ' and peso < 160:
                valor = ternero160*cantidad*peso
            elif tipo == 'Ternero             ' and peso < 180:
                valor = ternero180*cantidad*peso
            elif tipo == 'Ternero             ' and peso <= 200:
                valor = ternero200*cantidad*peso
            elif tipo == 'Ternero             ' and peso > 200:
                valor = ternero230*cantidad*peso
            elif tipo == 'Ternero             ' and peso == 0:
                valor = ternero200*cantidad*peso
            elif tipo == 'Novillito       ' and peso < 260:
                valor = novillo260*cantidad*peso
            elif tipo == 'Novillito       ' and peso <= 300:
                valor = novillo300*cantidad*peso
            elif tipo == 'Novillito       ' and peso > 300:
                valor = novillo300*cantidad*peso
            elif tipo == 'Novillito       ' and peso == 0:
                valor = novillo300*cantidad*peso
            elif tipo == 'Ternera             ' and peso < 150:
                valor = ternera150*cantidad*peso
            elif tipo == 'Ternera             ' and peso < 170:
                valor = ternera170*cantidad*peso
            elif tipo == 'Ternera             ' and peso <= 190:
                valor = ternera190*cantidad*peso
            elif tipo == 'Ternera             ' and peso > 190:
                valor = ternera210*cantidad*peso
            elif tipo == 'Ternera             ' and peso == 0:
                valor = ternera190*cantidad*peso
            elif tipo == 'Vaquillona        ' and peso < 250:
                valor = vaquillona250*cantidad*peso
            elif tipo == 'Vaquillona        ' and peso <= 290:
                valor = vaquillona290*cantidad*peso
            elif tipo == 'Vaquillona        ' and peso > 290:
                valor = vaquillona291*cantidad*peso
            elif tipo == 'Vaquillona        ' and peso == 0:
                valor = vaquillona290*cantidad*peso
            elif tipo == 'Vaca                ':
                valor = vacas*cantidad
            valor = int(valor*0.9) #ESTAMOS CASTIGANDO 10% EL VALOR DE ESTIMACIÓN
            return valor #valor de ajuste
        valor=valores()
        d = [tipo, cantidad, peso, valor]
        return d
    metalista=[]
    if "dfa" not in st.session_state:
        st.session_state.dfa = pd.DataFrame(columns=("Categoría", "Cantidad", "Peso", "Valuación"))
    if submit:
        metalista.append(constructor())
        dfb = pd.DataFrame(metalista, columns=("Categoría", "Cantidad", "Peso", "Valuación"))
        st.session_state.dfa = pd.concat([st.session_state.dfa, dfb])
    css()
    valuacion_total = st.session_state.dfa['Valuación'].sum()
    right.metric('La valuación total de hacienda es: ', '${:,}'.format(valuacion_total))

    del_button = right.button("Borrar última fila")
    if del_button and len(st.session_state.dfa) > 0:
        st.session_state.dfa = st.session_state.dfa.iloc[:-1]

    right.write("Tabla para copiar:")
    right.table(st.session_state.dfa.style.format({"Cantidad":"{:.0f}", "Peso":"{:.0f}", "Valuación":"${:,}","RindeProm":"{:.2f}"}))
    right.write(f'Los precios considerados son de la {fecha}')
    promedios = pd.DataFrame(
        {'Categoria': ['Ternero', 'Novillo', 'Ternera', 'Vaquillonas'],
         'Peso': ['180', '260', '170','250']})
    st.write('Pesos promedio para tipo de hacienda (en caso que no se informe el peso). En vacas poner peso cero')
    st.table(promedios.assign(hack='').set_index('hack'))

#COTIZACIONES GRANOS
# URL de la página web que contiene los datos
url = "https://www.ggsa.com.ar/get_pizarra/"

# Realizar la solicitud HTTP para obtener el contenido JSON
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
response = requests.get(url, verify=False)

# Verificar si la solicitud fue exitosa (código 200)
if response.status_code == 200:
    # Obtener el contenido JSON de la respuesta
    data = response.json()

    # Extraer los valores para Rosario y los nombres de los cultivos
    pizarra_data = data["pizarra"][0]
    cultivos = ["trigo", "soja", "maiz", "girasol", "sorgo"]
    valores_rosario = {}

    # Verificar si el valor de Rosario es "0.00" y usar el valor estimativo en su lugar
    for cultivo in cultivos:
        valor_rosario = pizarra_data[cultivo]["rosario"]
        valor_estimativo = pizarra_data[cultivo]["estimativo"]

        if valor_rosario == "0.00":
            valores_rosario["pp" + cultivo] = float(valor_estimativo)
        else:
            valores_rosario["pp" + cultivo] = float(valor_rosario)

# Extraer la fecha
fecha1 = "11/04/2024" #pizarra_data["fecha"]#  #   Sacar fecha y numeral y tabular

# Asignar los valores a las variables con los nombres personalizados
pptrigo = 258800 #valores_rosario["pptrigo"]    
ppsoja = 430500 #valores_rosario["ppsoja"]     
ppmaiz = 251300 #valores_rosario["ppmaiz"]     
ppgirasol = 535225 #valores_rosario["ppgirasol"] 
ppsorgo = 257450 #valores_rosario["ppsorgo"]     


def app1():
    fecha = fecha1
    st.title("🌾 Valuación de granos")
    st.write(f'Precios de pizarra del Mercado de Rosario al {fecha}')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Soja", '${:,}'.format(int(ppsoja)))
    col2.metric("Trigo", '${:,}'.format(int(pptrigo)))
    col3.metric("Maíz", '${:,}'.format(int(ppmaiz)))
    col4.metric("Sorgo", '${:,}'.format(int(ppsorgo)))
    col5.metric("Girasol",'${:,}'.format(int(ppgirasol)))
    left, right = st.columns(2)
    left.write("Completar:")
    form = left.form("template_form")
    tipo = form.selectbox('Ingrese tipo de grano: ', ["Soja","Trigo","Maíz","Sorgo","Girasol"])
    cantidad = form.number_input("Ingrese toneladas: ", step=1)
    submit = form.form_submit_button("Ingresar")
    def lista():
        def valor():
            if tipo == "Soja":
                precio = ppsoja
            elif tipo == "Trigo":
                precio = pptrigo
            elif tipo == "Maíz":
                precio = ppmaiz
            elif tipo == "Sorgo":
                precio = ppsorgo
            else:
                precio = ppgirasol
            return int(cantidad*precio)
        valor = valor()
        lista = [tipo, cantidad, valor]
        return lista
    cereales=[]
    if "dfs" not in st.session_state:
        st.session_state.dfs = pd.DataFrame(columns=("Tipo grano", "Cantidad (tn)", "Valuación"))
    if submit:
        cereales.append(lista())
        dfd = pd.DataFrame(cereales, columns=("Tipo grano", "Cantidad (tn)", "Valuación"))
        st.session_state.dfs = pd.concat([st.session_state.dfs, dfd])
    css()
    valuacion_total = st.session_state.dfs['Valuación'].sum()
    right.metric('La valuación total de granos es: ', '${:,}'.format(valuacion_total))
    del_button = right.button("Borrar última fila")
    if del_button and len(st.session_state.dfs) > 0:
        st.session_state.dfs = st.session_state.dfs.iloc[:-1]
    right.write("Tabla para copiar:")
    right.table(st.session_state.dfs.style.format({"Cantidad (tn)":"{:.0f}", "Valuación":"${:,}"}))

def app2():
    if "ingresos_totales1" not in st.session_state:
        st.session_state["ingresos_totales1"] = 0
    st.title("🚜 Servicios agrícolas")
    left, right = st.columns(2)
    left.write("Completar:")
    form = left.form("template_form")
    tipo = form.selectbox('Ingrese tipo de servicio: ', ["Cosecha","Siembra","Pulverización","Laboreos"])
    valormins = valors*0.50 #valor minimo siembra
    valormaxs = valors*1.50 #valor maximo siembra
    cantidad = form.number_input("Ingrese superficie (has): ", step=1)
    precio = form.number_input("Ingrese precio por ha", step=1)
    submit = form.form_submit_button("Ingresar")
    
    def lista():
        def valor():
            return cantidad*precio
        valor = valor()
        lista = [tipo, cantidad, precio, valor]
        return lista
    servagro=[]
    if "dfx" not in st.session_state:
        st.session_state.dfx = pd.DataFrame(columns=("Categoría", "Superficie(ha)", "Precio", "Ingreso estimado"))
    if submit:
        servagro.append(lista())
        st.session_state["ingresos_totales1"] += cantidad*precio
        dfy = pd.DataFrame(servagro, columns=("Categoría", "Superficie(ha)", "Precio", "Ingreso estimado"))
        st.session_state.dfx = pd.concat([st.session_state.dfx, dfy])
        if tipo == 'Cosecha' and (precio > valormaxc or precio < valorminc):
            st.warning("ALERTA! El precio por ha de cosecha cargado esta fuera de los promedios de mercado. Ver precios de referencia abajo")
        elif tipo == 'Siembra' and (precio > valormaxs or precio < valormins):
            st.warning("ALERTA! El precio por ha de siembra cargado esta fuera de los promedios de mercado. Ver precios de referencia abajo")
        else:
            pass
    
    right.metric('Los ingresos totales por servicios agrícolas son: ', "${:,}".format(st.session_state["ingresos_totales1"]))    

    delete_last_row = right.button("Borrar última fila")
    if delete_last_row:
        if not st.session_state.dfx.empty:
            st.session_state["ingresos_totales1"] -= st.session_state.dfx["Ingreso estimado"].iloc[-1]
            st.session_state.dfx = st.session_state.dfx.iloc[:-1]
    css()
    
    right.write("Tabla para copiar:")
    right.table(st.session_state.dfx.style.format({"Superficie(ha)":"{:.0f}", "Precio":"${:,}", "Ingreso estimado":"${:,}"}))
    
    facmalink = "http://www.facma.com.ar"
    st.markdown(f"**[Precios de referencia Cosecha - Siembra]({facmalink})**")
    
    return st.session_state.dfx
    
def app3():
    """Riesgo climático"""
    st.title("⛅️ Riesgo climático - Evolución campaña")

    # Código HTML para embed de Tableau
    tableau_html = """
    <div class='tableauPlaceholder' id='viz1740438454339' style='position: relative'>
    <noscript>
    <a href='#'>
    <img alt='Dashboard 1' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Es&#47;EstadoyHumedaddelosCultivos&#47;Dashboard1&#47;1_rss.png' style='border: none' />
    </a>
    </noscript>
    <object class='tableauViz' style='display:none;'>
    <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
    <param name='embed_code_version' value='3' />
    <param name='site_root' value='' />
    <param name='name' value='EstadoyHumedaddelosCultivos&#47;Dashboard1' />
    <param name='tabs' value='no' />
    <param name='toolbar' value='yes' />
    <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Es&#47;EstadoyHumedaddelosCultivos&#47;Dashboard1&#47;1.png' />
    <param name='animate_transition' value='yes' />
    <param name='display_static_image' value='yes' />
    <param name='display_spinner' value='yes' />
    <param name='display_overlay' value='yes' />
    <param name='display_count' value='yes' />
    <param name='language' value='es-ES' />
    </object>
    </div>
    <script type='text/javascript'>
    var divElement = document.getElementById('viz1740438454339');
    var vizElement = divElement.getElementsByTagName('object')[0];
    if (divElement.offsetWidth > 800) {
    vizElement.style.width='1300px';
    vizElement.style.height='827px';
    } else if (divElement.offsetWidth > 500) {
    vizElement.style.width='1300px';
    vizElement.style.height='827px';
    } else {
    vizElement.style.width='100%';
    vizElement.style.height='727px';
    }
    var scriptElement = document.createElement('script');
    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
    vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
    """

    # Mostrar el dashboard
    components.html(tableau_html, height=850)


# Variable global para almacenar departamento_seleccionado
departamento_seleccionado = None

if 'tipo_seleccionado' not in st.session_state:
    st.session_state.tipo_seleccionado = "Soja 1ra"  # Valor inicial

if 'tipo_cultivo_form' not in st.session_state:
    st.session_state.tipo_cultivo_form = "Soja 1ra" 

def app4():
    
    # Estilo CSS para ajustar el margen superior de toda la página
    st.markdown(
        """
        <style>
            .block-container {
                margin-top: -80px;
            }
            
            .st-emotion-cache-6qob1r.eczjsme3 {
                padding-top: 80px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Mensajes personalizados
    # URL del archivo JSON
    url_archivo = 'https://raw.githubusercontent.com/Jthl1986/T1/master/mensaje.json'
    
    # Realizar la solicitud HTTP para descargar el archivo
    response = requests.get(url_archivo)
    
    # Verificar si la solicitud fue exitosa (código de respuesta 200)
    if response.status_code == 200:
        # Cargar el contenido JSON desde la respuesta
        contenido_json = response.json()
    
        # Inicializar la cadena HTML una sola vez
        mensajes_html = '<div style="padding-top: 20px;"><marquee behavior="scroll" direction="left" scrollamount="6">'
    
        # Iterar sobre los mensajes en el JSON y agregarlos a la cadena HTML
        for i, mensaje_info in enumerate(contenido_json):
            # Obtener el valor asociado a la clave "mensaje"
            mensaje = mensaje_info.get("mensaje", "")
    
            # Obtener el valor asociado a la clave "enlace" o establecer enlace como None si no existe
            enlace = mensaje_info.get("enlace", None)
    
            # Agregar el mensaje al HTML con o sin enlace y la separación entre mensajes
            if enlace:
                mensajes_html += f'<a href="{enlace}" target="_blank">{mensaje}</a>'
            else:
                mensajes_html += mensaje
    
            # Agregar la separación si no es el último mensaje
            if i < len(contenido_json) - 1:
                mensajes_html += ' - '
    
        # Cerrar la etiqueta marquee y div
        mensajes_html += '</marquee></div>'
    
        # Mostrar el HTML en Streamlit
        st.components.v1.html(mensajes_html, height=50)
    else:
        print(f"No se pudo acceder al archivo JSON. Código de estado: {response.status_code}")
    
    st.title("🌽 Planteo productivo")
    left, center, right = st.columns(3)

#API TIPO DE CAMBIO
    url = "https://dolarapi.com/v1/dolares/mayorista"
    response = requests.get(url)
    if response.status_code == 200:
      api_data = response.json()
      value = api_data['venta']
      dol = value
    else:
       dol = 1401  # Valor por defecto en caso de fallo
       print("Failed to retrieve data")
    
    #dol = float(1401) #En caso de fallas sacar el numero del principio de la línea
    left.metric("Dolar mayorista", '${:,}'.format(float(dol)))
     
#SELECCIÓN DEPARTAMENTE Y PROVINCIA (INICIALIZACION)
    if 'provincia_seleccionada' not in st.session_state:
        st.session_state.provincia_seleccionada = None    
    if 'departamento_seleccionado' not in st.session_state:
        st.session_state.departamento_seleccionado = None    
    url = "https://raw.githubusercontent.com/Jthl1986/T1/main/Estimaciones8.csv"
    dfr = pd.read_csv(url, encoding='ISO-8859-1', sep=',')

    mapeo_cultivos_csv = {
    "Trigo": "Trigo total",
    "Maíz": "Maíz",
    "Soja 1ra": "Soja 1ra",
    "Soja 2da": "Soja 2da",
    "Girasol": "Girasol",
    "Sorgo": "Sorgo",
    "Cebada": "Cebada"}

    # Obtener las provincias únicas
    provincias = dfr['Provincia'].unique()    
    # Interfaz de usuario
    st.session_state.provincia_seleccionada = left.selectbox("Provincia", provincias)
    # Filtrar departamentos según la provincia seleccionada
    departamentos_provincia = dfr.loc[dfr['Provincia'] == st.session_state.provincia_seleccionada, 'Departamento'].unique()
    # Si st.session_state.departamento_seleccionado no está en departamentos_provincia, seleccionar el primer elemento por defecto
    if st.session_state.departamento_seleccionado not in departamentos_provincia:
        st.session_state.departamento_seleccionado = departamentos_provincia[0]
    st.session_state.departamento_seleccionado = left.selectbox("Departamento", departamentos_provincia, index=departamentos_provincia.tolist().index(st.session_state.departamento_seleccionado))

#SEGMENTACION DE ZONAS    
    nucleo_norte = ["MARCOS JUAREZ","UNION","DIAMANTE", "VICTORIA", "BELGRANO", "CASEROS", "IRIONDO", "ROSARIO", "SAN JERONIMO", "SAN LORENZO", "SAN MARTIN"]
    nucleo_sur = ["ALBERTI", "ARRECIFES", "BARADERO", "BRAGADO", "CAMPANA", "CAPITAN SARMIENTO", "CARMEN DE ARECO", "CHACABUCO", "CHIVILCOY", "COLON", "EXALTACION DE LA CRUZ", "GENERAL ARENALES", "GENERAL RODRIGUEZ", "JUNIN", "LEANDRO N. ALEM", "LUJAN", "MARCOS PAZ", "MERCEDES", "PERGAMINO", "PILAR", "RAMALLO", "ROJAS", "SALTO", "SAN ANDRES DE GILES", "SAN ANTONIO DE ARECO", "SAN NICOLAS", "SAN PEDRO", "SUIPACHA", "ZARATE", "CONSTITUCION", "GENERAL LOPEZ"]
    oeste_baires = ["9 DE JULIO", "CARLOS CASARES", "CARLOS TEJEDOR", "FLORENTINO AMEGHINO", "GENERAL PINTO", "GENERAL VIAMONTE", "GENERAL VILLEGAS", "LINCOLN", "PEHUAJO", "PELLEGRINI", "RIVADAVIA", "TRENQUE LAUQUEN","CATRILO","CHAPALEUFU", "CONHELO", "MARACO","QUEMU QUEMU","RANCUL","REALICO","TRENEL"]
    so_baires = ["BAHIA BLANCA", "CORONEL DE MARINA L ROSALES", "CORONEL SUAREZ","GENERAL LA MADRID","GUAMINI","PATAGONES","PUAN","SAAVEDRA","SALLIQUELO", "TORNQUIST","TRES LOMAS","VILLARINO","ATREUCO","CALEU CALEU","CAPITAL","GUATRACHE","HUCAL","LIHUEL CALEL","LOVENTUE","TOAY","UTRACAN","ADOLFO ALSINA"]
    se_baires = ["ADOLFO GONZALES CHAVES","BALCARCE","BENITO JUAREZ","CORONEL DORREGO","CORONEL PRINGLES","GENERAL ALVARADO","GENERAL PUEYRREDON","LAPRIDA","LOBERIA","MAR CHIQUITA","MONTE HERMOSO","NECOCHEA","SAN CAYETANO","TANDIL","TRES ARROYOS"]
    centro_baires = ["25 DE MAYO","AYACUCHO","AZUL","BOLIVAR","DAIREAUX","GENERAL ALVEAR","HIPOLITO YRIGOYEN","LAS FLORES","NAVARRO","OLAVARRIA","RAUCH","ROQUE PEREZ","SALADILLO","TAPALQUE"]
    cuenca_salado = ["BRANDSEN","CANUELAS","CASTELLI","CHASCOMUS","DOLORES","GENERAL BELGRANO","GENERAL GUIDO","GENERAL JUAN MADARIAGA","GENERAL LAS HERAS","GENERAL LAVALLE","GENERAL PAZ","LA COSTA","LA PLATA","LEZAMA","LOBOS","MAGDALENA","MAIPU","MONTE","PILA","PUNTA INDIO","SAN VICENTE","TORDILLO","VILLA GESELL"]
    sur_cordoba = ["GENERAL ROCA","JUAREZ CELMAN","PRESIDENTE ROQUE SAENZ PENA", "RIO CUARTO"]
    centronorte_cba = ["CALAMUCHITA","CAPITAL","COLON", "CRUZ DEL EJE","GENERAL SAN MARTIN", "ISCHILIN","MINAS","POCHO","PUNILLA","RIO PRIMERO","RIO SECO","RIO SEGUNDO","SAN ALBERTO","SAN JAVIER","SAN JUSTO","SANTA MARIA","SOBREMONTE","TERCERO ARRIBA","TOTORAL","TULUMBA"]
    santafe_centro = ["CASTELLANOS","GARAY","LA CAPITAL","LAS COLONIAS","SAN JUSTO"]
    santafe_norte = ["9 DE JULIO","GENERAL OBLIGADO","SAN CRISTOBAL", "SAN JAVIER", "VERA"]
    nea_oeste=["AGUIRRE","ALBERDI","ATAMISQUI","AVELLANEDA","BELGRANO","COPO","GENERAL TABOADA","JUAN F. IBARRA","MITRE","MORENO","RIVADAVIA"]
    noa = ["AMBASTO","ANCASTI","CAPAYAN","CAPITAL","EL ALTO","FRAY MAMERTO ESQUIU","LA PAZ","PACLIN","SANTA ROSA","VALLE VIEJO","DR. MANUEL BELGRANO","EL CARMEN","HUMAHUACA","LEDESMA","PALPALA","SAN ANTONIO","SAN PEDRO","SANTA BARBARA","TILCARA","TUMBAYA","VALLE GRANDE","GENERAL SAN MARTIN","ANTA","CACHI","CAPITAL","CERRILLOS","CHICOANA","GENERAL GUEMES","GENERAL JOSE DE SAN MARTIN","GUACHIPAS","IRUYA","LA CALDERA","LA CANDELARIA","LA VINA","METAN","ORAN","RIVADAVIA","ROSARIO DE LA FRONTERA","ROSARIO DE LERMA","SANTA VICTORIA","BANDA","CAPITAL","CHOYA","FIGUEROA","GUASAYAN","JIMENEZ","LORETO","OJO DE AGUA","PELLEGRINI","RIO HONDO","ROBLES","SAN MARTIN","SARMIENTO","SILIPICA","BURRUYACU","CAPITAL","CHICLIGASTA","CRUZ ALTA","FAMAILLA","GRANEROS","JUAN B. ALBERDI","LA COCHA","LEALES","LULES","MONTEROS","RIO CHICO","SIMOCA","TAFI DEL VALLE","TAFI VIEJO","TRANCAS","YERBA BUENA"]
    nea_este=["CHACO","FORMOSA"]
    
#AGRUPAMIENTO PROVINCIAS POR ZONA
    nnorte = ["CORDOBA","SANTA FE","ENTRE RIOS"]  
    nsur = ["BUENOS AIRES","SANTA FE"]
    obaires = ["LA PAMPA","BUENOS AIRES"] #Obaires, Sobaires
    baires = ["BUENOS AIRES"] #Sebaires,, Cenbaires, Salado
    cord = ["CORDOBA"] #Sur y Centro Cba
    stafe = ["SANTA FE"]#Santa Fe centro y norte
    neaoeste = ["SANTIAGO DEL ESTERO"]
    noap = ["CATAMARCA","JUJUY","LA RIOJA","SALTA","SANTIAGO DEL ESTERO", "TUCUMAN"]
    
    if st.session_state.provincia_seleccionada in nea_este:
        region = "NEA Este"
    elif st.session_state.provincia_seleccionada == "SAN LUIS":
        region = "San Luis"
    elif st.session_state.provincia_seleccionada == "ENTRE RIOS":
        region = "Centro Este Entre Rios"        
    elif st.session_state.departamento_seleccionado in nucleo_norte and st.session_state.provincia_seleccionada in nnorte:
        region = "Zona Nucleo Norte"
    elif st.session_state.departamento_seleccionado in nucleo_sur and st.session_state.provincia_seleccionada in nsur:
        region = "Zona Nucleo Sur"
    elif st.session_state.departamento_seleccionado in oeste_baires and st.session_state.provincia_seleccionada in obaires:
        region = "Oeste Bs As - N La Pampa"
    elif st.session_state.departamento_seleccionado in so_baires and st.session_state.provincia_seleccionada in obaires:
        region = "SO Bs As - S La Pampa"
    elif st.session_state.departamento_seleccionado in se_baires and st.session_state.provincia_seleccionada in baires:
        region = "SE Bs As"
    elif st.session_state.departamento_seleccionado in centro_baires and st.session_state.provincia_seleccionada in baires:
        region = "Centro Bs As"
    elif st.session_state.departamento_seleccionado in cuenca_salado and st.session_state.provincia_seleccionada in baires:
        region = "Cuenca Salado"
    elif st.session_state.departamento_seleccionado in sur_cordoba and st.session_state.provincia_seleccionada in cord:
            region = "Sur Cordoba"
    elif st.session_state.departamento_seleccionado in centronorte_cba and st.session_state.provincia_seleccionada in cord:
            region = "Centro Norte Cordoba"
    elif st.session_state.departamento_seleccionado in santafe_centro and st.session_state.provincia_seleccionada in stafe:
            region = "Santa Fe Centro"
    elif st.session_state.departamento_seleccionado in santafe_norte and st.session_state.provincia_seleccionada in stafe:
            region = "Santa Fe Norte"
    elif st.session_state.departamento_seleccionado in nea_oeste and st.session_state.provincia_seleccionada in neaoeste:
            region = "NEA Oeste"
    elif st.session_state.departamento_seleccionado in noa and st.session_state.provincia_seleccionada in noap:
            region = "NOA"
        
    left.markdown(f"Corresponde a **{region}**")

          
        
#RINDE AUTOMATICO
    # RINDE AUTOMATICO - Versión que calcula 5 escenarios
    def rindeautomatico(tipo):
        cultivo_csv = mapeo_cultivos_csv.get(tipo, tipo)
        
        # Filtrar el DataFrame según las selecciones del usuario
        filtro_provincia = (dfr['Provincia'] == st.session_state.provincia_seleccionada)
        filtro_departamento = (dfr['Departamento'] == st.session_state.departamento_seleccionado)
        filtro_cultivos = (dfr['Cultivo'] == cultivo_csv)  # Usar cultivo_csv en vez de tipo
        df_filtrado = dfr[filtro_provincia & filtro_departamento & filtro_cultivos]
        
        # Verificar si hay datos suficientes para calcular escenarios
        rendimientos = df_filtrado['Rendimiento'].astype(float).tolist()
        
        if len(rendimientos) >= 5:
            import numpy as np
            rendimientos = np.array(rendimientos)
            
            # Calcular percentiles para 5 escenarios
            p10 = np.percentile(rendimientos, 10)
            p25 = np.percentile(rendimientos, 25)
            p50 = np.percentile(rendimientos, 50)  # Mediana
            p75 = np.percentile(rendimientos, 75)
            p90 = np.percentile(rendimientos, 90)
            p95 = np.percentile(rendimientos, 95)
            
            # Calcular los 5 rindes:
            # 1. Muy bajo: promedio hasta el percentil 10
            rendimientos_muy_bajos = rendimientos[rendimientos <= p10]
            muy_bajo = rendimientos_muy_bajos.mean() if len(rendimientos_muy_bajos) > 0 else p10
            
            # 2. Bajo: promedio entre P10 y P25
            rendimientos_bajos = rendimientos[(rendimientos > p10) & (rendimientos <= p25)]
            bajo = rendimientos_bajos.mean() if len(rendimientos_bajos) > 0 else p25
            
            # 3. Normal: promedio entre P25 y P75
            rendimientos_normales = rendimientos[(rendimientos > p25) & (rendimientos <= p75)]
            normal = rendimientos_normales.mean() if len(rendimientos_normales) > 0 else p50
            
            # 4. Alto: promedio entre P75 y P90
            rendimientos_altos = rendimientos[(rendimientos > p75) & (rendimientos < p90)]
            alto = rendimientos_altos.mean() if len(rendimientos_altos) > 0 else p75
            
            # 5. Muy alto: promedio después del percentil 90
            rendimientos_muy_altos = rendimientos[rendimientos >= p90]
            muy_alto = rendimientos_muy_altos.mean() if len(rendimientos_muy_altos) > 0 else p90
            
            # Convertir a tn/ha y redondear
            return {
                'muy_bajo': round(muy_bajo / 1000, 2),
                'bajo': round(bajo / 1000, 2),
                'normal': round(normal / 1000, 2),
                'alto': round(alto / 1000, 2),
                'muy_alto': round(muy_alto / 1000, 2)
            }
        else:
            # Si no hay suficientes datos, calcular estimaciones
            if not df_filtrado.empty:
                promedio = df_filtrado['Rendimiento'].mean()
                promedio_tn = round(promedio / 1000, 2)
                return {
                    'muy_bajo': promedio_tn * 0.7,
                    'bajo': promedio_tn * 0.85,
                    'normal': promedio_tn,
                    'alto': promedio_tn * 1.15,
                    'muy_alto': promedio_tn * 1.3
                }
            else:
                return {
                    'muy_bajo': 0,
                    'bajo': 0,
                    'normal': 0,
                    'alto': 0,
                    'muy_alto': 0
                }
      
#LECTURA VARIABLES
    df = pd.read_csv('https://raw.githubusercontent.com/Jthl1986/T1/main/variablessep25vf1.csv')

    # Crear un diccionario para almacenar las variables y valores
    variables_dict = {}
    
    # Iterar sobre el DataFrame y llenar el diccionario
    for _, row in df.iterrows():
        variable = row['variable']
        valor = row['valor']
    
        # Almacenar la variable y su valor en el diccionario
        variables_dict[variable] = valor    
    
    # Definir cada variable en el espacio de nombres global
    for variable, valor in variables_dict.items():
        globals()[variable] = valor    
                
    # Mapear los nombres de los cultivos a las variables correspondientes
    mapeo_cultivos_variables = {
        "Soja 1ra": "psoja1",
        "Soja 2da": "psoja2",
        "Trigo": "ptrigo",
        "Maíz": "pmaiz",
        "Girasol": "pgirasol",
        "Sorgo": "psorgo",
        "Cebada": "pcebada"}
    
    def obtener_precio(tipo):
        # Obtener el nombre de la variable correspondiente al cultivo
        variable_cultivo = mapeo_cultivos_variables.get(tipo, None)
        if variable_cultivo:
            return variables_dict.get(variable_cultivo, "Cultivo no encontrado en la lista")
        else:
            return "Cultivo no encontrado en la lista"
    
#LECTURA DE RINDES
    rind = {}
    for variable in list(variables_dict.keys())[245:355]:
        rind[variable] = variables_dict[variable]
        
    rind_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": rtrigo1, "Maíz": rmaiz1, "Soja 1ra": rsoja11, "Soja 2da": rsoja21, "Girasol":rgirasol1 , "Cebada": rcebada1, "Sorgo": rsorgo1},
        "Zona Nucleo Sur" : {"Trigo": rtrigo2, "Maíz": rmaiz2, "Soja 1ra": rsoja12, "Soja 2da": rsoja22, "Girasol":rgirasol2 , "Cebada": rcebada2, "Sorgo": rsorgo2},
        "Oeste Bs As - N La Pampa" : {"Trigo": rtrigo3, "Maíz": rmaiz3, "Soja 1ra": rsoja13, "Soja 2da": rsoja23, "Girasol":rgirasol3, "Cebada": rcebada3, "Sorgo": rsorgo3},
        "SO Bs As - S La Pampa" : {"Trigo": rtrigo4, "Maíz": rmaiz4, "Soja 1ra": rsoja14, "Soja 2da": rsoja24, "Girasol":rgirasol4, "Cebada": rcebada4, "Sorgo": rsorgo4},
        "SE Bs As" : {"Trigo": rtrigo5, "Maíz": rmaiz5, "Soja 1ra": rsoja15, "Soja 2da": rsoja25, "Girasol":rgirasol5, "Cebada": rcebada5, "Sorgo": rsorgo5},
        "Centro Bs As" : {"Trigo": rtrigo6, "Maíz": rmaiz6, "Soja 1ra": rsoja16, "Soja 2da": rsoja26, "Girasol":rgirasol6, "Cebada": rcebada6, "Sorgo": rsorgo6},
        "Cuenca Salado" : {"Trigo": rtrigo7, "Maíz": rmaiz7, "Soja 1ra": rsoja17, "Soja 2da": rsoja27, "Girasol":rgirasol7, "Cebada": rcebada7, "Sorgo": rsorgo7},
        "Sur Cordoba" : {"Trigo": rtrigo8, "Maíz": rmaiz8, "Soja 1ra": rsoja18, "Soja 2da": rsoja28, "Girasol":rgirasol8, "Cebada": rcebada8, "Sorgo": rsorgo8},
        "Centro Norte Cordoba" : {"Trigo": rtrigo9, "Maíz": rmaiz9, "Soja 1ra": rsoja19, "Soja 2da": rsoja29, "Girasol":rgirasol9, "Cebada": rcebada9, "Sorgo": rsorgo9},
        "Santa Fe Centro" : {"Trigo": rtrigo10, "Maíz": rmaiz10, "Soja 1ra": rsoja110, "Soja 2da": rsoja210, "Girasol":rgirasol10, "Cebada": rcebada10, "Sorgo": rsorgo11},
        "Santa Fe Norte" : {"Trigo": rtrigo11, "Maíz": rmaiz11, "Soja 1ra": rsoja111, "Soja 2da": rsoja211, "Girasol":rgirasol11, "Sorgo": rsorgo11},
        "Centro Este Entre Rios" : {"Trigo": rtrigo12, "Maíz": rmaiz12, "Soja 1ra": rsoja112, "Soja 2da": rsoja212, "Girasol":rgirasol12, "Cebada": rcebada12, "Sorgo": rsorgo12},
        "NEA Oeste" : {"Trigo": rtrigo13, "Maíz": rmaiz13, "Soja 1ra": rsoja113, "Soja 2da": rsoja213, "Girasol":rgirasol13, "Cebada": rcebada13, "Sorgo": rsorgo13},
        "NEA Este" : {"Trigo": rtrigo14, "Maíz": rmaiz14, "Soja 1ra": rsoja114, "Soja 2da": rsoja214, "Girasol":rgirasol14, "Cebada": rtrigo14, "Sorgo": rsorgo14},
        "NOA" : {"Trigo": rtrigo15, "Maíz": rmaiz15, "Soja 1ra": rsoja115, "Soja 2da": rsoja215, "Girasol":rgirasol15, "Cebada": rcebada15, "Sorgo": rsorgo15},
        "San Luis" : {"Trigo": rtrigo16, "Maíz": rmaiz16, "Soja 1ra": rsoja116, "Soja 2da": rsoja216, "Girasol":rgirasol16, "Cebada": rcebada16, "Sorgo": rsorgo16},
    }
    
    # Función para obtener el gasto estructura para campo arrendado de un cultivo en una región
    def obtener_rind(region, tipo):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in rind_por_region_cultivo and tipo in rind_por_region_cultivo[region]:
            return rind_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
    
#LECTURA DE COSTOS
    costos = {}
    for variable in list(variables_dict.keys())[7:120]:
        costos[variable] = variables_dict[variable]
        
    # Crear un diccionario para almacenar los costos por región y cultivo
        costos_por_region_cultivo = {
            "Zona Nucleo Norte": {"Trigo": ctrigo1, "Maíz": cmaiz1, "Soja 1ra": csoja11, "Soja 2da": csoja21, "Girasol":cgirasol1 , "Cebada": ccebada1, "Sorgo": csorgo1},
            "Zona Nucleo Sur" : {"Trigo": ctrigo2, "Maíz": cmaiz2, "Soja 1ra": csoja12, "Soja 2da": csoja22, "Girasol":cgirasol2 , "Cebada": ccebada2, "Sorgo": csorgo2},
            "Oeste Bs As - N La Pampa" : {"Trigo": ctrigo3, "Maíz": cmaiz3, "Soja 1ra": csoja13, "Soja 2da": csoja23, "Girasol":cgirasol3, "Cebada": ccebada3, "Sorgo": csorgo3},
            "SO Bs As - S La Pampa" : {"Trigo": ctrigo4, "Maíz": cmaiz4, "Soja 1ra": csoja14, "Soja 2da": csoja24, "Girasol":cgirasol4, "Cebada": ccebada4, "Sorgo": csorgo4},
            "SE Bs As" : {"Trigo": ctrigo5, "Maíz": cmaiz5, "Soja 1ra": csoja15, "Soja 2da": csoja25, "Girasol":cgirasol5, "Cebada": ccebada5, "Sorgo": csorgo5},
            "Centro Bs As" : {"Trigo": ctrigo6, "Maíz": cmaiz6, "Soja 1ra": csoja16, "Soja 2da": csoja26, "Girasol":cgirasol6, "Cebada": ccebada6, "Sorgo": csorgo6},
            "Cuenca Salado" : {"Trigo": ctrigo7, "Maíz": cmaiz7, "Soja 1ra": csoja17, "Soja 2da": csoja27, "Girasol":cgirasol7, "Cebada": ccebada7, "Sorgo": csorgo7},
            "Sur Cordoba" : {"Trigo": ctrigo8, "Maíz": cmaiz8, "Soja 1ra": csoja18, "Soja 2da": csoja28, "Girasol":cgirasol8, "Cebada": ccebada8, "Sorgo": csorgo8},
            "Centro Norte Cordoba" : {"Trigo": ctrigo9, "Maíz": cmaiz9, "Soja 1ra": csoja19, "Soja 2da": csoja29, "Girasol":cgirasol9, "Cebada": ccebada9, "Sorgo": csorgo9},
            "Santa Fe Centro" : {"Trigo": ctrigo10, "Maíz": cmaiz10, "Soja 1ra": csoja110, "Soja 2da": csoja210, "Girasol":cgirasol10, "Cebada": ccebada10, "Sorgo": csorgo11},
            "Santa Fe Norte" : {"Trigo": ctrigo11, "Maíz": cmaiz11, "Soja 1ra": csoja111, "Soja 2da": csoja211, "Girasol":cgirasol11, "Cebada": notuse11, "Sorgo": csorgo11},
            "Centro Este Entre Rios" : {"Trigo": ctrigo12, "Maíz": cmaiz12, "Soja 1ra": csoja112, "Soja 2da": csoja212, "Girasol":cgirasol12, "Cebada": ccebada12, "Sorgo": csorgo12},
            "NEA Oeste" : {"Trigo": ctrigo13, "Maíz": cmaiz13, "Soja 1ra": csoja113, "Soja 2da": csoja213, "Girasol":cgirasol13, "Cebada": ccebada13, "Sorgo": csorgo13},
            "NEA Este" : {"Trigo": ctrigo14, "Maíz": cmaiz14, "Soja 1ra": csoja114, "Soja 2da": csoja214, "Girasol":cgirasol14, "Cebada": notuse14, "Sorgo": csorgo14},
            "NOA" : {"Trigo": ctrigo15, "Maíz": cmaiz15, "Soja 1ra": csoja115, "Soja 2da": csoja215, "Girasol":cgirasol15, "Cebada": ccebada15, "Sorgo": csorgo15},
            "San Luis" : {"Trigo": ctrigo16, "Maíz": cmaiz16, "Soja 1ra": csoja116, "Soja 2da": csoja216, "Girasol":cgirasol16, "Cebada": ccebada16, "Sorgo": csorgo16},
            } #No hay  cebada en zona 14 se asignó notuse14
    
    # Función para obtener el costo de un cultivo en una región
    def obtener_costo(region, tipo):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in costos_por_region_cultivo and tipo in costos_por_region_cultivo[region]:
            return costos_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
        
    gasvar = {}
    for variable in list(variables_dict.keys())[355:467]:
        gasvar[variable] = variables_dict[variable]
    
    gasvar_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": gasvartrigo1, "Maíz": gasvarmaiz1, "Soja 1ra": gasvarsoja11, "Soja 2da": gasvarsoja21, "Girasol":gasvargirasol1 , "Cebada": gasvarcebada1, "Sorgo": gasvarsorgo1},
        "Zona Nucleo Sur" : {"Trigo": gasvartrigo2, "Maíz": gasvarmaiz2, "Soja 1ra": gasvarsoja12, "Soja 2da": gasvarsoja22, "Girasol":gasvargirasol2 , "Cebada": gasvarcebada2, "Sorgo": gasvarsorgo2},
        "Oeste Bs As - N La Pampa" : {"Trigo": gasvartrigo3, "Maíz": gasvarmaiz3, "Soja 1ra": gasvarsoja13, "Soja 2da": gasvarsoja23, "Girasol":gasvargirasol3, "Cebada": gasvarcebada3, "Sorgo": gasvarsorgo3},
        "SO Bs As - S La Pampa" : {"Trigo": gasvartrigo4, "Maíz": gasvarmaiz4, "Soja 1ra": gasvarsoja14, "Soja 2da": gasvarsoja24, "Girasol":gasvargirasol4, "Cebada": gasvarcebada4, "Sorgo": gasvarsorgo4},
        "SE Bs As" : {"Trigo": gasvartrigo5, "Maíz": gasvarmaiz5, "Soja 1ra": gasvarsoja15, "Soja 2da": gasvarsoja25, "Girasol":gasvargirasol5, "Cebada": gasvarcebada5, "Sorgo": gasvarsorgo5},
        "Centro Bs As" : {"Trigo": gasvartrigo6, "Maíz": gasvarmaiz6, "Soja 1ra": gasvarsoja16, "Soja 2da": gasvarsoja26, "Girasol":gasvargirasol6, "Cebada": gasvarcebada6, "Sorgo": gasvarsorgo6},
        "Cuenca Salado" : {"Trigo": gasvartrigo7, "Maíz": gasvarmaiz7, "Soja 1ra": gasvarsoja17, "Soja 2da": gasvarsoja27, "Girasol":gasvargirasol7, "Cebada": gasvarcebada7, "Sorgo": gasvarsorgo7},
        "Sur Cordoba" : {"Trigo": gasvartrigo8, "Maíz": gasvarmaiz8, "Soja 1ra": gasvarsoja18, "Soja 2da": gasvarsoja28, "Girasol":gasvargirasol8, "Cebada": gasvarcebada8, "Sorgo": gasvarsorgo8},
        "Centro Norte Cordoba" : {"Trigo": gasvartrigo9, "Maíz": gasvarmaiz9, "Soja 1ra": gasvarsoja19, "Soja 2da": gasvarsoja29, "Girasol":gasvargirasol9, "Cebada": gasvarcebada9, "Sorgo": gasvarsorgo9},
        "Santa Fe Centro" : {"Trigo": gasvartrigo10, "Maíz": gasvarmaiz10, "Soja 1ra": gasvarsoja110, "Soja 2da": gasvarsoja210, "Girasol":gasvargirasol10, "Cebada": gasvarcebada10, "Sorgo": gasvarsorgo11},
        "Santa Fe Norte" : {"Trigo": gasvartrigo11, "Maíz": gasvarmaiz11, "Soja 1ra": gasvarsoja111, "Soja 2da": gasvarsoja211, "Girasol":gasvargirasol11, "Cebada": gasvarcebada11, "Sorgo": gasvarsorgo11},
        "Centro Este Entre Rios" : {"Trigo": gasvartrigo12, "Maíz": gasvarmaiz12, "Soja 1ra": gasvarsoja112, "Soja 2da": gasvarsoja212, "Girasol":gasvargirasol12, "Cebada": gasvarcebada12, "Sorgo": gasvarsorgo12},
        "NEA Oeste" : {"Trigo": gasvartrigo13, "Maíz": gasvarmaiz13, "Soja 1ra": gasvarsoja113, "Soja 2da": gasvarsoja213, "Girasol":gasvargirasol13, "Cebada": gasvarcebada13, "Sorgo": gasvarsorgo13},
        "NEA Este" : {"Trigo": gasvartrigo14, "Maíz": gasvarmaiz14, "Soja 1ra": gasvarsoja114, "Soja 2da": gasvarsoja214, "Girasol":gasvargirasol14, "Cebada": gasvarcebada14, "Sorgo": gasvarsorgo14},
        "NOA" : {"Trigo": gasvartrigo15, "Maíz": gasvarmaiz15, "Soja 1ra": gasvarsoja115, "Soja 2da": gasvarsoja215, "Girasol":gasvargirasol15, "Cebada": gasvarcebada15, "Sorgo": gasvarsorgo15},
        "San Luis" : {"Trigo": gasvartrigo16, "Maíz": gasvarmaiz16, "Soja 1ra": gasvarsoja116, "Soja 2da": gasvarsoja216, "Girasol":gasvargirasol16, "Cebada": gasvarcebada16, "Sorgo": gasvarsorgo16},
    } #No hay faltantes
    
    # Función para obtener el gasto variable de un cultivo en una región
    def obtener_gasvar(region, tipo):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in gasvar_por_region_cultivo and tipo in gasvar_por_region_cultivo[region]:
            return gasvar_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
        
###########
    #estimador gastos de estructura
    nro_hectareas = 0
    gestimado = 0
            
    gesp = {}
    for variable in list(variables_dict.keys())[467:578]:
        gesp[variable] = variables_dict[variable]
        
    gesp_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": gesptrigo1, "Maíz": gespmaiz1, "Soja 1ra": gespsoja11, "Soja 2da": gespsoja21, "Girasol":gespgirasol1 , "Cebada": gespcebada1, "Sorgo": gespsorgo1},
        "Zona Nucleo Sur" : {"Trigo": gesptrigo2, "Maíz": gespmaiz2, "Soja 1ra": gespsoja12, "Soja 2da": gespsoja22, "Girasol":gespgirasol2 , "Cebada": gespcebada2, "Sorgo": gespsorgo2},
        "Oeste Bs As - N La Pampa" : {"Trigo": gesptrigo3, "Maíz": gespmaiz3, "Soja 1ra": gespsoja13, "Soja 2da": gespsoja23, "Girasol":gespgirasol3, "Cebada": gespcebada3, "Sorgo": gespsorgo3},
        "SO Bs As - S La Pampa" : {"Trigo": gesptrigo4, "Maíz": gespmaiz4, "Soja 1ra": gespsoja14, "Soja 2da": gespsoja24, "Girasol":gespgirasol4, "Cebada": gespcebada4, "Sorgo": gespsorgo4},
        "SE Bs As" : {"Trigo": gesptrigo5, "Maíz": gespmaiz5, "Soja 1ra": gespsoja15, "Soja 2da": gespsoja25, "Girasol":gespgirasol5, "Cebada": gespcebada5, "Sorgo": gespsorgo5},
        "Centro Bs As" : {"Trigo": gesptrigo6, "Maíz": gespmaiz6, "Soja 1ra": gespsoja16, "Soja 2da": gespsoja26, "Girasol":gespgirasol6, "Cebada": gespcebada6, "Sorgo": gespsorgo6},
        "Cuenca Salado" : {"Trigo": gesptrigo7, "Maíz": gespmaiz7, "Soja 1ra": gespsoja17, "Soja 2da": gespsoja27, "Girasol":gespgirasol7, "Cebada": gespcebada7, "Sorgo": gespsorgo7},
        "Sur Cordoba" : {"Trigo": gesptrigo8, "Maíz": gespmaiz8, "Soja 1ra": gespsoja18, "Soja 2da": gespsoja28, "Girasol":gespgirasol8, "Cebada": gespcebada8, "Sorgo": gespsorgo8},
        "Centro Norte Cordoba" : {"Trigo": gesptrigo9, "Maíz": gespmaiz9, "Soja 1ra": gespsoja19, "Soja 2da": gespsoja29, "Girasol":gespgirasol9, "Cebada": gespcebada9, "Sorgo": gespsorgo9},
        "Santa Fe Centro" : {"Trigo": gesptrigo10, "Maíz": gespmaiz10, "Soja 1ra": gespsoja110, "Soja 2da": gespsoja210, "Girasol":gespgirasol10, "Cebada": gespcebada10, "Sorgo": gespsorgo11},
        "Santa Fe Norte" : {"Trigo": gesptrigo11, "Maíz": gespmaiz11, "Soja 1ra": gespsoja111, "Soja 2da": gespsoja211, "Girasol":gespgirasol11, "Cebada": gespcebada10, "Sorgo": gespsorgo11},
        "Centro Este Entre Rios" : {"Trigo": gesptrigo12, "Maíz": gespmaiz12, "Soja 1ra": gespsoja112, "Soja 2da": gespsoja212, "Girasol":gespgirasol12, "Cebada": gespcebada12, "Sorgo": gespsorgo12},
        "NEA Oeste" : {"Trigo": gesptrigo13, "Maíz": gespmaiz13, "Soja 1ra": gespsoja113, "Soja 2da": gespsoja213, "Girasol":gespgirasol13, "Cebada": gespcebada13, "Sorgo": gespsorgo13},
        "NEA Este" : {"Trigo": gesptrigo14, "Maíz": gespmaiz14, "Soja 1ra": gespsoja114, "Soja 2da": gespsoja214, "Girasol":gespgirasol14, "Cebada": gesptrigo14, "Sorgo": gespsorgo14},
        "NOA" : {"Trigo": gesptrigo15, "Maíz": gespmaiz15, "Soja 1ra": gespsoja115, "Soja 2da": gespsoja215, "Girasol":gespgirasol15, "Cebada": gespcebada15, "Sorgo": gespsorgo15},
        "San Luis" : {"Trigo": gesptrigo16, "Maíz": gespmaiz16, "Soja 1ra": gespsoja116, "Soja 2da": gespsoja216, "Girasol":gespgirasol16, "Cebada": gespcebada16, "Sorgo": gespsorgo16},
    }
    #No hay gesp de cebada en zona 14 se asignó trigo misma zona
    
    # Función para obtener el gasto variable de un cultivo en una región
    def obtener_gesp(region, tipo, cantidad):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in gesp_por_region_cultivo and tipo in gesp_por_region_cultivo[region]:
            return cantidad * gesp_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
    
    if 'gespr' not in st.session_state:
        st.session_state.gespr = []
        
    def gastos_estructura1():
        result = obtener_gesp(region, tipo, cantidad)
        result = round(result * dol, 2)
        st.session_state.gespr.append(result)


    gesa = {}
    for variable in list(variables_dict.keys())[578:585]:
        gesa[variable] = variables_dict[variable]
    
        
    gesa_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Zona Nucleo Sur" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Oeste Bs As - N La Pampa" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "SO Bs As - S La Pampa" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "SE Bs As" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Centro Bs As" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Cuenca Salado" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Sur Cordoba" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Centro Norte Cordoba" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Santa Fe Centro" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Santa Fe Norte" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "Centro Este Entre Rios" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "NEA Oeste" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "NEA Este" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "NOA" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
        "San Luis" : {"Trigo": gesatrigo, "Maíz": gesamaiz, "Soja 1ra": gesasoja1, "Soja 2da": gesasoja2, "Girasol": gesagirasol, "Cebada": gesacebada, "Sorgo": gesasorgo},
    }
    
    # Función para obtener el gasto estructura para campo arrendado de un cultivo en una región
    def obtener_gesa(region, tipo, cantidad):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in gesa_por_region_cultivo and tipo in gesa_por_region_cultivo[region]:
            return cantidad * gesa_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
    
    
    if 'gesar' not in st.session_state:
        st.session_state.gesar = []
        
    def gastos_estructura2():
        result = obtener_gesa(region, tipo, cantidad)
        result = round(result * dol, 2)
        st.session_state.gesar.append(result)

    arrend = {}
    for variable in list(variables_dict.keys())[585:]:
        arrend[variable] = variables_dict[variable]
        
    arrend_por_region_cultivo = {
        "Zona Nucleo Norte": {"Trigo": arrendtrigo1, "Maíz": arrendmaiz1, "Soja 1ra": arrendsoja11, "Soja 2da": arrendsoja21, "Girasol":arrendgirasol1 , "Cebada": arrendcebada1, "Sorgo": arrendsorgo1},
        "Zona Nucleo Sur" : {"Trigo": arrendtrigo2, "Maíz": arrendmaiz2, "Soja 1ra": arrendsoja12, "Soja 2da": arrendsoja22, "Girasol":arrendgirasol2 , "Cebada": arrendcebada2, "Sorgo": arrendsorgo2},
        "Oeste Bs As - N La Pampa" : {"Trigo": arrendtrigo3, "Maíz": arrendmaiz3, "Soja 1ra": arrendsoja13, "Soja 2da": arrendsoja23, "Girasol":arrendgirasol3, "Cebada": arrendcebada3, "Sorgo": arrendsorgo3},
        "SO Bs As - S La Pampa" : {"Trigo": arrendtrigo4, "Maíz": arrendmaiz4, "Soja 1ra": arrendsoja14, "Soja 2da": arrendsoja24, "Girasol":arrendgirasol4, "Cebada": arrendcebada4, "Sorgo": arrendsorgo4},
        "SE Bs As" : {"Trigo": arrendtrigo5, "Maíz": arrendmaiz5, "Soja 1ra": arrendsoja15, "Soja 2da": arrendsoja25, "Girasol":arrendgirasol5, "Cebada": arrendcebada5, "Sorgo": arrendsorgo5},
        "Centro Bs As" : {"Trigo": arrendtrigo6, "Maíz": arrendmaiz6, "Soja 1ra": arrendsoja16, "Soja 2da": arrendsoja26, "Girasol":arrendgirasol6, "Cebada": arrendcebada6, "Sorgo": arrendsorgo6},
        "Cuenca Salado" : {"Trigo": arrendtrigo7, "Maíz": arrendmaiz7, "Soja 1ra": arrendsoja17, "Soja 2da": arrendsoja27, "Girasol":arrendgirasol7, "Cebada": arrendcebada7, "Sorgo": arrendsorgo7},
        "Sur Cordoba" : {"Trigo": arrendtrigo8, "Maíz": arrendmaiz8, "Soja 1ra": arrendsoja18, "Soja 2da": arrendsoja28, "Girasol":arrendgirasol8, "Cebada": arrendcebada8, "Sorgo": arrendsorgo8},
        "Centro Norte Cordoba" : {"Trigo": arrendtrigo9, "Maíz": arrendmaiz9, "Soja 1ra": arrendsoja19, "Soja 2da": arrendsoja29, "Girasol":arrendgirasol9, "Cebada": arrendcebada9, "Sorgo": arrendsorgo9},
        "Santa Fe Centro" : {"Trigo": arrendtrigo10, "Maíz": arrendmaiz10, "Soja 1ra": arrendsoja110, "Soja 2da": arrendsoja210, "Girasol":arrendgirasol10, "Cebada": arrendcebada10, "Sorgo": arrendsorgo11},
        "Santa Fe Norte" : {"Trigo": arrendtrigo11, "Maíz": arrendmaiz11, "Soja 1ra": arrendsoja111, "Soja 2da": arrendsoja211, "Girasol":arrendgirasol11, "Cebada": arrendcebada11, "Sorgo": arrendsorgo11},
        "Centro Este Entre Rios" : {"Trigo": arrendtrigo12, "Maíz": arrendmaiz12, "Soja 1ra": arrendsoja112, "Soja 2da": arrendsoja212, "Girasol":arrendgirasol12, "Cebada": arrendcebada12, "Sorgo": arrendsorgo12},
        "NEA Oeste" : {"Trigo": arrendtrigo13, "Maíz": arrendmaiz13, "Soja 1ra": arrendsoja113, "Soja 2da": arrendsoja213, "Girasol":arrendgirasol13, "Cebada": arrendcebada13, "Sorgo": arrendsorgo13},
        "NEA Este" : {"Trigo": arrendtrigo14, "Maíz": arrendmaiz14, "Soja 1ra": arrendsoja114, "Soja 2da": arrendsoja214, "Girasol":arrendgirasol14, "Cebada": arrendtrigo14, "Sorgo": arrendsorgo14},
        "NOA" : {"Trigo": arrendtrigo15, "Maíz": arrendmaiz15, "Soja 1ra": arrendsoja115, "Soja 2da": arrendsoja215, "Girasol":arrendgirasol15, "Cebada": arrendcebada15, "Sorgo": arrendsorgo15},
        "San Luis" : {"Trigo": arrendtrigo16, "Maíz": arrendmaiz16, "Soja 1ra": arrendsoja116, "Soja 2da": arrendsoja216, "Girasol":arrendgirasol16, "Cebada": arrendcebada16, "Sorgo": arrendsorgo16},
    }
    
    # Función para obtener el gasto estructura para campo arrendado de un cultivo en una región
    def obtener_arrend(region, tipo, cantidad, qq_ha_override=None):
        """
        Calcula el arrendamiento con opción de sobrescribir qq/ha
        qq_ha_override: si se proporciona, usa este valor en lugar del predeterminado
        """
        if region in arrend_por_region_cultivo and tipo in arrend_por_region_cultivo[region]:
            arrend_base = arrend_por_region_cultivo[region][tipo]
            
            # Si hay un valor personalizado de qq/ha, recalcular el arrendamiento
            if qq_ha_override is not None:
                # Calcular qq/ha original
                precio_soja = variables_dict.get('psoja1', 300)  # Precio base de soja
                qq_ha_original = arrend_base / precio_soja * 10
                
                # Calcular nuevo arrendamiento con qq/ha personalizado
                arrend_modificado = (qq_ha_override * precio_soja) / 10
                return cantidad * arrend_modificado
            
            return cantidad * arrend_base
        else:
            return 0
    
    if 'arrenda' not in st.session_state:
        st.session_state.arrenda = []
        
    def arrendamiento(qq_ha_custom=None):
        resultado = obtener_arrend(region, tipo, cantidad, qq_ha_custom)
        resultado = round(resultado * dol, 2)
        st.session_state.arrenda.append(resultado)
        return resultado

    def arrendamiento_inf():
        if propio == "Propios":
            return 0
        else:
            return obtener_arrend(region, tipo, 1)
    
    def ges_inf():
        if propio == "Propios":
            return obtener_gesp(region, tipo, 1)
        else:
            return obtener_gesa(region, tipo, 1)
    
    def gc_inf():
        # Usar rinde promedio si rinde aún no está definido
        rinde_calc = rindeprom if 'rinde' not in locals() else rinde
        return gasto*precio*rinde_calc
    
    # Inicializar porcentaje de aparcería por defecto
    if 'porcentaje_aparceria' not in st.session_state:
        st.session_state.porcentaje_aparceria = 60
    
    # Inicializar diccionario de qq/ha personalizados por línea
    if 'qq_ha_personalizados' not in st.session_state:
        st.session_state.qq_ha_personalizados = {}
    
    # Contador de líneas cargadas para generar keys únicos
    if 'contador_lineas' not in st.session_state:
        st.session_state.contador_lineas = 0

############FORMULARIO DE CARGA SIMPLIFICADO      
    center.write("**Cargar cultivo:**")

    # SELECTBOX DE CULTIVO FUERA DEL FORM (actualización instantánea)
    st.session_state.tipo_cultivo_form = center.selectbox(
        'Tipo de cultivo: ', 
        ["Soja 1ra", "Soja 2da", "Trigo", "Maíz", "Girasol", "Sorgo", "Cebada"],
        key="selectbox_cultivo_instant"
    )
    tipo = st.session_state.tipo_cultivo_form
    
    # SELECTBOX DE TIPO DE CAMPO FUERA DEL FORM (actualización instantánea)
    propio = center.selectbox('Tipo de campo: ', ["Propios","Arrendados","Aparcería"], key="tipo_campo_instant")
    
    # AHORA SÍ podemos calcular valores que dependen de region y tipo
    rindeprom = round(float(obtener_rind(region, tipo)),2)
    precio = float(obtener_precio(tipo))
    costo = float(obtener_costo(region,tipo))
    gasto = float(obtener_gasvar(region,tipo))
    
    # Calcular qq/ha estimado para arrendados (fuera del form)
    qq_ha_custom = None
    if propio == "Arrendados":
        arrend_base = arrend_por_region_cultivo.get(region, {}).get(tipo, 0)
        precio_soja = variables_dict.get('psoja1', 300)
        qq_ha_estimado = arrend_base / precio_soja * 10
        
        center.markdown(f"**Arrendamiento estimado: {qq_ha_estimado:.1f} qq/ha**")
        
        modificar_qq = center.checkbox("✏️ Ajustar qq/ha para esta línea", key="modificar_qq_instant")
        
        if modificar_qq:
            qq_ha_custom = center.number_input(
                "qq/ha personalizado:",
                min_value=1.0,
                max_value=50.0,
                value=qq_ha_estimado,
                step=0.5,
                format="%.1f",
                key="qq_ha_custom_instant"
            )
    
    # MOSTRAR AJUSTE DE APARCERÍA FUERA DEL FORM
    if propio == "Aparcería":
        aparceria_input = center.number_input(
            "% Aparcería (default 60%):", 
            min_value=1, 
            max_value=100, 
            value=st.session_state.porcentaje_aparceria,
            step=1,
            key="aparceria_input_instant"
        )
        aparceria = aparceria_input / 100
    else:
        aparceria = st.session_state.porcentaje_aparceria / 100
    
    ### PARA ELIMINAR LOS BORDES DEL FORMULARIO
    st.markdown("""
        <style>
        /* Ocultar borde del form */
        div[data-testid="stForm"] {
            border: 0px !important;
            padding: 0px !important;
        }
        /* Ocultar borde interno */
        .stForm {
            border: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    form = center.form("template_form") 
    cantidad = form.number_input("Superficie (has): ", step=1)
    
    submit = form.form_submit_button("✅ Ingresar cultivo")

    # El rinde siempre es automático ahora
    on = True

#ANÁLISIS DE RENDIMIENTOS    
    with left.expander("📊 Análisis de Rendimientos"):
        cultivo_csv = mapeo_cultivos_csv.get(st.session_state.tipo_cultivo_form, st.session_state.tipo_cultivo_form)
        # Filtrar el DataFrame según las selecciones del usuario
        filtro_provincia = (dfr['Provincia'] == st.session_state.provincia_seleccionada)
        filtro_departamento = (dfr['Departamento'] == st.session_state.departamento_seleccionado)
        filtro_cultivos = (dfr['Cultivo'] == cultivo_csv)
        
        df_filtrado = dfr[filtro_provincia & filtro_departamento & filtro_cultivos]
        
        # Nueva sección para calcular y mostrar los 5 escenarios
        st.subheader("Escenarios de Rendimiento")
        
        # Calcular los escenarios usando percentiles
        rendimientos = df_filtrado['Rendimiento'].astype(float).tolist()
        
        if len(rendimientos) >= 5:
            import numpy as np
            rendimientos = np.array(rendimientos)
            
            # Calcular percentiles
            p10 = np.percentile(rendimientos, 10)
            p25 = np.percentile(rendimientos, 25)
            p75 = np.percentile(rendimientos, 75)
            p90 = np.percentile(rendimientos, 90)
            
            # Calcular los 5 rindes
            # 1. Muy bajo: promedio hasta el percentil 10
            rendimientos_muy_bajos = rendimientos[rendimientos <= p10]
            muy_bajo = rendimientos_muy_bajos.mean()/1000 if len(rendimientos_muy_bajos) > 0 else p10/1000
            
            # 2. Bajo: promedio entre P10 y P25
            rendimientos_bajos = rendimientos[(rendimientos > p10) & (rendimientos <= p25)]
            bajo = rendimientos_bajos.mean()/1000 if len(rendimientos_bajos) > 0 else p25/1000
            
            # 3. Normal: promedio entre P25 y P75
            rendimientos_normales = rendimientos[(rendimientos > p25) & (rendimientos <= p75)]
            normal = rendimientos_normales.mean()/1000 if len(rendimientos_normales) > 0 else np.median(rendimientos)/1000
            
            # 4. Alto: promedio entre P75 y P90
            rendimientos_altos = rendimientos[(rendimientos > p75) & (rendimientos <= p90)]
            alto = rendimientos_altos.mean()/1000 if len(rendimientos_altos) > 0 else p75/1000
            
            # 5. Muy alto: promedio después del percentil 90
            rendimientos_muy_altos = rendimientos[rendimientos > p90]
            muy_alto = rendimientos_muy_altos.mean()/1000 if len(rendimientos_muy_altos) > 0 else p90/1000
            
            # Crear tabla de resultados con 5 escenarios
            escenarios_data = {
                "Escenario": ["Muy Bajo", "Bajo", "Normal", "Alto", "Muy Alto"],
                "Rendimiento (tn/ha)": [
                    f"{muy_bajo:.2f}",
                    f"{bajo:.2f}",
                    f"{normal:.2f}",
                    f"{alto:.2f}",
                    f"{muy_alto:.2f}"
                ],
                "Rango de percentiles": ["hasta P10", "P10-P25", "P25-P75", "P75-P90", "P90+"]
            }
            st.table(escenarios_data)
        else:
            st.warning("Se requieren al menos 5 campañas para calcular los escenarios")
    
    # Calcular rinde de indiferencia usando el promedio de la región
    rindeinf = round(float((costo + arrendamiento_inf() + ges_inf() + (gasto*precio*rindeprom))/ precio),2)
     
    # Inicializar lista de departamentos cargados si no existe
    if 'departamentos_cargados' not in st.session_state:
        st.session_state.departamentos_cargados = []

    # Inicializar precio de soja para cálculos de arrendamiento
    precio_soja = variables_dict.get('psoja1', 300)

    # Imprimir la lista de datos        
    def lista(rinde_actual):
        def valor1():
            if propio == "Aparcería":
                return precio*dol*rinde_actual*cantidad*aparceria
            else:
                return precio*dol*rinde_actual*cantidad
        valors = round(valor1())
        
        def costo1():
            if propio == "Aparcería":
                return costo*dol*cantidad*aparceria
            else:
                return costo*dol*cantidad
        cost = round(costo1())
        
        def gc1():
            return gasto*valors
        gc = round(gc1())
        
        def neto():
            return valors-cost-gc
        net = round(neto()) 
        
        # CAMBIO IMPORTANTE: Agregar provincia a la lista (después de region)
        lista = [region, st.session_state.provincia_seleccionada, st.session_state.departamento_seleccionado, propio, tipo, cantidad, rinde_actual, valors, cost, gc, net, rindeprom, rindeinf]
        return lista

    datos = []
    if "dfp" not in st.session_state:
        st.session_state.dfp = pd.DataFrame(columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ', 'Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos', 'Gastos comercialización','Margen bruto', 'RindeRegion', 'RindeIndif'))

    # Crear DataFrames para los 5 escenarios
    if "dfp_bajo" not in st.session_state:
        st.session_state.dfp_bajo = pd.DataFrame(columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ', 'Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos', 'Gastos comercialización','Margen bruto', 'RindeRegion', 'RindeIndif'))
    if "dfp_normal" not in st.session_state:
        st.session_state.dfp_normal = pd.DataFrame(columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ', 'Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos', 'Gastos comercialización','Margen bruto', 'RindeRegion', 'RindeIndif'))
    if "dfp_alto" not in st.session_state:
        st.session_state.dfp_alto = pd.DataFrame(columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ', 'Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos', 'Gastos comercialización','Margen bruto', 'RindeRegion', 'RindeIndif'))
    if "dfp_muy_bajo" not in st.session_state:
        st.session_state.dfp_muy_bajo = pd.DataFrame(columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ', 'Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos', 'Gastos comercialización','Margen bruto', 'RindeRegion', 'RindeIndif'))
    if "dfp_muy_alto" not in st.session_state:
        st.session_state.dfp_muy_alto = pd.DataFrame(columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ', 'Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos', 'Gastos comercialización','Margen bruto', 'RindeRegion', 'RindeIndif'))


    if submit:
        if propio == "Aparcería" and aparceria == 0:
            st.warning("Falta completar porcentaje de aparcería")
        else:
            # Incrementar contador de líneas
            st.session_state.contador_lineas += 1
            
            # AGREGAR DEPARTAMENTO
            if st.session_state.departamento_seleccionado not in st.session_state.departamentos_cargados:
                st.session_state.departamentos_cargados.append(st.session_state.departamento_seleccionado)
            
            # Siempre usar rindes automáticos
            rindes = rindeautomatico(tipo)
            
            # Generar datos para los 5 escenarios
            datos_muy_bajo = lista(float(rindes['muy_bajo']))
            datos_bajo = lista(float(rindes['bajo']))
            datos_normal = lista(float(rindes['normal']))
            datos_alto = lista(float(rindes['alto']))
            datos_muy_alto = lista(float(rindes['muy_alto']))
            
            # Agregar a los DataFrames correspondientes
            dfo_muy_bajo = pd.DataFrame([datos_muy_bajo], columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ','Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos','Gastos comercialización', 'Margen bruto', 'RindeRegion', 'RindeIndif'))
            dfo_bajo = pd.DataFrame([datos_bajo], columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ','Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos','Gastos comercialización', 'Margen bruto', 'RindeRegion', 'RindeIndif'))
            dfo_normal = pd.DataFrame([datos_normal], columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ','Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos','Gastos comercialización', 'Margen bruto', 'RindeRegion', 'RindeIndif'))
            dfo_alto = pd.DataFrame([datos_alto], columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ','Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos','Gastos comercialización', 'Margen bruto', 'RindeRegion', 'RindeIndif'))
            dfo_muy_alto = pd.DataFrame([datos_muy_alto], columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ','Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos','Gastos comercialización', 'Margen bruto', 'RindeRegion', 'RindeIndif'))
            
            st.session_state.dfp_muy_bajo = pd.concat([st.session_state.dfp_muy_bajo, dfo_muy_bajo])
            st.session_state.dfp_bajo = pd.concat([st.session_state.dfp_bajo, dfo_bajo])
            st.session_state.dfp_normal = pd.concat([st.session_state.dfp_normal, dfo_normal])
            st.session_state.dfp_alto = pd.concat([st.session_state.dfp_alto, dfo_alto])
            st.session_state.dfp_muy_alto = pd.concat([st.session_state.dfp_muy_alto, dfo_muy_alto])
            
            # ACTUALIZAR GASTOS AUTOMÁTICAMENTE
            if propio == "Propios":
                gastos_estructura1()
            elif propio == "Arrendados":
                # Guardar el qq/ha personalizado si existe
                if qq_ha_custom is not None:
                    linea_key = f"{st.session_state.contador_lineas}_{region}_{tipo}"
                    st.session_state.qq_ha_personalizados[linea_key] = qq_ha_custom
                arrendamiento(qq_ha_custom)
                gastos_estructura2()
            elif propio == "Aparcería":
                # Actualizar el porcentaje global si cambió
                st.session_state.porcentaje_aparceria = int(aparceria * 100)
                gastos_estructura2()

        
    def borra1():
        """Borrar gastos de estructura para campos propios"""
        if st.session_state.gespr:
            st.session_state.gespr = st.session_state.gespr[:-1]

    def borra2():
        """Borrar gastos de estructura y arrendamiento para campos arrendados"""
        if st.session_state.gesar:
            st.session_state.gesar = st.session_state.gesar[:-1]
        if st.session_state.arrenda:
            st.session_state.arrenda = st.session_state.arrenda[:-1]

    def borra3():
        """Borrar gastos de estructura para campos en aparcería"""
        if st.session_state.gesar:
            st.session_state.gesar = st.session_state.gesar[:-1]

    def borrar_ultima_fila_completa():
        """Borrar la última fila de todos los DataFrames y actualizar gastos"""
        if not st.session_state.dfp_normal.empty:
            ultimo_tipo_campo = st.session_state.dfp_normal['Campos     '].iloc[-1].strip()
            
            # Borrar de los 5 DataFrames
            st.session_state.dfp_muy_bajo = st.session_state.dfp_muy_bajo.iloc[:-1]
            st.session_state.dfp_bajo = st.session_state.dfp_bajo.iloc[:-1]
            st.session_state.dfp_normal = st.session_state.dfp_normal.iloc[:-1]
            st.session_state.dfp_alto = st.session_state.dfp_alto.iloc[:-1]
            st.session_state.dfp_muy_alto = st.session_state.dfp_muy_alto.iloc[:-1]
            
            # Decrementar contador de líneas
            if st.session_state.contador_lineas > 0:
                st.session_state.contador_lineas -= 1
            
            # Actualizar los gastos según el tipo de campo
            if ultimo_tipo_campo == "Propios":
                borra1()
            elif ultimo_tipo_campo == "Arrendados":
                borra2()
            elif ultimo_tipo_campo == "Aparcería":
                borra3()
                
            st.success("Última fila eliminada de todos los escenarios")
        else:
            st.warning("No hay filas para borrar")

    # MOSTRAR RESUMEN AUTOMÁTICO EN ANCHO COMPLETO
    if st.session_state.dfp_normal is not None and not st.session_state.dfp_normal.empty:
        st.markdown("---")
        st.markdown("### 📊 Resumen del Planteo")
        
        heca_arrendados = st.session_state.dfp_normal.loc[st.session_state.dfp_normal['Campos     '] == 'Arrendados', 'Superficie (has)'].sum()
        hecp_propios = st.session_state.dfp_normal.loc[st.session_state.dfp_normal['Campos     '] == 'Propios', 'Superficie (has)'].sum()
        hecp_aparceria = st.session_state.dfp_normal.loc[st.session_state.dfp_normal['Campos     '] == 'Aparcería', 'Superficie (has)'].sum()
        
        gastos = sum(st.session_state.gespr) + sum(st.session_state.gesar)
        arrenda_resultante = sum(st.session_state.arrenda)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total hectáreas", f"{heca_arrendados + hecp_propios + hecp_aparceria:.0f} has")
        col2.metric("Gastos estructura", f"${gastos:,.0f}")
        col3.metric("Arrendamientos", f"${arrenda_resultante:,.0f}")
        col4.metric("Total gastos fijos", f"${gastos + arrenda_resultante:,.0f}")
    
    # FUNCIONALIDAD: Borrar filas específicas
    if not st.session_state.dfp_normal.empty:
        with st.expander("🎯 Eliminar filas específicas"):
            st.write("Selecciona las filas que deseas eliminar:")
            
            # Crear una copia del dataframe con índice visible para el usuario
            df_display = st.session_state.dfp_normal.reset_index(drop=True).copy()
            df_display.insert(0, 'Nº', range(1, len(df_display) + 1))
            
            # Mostrar tabla con información clave
            df_seleccion = df_display[['Nº', 'Departamento', 'Cultivo', 'Campos     ', 'Superficie (has)', 'Rinde']].copy()
            
            st.dataframe(df_seleccion, hide_index=True)
            
            # Input para seleccionar números de fila
            filas_a_borrar = st.multiselect(
                "Selecciona el número de fila(s) a eliminar:",
                options=list(range(1, len(df_display) + 1)),
                format_func=lambda x: f"Fila {x}: {df_seleccion.iloc[x-1]['Cultivo']} - {df_seleccion.iloc[x-1]['Departamento']} ({df_seleccion.iloc[x-1]['Superficie (has)']} has)"
            )
            
            col1, col2 = st.columns([1, 3])
            
            if col1.button("❌ Eliminar seleccionadas", type="primary", key="btn_eliminar_especificas"):
                if filas_a_borrar:
                    # Convertir números de fila (1-indexed) a índices (0-indexed)
                    indices_a_borrar = [x - 1 for x in filas_a_borrar]
                    
                    # Resetear índices antes de operar para asegurar índices 0, 1, 2, ...
                    st.session_state.dfp_muy_bajo = st.session_state.dfp_muy_bajo.reset_index(drop=True)
                    st.session_state.dfp_bajo = st.session_state.dfp_bajo.reset_index(drop=True)
                    st.session_state.dfp_normal = st.session_state.dfp_normal.reset_index(drop=True)
                    st.session_state.dfp_alto = st.session_state.dfp_alto.reset_index(drop=True)
                    st.session_state.dfp_muy_alto = st.session_state.dfp_muy_alto.reset_index(drop=True)
                    
                    # Obtener información de las filas a borrar ANTES de eliminarlas
                    tipos_campo_borrados = []
                    for idx in indices_a_borrar:
                        tipo_campo = st.session_state.dfp_normal.iloc[idx]['Campos     '].strip()
                        tipos_campo_borrados.append(tipo_campo)
                    
                    # Crear máscara booleana: True para mantener, False para eliminar
                    mask = [i not in indices_a_borrar for i in range(len(st.session_state.dfp_normal))]
                    
                    # Aplicar máscara a todos los DataFrames
                    st.session_state.dfp_muy_bajo = st.session_state.dfp_muy_bajo[mask].reset_index(drop=True)
                    st.session_state.dfp_bajo = st.session_state.dfp_bajo[mask].reset_index(drop=True)
                    st.session_state.dfp_normal = st.session_state.dfp_normal[mask].reset_index(drop=True)
                    st.session_state.dfp_alto = st.session_state.dfp_alto[mask].reset_index(drop=True)
                    st.session_state.dfp_muy_alto = st.session_state.dfp_muy_alto[mask].reset_index(drop=True)
                    
                    # Actualizar gastos según tipo de campo
                    for tipo_campo in tipos_campo_borrados:
                        if tipo_campo == "Propios":
                            borra1()
                        elif tipo_campo == "Arrendados":
                            borra2()
                        elif tipo_campo == "Aparcería":
                            borra3()
                        
                        # Decrementar contador
                        if st.session_state.contador_lineas > 0:
                            st.session_state.contador_lineas -= 1
                    
                    # Marcar que se realizó una eliminación exitosa
                    st.session_state.ultima_eliminacion = len(filas_a_borrar)
                else:
                    st.warning("⚠️ No has seleccionado ninguna fila para eliminar")
            
            # Mostrar mensaje de éxito si hubo eliminación reciente
            if hasattr(st.session_state, 'ultima_eliminacion') and st.session_state.ultima_eliminacion > 0:
                st.success(f"✓ {st.session_state.ultima_eliminacion} fila(s) eliminada(s) correctamente")
                st.session_state.ultima_eliminacion = 0  # Reset
            
            if filas_a_borrar:
                col2.info(f"📝 {len(filas_a_borrar)} fila(s) seleccionada(s)")


    # SECCIÓN DE CONFIGURACIÓN GLOBAL EN EL SIDEBAR
    with right:
        st.markdown("---")
        st.markdown("### ⚙️ Configuración Global")
        
        # Mostrar configuración actual de aparcería
        nuevo_pct_aparceria = st.number_input(
            "% Aparcería por defecto:",
            min_value=1,
            max_value=100,
            value=st.session_state.porcentaje_aparceria,
            step=1,
            help="Este porcentaje se aplicará a nuevos campos en aparcería"
        )
        
        if nuevo_pct_aparceria != st.session_state.porcentaje_aparceria:
            st.session_state.porcentaje_aparceria = nuevo_pct_aparceria
            st.info(f"✓ Porcentaje de aparcería actualizado a {nuevo_pct_aparceria}%")

    # Crear pestañas para los 5 escenarios
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📉 Muy Bajo", "📊 Bajo", "⚖️ Normal", "📈 Alto", "🚀 Muy Alto"])

    with tab1:
        st.subheader("Escenario Muy Bajo (Percentil 10)")
        st.dataframe(st.session_state.dfp_muy_bajo.style.format({
            "Superficie (has)": "{:.0f}", 
            "Rinde": "{:.2f}", 
            "Ingreso": "${:,}", 
            "Costos directos": "${:,}", 
            "Gastos comercialización": "${:,}", 
            "Margen bruto": "${:,}", 
            "RindeRegion": "{:.2f}", 
            "RindeIndif": "{:.2f}"
        }))
        

    with tab2:
        st.subheader("Escenario Bajo (Percentil 10-25)")
        st.dataframe(st.session_state.dfp_bajo.style.format({
            "Superficie (has)": "{:.0f}", 
            "Rinde": "{:.2f}", 
            "Ingreso": "${:,}", 
            "Costos directos": "${:,}", 
            "Gastos comercialización": "${:,}", 
            "Margen bruto": "${:,}", 
            "RindeRegion": "{:.2f}", 
            "RindeIndif": "{:.2f}"
        }))
        

    with tab3:
        st.subheader("Escenario Normal (Percentil 25-75)")
        st.dataframe(st.session_state.dfp_normal.style.format({
            "Superficie (has)": "{:.0f}", 
            "Rinde": "{:.2f}", 
            "Ingreso": "${:,}", 
            "Costos directos": "${:,}", 
            "Gastos comercialización": "${:,}", 
            "Margen bruto": "${:,}", 
            "RindeRegion": "{:.2f}", 
            "RindeIndif": "{:.2f}"
        }))


    with tab4:
        st.subheader("Escenario Alto (Percentil 75-90)")
        st.dataframe(st.session_state.dfp_alto.style.format({
            "Superficie (has)": "{:.0f}", 
            "Rinde": "{:.2f}", 
            "Ingreso": "${:,}", 
            "Costos directos": "${:,}", 
            "Gastos comercialización": "${:,}", 
            "Margen bruto": "${:,}", 
            "RindeRegion": "{:.2f}", 
            "RindeIndif": "{:.2f}"
        }))
        

    with tab5:
        st.subheader("Escenario Muy Alto (Percentil 90+)")
        st.dataframe(st.session_state.dfp_muy_alto.style.format({
            "Superficie (has)": "{:.0f}", 
            "Rinde": "{:.2f}", 
            "Ingreso": "${:,}", 
            "Costos directos": "${:,}", 
            "Gastos comercialización": "${:,}", 
            "Margen bruto": "${:,}", 
            "RindeRegion": "{:.2f}", 
            "RindeIndif": "{:.2f}"
        }))
        css()


    # NUEVO CÓDIGO: Expander para mostrar cálculos detallados (SOLO ESCENARIO NORMAL)
    if not st.session_state.dfp_normal.empty:
        with st.expander("📊 Ver detalles del cálculo de márgenes"):
            st.write("Este panel muestra cómo se calcularon los ingresos, costos directos y gastos de comercialización para cada cultivo (escenario normal).")
            
            # Mostrar información sobre los 3 escenarios de rinde
            st.info("ℹ️ **Nota:** Se están calculando 3 escenarios diferentes basados en percentiles históricos. Esta explicación muestra solo el **escenario normal** (percentiles 25-75).")
            
            # Usar tabs en lugar de expanders anidados
            tabs = st.tabs([f"{row['Cultivo']} - {row['Campos     '].strip()}" 
                        for index, row in st.session_state.dfp_normal.iterrows()])
            
            for idx, tab in enumerate(tabs):
                with tab:
                    row = st.session_state.dfp_normal.iloc[idx]
                    
                    # Obtener también los rindes de los otros escenarios para referencia
                    rinde_bajo = st.session_state.dfp_bajo.iloc[idx]['Rinde'] if len(st.session_state.dfp_bajo) > idx else 0
                    rinde_alto = st.session_state.dfp_alto.iloc[idx]['Rinde'] if len(st.session_state.dfp_alto) > idx else 0
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Fórmulas utilizadas:**")
                        st.markdown("- **Ingreso** = Precio × Rinde × Superficie")
                        st.markdown("- **Costos directos** = Costo/ha × Superficie")
                        st.markdown("- **Gastos de comercialización** = Porcentaje de gastos × Ingreso")
                        st.markdown("- **Margen bruto** = Ingreso - Costos directos - Gastos de comercialización")
                        
                        # Mostrar breve comparación de rindes
                        st.markdown("**Rindes por escenario:**")
                        st.markdown(f"- 📉 **Bajo:** {rinde_bajo:.2f} tn/ha")
                        st.markdown(f"- 📊 **Normal:** {row['Rinde']:.2f} tn/ha")
                        st.markdown(f"- 📈 **Alto:** {rinde_alto:.2f} tn/ha")
                    
                    with col2:
                        st.markdown("**Valores aplicados:**")
                        st.markdown(f"- Superficie: {row['Superficie (has)']} ha")
                        st.markdown(f"- Rinde: {row['Rinde']} tn/ha")
                        
                        # Obtener precio y gasto para este cultivo específico
                        cultivo_tipo = row['Cultivo']
                        precio_actual = float(obtener_precio(cultivo_tipo))
                        costo_actual = float(obtener_costo(region, cultivo_tipo))
                        gasto_actual = float(obtener_gasvar(region, cultivo_tipo))
                        
                        st.markdown(f"- Cotización grano: u$s {precio_actual:,.2f}/tn")
                        st.markdown(f"- Costo directo/ha: u$s {costo_actual:,.2f}")
                        st.markdown(f"- % Gastos comercialización: {gasto_actual*100:.1f}%")
                        
                        if row['Campos     '].strip() == "Aparcería":
                            aparceria_local = st.session_state.porcentaje_aparceria / 100
                            st.markdown(f"- % Aparcería: {aparceria_local*100:.0f}%")
                            st.markdown("*(En aparcería, ingresos y costos se comparten según porcentaje)*")
                    
                    st.divider()
                    
                    # Mostrar cálculo paso a paso
                    st.markdown("**Cálculo paso a paso:**")
                    
                    # Cálculo de ingresos
                    if row['Campos     '].strip() == "Aparcería":
                        aparceria_local = st.session_state.porcentaje_aparceria / 100
                        ingreso_base = precio_actual * dol * row['Rinde'] * row['Superficie (has)']
                        ingreso_final = ingreso_base * aparceria_local
                        st.markdown(f"1. **Ingreso base**: u$s {precio_actual:,.2f}/tn × {dol} × {row['Rinde']} tn/ha × {row['Superficie (has)']} ha = ${ingreso_base:,.0f}")
                        st.markdown(f"2. **Ajuste por aparcería**: ${ingreso_base:,.0f} × {aparceria_local*100:.0f}% = **${ingreso_final:,.0f}**")
                    else:
                        ingreso_final = precio_actual * dol * row['Rinde'] * row['Superficie (has)']
                        st.markdown(f"1. **Ingreso**: u$s {precio_actual:,.2f}/tn × {dol} × {row['Rinde']} tn/ha × {row['Superficie (has)']} ha = **${ingreso_final:,.0f}**")
                    
                    # Cálculo de costos directos
                    if row['Campos     '].strip() == "Aparcería":
                        aparceria_local = st.session_state.porcentaje_aparceria / 100
                        costo_base = costo_actual * dol * row['Superficie (has)']
                        costo_final = costo_base * aparceria_local
                        st.markdown(f"3. **Costo directo base**: u$s {costo_actual:,.2f}/ha × {dol} × {row['Superficie (has)']} ha = ${costo_base:,.0f}")
                        st.markdown(f"4. **Ajuste por aparcería**: ${costo_base:,.0f} × {aparceria_local*100:.0f}% = **${costo_final:,.0f}**")
                    else:
                        costo_final = costo_actual * dol * row['Superficie (has)']
                        st.markdown(f"2. **Costo directo**: u$s {costo_actual:,.2f}/ha × {dol} × {row['Superficie (has)']} ha = **${costo_final:,.0f}**")
                    
                    # Cálculo de gastos de comercialización
                    gasto_final = gasto_actual * ingreso_final
                    st.markdown(f"3. **Gastos de comercialización**: {gasto_actual*100:.1f}% × ${ingreso_final:,.0f} = **${gasto_final:,.0f}**")
                    
                    # Cálculo de margen bruto
                    margen_final = ingreso_final - costo_final - gasto_final
                    st.markdown(f"4. **Margen bruto**: ${ingreso_final:,.0f} - ${costo_final:,.0f} - ${gasto_final:,.0f} = **${margen_final:,.0f}**")
                    
                    # Mostrar cómo afectaría un cambio de escenario (opcional, simple)
                    st.divider()
                    st.markdown("**¿Cómo cambiaría con otros escenarios?**")
                    st.markdown(f"- Con rinde bajo ({rinde_bajo:.2f} tn/ha): Margen ≈ **${precio_actual * dol * rinde_bajo * row['Superficie (has)'] - costo_final - (gasto_actual * precio_actual * dol * rinde_bajo * row['Superficie (has)']):,.0f}**")
                    st.markdown(f"- Con rinde alto ({rinde_alto:.2f} tn/ha): Margen ≈ **${precio_actual * dol * rinde_alto * row['Superficie (has)'] - costo_final - (gasto_actual * precio_actual * dol * rinde_alto * row['Superficie (has)']):,.0f}**")              
               
    # Actualizar automáticamente los gastos y preparar df1
    if st.session_state.dfp_normal is not None and not st.session_state.dfp_normal.empty:
        heca_arrendados = st.session_state.dfp_normal.loc[st.session_state.dfp_normal['Campos     '] == 'Arrendados', 'Superficie (has)'].sum()
        hecp_propios = st.session_state.dfp_normal.loc[st.session_state.dfp_normal['Campos     '] == 'Propios', 'Superficie (has)'].sum()
        hecp_aparceria = st.session_state.dfp_normal.loc[st.session_state.dfp_normal['Campos     '] == 'Aparcería', 'Superficie (has)'].sum()
        heca = heca_arrendados + hecp_aparceria
        hecp = hecp_propios
        nro_hectareas = heca + hecp

        if nro_hectareas > 0:
            gastos = sum(st.session_state.gespr) + sum(st.session_state.gesar)
            gestimado = gastos
            arrenda_resultante = sum(st.session_state.arrenda)
            
            # Actualizar df1 automáticamente
            st.session_state.df1 = [arrenda_resultante, gestimado, st.session_state.porcentaje_aparceria / 100]
            
            # Guardar valores adicionales necesarios
            st.session_state.dol = dol
            st.session_state.region = region
            st.session_state.gasvar_dict = gasvar_por_region_cultivo




def app9():
    st.title("🌄 Sitios de utilidad")
    st.subheader("Valor de la tierra")

    # Lista de enlaces
    enlaces = {
        "Buenos Aires": "https://www.margenes.com/wp-content/uploads/2025/06/Buenos-Aires-Jun-25.pdf",
        "Chaco": "https://www.margenes.com/wp-content/uploads/2025/08/Chaco-Ago-25.pdf",
        "Córdoba": "https://www.margenes.com/wp-content/uploads/2025/07/Cordoba-Jul-25.pdf",
        "Corrientes": "https://www.margenes.com/wp-content/uploads/2025/11/Corrientes-Nov-25.pdf",
        "Entre Ríos": "https://www.margenes.com/wp-content/uploads/2025/03/Entre-Rios-Mar-25.pdf",
        "La Pampa": "https://www.margenes.com/wp-content/uploads/2025/09/La-Pampa-Sep-25.pdf",
        "Mendoza": "https://www.margenes.com/wp-content/uploads/2024/12/Mendoza-Dic-24.pdf",
        "NOA": "https://www.margenes.com/wp-content/uploads/2025/12/NOA-Dic-25.pdf",
        "San Luis": "https://www.margenes.com/wp-content/uploads/2023/11/San-Luis-Oct-23.pdf",
        "Santa Fe": "https://www.margenes.com/wp-content/uploads/2025/02/Santa-Fe-Feb-25.pdf",
        "Santiago de Estero": "https://www.margenes.com/wp-content/uploads/2025/10/Santiago-de-Estero-Oct-25.pdf"
    }
    
    # Dividir los enlaces en grupos de cinco
    enlaces_por_filas = [list(enlaces.items())[i:i+5] for i in range(0, len(enlaces), 5)]
    
    # Mostrar cada grupo de enlaces en una fila
    for fila in enlaces_por_filas:
        col1, col2, col3, col4, col5 = st.columns(5)
        for idx, (lugar, enlace) in enumerate(fila):
            if idx == 0:
                col1.markdown(f"**[{lugar}]({enlace})**")
            elif idx == 1:
                col2.markdown(f"**[{lugar}]({enlace})**")
            elif idx == 2:
                col3.markdown(f"**[{lugar}]({enlace})**")
            elif idx == 3:
                col4.markdown(f"**[{lugar}]({enlace})**")
            elif idx == 4:
                col5.markdown(f"**[{lugar}]({enlace})**")

    st.subheader("Reservas hídricas por zona - ORA")
    ora_semanal_link = "http://www.ora.gob.ar/camp_actual_reservas.php"
    st.markdown(f"**[Reservas hídricas (todas las regiones)]({ora_semanal_link})**")
    
    st.subheader("Reservas hídricas y evolución cultivos semanal - INTA SEPA")
    inta_semanal_link = "https://www.argentina.gob.ar/agromet-semanal"
    st.markdown(f"**[Reservas hídricas INTA (todas las regiones)]({inta_semanal_link})**")
        
    st.subheader("Informe semanal zona núcleo - GEA - Bolsa de Rosario")
    gea_semanal_link = "https://www.bcr.com.ar/es/mercados/gea/seguimiento-de-cultivos/informe-semanal-zona-nucleo"
    st.markdown(f"**[Informe semanal Zona Núcleo]({gea_semanal_link})**")

    st.subheader("Informe semanal Secretaria Agricultura")
    sec_semanal_link = "https://www.magyp.gob.ar/sitio/areas/estimaciones/estimaciones/informes/"
    st.markdown(f"**[Informe semanal Secretaria Agricultura (todas las regiones)]({sec_semanal_link})**")

    st.subheader("Mapa de datos e informes PAS - Bolsa de Buenos Aires")
    panorama_agricola_semanal_link = "https://www.bolsadecereales.com/estimaciones-informes"
    st.markdown(f"**[Panorama Agrícola Semanal]({panorama_agricola_semanal_link})**")
    
    st.subheader("Mapa semanal reservas hídricas - INTA SEPA (solo mapa sin informe)")
    sepasemanal_link = "https://sepa.inta.gob.ar/productos/"
    st.markdown(f"**[Mapa INTA SEPA]({sepasemanal_link})**")
    
    st.subheader("Datos de otros cultivos (arroz, algodón, maní, legumbres, etc)")
    sagyp_link = "https://www.magyp.gob.ar/sitio/areas/analisis_economico/tablero/agricolas/arroz-algodon-legumbres.php?accion=imp"
    st.markdown(f"**[Resultados de cultivos Arroz, algodón, maní, legumbres]({sagyp_link})**")
    
    st.subheader("Informe semanal ROSGAN (ganadería)")
    rosgan_link = "https://www.rosgan.com.ar/lote-de-noticias/"
    st.markdown(f"**[Informes ROSGAN]({rosgan_link})**")
        
def app5():

    layout_centrado()
    left, right = st.columns(2)
    css()
   
    # Obtener los dataframes existentes o None si no existen
    dfp = getattr(st.session_state, 'dfp', None)
    dfp_muy_bajo = getattr(st.session_state, 'dfp_muy_bajo', None)
    dfp_bajo = getattr(st.session_state, 'dfp_bajo', None)
    dfp_normal = getattr(st.session_state, 'dfp_normal', None)
    dfp_alto = getattr(st.session_state, 'dfp_alto', None)
    dfp_muy_alto = getattr(st.session_state, 'dfp_muy_alto', None)
    dfs = getattr(st.session_state, 'dfs', None)
    dfx = getattr(st.session_state, 'dfx', None)
    dfa = getattr(st.session_state, 'dfa', None)
    df1 = getattr(st.session_state, 'df1', None)
    
    # Verificar si hay datos en los DataFrames de escenarios
    hay_escenarios = any([
        dfp_muy_bajo is not None and not dfp_muy_bajo.empty,
        dfp_bajo is not None and not dfp_bajo.empty,
        dfp_normal is not None and not dfp_normal.empty,
        dfp_alto is not None and not dfp_alto.empty,
        dfp_muy_alto is not None and not dfp_muy_alto.empty
    ])
    
        # Asegurar que todos los dataframes tienen columna Provincia y Departamento
    for df_name in ['dfp_muy_bajo', 'dfp_bajo', 'dfp_normal', 'dfp_alto', 'dfp_muy_alto']:
        if hasattr(st.session_state, df_name):
            df = getattr(st.session_state, df_name)
            if df is not None and not df.empty:
                # Si no existe la columna Provincia, agregarla desde session_state
                if 'Provincia' not in df.columns and hasattr(st.session_state, 'provincia_seleccionada'):
                    # Intentar obtener provincia de la región
                    # (esto asume que todas las filas del df son de la misma provincia)
                    df['Provincia'] = st.session_state.provincia_seleccionada

    # Usar dfp_normal como referencia principal (o dfp si no hay escenarios)
    if dfp_normal is not None and not dfp_normal.empty:
        df_referencia = dfp_normal
        df_fina = dfp_normal[(dfp_normal['Cultivo'] == "Trigo") | (dfp_normal['Cultivo'] == "Cebada")]
        df_gruesa = dfp_normal[(dfp_normal['Cultivo'] != "Trigo") & (dfp_normal['Cultivo'] != "Cebada")]
    elif dfp is not None and not dfp.empty:
        df_referencia = dfp
        df_fina = dfp[(dfp['Cultivo'] == "Trigo") | (dfp['Cultivo'] == "Cebada")]
        df_gruesa = dfp[(dfp['Cultivo'] != "Trigo") & (dfp['Cultivo'] != "Cebada")]
    else:
        df_referencia = None
        df_fina = pd.DataFrame()
        df_gruesa = pd.DataFrame()
    
    if df_referencia is not None:
        st.subheader("Planteo productivo - Campaña 2025/2026")
                       
        # CALCULOS PRINCIPALES (usando escenario normal o dfp original)
        ingtotal = df_referencia['Ingreso'].sum()
        costtotal = df_referencia['Costos directos'].sum()
        gctotal = df_referencia['Gastos comercialización'].sum()
        mbtotal = df_referencia['Margen bruto'].sum()
        ingtotalfina = df_fina['Ingreso'].sum()
        costtotalfina = df_fina['Costos directos'].sum()
        gctotalfina = df_fina['Gastos comercialización'].sum()
        mbtotalfina = df_fina['Margen bruto'].sum()
        ingtotalgruesa = df_gruesa['Ingreso'].sum()
        costtotalgruesa = df_gruesa['Costos directos'].sum()
        gctotalgruesa = df_gruesa['Gastos comercialización'].sum()
        mbtotalgruesa = df_gruesa['Margen bruto'].sum()
    
    if df1 is not None:
        left, middle, right = st.columns(3)
        arrend = st.session_state.df1[0]
        gas = st.session_state.df1[1]
        result = int(mbtotal)-int(arrend)-int(gas)
        
        # Calcular resultado final para campañas
        result_fina = int(mbtotalfina) - int(arrend * (ingtotalfina / ingtotal if ingtotal > 0 else 0)) - int(gas * (ingtotalfina / ingtotal if ingtotal > 0 else 0))
        result_gruesa = int(mbtotalgruesa) - int(arrend * (ingtotalgruesa / ingtotal if ingtotal > 0 else 0)) - int(gas * (ingtotalgruesa / ingtotal if ingtotal > 0 else 0))
        
        # Crear una lista de diccionarios con los datos
        data = [
            {'Concepto': 'Facturación campaña', 'Total': '${:,}'.format(round(ingtotal))},
            {'Concepto': 'Costos directos', 'Total': '${:,}'.format(round(costtotal))},
            {'Concepto': 'Gastos comercialización y cosecha', 'Total': '${:,}'.format(round(gctotal))},
            {'Concepto': 'Margen bruto total', 'Total': '${:,}'.format(round(mbtotal))},
            {'Concepto': 'Arrendamiento', 'Total': '${:,}'.format(arrend)},
            {'Concepto': 'Gastos estructura', 'Total': '${:,}'.format(gas)},
            {'Concepto': 'Generación operativa de fondos', 'Total': '${:,}'.format(result)}
        ]
        
        # Preparar datos fina/gruesa (se usarán más adelante)
        datafg = {
            'Concepto': ['Ingresos totales', 'Costos directos', 'Gastos comercialización', 'Resultado bruto', 'Resultado neto' ],
            'Campaña Fina': [ingtotalfina, costtotalfina, gctotalfina, mbtotalfina, result_fina],
            'Campaña Gruesa': [ingtotalgruesa, costtotalgruesa, gctotalgruesa, mbtotalgruesa, result_gruesa]
        }
    
        df_totales = pd.DataFrame(datafg)

        try:
            valuacion_total = st.session_state.dfs['Valuación'].sum()
        except (AttributeError, KeyError):
            valuacion_total = 0

        margenb = mbtotal/ingtotal
        margenb_porcentaje = "{:.0%}".format(margenb)
        costototal = "${:,.1f}MM".format(costtotal/1000000)
        margenn = result/ingtotal
        margenn_porcentaje = "{:.0%}".format(margenn)
        granos = "${:,.1f}MM".format(valuacion_total/1000000)

        col1, col2, col3, col4 = st.columns(4)  
        
        col1.metric(label="Superficie has (con rotación)", value=df_referencia["Superficie (has)"].sum())
        col2.metric(label="Arrendamiento", value ='${:.1f}MM'.format(arrend/1000000))
        col3.metric(label="Costo directo", value=costototal)
        col4.metric(label="Tenencia de granos", value= granos)

        # CÓDIGO MODIFICADO PARA EL HEATMAP CON RANGOS
# Este código reemplaza la sección del heatmap en app5

        # MOSTRAR TABLA COMPARATIVA DE LOS 5 ESCENARIOS
        if hay_escenarios:
            # AGREGAR HEATMAP CON RESULTADO FINAL POR ESCENARIO DE RINDE Y PRECIO
            st.markdown("### 📊 Matriz de Resultado Final: Escenarios de Rinde × Precio")

            # Obtener dólar desde session_state
            dol = getattr(st.session_state, 'dol', 1401)

            # Definir función local de obtener_gasvar
            def obtener_gasvar_local(cultivo, df_row):
                """Obtiene el % de gastos de comercialización desde los datos ya calculados"""
                if df_row['Ingreso'] > 0:
                    return df_row['Gastos comercialización'] / df_row['Ingreso']
                else:
                    return 0.05  # 5% por defecto

            # Cargar datos históricos para calcular percentiles
            url = "https://raw.githubusercontent.com/Jthl1986/T1/main/Estimaciones8.csv"
            dfr = pd.read_csv(url, encoding='ISO-8859-1', sep=',')
            
            # Mapeo de cultivos
            mapeo_cultivos_csv = {
                "Trigo": "Trigo total",
                "Maíz": "Maíz",
                "Soja 1ra": "Soja 1ra",
                "Soja 2da": "Soja 2da",
                "Girasol": "Girasol",
                "Sorgo": "Sorgo",
                "Cebada": "Cebada"
            }

            # Definir escenarios de precio (variación de ±15% respecto a precio base)
            escenarios_precio = {
                'Bajo (-15%)': {
                    'Trigo': 190 * 0.92,
                    'Soja 1ra': 300 * 0.92,
                    'Soja 2da': 300 * 0.92,
                    'Maíz': 175 * 0.92,
                    'Cebada': 165 * 0.92,
                    'Girasol': 330 * 0.92,
                    'Sorgo': 160 * 0.92
                },
                'Normal': {
                    'Trigo': 190,
                    'Soja 1ra': 300,
                    'Soja 2da': 300,
                    'Maíz': 175,
                    'Cebada': 165,
                    'Girasol': 330,
                    'Sorgo': 160
                },
                'Alto (+15%)': {
                    'Trigo': 190 * 1.08,
                    'Soja 1ra': 300 * 1.08,
                    'Soja 2da': 300 * 1.08,
                    'Maíz': 175 * 1.08,
                    'Cebada': 165 * 1.08,
                    'Girasol': 330 * 1.08,
                    'Sorgo': 160 * 1.08
                }
            }

            # Función para calcular percentiles de rinde por cultivo/departamento
            def calcular_percentiles_rinde(cultivo, departamento, provincia):
                """Calcula los percentiles de rinde para un cultivo/departamento específico"""
                cultivo_csv = mapeo_cultivos_csv.get(cultivo, cultivo)
                
                filtro = (dfr['Provincia'] == provincia) & \
                        (dfr['Departamento'] == departamento) & \
                        (dfr['Cultivo'] == cultivo_csv)
                df_hist = dfr[filtro]
                
                if len(df_hist) >= 5:
                    rendimientos = df_hist['Rendimiento'].astype(float).values
                    return {
                        'p10': np.percentile(rendimientos, 10) / 1000,
                        'p25': np.percentile(rendimientos, 25) / 1000,
                        'p75': np.percentile(rendimientos, 75) / 1000,
                        'p90': np.percentile(rendimientos, 90) / 1000,
                        'min': rendimientos.min() / 1000,
                        'max': rendimientos.max() / 1000
                    }
                return None

            # Función para recalcular resultado con precios y RANGO de rindes
            def calcular_resultado_con_rango(df_base, precios_dict, arrend, gas, rinde_min_factor, rinde_max_factor):
                """
                Calcula resultado mínimo y máximo para un escenario de precio con rango de rindes
                rinde_min_factor/max_factor: multiplicadores para calcular rinde mínimo y máximo del escenario
                Retorna: (resultado_min, resultado_max, margen_min, margen_max)
                """
                # Calcular con rinde mínimo
                ingreso_min = 0
                costo_min = 0
                gc_min = 0
                
                # Calcular con rinde máximo
                ingreso_max = 0
                costo_max = 0
                gc_max = 0
                
                for idx, row in df_base.iterrows():
                    cultivo = row['Cultivo']
                    departamento = row['Departamento']
                    provincia = row.get('Provincia', '')
                    superficie = row['Superficie (has)']
                    
                    # Obtener percentiles para este cultivo/departamento
                    percentiles = calcular_percentiles_rinde(cultivo, departamento, provincia)
                    
                    if percentiles:
                        rinde_base_min = percentiles.get(rinde_min_factor, row['Rinde'])
                        rinde_base_max = percentiles.get(rinde_max_factor, row['Rinde'])
                    else:
                        # Si no hay datos históricos, usar variación del 10%
                        rinde_base_min = row['Rinde'] * 0.9
                        rinde_base_max = row['Rinde'] * 1.1
                    
                    precio_nuevo = precios_dict.get(cultivo, 0)
                    
                    # Calcular con aparcería si aplica
                    if row['Campos     '].strip() == "Aparcería":
                        aparceria = st.session_state.df1[2] if len(st.session_state.df1) > 2 else 0.6
                        ing_min = precio_nuevo * dol * rinde_base_min * superficie * aparceria
                        ing_max = precio_nuevo * dol * rinde_base_max * superficie * aparceria
                        costo = row['Costos directos']
                    else:
                        ing_min = precio_nuevo * dol * rinde_base_min * superficie
                        ing_max = precio_nuevo * dol * rinde_base_max * superficie
                        costo = row['Costos directos']
                    
                    # Gastos de comercialización
                    gasto_pct = obtener_gasvar_local(cultivo, row)
                    gc_m = gasto_pct * ing_min
                    gc_M = gasto_pct * ing_max
                    
                    ingreso_min += ing_min
                    ingreso_max += ing_max
                    costo_min += costo
                    costo_max += costo
                    gc_min += gc_m
                    gc_max += gc_M
                
                # Calcular resultados
                mb_min = ingreso_min - costo_min - gc_min
                mb_max = ingreso_max - costo_max - gc_max
                
                resultado_min = (mb_min - arrend - gas) / 1_000_000
                resultado_max = (mb_max - arrend - gas) / 1_000_000
                
                margen_min = ((mb_min - arrend - gas) / ingreso_min * 100) if ingreso_min > 0 else 0
                margen_max = ((mb_max - arrend - gas) / ingreso_max * 100) if ingreso_max > 0 else 0
                
                return resultado_min, resultado_max, margen_min, margen_max

            # Definir los rangos de percentiles para cada escenario de rinde
            rangos_rinde = {
                "Muy Bajo": ('min', 'p10'),
                "Bajo": ('p10', 'p25'),
                "Normal": ('p25', 'p75'),
                "Alto": ('p75', 'p90'),
                "Muy Alto": ('p90', 'max')
            }

            escenarios_rinde_nombres = ["Muy Bajo", "Bajo", "Normal", "Alto", "Muy Alto"]

            heatmap_data_min = []
            heatmap_data_max = []
            margenes_data_min = []
            margenes_data_max = []
            hover_data = []

            # Iterar por precios (filas) y rindes (columnas)
            for nombre_precio, precios in escenarios_precio.items():
                fila_valores_min = []
                fila_valores_max = []
                fila_margenes_min = []
                fila_margenes_max = []
                fila_hover = []
                
                for nombre_rinde in escenarios_rinde_nombres:
                    if dfp_normal is None or dfp_normal.empty:
                        continue
                    
                    rinde_min_key, rinde_max_key = rangos_rinde[nombre_rinde]
                    
                    # Calcular resultado con rango de rindes
                    resultado_min, resultado_max, margen_min, margen_max = calcular_resultado_con_rango(
                        dfp_normal,
                        precios,
                        arrend,
                        gas,
                        rinde_min_key,
                        rinde_max_key
                    )
                    
                    # Usar el promedio para el color del heatmap
                    resultado_promedio = (resultado_min + resultado_max) / 2
                    
                    fila_valores_min.append(resultado_min)
                    fila_valores_max.append(resultado_max)
                    fila_margenes_min.append(margen_min)
                    fila_margenes_max.append(margen_max)
                    
                    # Crear texto hover detallado
                    hover_text = f"<b>Precio: {nombre_precio}</b><br>"
                    hover_text += f"<b>Rinde: {nombre_rinde}</b><br><br>"
                    hover_text += f"<b>Resultado Mín:</b> ${resultado_min:,.2f}M ({margen_min:+.1f}%)<br>"
                    hover_text += f"<b>Resultado Máx:</b> ${resultado_max:,.2f}M ({margen_max:+.1f}%)<br>"
                    hover_text += f"<b>Rango:</b> ${resultado_max - resultado_min:,.2f}M<br><br>"
                    hover_text += "<b>Precios aplicados:</b><br>"
                    for cultivo, precio in precios.items():
                        if cultivo in dfp_normal['Cultivo'].values:
                            hover_text += f"  • {cultivo}: u$s{precio:.0f}/tn<br>"
                    
                    fila_hover.append(hover_text)
                
                heatmap_data_min.append(fila_valores_min)
                heatmap_data_max.append(fila_valores_max)
                margenes_data_min.append(fila_margenes_min)
                margenes_data_max.append(fila_margenes_max)
                hover_data.append(fila_hover)

            # Crear DataFrame para el heatmap (usar promedio para colores)
            heatmap_data_promedio = [
                [(min_val + max_val) / 2 for min_val, max_val in zip(fila_min, fila_max)]
                for fila_min, fila_max in zip(heatmap_data_min, heatmap_data_max)
            ]

            df_heatmap_matriz = pd.DataFrame(
                heatmap_data_promedio,
                index=list(escenarios_precio.keys()),
                columns=escenarios_rinde_nombres
            )

            # CREAR ESCALA DE COLORES CENTRADA EN CERO
            valores = df_heatmap_matriz.values.flatten()
            valor_max = np.max(np.abs(valores))

            colorscale = [
                [0.0, '#C62828'],    # Rojo intenso (muy negativo)
                [0.25, '#E57373'],   # Rojo claro
                [0.4, '#FFCDD2'],    # Rosa muy claro
                [0.475, '#F5F5F5'],  # Gris muy claro
                [0.5, '#FAFAFA'],    # Casi blanco (cero)
                [0.525, '#FAFAFA'],  # Casi blanco (cero)
                [0.55, '#E8F5E9'],   # Verde casi blanco
                [0.65, '#81C784'],   # Verde suave
                [0.8, '#4CAF50'],    # Verde material
                [1.0, '#388E3C']     # Verde oscuro (muy positivo)
            ]

            # Crear anotaciones para mostrar RANGOS en cada celda
            annotations = []
            for i, y_label in enumerate(df_heatmap_matriz.index):
                for j, x_label in enumerate(df_heatmap_matriz.columns):
                    resultado_min = heatmap_data_min[i][j]
                    resultado_max = heatmap_data_max[i][j]
                    margen_min = margenes_data_min[i][j]
                    margen_max = margenes_data_max[i][j]
                    
                    # Texto a mostrar: rango de resultado y rango de margen
                    texto = f"<b>${resultado_min:.0f}-{resultado_max:.0f}MM</b><br>{margen_min:+.0f}% - {margen_max:+.0f}%"
                    
                    annotations.append(
                        dict(
                            x=x_label,
                            y=y_label,
                            text=texto,
                            showarrow=False,
                            font=dict(
                                size=11,
                                color='black',
                                family='Arial, sans-serif'
                            ),
                            xref='x',
                            yref='y'
                        )
                    )

            # Crear el heatmap con plotly
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=df_heatmap_matriz.values,
                x=df_heatmap_matriz.columns,
                y=df_heatmap_matriz.index,
                colorscale=colorscale,
                zmid=0,
                hovertext=hover_data,
                hoverinfo='text',
                showscale=True,
                colorbar=dict(
                    title="Resultado<br>Promedio<br>($MM)",
                    tickformat="$,.0f",
                    ticksuffix="MM",
                    len=0.7
                )
            ))

            fig_heatmap.update_layout(
                annotations=annotations,
                xaxis_title="<b>Escenario de Rinde</b>",
                yaxis_title="<b>Escenario de Precio</b>",
                xaxis=dict(
                    side='top',
                    tickfont=dict(size=12, color='black'),
                    title_standoff=10
                ),
                yaxis=dict(
                    tickfont=dict(size=12, color='black')
                ),
                height=400,
                font=dict(size=12),
                margin=dict(t=50, b=0, l=100, r=100)
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)

            # Estadísticas rápidas
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            # Encontrar mejor y peor escenario (usando valores máximos y mínimos)
            mejor_resultado = max([max(fila) for fila in heatmap_data_max])
            peor_resultado = min([min(fila) for fila in heatmap_data_min])
            
            # Encontrar índices
            for i in range(len(heatmap_data_max)):
                for j in range(len(heatmap_data_max[i])):
                    if heatmap_data_max[i][j] == mejor_resultado:
                        mejor_margen = margenes_data_max[i][j]
                    if heatmap_data_min[i][j] == peor_resultado:
                        peor_margen = margenes_data_min[i][j]

            # Contar escenarios positivos
            escenarios_positivos = sum(1 for fila_min in heatmap_data_min for val in fila_min if val > 0)
            total_escenarios = len(heatmap_data_min) * len(heatmap_data_min[0])

            col1.metric(
                label="Mejor Escenario", 
                value=f"${mejor_resultado:,.1f}MM", 
                delta=f"{mejor_margen:+.1f}% Margen"
            )

            col2.metric(
                label="Peor Escenario", 
                value=f"${peor_resultado:,.1f}MM", 
                delta=f"{peor_margen:+.1f}% Margen",
                delta_color="normal"
            )

            col3.metric(
                label="Escenarios Positivos", 
                value=f"{escenarios_positivos}/{total_escenarios}", 
                delta=f"{escenarios_positivos/total_escenarios*100:.0f}% del total",
                delta_color="off"
            )

                    
            mapeo_cultivos_csv = {
            "Trigo": "Trigo total",
            "Maíz": "Maíz",
            "Soja 1ra": "Soja 1ra",
            "Soja 2da": "Soja 2da",
            "Girasol": "Girasol",
            "Sorgo": "Sorgo",
            "Cebada": "Cebada"}

            # AGREGAR TABLA RESUMEN DE AÑOS POR ESCENARIO
            with st.expander("📅 Ver rindes históricos por campaña, departamento y cultivo"):
                st.markdown("**Rindes históricos de las últimas campañas (en toneladas/ha)**")
                st.markdown("*Las celdas están coloreadas según el escenario de rendimiento para cada cultivo y departamento*")
                
                # Definir colores para cada escenario (misma paleta del heatmap)
                colores_escenarios = {
                    'Muy Bajo': '#C62828',
                    'Bajo': '#E57373',
                    'Normal': '#C5E1A5',
                    'Alto': '#4CAF50',
                    'Muy Alto': '#388E3C'
                }
                
                # Mapeo de cultivos
                mapeo_cultivos_csv = {
                    "Trigo": "Trigo total",
                    "Maíz": "Maíz",
                    "Soja 1ra": "Soja 1ra",
                    "Soja 2da": "Soja 2da",
                    "Girasol": "Girasol",
                    "Sorgo": "Sorgo",
                    "Cebada": "Cebada"
                }
                
                # Cargar datos históricos
                url = "https://raw.githubusercontent.com/Jthl1986/T1/main/Estimaciones11.csv"
                dfr = pd.read_csv(url, encoding='ISO-8859-1', sep=',')
                
                # Obtener todos los departamentos únicos del planteo
                if df_referencia is not None and not df_referencia.empty:
                    departamentos_unicos = df_referencia['Departamento'].unique()
                    
                    # Crear estructura para almacenar todos los datos
                    datos_completos = []
                    columnas_nombres = []  # Cambio: usaremos nombres simples en lugar de tuplas
                    
                    # Iterar por cada departamento
                    for departamento in sorted(departamentos_unicos):
                        # Obtener provincia para este departamento
                        if 'Provincia' in df_referencia.columns:
                            provincia = df_referencia[df_referencia['Departamento'] == departamento]['Provincia'].iloc[0]
                        else:
                            provincia = getattr(st.session_state, 'provincia_seleccionada', '')
                        
                        # Obtener cultivos de este departamento
                        cultivos_dept = df_referencia[df_referencia['Departamento'] == departamento]['Cultivo'].unique()
                        
                        # Iterar por cada cultivo
                        for cultivo in sorted(cultivos_dept):
                            cultivo_csv = mapeo_cultivos_csv.get(cultivo, cultivo)
                            
                            # Filtrar datos históricos
                            filtro = (dfr['Provincia'] == provincia) & \
                                    (dfr['Departamento'] == departamento) & \
                                    (dfr['Cultivo'] == cultivo_csv)
                            df_hist = dfr[filtro].copy()
                            
                            if not df_hist.empty and len(df_hist) >= 5:
                                # Calcular percentiles para este cultivo/departamento
                                rendimientos = df_hist['Rendimiento'].astype(float).values
                                p10 = np.percentile(rendimientos, 10)
                                p25 = np.percentile(rendimientos, 25)
                                p75 = np.percentile(rendimientos, 75)
                                p90 = np.percentile(rendimientos, 90)
                                
                                # Crear diccionario de campaña -> (rinde, escenario)
                                datos_cultivo_dept = {}
                                for _, row_hist in df_hist.iterrows():
                                    rend = float(row_hist['Rendimiento']) / 1000
                                    campaña = str(row_hist['Campaña']).strip()
                                    
                                    # Clasificar en escenario
                                    if row_hist['Rendimiento'] <= p10:
                                        escenario = 'Muy Bajo'
                                    elif p10 < row_hist['Rendimiento'] <= p25:
                                        escenario = 'Bajo'
                                    elif p25 < row_hist['Rendimiento'] <= p75:
                                        escenario = 'Normal'
                                    elif p75 < row_hist['Rendimiento'] <= p90:
                                        escenario = 'Alto'
                                    else:
                                        escenario = 'Muy Alto'
                                    
                                    datos_cultivo_dept[campaña] = {
                                        'rinde': rend,
                                        'escenario': escenario
                                    }
                                
                                datos_completos.append(datos_cultivo_dept)
                                # Crear nombre de columna como string: "Departamento - Cultivo"
                                columnas_nombres.append(f"{departamento} - {cultivo}")
                            else:
                                datos_completos.append({})
                                columnas_nombres.append(f"{departamento} - {cultivo}")
                    
                    # Obtener todas las campañas únicas
                    todas_campañas = set()
                    for datos in datos_completos:
                        todas_campañas.update(datos.keys())
                    
                    # Filtrar campañas que tienen al menos un dato
                    campañas_con_datos = []
                    for campaña in todas_campañas:
                        tiene_datos = any(campaña in datos for datos in datos_completos)
                        if tiene_datos:
                            campañas_con_datos.append(campaña)
                    
                    campañas_ordenadas = sorted(campañas_con_datos)
                    
                    # Crear DataFrame con nombres simples de columnas
                    if campañas_ordenadas and columnas_nombres:
                        # Crear matriz de datos (rindes)
                        matriz_rindes = []
                        matriz_escenarios = []
                        
                        for campaña in campañas_ordenadas:
                            fila_rindes = []
                            fila_escenarios = []
                            
                            for datos in datos_completos:
                                if campaña in datos:
                                    fila_rindes.append(datos[campaña]['rinde'])
                                    fila_escenarios.append(datos[campaña]['escenario'])
                                else:
                                    fila_rindes.append(np.nan)
                                    fila_escenarios.append(None)
                            
                            matriz_rindes.append(fila_rindes)
                            matriz_escenarios.append(fila_escenarios)
                        
                        # Crear DataFrame principal con columnas simples
                        df_tabla = pd.DataFrame(
                            matriz_rindes,
                            index=campañas_ordenadas,
                            columns=columnas_nombres
                        )
                        
                        # Crear DataFrame auxiliar con escenarios
                        df_escenarios = pd.DataFrame(
                            matriz_escenarios,
                            index=campañas_ordenadas,
                            columns=columnas_nombres
                        )
                        
                        # Función para aplicar colores según escenario
                        def aplicar_colores(val, escenario):
                            if pd.isna(val) or escenario is None:
                                return 'background-color: #E0E0E0; color: gray'
                            
                            color = colores_escenarios.get(escenario, '#FFFFFF')
                            texto_color = 'black' if escenario in ['Normal', 'Bajo', 'Alto'] else 'white'
                            
                            return f'background-color: {color}; color: {texto_color}; font-weight: bold'
                        
                        # Aplicar estilo
                        def style_table(row):
                            campaña = row.name
                            idx = campañas_ordenadas.index(campaña)
                            
                            estilos = []
                            for i in range(len(columnas_nombres)):
                                val = row.iloc[i]
                                escenario = df_escenarios.iloc[idx, i]
                                estilos.append(aplicar_colores(val, escenario))
                            
                            return estilos
                        
                        styled_tabla = df_tabla.style.apply(style_table, axis=1).format(
                            '{:.2f}',
                            na_rep='-'
                        )
                        
                        # Mostrar tabla
                        st.dataframe(styled_tabla, use_container_width=True, height=600)
                        
                        # Leyenda
                        st.markdown("---")
                        st.markdown("**Leyenda de colores: Escenarios**")
                        col1, col2, col3, col4, col5 = st.columns(5)
                        
                        with col1:
                            st.markdown(f"<div style='background-color: {colores_escenarios['Muy Bajo']}; padding: 10px; border-radius: 5px; text-align: center; color: white; font-weight: bold'>Muy Bajo (≤P10)</div>", unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"<div style='background-color: {colores_escenarios['Bajo']}; padding: 10px; border-radius: 5px; text-align: center; color: black; font-weight: bold'>Bajo (P10-P25)</div>", unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f"<div style='background-color: {colores_escenarios['Normal']}; padding: 10px; border-radius: 5px; text-align: center; color: black; font-weight: bold'>Normal (P25-P75)</div>", unsafe_allow_html=True)
                        
                        with col4:
                            st.markdown(f"<div style='background-color: {colores_escenarios['Alto']}; padding: 10px; border-radius: 5px; text-align: center; color: white; font-weight: bold'>Alto (P75-P90)</div>", unsafe_allow_html=True)
                        
                        with col5:
                            st.markdown(f"<div style='background-color: {colores_escenarios['Muy Alto']}; padding: 10px; border-radius: 5px; text-align: center; color: white; font-weight: bold'>Muy Alto (≥P90)</div>", unsafe_allow_html=True)
                        
                        # Estadísticas resumidas
                        st.markdown("---")
                        st.markdown("**📊 Estadísticas por Departamento y Cultivo:**")
                        
                        stats_data = []
                        for col_name in columnas_nombres:
                            col_data = df_tabla[col_name].dropna()
                            escenarios_col = df_escenarios[col_name].dropna()
                            
                            if len(col_data) > 0:
                                # Separar departamento y cultivo del nombre de columna
                                partes = col_name.split(' - ')
                                dept = partes[0] if len(partes) > 0 else col_name
                                cultivo = partes[1] if len(partes) > 1 else ''
                                
                                stats_data.append({
                                    'Departamento': dept,
                                    'Cultivo': cultivo,
                                    'Rinde Promedio': f"{col_data.mean():.2f} tn/ha",
                                    'Rinde Mín': f"{col_data.min():.2f} tn/ha",
                                    'Rinde Máx': f"{col_data.max():.2f} tn/ha",
                                    'Campañas': len(col_data),
                                    'Escenario más frecuente': escenarios_col.mode()[0] if len(escenarios_col.mode()) > 0 else '-'
                                })
                        
                        df_stats = pd.DataFrame(stats_data)
                        st.dataframe(df_stats, hide_index=True, use_container_width=True)
                    else:
                        st.warning("No hay suficientes datos históricos para mostrar la tabla")
                else:
                    st.warning("No hay datos del planteo para mostrar rindes históricos")

    # CÓDIGO A AGREGAR EN APP5 DESPUÉS DEL EXPANDER DE RINDES HISTÓRICOS

        # AGREGAR TABLA DE FUTUROS Y RANGOS DE PRECIOS
        st.markdown("---")
        st.markdown("### 💰 Futuros Utilizados y Rangos de Precios por Escenario")

        # Definir los meses de los futuros para cada cultivo
        meses_futuros = {
            'Trigo': 'ENERO',
            'Cebada': 'ENERO',
            'Girasol': 'FEBRERO',
            'Maíz': 'ABRIL',
            'Sorgo': 'ABRIL',
            'Soja 1ra': 'MAYO',
            'Soja 2da': 'MAYO'
        }

        # Mapeo de cultivos a variables de precio (de app4)
        mapeo_cultivos_variables = {
            "Soja 1ra": "psoja1",
            "Soja 2da": "psoja2",
            "Trigo": "ptrigo",
            "Maíz": "pmaiz",
            "Girasol": "pgirasol",
            "Sorgo": "psorgo",
            "Cebada": "pcebada"
        }

        # Obtener cultivos únicos del planteo cargado
        if df_referencia is not None and not df_referencia.empty:
            cultivos_cargados = df_referencia['Cultivo'].unique()
            
            # Obtener precios base desde las variables cargadas en app4
            # Las variables están en st.session_state desde app4
            variables_dict = {}
            if hasattr(st.session_state, 'dfp_normal'):
                # Intentar obtener las variables desde session_state
                # O leerlas nuevamente desde el CSV
                try:
                    df_variables = pd.read_csv('https://raw.githubusercontent.com/Jthl1986/T1/main/variablessep25vf1.csv')
                    for _, row in df_variables.iterrows():
                        variables_dict[row['variable']] = row['valor']
                except:
                    # Valores por defecto si no se pueden cargar
                    variables_dict = {
                        'psoja1': 300,
                        'psoja2': 300,
                        'ptrigo': 190,
                        'pmaiz': 175,
                        'pgirasol': 330,
                        'psorgo': 160,
                        'pcebada': 165
                    }
            
            # Obtener precios base desde las variables
            precios_base = {}
            for cultivo in cultivos_cargados:
                variable_precio = mapeo_cultivos_variables.get(cultivo)
                if variable_precio:
                    precios_base[cultivo] = variables_dict.get(variable_precio, 0)
            
            # Precios de referencia (los que antes eran "base" en el código original)
            precios_referencia = {
                'Trigo': 190,
                'Cebada': 165,
                'Girasol': 330,
                'Maíz': 180,
                'Sorgo': 160,
                'Soja 1ra': 315,
                'Soja 2da': 315
            }
            
            # Crear datos de la tabla solo para cultivos cargados
            datos_futuros = []
            for cultivo in sorted(cultivos_cargados):
                precio_base = precios_base.get(cultivo, 0)
                precio_bajo = precio_base * 0.92
                precio_alto = precio_base * 1.08
                
                datos_futuros.append({
                    'Cultivo': cultivo,
                    'Futuro': meses_futuros.get(cultivo, '-'),
                    'Precio Futuro Actual (u$s/tn)': f"${precio_base:.0f}",
                    'Escenario Bajo': f"≤ ${precio_bajo:.0f}",
                    'Escenario Normal': f"${precio_bajo:.0f} - ${precio_alto:.0f}",
                    'Escenario Alto': f"≥ ${precio_alto:.0f}"
                })
            
            if datos_futuros:
                df_futuros = pd.DataFrame(datos_futuros)
                
                # Función para aplicar estilo a la tabla
                def highlight_precio_actual(row):
                    # Resaltar la columna "Precio Futuro Actual" en verde
                    styles = [''] * len(row)
                    styles[2] = 'background-color: #4CAF50; color: white; font-weight: bold'  # Precio Futuro Actual
                    return styles
                
                # Aplicar estilo
                styled_futuros = df_futuros.style.apply(highlight_precio_actual, axis=1)
                
                # Mostrar tabla
                st.dataframe(styled_futuros, hide_index=True, use_container_width=True)
                
                # Texto explicativo simple
                st.markdown("*Los precios futuros actuales corresponden a los valores utilizados en los cálculos del heatmap*")
            else:
                st.warning("No hay cultivos cargados en el planteo")
        else:
            st.warning("No hay datos del planteo para mostrar los futuros")

        # Crear tabla comparativa
        st.markdown("### 📊 Comparativa de escenarios con las cotizaciones actuales de granos")
        
        # Calcular totales para cada escenario
        escenarios_data = []
        
        for nombre_escenario, df_escenario in [
            ("Muy Bajo (P10)", dfp_muy_bajo), 
            ("Bajo (P10-P25)", dfp_bajo), 
            ("Normal (P25-P75)", dfp_normal), 
            ("Alto (P75-P90)", dfp_alto),
            ("Muy Alto (P90+)", dfp_muy_alto)
        ]:
            if df_escenario is not None and not df_escenario.empty:
                ingtotal_esc = df_escenario['Ingreso'].sum()
                costtotal_esc = df_escenario['Costos directos'].sum()
                gctotal_esc = df_escenario['Gastos comercialización'].sum()
                mbtotal_esc = df_escenario['Margen bruto'].sum()
                
                if df1 is not None:
                    arrend = st.session_state.df1[0]
                    gas = st.session_state.df1[1]
                    result_esc = int(mbtotal_esc)-int(arrend)-int(gas)
                    result_net = (result_esc/ingtotal_esc)*100
                else:
                    arrend = 0
                    gas = 0
                    result_esc = mbtotal_esc
                
                escenarios_data.append({
                    'Escenario': nombre_escenario,
                    'Ingreso Total': ingtotal_esc,
                    'Costos Directos': costtotal_esc,
                    'Gastos Comercialización': gctotal_esc,
                    'Margen Bruto': mbtotal_esc,
                    'Arrendamiento': arrend,
                    'Gastos Estructura': gas,
                    'Resultado Final': result_esc,
                    'Margen neto': result_net
                })
        
        if escenarios_data:
            df_comparativa = pd.DataFrame(escenarios_data)
            
            # Formatear la tabla
            st.dataframe(df_comparativa.style.format({
                'Ingreso Total': '${:,.0f}',
                'Costos Directos': '${:,.0f}',
                'Gastos Comercialización': '${:,.0f}',
                'Margen Bruto': '${:,.0f}',
                'Arrendamiento': '${:,.0f}',
                'Gastos Estructura': '${:,.0f}',
                'Resultado Final': '${:,.0f}',
                'Margen neto': '{:.1f}%'
            }),
            hide_index=True)

                        
        # Barras y gráficos en tres columnas
        left, right = st.columns(2)
        # Agrupar por Cultivo y Departamento
        df_grouped = df_referencia.groupby(['Cultivo', 'Departamento'])['Superficie (has)'].sum().reset_index()

        colors = px.colors.qualitative.Plotly
        fig_stacked = px.bar(
            df_grouped, 
            x='Cultivo', 
            y='Superficie (has)', 
            color='Departamento',
            color_discrete_sequence=colors,
            title="Superficie por Cultivo por Departamento",
            labels={'Superficie (has)': 'Superficie (ha)'}
        )
        fig_stacked.update_layout(
            margin=dict(t=40, b=0),
            barmode='stack'  # Barras apiladas
        )
        left.plotly_chart(fig_stacked, use_container_width=True)
        
        #GRAFICO DE TORTA
        df_sunburst = df_referencia.groupby(['Campos     ', 'Departamento'])['Superficie (has)'].sum().reset_index()
        df_sunburst['Campos_clean'] = df_sunburst['Campos     '].str.strip()

        # Crear mapa de colores completo
        color_discrete_map = {
            'Propios': '#2E7D32',
            'Arrendados': '#d73027',
            'Aparcería': '#1565C0'
        }

        fig_sunburst = px.sunburst(
            df_sunburst,
            path=['Campos_clean', 'Departamento'],
            values='Superficie (has)',
            color='Campos_clean',
            color_discrete_map=color_discrete_map,
            title="Distribución: <br>Tipo de Campo → Localidad"
        )

        fig_sunburst.update_traces(
            textinfo='label+percent parent',
            textfont=dict(size=12, color='black')
        )

        fig_sunburst.update_layout(margin=dict(t=40, b=0))
        right.plotly_chart(fig_sunburst, use_container_width=True)
        
        # COLUMNA 3: Tabla Campaña Fina/Gruesa (MOVIDA AQUÍ)
        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Campaña Fina',
            x=df_totales['Concepto'],
            y=df_totales['Campaña Fina'],
            text=df_totales['Campaña Fina'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside',
            marker_color='#667eea',
            textfont=dict(size=11)
        ))

        fig.add_trace(go.Bar(
            name='Campaña Gruesa',
            x=df_totales['Concepto'],
            y=df_totales['Campaña Gruesa'],
            text=df_totales['Campaña Gruesa'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside',
            marker_color='#d73027',
            textfont=dict(size=11)
        ))

        fig.update_layout(
                    barmode='group',
                    height=450,
                    # Configuración detallada del título
                    title={
                        'text': 'Comparación <br>Campaña Fina vs Gruesa',
                        'y': 0.95,          # Lo sube un poco más (1 es el tope)
                        'x': 0.5,           # Lo centra horizontalmente
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': dict(size=18)
                    },
                    # AJUSTE DE MÁRGENES: El valor 't' le da aire al título
                    margin=dict(t=120, b=50, l=50, r=50), 
                    
                    xaxis_title='',
                    yaxis_title='Monto ($)',
                    # Ajustamos la leyenda para que no choque con el título centrado
                    legend=dict(
                        orientation="h", 
                        yanchor="bottom", 
                        y=1.02, 
                        xanchor="center", # Centrada también para armonía visual
                        x=0.5
                    ),
                    hovermode='x unified'
                )

        st.plotly_chart(fig, use_container_width=True)
        
        # AGREGAR PESTAÑAS CON TODOS LOS ESCENARIOS AL FINAL
        st.subheader("📊 Detalle por Escenario de Rendimiento")
        
        # Crear pestañas para los 5 escenarios
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📉 Muy Bajo", "📊 Bajo", "⚖️ Normal", "📈 Alto", "🚀 Muy Alto"])

        with tab1:
            st.markdown("**Escenario Muy Bajo (hasta P10)**")
            st.dataframe(dfp_muy_bajo.style.format({
                "Superficie (has)": "{:.0f}", 
                "Rinde": "{:.2f}", 
                "Ingreso": "${:,}", 
                "Costos directos": "${:,}", 
                "Gastos comercialización": "${:,}", 
                "Margen bruto": "${:,}", 
                "RindeRegion": "{:.2f}", 
                "RindeIndif": "{:.2f}"
            }))
            

        with tab2:
            st.markdown("**Escenario Bajo (P10-P25)**")
            st.dataframe(dfp_bajo.style.format({
                "Superficie (has)": "{:.0f}", 
                "Rinde": "{:.2f}", 
                "Ingreso": "${:,}", 
                "Costos directos": "${:,}", 
                "Gastos comercialización": "${:,}", 
                "Margen bruto": "${:,}", 
                "RindeRegion": "{:.2f}", 
                "RindeIndif": "{:.2f}"
            }))
            


        with tab3:
            st.markdown("**Escenario Normal (P25-P75)**")
            st.dataframe(dfp_normal.style.format({
                "Superficie (has)": "{:.0f}", 
                "Rinde": "{:.2f}", 
                "Ingreso": "${:,}", 
                "Costos directos": "${:,}", 
                "Gastos comercialización": "${:,}", 
                "Margen bruto": "${:,}", 
                "RindeRegion": "{:.2f}", 
                "RindeIndif": "{:.2f}"
            }))
            

        with tab4:
            st.markdown("**Escenario Alto (P75-P90)**")
            st.dataframe(dfp_alto.style.format({
                "Superficie (has)": "{:.0f}", 
                "Rinde": "{:.2f}", 
                "Ingreso": "${:,}", 
                "Costos directos": "${:,}", 
                "Gastos comercialización": "${:,}", 
                "Margen bruto": "${:,}", 
                "RindeRegion": "{:.2f}", 
                "RindeIndif": "{:.2f}"
            }))
            

        with tab5:
            st.markdown("**Escenario Muy Alto (P90+)**")
            st.dataframe(dfp_muy_alto.style.format({
                "Superficie (has)": "{:.0f}", 
                "Rinde": "{:.2f}", 
                "Ingreso": "${:,}", 
                "Costos directos": "${:,}", 
                "Gastos comercialización": "${:,}", 
                "Margen bruto": "${:,}", 
                "RindeRegion": "{:.2f}", 
                "RindeIndif": "{:.2f}"
            }))
            
        
        css()

        if dfp is not None and df1 is None:
            st.write ("Sin planteo productivo o falta cargar gastos de estructura")
            
        if dfs is not None or dfx is not None or dfa is not None:
            if (dfs is not None and dfx is not None) or (dfs is not None and dfa is not None) or (dfx is not None and dfa is not None):
                valuacion_total = st.session_state.dfs['Valuación'].sum()
                st.subheader(f"Existencia de granos: ${valuacion_total:,}")
                st.table(dfs.style.format({"Cantidad (tn)":"{:.0f}", "Valuación":"${:,}"}))
            if dfx is not None:
                valuacion_total = st.session_state.dfx["Ingreso estimado"].sum()
                st.subheader(f"Ingresos Serv. agrícolas: ${valuacion_total:,}")
                st.table(dfx.style.format({"Superficie(ha)":"{:.0f}", "Precio":"${:,}", "Ingreso estimado":"${:,}"}))
            if dfa is not None:
                valuacion_total = st.session_state.dfa['Valuación'].sum()
                st.subheader(f"Existencia de hacienda: ${valuacion_total:,}")
                st.table(dfa.style.format({"Cantidad":"{:.0f}", "Peso":"{:.0f}", "Valuación":"${:,}"}))

#configuraciones de página   
#lottie_book = load_lottieurl('https://assets7.lottiefiles.com/packages/lf20_d7OjnJ.json')
with st.sidebar:
    url = "https://raw.githubusercontent.com/Jthl1986/T1/master/logo.png"
    st.markdown(f'<div style="margin-top: -140px;"><img src="{url}" style="object-fit: cover; width: 100%; height: 100%;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 style="margin-top: -110px; text-align: center;">AgroApp</h1>', unsafe_allow_html=True)
my_button = st.sidebar.radio("Modulos",('Planteo productivo', 'Riesgo climático', 'Tenencia granos', 'Tenencia hacienda', 'Servicios agrícolas', 'Sitios de utilidad', 'Cuadro resumen'))
if my_button == 'Tenencia hacienda':
    app()
elif my_button == 'Tenencia granos':
    app1()
elif my_button == 'Servicios agrícolas':
    app2()
elif my_button == 'Riesgo climático':
    app3()
elif my_button == 'Sitios de utilidad':
    app9()
elif my_button == 'Cuadro resumen':
    app5()
else:    
    app4()
  
rss_url = "https://bichosdecampo.com/feed/"
rss_url1 = "https://www.infocampo.com.ar/feed/"
rss_url2 = "https://www.clarin.com/rss/rural/"
feed = feedparser.parse(rss_url)
feed1 = feedparser.parse(rss_url1)
feed2 = feedparser.parse(rss_url2)



with st.sidebar:
    st.markdown("---")
    st.markdown('<h4 style="margin-top: -25px; text-align: left;">Noticias</h4>', unsafe_allow_html=True)
    with st.spinner('Cargando noticias...'):
        news_html = ""
        for item in feed["items"][:10]:
            news_html += f'<a href="{item["link"]}" target="_blank">{item["title"]}</a> | '
        st.components.v1.html(f'<marquee behavior="scroll" direction="left" scrollamount="6">{news_html}</marquee>', height=30)
    with st.spinner('Cargando noticias...'):
        news_html = ""
        for item in feed1["items"][:10]:
            news_html += f'<a href="{item["link"]}" target="_blank">{item["title"]}</a> | '
        st.components.v1.html(f'<marquee behavior="scroll" direction="left" scrollamount="4">{news_html}</marquee>', height=30)
    with st.spinner('Cargando noticias...'):
        news_html = ""
        for item in feed2["items"][:10]:
            news_html += f'<a href="{item["link"]}" target="_blank">{item["title"]}</a> | '
        st.components.v1.html(f'<marquee behavior="scroll" direction="left" scrollamount="2">{news_html}</marquee>', height=30)
    st.markdown("---")
    # Enlace al que quieres que lleve al hacer clic en "JSaborido"
    link_jsaborido = "https://www.magyp.gob.ar/sitio/areas/analisis_economico/margenes/"#https://docs.google.com/spreadsheets/d/1CzxbLmVj8oT_dBilAjbxBRRR6oYNsM30TmFMp5VGjEU/edit?usp=sharing
# Usar HTML en st.markdown para incluir el enlace sin que se note la diferencia en estilo
    st.caption("""
    Desarrollado por JSantacecilia  y JSaborido
    para Equipo Agro 
    """, unsafe_allow_html=True)
    st.caption("Datos del Informe Septiembre 2025 SAGYP")
    abrir_google_maps()
    #st_lottie(lottie_book, speed=0.5, height=50, key="initial")
