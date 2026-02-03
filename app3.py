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
url = "https://raw.githubusercontent.com/Jthl1986/T1/main/Estimaciones.csv"
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
    ternero=tabla[0:5] 
    novillito=tabla[5:7]
    ternera=tabla[7:11]
    vaquillona=tabla[11:14]
    vaca=tabla[22:23]  
    fecha=  "Semana: 15/12/2025 al 19/12/2025" #(tabla[25:26].values)[0][0] #el predeterminado es 25:26 
    ternero160=int(ternero.promedio[0][2:6])
    ternero180=int(ternero.promedio[1][2:6])
    ternero200=int(ternero.promedio[2][2:6])
    ternero230=int(ternero.promedio[3][2:6])
    novillo260=int(novillito.promedio[5][2:6])
    novillo300=int(novillito.promedio[6][2:6])
    ternera150=int(ternera.promedio[7][2:6])
    ternera170=int(ternera.promedio[8][2:6])
    ternera190=int(ternera.promedio[9][2:6])
    ternera210=int(ternera.promedio[10][2:6])
    vaquillona250=int(vaquillona.promedio[11][2:6])
    vaquillona290=int(vaquillona.promedio[12][2:6])
    vaquillona291=int(vaquillona.promedio[13][2:6])
    vacas= 738704 #int(vaca.promedio[22][2:8])
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
fecha1 = pizarra_data["fecha"] #"11/04/2024" #   Sacar fecha y numeral y tabular

# Asignar los valores a las variables con los nombres personalizados
pptrigo = valores_rosario["pptrigo"]    
ppsoja = valores_rosario["ppsoja"]     
ppmaiz = valores_rosario["ppmaiz"]     
ppgirasol = valores_rosario["ppgirasol"] 
ppsorgo = valores_rosario["ppsorgo"]     


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
    st.title("⛅️ Riesgo climático (en construcción)")


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
    def obtener_arrend(region, tipo, cantidad):
        # Verificar si la región y el cultivo existen en el diccionario
        if region in arrend_por_region_cultivo and tipo in arrend_por_region_cultivo[region]:
            return cantidad * arrend_por_region_cultivo[region][tipo]
        else:
            return "Región o cultivo no encontrados en la lista"
    
    if 'arrenda' not in st.session_state:
        st.session_state.arrenda = []
        
    def arrendamiento():
        resultado = obtener_arrend(region, tipo, cantidad)
        resultado = round(resultado * dol, 2)
        st.session_state.arrenda.append(resultado)

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
        return gasto*precio*rinde
    

    if 'aparceria_value' not in st.session_state:
        st.session_state.aparceria_value = 0
############FORMULARIO DE CARGA        
    center.write("Completar:")

        # SELECTBOX FUERA DEL FORM (actualización instantánea)
    st.session_state.tipo_cultivo_form = center.selectbox(
        'Tipo de cultivo: ', 
        ["Soja 1ra", "Soja 2da", "Trigo", "Maíz", "Girasol", "Sorgo", "Cebada"],
        key="selectbox_cultivo_instant"
    )
    tipo = st.session_state.tipo_cultivo_form
    
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
    propio = form.selectbox('Campos: ', ["Propios","Arrendados","Aparcería"])   
    cantidad = form.number_input("Superficie (has): ", step=1)   

    on = left.toggle("Rinde automático", value=True)

#PRUEBA    
        
    with left.expander("Análisis de Rendimientos"):
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
            
    if not on:
        rinde = form.number_input("Rendimiento informado (en tn)")

    submit = form.form_submit_button("Ingresar")
     
    # Inicializar lista de departamentos cargados si no existe
    if 'departamentos_cargados' not in st.session_state:
        st.session_state.departamentos_cargados = []

    aparceria = st.session_state.aparceria_value / 100 if st.session_state.aparceria_value > 0 else 0

    # Modificar la sección donde se hace submit para guardar el departamento
    if submit:
        if propio == "Aparcería" and aparceria == 0:
            st.warning("Falta completar porcentaje de aparcería")
        else:
            # AGREGAR ESTA LÍNEA PARA GUARDAR EL DEPARTAMENTO
            if st.session_state.departamento_seleccionado not in st.session_state.departamentos_cargados:
                st.session_state.departamentos_cargados.append(st.session_state.departamento_seleccionado)

    # CORRECCIÓN AQUÍ:
    if on:
        # Obtener el diccionario con los 3 rindes
        rindes = rindeautomatico(tipo)  # Devuelve {'bajo': X, 'normal': Y, 'alto': Z}
        # Usar el rinde normal para cálculos principales
        rinde = float(rindes['normal'])
        
    right.write("Cuadro gastos (se completa solo una vez):")
    form2 = right.form("template_form2") 
    aparceria_input = form2.number_input("Porcentaje de aparcería (si falta el dato, sugerido 60%)", step=1)
    aparceria = aparceria_input/100

    rindeprom = round(float(obtener_rind(region, tipo)),2)
    precio = float(obtener_precio(tipo))
    costo = float(obtener_costo(region,tipo))
    gasto = float(obtener_gasvar(region,tipo))
    rindeinf = round(float((costo + arrendamiento_inf() + ges_inf() + gc_inf())/ precio),2)

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
            # AGREGAR ESTA LÍNEA PARA GUARDAR EL DEPARTAMENTO
            if st.session_state.departamento_seleccionado not in st.session_state.departamentos_cargados:
                st.session_state.departamentos_cargados.append(st.session_state.departamento_seleccionado)
            
            if on:
                if 'rindes' not in locals() and 'rindes' not in globals():
                    rindes = rindeautomatico(tipo)
                
                # Generar datos para los 5 escenarios
                datos_muy_bajo = lista(float(rindes['muy_bajo']))
                datos_bajo = lista(float(rindes['bajo']))
                datos_normal = lista(float(rindes['normal']))
                datos_alto = lista(float(rindes['alto']))
                datos_muy_alto = lista(float(rindes['muy_alto']))
                
                # Agregar a los DataFrames correspondientes - AHORA CON PROVINCIA
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
                
            else:
                # Para rinde manual, usar el mismo valor en los 5 escenarios
                datos_manual = lista(float(rinde))
                dfo_manual = pd.DataFrame([datos_manual], columns=('Región                    ', 'Provincia', 'Departamento', 'Campos     ','Cultivo', 'Superficie (has)', 'Rinde', 'Ingreso', 'Costos directos','Gastos comercialización', 'Margen bruto', 'RindeRegion', 'RindeIndif'))
                
                st.session_state.dfp_muy_bajo = pd.concat([st.session_state.dfp_muy_bajo, dfo_manual])
                st.session_state.dfp_bajo = pd.concat([st.session_state.dfp_bajo, dfo_manual])
                st.session_state.dfp_normal = pd.concat([st.session_state.dfp_normal, dfo_manual])
                st.session_state.dfp_alto = pd.concat([st.session_state.dfp_alto, dfo_manual])
                st.session_state.dfp_muy_alto = pd.concat([st.session_state.dfp_muy_alto, dfo_manual])

        
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

    # BOTÓN BORRAR ÚLTIMA FILA 
    delete_last_row = st.button("Borrar última fila")
    if delete_last_row:
        borrar_ultima_fila_completa()  # Usa la nueva función que borra los 3 DataFrames

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
                            st.markdown(f"- % Aparcería: {aparceria*100:.0f}%")
                            st.markdown("*(En aparcería, ingresos y costos se comparten según porcentaje)*")
                    
                    st.divider()
                    
                    # Mostrar cálculo paso a paso
                    st.markdown("**Cálculo paso a paso:**")
                    
                    # Cálculo de ingresos
                    if row['Campos     '].strip() == "Aparcería":
                        ingreso_base = precio_actual * dol * row['Rinde'] * row['Superficie (has)']
                        ingreso_final = ingreso_base * aparceria
                        st.markdown(f"1. **Ingreso base**: u$s {precio_actual:,.2f}/tn × {dol} × {row['Rinde']} tn/ha × {row['Superficie (has)']} ha = ${ingreso_base:,.0f}")
                        st.markdown(f"2. **Ajuste por aparcería**: ${ingreso_base:,.0f} × {aparceria*100:.0f}% = **${ingreso_final:,.0f}**")
                    else:
                        ingreso_final = precio_actual * dol * row['Rinde'] * row['Superficie (has)']
                        st.markdown(f"1. **Ingreso**: u$s {precio_actual:,.2f}/tn × {dol} × {row['Rinde']} tn/ha × {row['Superficie (has)']} ha = **${ingreso_final:,.0f}**")
                    
                    # Cálculo de costos directos
                    if row['Campos     '].strip() == "Aparcería":
                        costo_base = costo_actual * dol * row['Superficie (has)']
                        costo_final = costo_base * aparceria
                        st.markdown(f"3. **Costo directo base**: u$s {costo_actual:,.2f}/ha × {dol} × {row['Superficie (has)']} ha = ${costo_base:,.0f}")
                        st.markdown(f"4. **Ajuste por aparcería**: ${costo_base:,.0f} × {aparceria*100:.0f}% = **${costo_final:,.0f}**")
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
               
        if submit:
            if propio == "Propios":
                gastos_estructura1()
            else:
                gastos_estructura2()
        
        if st.session_state.dfp_normal is not None:
            heca_arrendados = st.session_state.dfp_normal.loc[st.session_state.dfp_normal['Campos     '] == 'Arrendados', 'Superficie (has)'].sum()
            hecp_propios = st.session_state.dfp_normal.loc[st.session_state.dfp_normal['Campos     '] == 'Propios', 'Superficie (has)'].sum()
            hecp_aparceria = st.session_state.dfp_normal.loc[st.session_state.dfp_normal['Campos     '] == 'Aparcería', 'Superficie (has)'].sum()
            heca = heca_arrendados + hecp_aparceria
            hecp = hecp_propios
            nro_hectareas = heca + hecp
    
            if nro_hectareas > 0:
                gastos = sum(st.session_state.gespr) + sum(st.session_state.gesar)
                gestimado = gastos
                            
         
    if submit:
        if propio == "Arrendados":
            arrendamiento()
    
    arrenda_resultante = sum(st.session_state.arrenda)
    gestimado_str = "${:,.0f}".format(gestimado)
    arrend_str = "${:,.0f}".format(arrenda_resultante )
    arrendamiento = form2.number_input(f"Gastos de arrendamiento - Estimador: {arrend_str} - {arrend_por_region_cultivo[region][tipo] / psoja1 * 10:.1f} qq/ha", step=1)
    gast = form2.number_input(f"Gastos de estructura - Estimador: {gestimado_str}", step=1)
    submit2 = form2.form_submit_button("Ingresar")
    
    if submit2:
        st.session_state.aparceria_value = aparceria_input
        st.session_state.df1 = [arrendamiento, gast, aparceria]
    

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
        costototal = "${:,.0f}".format(costtotal)
        margenn = result/ingtotal
        margenn_porcentaje = "{:.0%}".format(margenn)
        granos = "${:,.0f}".format(valuacion_total)

        col1, col2, col3, col4 = st.columns(4)  
        
        col1.metric(label="Superficie has (con rotación)", value=df_referencia["Superficie (has)"].sum())
        col2.metric(label="Arrendamiento", value='${:,}'.format(arrend))
        col3.metric(label="Costo directo", value=costototal)
        col4.metric(label="Tenencia de granos", value= granos)

        # MOSTRAR TABLA COMPARATIVA DE LOS 5 ESCENARIOS
        if hay_escenarios:
            # Crear tabla comparativa
            st.markdown("### 📊 Comparativa de Escenarios")
            
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
                
            # AGREGAR HEATMAP CON RESULTADO FINAL (NETO) Y AÑOS DE CAMPAÑA
            st.markdown("### 🔥 Heatmap de Resultado Final por Escenario y Cultivo")

            # Preparar datos para el heatmap
            heatmap_data = []
            escenarios_list = [
                ("Muy Bajo", dfp_muy_bajo),
                ("Bajo", dfp_bajo),
                ("Normal", dfp_normal),
                ("Alto", dfp_alto),
                ("Muy Alto", dfp_muy_alto)
            ]

            # Obtener lista única de cultivos
            cultivos = df_referencia['Cultivo'].unique()

            # Cargar datos históricos para mapear años a escenarios
            url = "https://raw.githubusercontent.com/Jthl1986/T1/main/Estimaciones8.csv"
            dfr = pd.read_csv(url, encoding='ISO-8859-1', sep=',')

            for cultivo in cultivos:
                fila = {'Cultivo': cultivo}
                
                for escenario_nombre, df_escenario in escenarios_list:
                    if df_escenario is not None and not df_escenario.empty:
                        cultivo_data = df_escenario[df_escenario['Cultivo'] == cultivo]
                        if not cultivo_data.empty:
                            # Obtener totales del escenario completo para calcular proporción
                            ingreso_total_escenario = df_escenario['Ingreso'].sum()
                            margen_total_escenario = df_escenario['Margen bruto'].sum()
                            
                            # Calcular margen bruto del cultivo
                            margen_cultivo = cultivo_data['Margen bruto'].sum()
                            superficie = cultivo_data['Superficie (has)'].sum()
                            
                            # Calcular resultado final total del escenario
                            resultado_final_total = margen_total_escenario - arrend - gas
                            
                            # Calcular proporción del cultivo en el resultado final
                            if margen_total_escenario > 0:
                                proporcion_cultivo = margen_cultivo / margen_total_escenario
                            else:
                                proporcion_cultivo = 0
                            
                            # Asignar resultado final proporcionalmente
                            resultado_final_cultivo = resultado_final_total * proporcion_cultivo
                            
                            if superficie > 0:
                                resultado_ha = resultado_final_cultivo 
                                fila[escenario_nombre] = resultado_ha
                            else:
                                fila[escenario_nombre] = 0
                        else:
                            fila[escenario_nombre] = 0
                
                heatmap_data.append(fila)

            df_heatmap = pd.DataFrame(heatmap_data)
            df_heatmap = df_heatmap.set_index('Cultivo')

            # NUEVA FUNCIÓN: Obtener años que corresponden a cada escenario para MÚLTIPLES departamentos
            def obtener_años_escenario_multi(cultivo, dfr, df_referencia):
                """
                Retorna un diccionario con los años de campaña que corresponden a cada escenario
                considerando TODOS los departamentos donde se cultivó este cultivo
                """
                mapeo_cultivos_csv = {
                    "Trigo": "Trigo total",
                    "Maíz": "Maíz",
                    "Soja 1ra": "Soja 1ra",
                    "Soja 2da": "Soja 2da",
                    "Girasol": "Girasol",
                    "Sorgo": "Sorgo",
                    "Cebada": "Cebada"
                }

                cultivo_csv = mapeo_cultivos_csv.get(cultivo, cultivo)
                años_por_escenario = {
                    'Muy Bajo': {},
                    'Bajo': {},
                    'Normal': {},
                    'Alto': {},
                    'Muy Alto': {}
                }

                # Obtener TODOS los departamentos donde se cultivó este cultivo
                cultivo_data = df_referencia[df_referencia['Cultivo'] == cultivo]
                
                if cultivo_data.empty:
                    return años_por_escenario
                
                # Obtener departamentos únicos
                departamentos_cultivo = cultivo_data['Departamento'].unique()
                
                # Procesar cada departamento
                for departamento in departamentos_cultivo:
                    # Obtener provincia para este departamento
                    if 'Provincia' in cultivo_data.columns:
                        provincia = cultivo_data[cultivo_data['Departamento'] == departamento]['Provincia'].iloc[0]
                    else:
                        # Fallback a session_state
                        if hasattr(st.session_state, 'provincia_seleccionada'):
                            provincia = st.session_state.provincia_seleccionada
                        else:
                            continue
                    
                    # Filtrar datos históricos para este departamento específico
                    filtro = (dfr['Provincia'] == provincia) & \
                            (dfr['Departamento'] == departamento) & \
                            (dfr['Cultivo'] == cultivo_csv)
                    df_hist = dfr[filtro].copy()
                    
                    if df_hist.empty or len(df_hist) < 5:
                        continue
                    
                    # Convertir rendimientos a float
                    rendimientos = df_hist['Rendimiento'].astype(float).values
                    campañas = df_hist['Campaña'].values
                    
                    # Calcular percentiles para este departamento
                    p10 = np.percentile(rendimientos, 10)
                    p25 = np.percentile(rendimientos, 25)
                    p75 = np.percentile(rendimientos, 75)
                    p90 = np.percentile(rendimientos, 90)
                    
                    # Clasificar cada año en su escenario
                    for i, rend in enumerate(rendimientos):
                        campaña = str(campañas[i])
                        
                        if rend <= p10:
                            escenario = 'Muy Bajo'
                        elif p10 < rend <= p25:
                            escenario = 'Bajo'
                        elif p25 < rend <= p75:
                            escenario = 'Normal'
                        elif p75 < rend <= p90:
                            escenario = 'Alto'
                        else:
                            escenario = 'Muy Alto'
                        
                        # Almacenar por departamento
                        if departamento not in años_por_escenario[escenario]:
                            años_por_escenario[escenario][departamento] = []
                        años_por_escenario[escenario][departamento].append(campaña)
                
                return años_por_escenario

            # Obtener todos los departamentos únicos de los DataFrames de escenarios
            departamentos_seleccionados = []
            for _, df_escenario in escenarios_list:
                if df_escenario is not None and not df_escenario.empty and 'Departamento' in df_escenario.columns:
                    departamentos_seleccionados.extend(df_escenario['Departamento'].unique().tolist())

            # Eliminar duplicados y mantener orden
            departamentos_seleccionados = list(dict.fromkeys(departamentos_seleccionados))

            # Si no se encontraron departamentos en los escenarios, usar el de session_state
            if not departamentos_seleccionados:
                if hasattr(st.session_state, 'departamento_seleccionado'):
                    departamentos_seleccionados = [st.session_state.departamento_seleccionado]
                else:
                    departamentos_seleccionados = []

            # Crear texto personalizado para el heatmap con años
            customdata = []
            hover_text = []

            for cultivo in df_heatmap.index:
                fila_custom = []
                fila_hover = []
                
                # Obtener años para este cultivo en TODOS los departamentos
                # CAMBIO: Pasar df_referencia en lugar de lista de departamentos
                años_dict = obtener_años_escenario_multi(cultivo, dfr, df_referencia)
                
                for escenario in df_heatmap.columns:
                    valor = df_heatmap.loc[cultivo, escenario]
                    
                    # Obtener años de este escenario por departamento
                    años_por_dept = años_dict.get(escenario, {})
                    
                    if años_por_dept:
                        # Construir texto con años organizados por departamento
                        texto_depts = []
                        for dept, años in años_por_dept.items():
                            años_unicos = sorted(set(años))
                            texto_depts.append(f"{dept}: {', '.join(años_unicos)}")
                        
                        años_str = "<br>".join(texto_depts)
                        texto_hover = f"{escenario}<br>Resultado: ${valor:,.0f}MM<br><b>Años por departamento:</b><br>{años_str}"
                    else:
                        texto_hover = f"{escenario}<br>Resultado: ${valor:,.0f}MM<br>Sin datos históricos"
                    
                    fila_custom.append(años_por_dept)
                    fila_hover.append(texto_hover)
                
                customdata.append(fila_custom)
                hover_text.append(fila_hover)

            # Crear el heatmap con plotly (Resultado Final en $/ha)
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=df_heatmap.values,
                x=df_heatmap.columns,
                y=df_heatmap.index,
                colorscale='RdYlGn',
                text=df_heatmap.values,
                texttemplate='$%{text:,.0f}MM',
                textfont={"size": 12},
                colorbar=dict(title="$MM"),
                hovertext=hover_text,
                hoverinfo='text',
                customdata=customdata
            ))

            fig_heatmap.update_layout(
                title="Resultado Final (Neto) por Escenario (en millones)<br><sub>Con indicaciones de campañas que han entrado en dichos escenarios por localidad</sub>",
                xaxis_title="Escenario",
                yaxis_title="Cultivo",
                height=400 + (len(cultivos) * 30)
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)

            mapeo_cultivos_csv = {
            "Trigo": "Trigo total",
            "Maíz": "Maíz",
            "Soja 1ra": "Soja 1ra",
            "Soja 2da": "Soja 2da",
            "Girasol": "Girasol",
            "Sorgo": "Sorgo",
            "Cebada": "Cebada"}

            # AGREGAR TABLA RESUMEN DE AÑOS POR ESCENARIO
            with st.expander("📅 Ver detalle de años por escenario, cultivo y departamento"):
                st.markdown("**Años de campaña históricos clasificados por escenario de rendimiento:**")
                st.markdown("*Las campañas están ordenadas cronológicamente y coloreadas según su escenario*")
                
                # Definir colores para cada escenario
                colores_escenarios = {
                    'Muy Bajo': '#d73027',      # Rojo
                    'Bajo': '#fc8d59',          # Naranja
                    'Normal': '#fee08b',        # Amarillo
                    'Alto': '#91cf60',          # Verde claro
                    'Muy Alto': '#1a9850'       # Verde oscuro
                }
                
                for cultivo in df_heatmap.index:
                    st.markdown(f"### {cultivo}")
                    
                    # Usar el cultivo actual para mapeo
                    cultivo_csv = mapeo_cultivos_csv.get(cultivo, cultivo)
                    
                    # CAMBIO IMPORTANTE: Obtener TODOS los departamentos donde se cultivó este cultivo
                    # Usar df_referencia que es dfp_normal o dfp según disponibilidad
                    cultivo_data = df_referencia[df_referencia['Cultivo'] == cultivo]
                    
                    if cultivo_data.empty:
                        st.warning(f"No hay datos para {cultivo}")
                        continue
                    
                    # CORRECCIÓN PRINCIPAL: Obtener TODOS los departamentos únicos para este cultivo
                    departamentos_cultivo = cultivo_data['Departamento'].unique()
                    
                    # Procesar cada departamento
                    for departamento in departamentos_cultivo:
                        st.markdown(f"#### 📍 {departamento}")
                        
                        # Obtener la provincia (puede variar según departamento)
                        if 'Provincia' in cultivo_data.columns:
                            # Si existe columna Provincia, usarla
                            provincia = cultivo_data[cultivo_data['Departamento'] == departamento]['Provincia'].iloc[0]
                        else:
                            # Si no existe, usar session_state
                            if hasattr(st.session_state, 'provincia_seleccionada'):
                                provincia = st.session_state.provincia_seleccionada
                            else:
                                st.warning(f"No se puede determinar la provincia para {departamento}")
                                continue
                        
                        # Filtrar datos históricos para este departamento específico
                        filtro = (dfr['Provincia'] == provincia) & \
                                (dfr['Departamento'] == departamento) & \
                                (dfr['Cultivo'] == cultivo_csv)
                        df_hist = dfr[filtro].copy()
                        
                        if not df_hist.empty and len(df_hist) >= 5:
                            # Convertir rendimientos a float y calcular percentiles
                            rendimientos = df_hist['Rendimiento'].astype(float).values
                            
                            p10 = np.percentile(rendimientos, 10)
                            p25 = np.percentile(rendimientos, 25)
                            p75 = np.percentile(rendimientos, 75)
                            p90 = np.percentile(rendimientos, 90)
                            
                            # Crear lista de campañas con su escenario
                            campañas_data = []
                            for idx, row_hist in df_hist.iterrows():
                                rend = float(row_hist['Rendimiento'])
                                campaña = str(row_hist['Campaña'])
                                
                                # Clasificar en escenario
                                if rend <= p10:
                                    escenario = 'Muy Bajo'
                                elif p10 < rend <= p25:
                                    escenario = 'Bajo'
                                elif p25 < rend <= p75:
                                    escenario = 'Normal'
                                elif p75 < rend <= p90:
                                    escenario = 'Alto'
                                else:
                                    escenario = 'Muy Alto'
                                
                                campañas_data.append({
                                    'Campaña': campaña,
                                    'Rendimiento (kg/ha)': int(rend),
                                    'Rendimiento (tn/ha)': round(rend/1000, 2),
                                    'Escenario': escenario
                                })
                            
                            # Crear DataFrame y ordenar cronológicamente
                            df_campañas = pd.DataFrame(campañas_data)
                            df_campañas = df_campañas.sort_values('Campaña')
                            
                            # Función para aplicar color de fondo según escenario
                            def color_escenario(row):
                                color = colores_escenarios.get(row['Escenario'], '#ffffff')
                                return [f'background-color: {color}; color: black' if col != 'Escenario' 
                                    else f'background-color: {color}; color: black; font-weight: bold' 
                                    for col in row.index]
                            
                            # Aplicar estilo y mostrar
                            styled_df = df_campañas.style.apply(color_escenario, axis=1).format({
                                'Rendimiento (kg/ha)': '{:,.0f}',
                                'Rendimiento (tn/ha)': '{:.2f}'
                            })
                            
                            st.dataframe(styled_df, hide_index=True, use_container_width=True)
                            
                            # Resumen estadístico
                            st.markdown("**Resumen por escenario:**")
                            resumen_data = df_campañas.groupby('Escenario').agg({
                                'Campaña': 'count',
                                'Rendimiento (tn/ha)': ['min', 'max', 'mean']
                            }).round(2)
                            resumen_data.columns = ['Cantidad de años', 'Rinde mín (tn/ha)', 'Rinde máx (tn/ha)', 'Rinde prom (tn/ha)']
                            
                            # Ordenar por escenario
                            orden_escenarios = ['Muy Bajo', 'Bajo', 'Normal', 'Alto', 'Muy Alto']
                            resumen_data = resumen_data.reindex([e for e in orden_escenarios if e in resumen_data.index])
                            
                            st.dataframe(resumen_data, use_container_width=True)
                            
                        else:
                            st.warning(f"No hay suficientes datos históricos para {cultivo} en {departamento}, {provincia}")
                        
                        st.markdown("---")  # Separador entre departamentos

                        
        st.write(f"**Aclaraciones del cálculo:** Los rindes utilizados para la proyección corresponden a los promedios históricos por localidad para las últimas campañas (desde 2013/2014 a 2024/2025) segmentadas por percentiles para la determinación de escenarios. Los gastos de arrendamiento y estructura fueron estimados según datos proporcionados por SAGYP")
        
        # Barras y gráficos en tres columnas
        left, middle, right = st.columns(3)
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
            title="Distribución: Tipo de Campo → Departamento"
        )

        fig_sunburst.update_traces(
            textinfo='label+percent parent',
            textfont=dict(size=12)
        )

        fig_sunburst.update_layout(margin=dict(t=40, b=0))
        middle.plotly_chart(fig_sunburst, use_container_width=True)
        
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
            title_text='Comparación Campaña Fina vs Gruesa',
            title_font_size=18,
            xaxis_title='',
            yaxis_title='Monto ($)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )

        right.plotly_chart(fig, use_container_width=True)
        
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
