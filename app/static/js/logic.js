const ATTRIBUTION = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
const URL_TEMPLATE = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}';
const M_DARK = L.tileLayer(URL_TEMPLATE, { attribution: ATTRIBUTION, maxZoom: 18, id: 'mapbox/dark-v10', accessToken: API_KEY});
const M_GRAYSCALE = L.tileLayer(URL_TEMPLATE, { attribution: ATTRIBUTION, maxZoom: 18, id: 'mapbox/light-v10', accessToken: API_KEY});
const M_OUTDOORS = L.tileLayer(URL_TEMPLATE, { attribution: ATTRIBUTION, maxZoom: 18, id: 'mapbox/outdoors-v11', accessToken: API_KEY});
const BASE_MAPS = {"Dark": M_DARK, "GrayScale": M_GRAYSCALE, "Outdoors": M_OUTDOORS};
const MY_MAP = L.map("map", {center: [19.2558, -99.0759], zoom: 8.5, layers:[M_DARK, M_GRAYSCALE, M_OUTDOORS]});
const vmapJson = "/vw_map"
const vmarks = '/datos_alt'


function getMarkers(data){

  cities = []
  data.forEach(element => {
    let city = L.marker(element.Location).bindPopup(`<h3> ${element.PRECIO} </h3><hr> <a href="${element.URL}"> Visitar publicacion </a>`)
    cities.push(city)
  });

  cities = L.layerGroup(cities);
  return cities;
}


function getCloro(data, valueProp, lowColow, highColor, title, symbol) {
  
    let layer = L.choropleth(data, {
        
        valueProperty: valueProp,
        scale: [lowColow, highColor],
        steps: 10,
        mode: "e",
        style: {
          // Border color
          color: "#fff",
          weight: 1,
          fillOpacity: 0.8
        },
        onEachFeature:(feature, layer) => {layer.bindPopup(`<h2>${feature.properties.ESTADO}</h2>
                                                <h3>Municipio: ${feature.properties.MUNICIPIO}</h3>
                                                <h4> ${title} </h4>
                                                <hr>
                                                <p>
                                               <strong>${new Intl.NumberFormat("mx-ES").format(feature.properties[valueProp])}${symbol} </strong></br>
                                               </p> `);}   



    
    }); 

    return layer;
  }

function getStates(data) {
  
  function chooseColor(codedo) {
    switch (codedo) {
    case 9:
      return "#e7e125";
    case 13:
      return "#85af16";
    case 15:
      return "#16af9c";
    case 17:
      return "#2535a7";
    case 21:
      return "#6025a7";
    case 29:
      return "#d03166";
    }
  }

    let layer = L.geoJSON(data, {
        

        
        style: (feature) => {return {opacity: 0.95, 
                                     fillOpacity: 0.60, 
                                     color: "gray",
                                     fillColor: chooseColor(feature.properties.COD_ESTADO),
                                      stroke: true, 
                                      weight: 0.75}},
        onEachFeature:(feature, layer) => {layer.bindPopup(`<h2>${feature.properties.ESTADO}</h2>
                                                <h3>Municipio: ${feature.properties.MUNICIPIO}</h3>
                                                <h4> # Propiedades: ${feature.properties.NUMERO}</h4>
                                            <hr>
                                            <p>
                  
                                               Precio:  <strong>${ new Intl.NumberFormat("mx-ES").format(feature.properties.PRECIO)} M.N </strong></br>
                                               Precio TerrenoM2:  <strong>${ new Intl.NumberFormat("mx-ES").format(feature.properties.PRECIO_M2)} M.N </strong></br>
                                               Precio Construccion M2:  <strong>${ new Intl.NumberFormat("mx-ES").format(feature.properties.PRECIO_CM2)} M.N </strong>
                                               </p> `);}   
    
    }); 

    return layer;
  }



  Promise.all([d3.json(vmapJson), d3.json(vmarks)]).then((data) =>{

    let markets = getMarkers(data[1])
    let states = getStates(data[0])
    let prices = getCloro(data[0], "PRECIO_M2","#b0baf0", "#00157e", "PRECIO PROMEDIO DEL METRO CUADRADO", " M.N")
    let pib = getCloro(data[0], "PIB","#ddccff", "#220066", "PIB PROMEDIO DE LA REGION", " ")
    let idh = getCloro(data[0], "IDH","#d2fad1", "#005908", "INDICE DE DESARROLLO HUMANO", " ")
    let no_vivienda = getCloro(data[0], "NUMERO","#f4d9c7", "#cf5200", "NUMERO DE PROPIEDADES EVALUADAS", " Unidades")
    let overlayMaps = {"States": states, "Prices":prices,"PIB":pib, "IDH":idh, "# Propiedades":no_vivienda, "Marcadores":markets};

    L.control.layers(BASE_MAPS,overlayMaps).addTo(MY_MAP);

    
});