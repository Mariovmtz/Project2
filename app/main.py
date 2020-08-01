from flask import Flask, render_template, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Integer, Column
from app import config as cfg
import json


app = Flask(__name__)

engine = create_engine(cfg.DATABASE_URL)
m = MetaData(schema='dbo')
Base = automap_base(metadata=m)
Table('vw_datos_estado',m, Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine)
Table('vw_datos_municipio',m, Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine)
Table('vw_map',m, Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine)
Table('vw_records',m, Column('id', Integer, primary_key=True), autoload=True, autoload_with=engine)

Base.prepare(engine, reflect=True)


#House_prices = Base.classes.house_prices
#Indicadores = Base.classes.indicadores
datos_coords = Base.classes.house_prices_alt
VW_Datos_Estado = Base.classes.vw_datos_estado
VW_Datos_Municipio = Base.classes.vw_datos_municipio
VW_Map = Base.classes.vw_map
VW_Records = Base.classes.vw_records

session = Session(engine)


@app.route("/house_prices")
def get_source_ds():
    result = session.query(VW_Records).all()
    recordlist = []
    for ele in result:
        tmpdict = {}
        tmpdict["COD_ESTADO"] = ele.c_estado
        tmpdict["TIPO_ASENTAMIENTO"] = ele.c_tipo_asenta
        tmpdict["ESTADO"] = ele.c_mnpio
        tmpdict["CIUDAD"] = ele.ciudad
        tmpdict["MUNICIPIO"] = ele.municipio
        tmpdict["COLONIA"] = ele.colonia
        tmpdict["PRECIO"] = ele.precio
        tmpdict["SUPERFICIE_TOTAL"] = ele.supeficie_t
        tmpdict["SUPERFICIE_CONSTRUIDA"] = ele.supeficie_c
        tmpdict["RECAMARAS"] = ele.recamaras
        tmpdict["BANOS"] = ele.banos
        tmpdict["ESTACIONAMIENTOS"] = ele.estacionamientos


        recordlist.append(tmpdict)
        response = jsonify(recordlist)
        response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/vw_datos_estado")
def get_vw_datos_estado():
    result = session.query(VW_Datos_Estado).all()
    recordlist = []
    for ele in result:
        tmpdict = {}
        tmpdict["COD_ESTADO"] = ele.c_estado
        tmpdict["ESTADO"] = ele.estado
        tmpdict["PROM_IDH"] = ele.prom_idh
        tmpdict["PROM_INDICE_SALUD"] = ele.prom_indice_salud
        tmpdict["PROM_INDICE_INGRESO"] = ele.prom_indice_ingreso
        tmpdict["PROM_INDICE_EDUCACION"] = ele.prom_indice_educacion
        tmpdict["SUM_FEMINICIDIOS"] = ele.sum_feminicidios
        tmpdict["SUM_HOMICIDIOS"] = ele.sum_homicidios
        tmpdict["SUM_ROBOS"] = ele.sum_robos
        tmpdict["SUM_LESIONES"] = ele.sum_lesiones
        tmpdict["SUM_ABUSO_SEXUAL"] = ele.sum_abuso_sexual
        tmpdict["SUM_SECUESTRO"] = ele.sum_secuestro
        tmpdict["NO_INMUEBLES"] = ele.no_inmuebles
        tmpdict["PROM_PRECIO"] = ele.prom_precio
        tmpdict["PROM_TERRENO"] = ele.prom_terreno
        tmpdict["PROM_CONSTRUCCION"] = ele.prom_construccion
        tmpdict["PROM_RECAMARAS"] = ele.prom_recamaras

        recordlist.append(tmpdict)
        response = jsonify(recordlist)
        response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/vw_datos_municipio")
def get_vw_datos_municipio():
    result = session.query(VW_Datos_Municipio).all()
    recordlist = []
    #print(result[0].__dict__.keys())
    for ele in result:
        tmpdict = {}
        tmpdict["COD_ESTADO"] = ele.c_estado
        tmpdict["ESTADO"] = ele.estado
        tmpdict["COD_MUNICIPIO"] = ele.c_mnpio
        tmpdict["MUNICIPIO"] = ele.municipio
        tmpdict["PROM_IDH"] = ele.prom_idh
        tmpdict["PROM_INDICE_SALUD"] = ele.prom_indice_salud
        tmpdict["PROM_INDICE_INGRESO"] = ele.prom_indice_ingreso
        tmpdict["PROM_INDICE_EDUCACION"] = ele.prom_indice_educacion
        tmpdict["SUM_FEMINICIDIOS"] = ele.sum_feminicidios
        tmpdict["SUM_HOMICIDIOS"] = ele.sum_homicidios
        tmpdict["SUM_ROBOS"] = ele.sum_robos
        tmpdict["SUM_LESIONES"] = ele.sum_lesiones
        tmpdict["SUM_ABUSO_SEXUAL"] = ele.sum_abuso_sexual
        tmpdict["SUM_SECUESTRO"] = ele.sum_secuestro
        tmpdict["NO_INMUEBLES"] = ele.no_inmuebles
        tmpdict["PROM_PRECIO"] = ele.prom_precio
        tmpdict["PROM_TERRENO"] = ele.prom_terreno
        tmpdict["PROM_CONSTRUCCION"] = ele.prom_construccion
        tmpdict["PROM_RECAMARAS"] = ele.prom_recamaras


        recordlist.append(tmpdict)
        response = jsonify(recordlist)
        response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/vw_map")
def get_vw_map():
    result = session.query(VW_Map).all()
    recordlist = []
    geoJson = {}
    geoJson["type"] = "FeatureCollection"
    geoJson["crs"] = { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } }
    geoJson["features"] = []

    for ele in result:
        tmpdict = {}
        tmpdict["type"] = "Feature"
        tmpdict["properties"] = {}
        tmpdict["properties"]["COD_ESTADO"] = ele.c_estado
        tmpdict["properties"]["ESTADO"] = ele.estado
        tmpdict["properties"]["COD_MUNICIPIO"] = ele.c_mnpio
        tmpdict["properties"]["MUNICIPIO"] = ele.municipio
        tmpdict["properties"]["IDH"] = ele.prom_idh
        tmpdict["properties"]["PIB"] = ele.prom_ingreso
        tmpdict["properties"]["PRECIO"] = ele.prom_precio
        tmpdict["properties"]["PRECIO_M2"] = ele.prom_precio_m2
        tmpdict["properties"]["PRECIO_CM2"] = ele.prom_precioc_m2
        tmpdict["properties"]["NUMERO"] = ele.numero_propiedades
        tmpdict["geometry"] = {}
        tmpdict["geometry"]["type"] = ele.ctype
        tmpdict["geometry"]["coordinates"] = json.loads(ele.coords)
        geoJson["features"].append(tmpdict)

    return(geoJson)
    #pprint.pprint(result)

@app.route("/datos_alt")
def datos_alt():
    result = session.query(datos_coords.lat, datos_coords.lon, datos_coords.url, datos_coords.precio).all()
    recordlist = []
    #print(result[0].__dict__.keys())
    for ele in result:
        tmpdict = {}
        tmpdict["Location"] = [ele.lat, ele.lon]
        tmpdict["URL"] = ele.url
        tmpdict["PRECIO"] = ele.precio
 
        recordlist.append(tmpdict)
        response = jsonify(recordlist)
        response.headers.add("Access-Control-Allow-Origin", "*")
    return response





@app.route("/")
def index():
    #pagetitle = "Analysis: Housing prices in Mexico"
    #pagecontent = "Please select an option to explore our dataset"

    return render_template("index.html")

@app.route("/map")
def map():

    return render_template("map.html")

@app.route("/graph")
def graph():


    return render_template("graph.html")

@app.route("/data")
def data():


    return render_template("data.html")
@app.route("/about")
def about():


    return render_template("about.html")

    