/*{# https://openlayersbook.github.io/ch02-key-concepts-in-openlayers/example-02.html  #}*/
window.API = window.API || {}
API.omap_layout = function(data) {
    let {lon, lat, zoom, mapid} = data;
    lat = +lat
    lon = +lon
    zoom = +zoom
    const map = new ol.Map({
        target: 'map-' + mapid,
        layers: [
            new ol.layer.Tile({
            source: new ol.source.OSM()
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([lon,lat]),
            zoom: zoom
        })
    });

    const popup = new ol.Overlay({
        element: document.getElementById('overlay-'+mapid),
        positioning: 'bottom-center'
    });
    popup.setPosition(ol.proj.fromLonLat([lon,lat]));
    map.addOverlay(popup);
}