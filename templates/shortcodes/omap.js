/*{# https://openlayersbook.github.io/ch02-key-concepts-in-openlayers/example-02.html  #}*/
API.omap_layout = function(data) {
    let {lon, lat, z, mapid} = data;
    lat = +lat
    lon = +lon
    z = +z
    const map = new ol.Map({
        target: 'map-' + mapid,
        layers: [
            new ol.layer.Tile({
            source: new ol.source.OSM()
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([lon,lat]),
            zoom: z
        })
    });

    const popup = new ol.Overlay({
        element: document.getElementById('overlay-'+mapid),
        positioning: 'bottom-center'
    });
    popup.setPosition(ol.proj.fromLonLat([lon,lat]));
    map.addOverlay(popup);
}