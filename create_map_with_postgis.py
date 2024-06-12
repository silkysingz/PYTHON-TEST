import folium

# Create a map object centered around a location
mymap = folium.Map(location=[13.332465, -16.701183], zoom_start=12.0)

# Add base maps
folium.TileLayer('cartodbdark_matter').add_to(mymap)  # Black base map
folium.TileLayer('cartodbpositron').add_to(mymap)     # Black and white base map
folium.TileLayer('openstreetmap').add_to(mymap)       # OpenStreetMap base map

# Define the GeoServer WMS URL
wms_url = 'http://localhost:8085/geoserver/mastersthesis_2023/wms'

# Define the layer names and corresponding titles for the layer switcher
layer_info = [
    ('mastersthesis_2023:gba_lcr_1983_1993', 'Land Cover 1983-1993'),
    ('mastersthesis_2023:gba_lcr_1993_2003', 'Land Cover 1993-2003'),
    ('mastersthesis_2023:gba_lcr_2003_2013', 'Land Cover 2003-2013'),
    ('mastersthesis_2023:gba_lcr_2013_2023', 'Land Cover 2013-2023'),
    ('GMBLULC:gmb_lulc_2017_2018', 'Land Cover 2017-2018'),
    # Add more layer names and titles as needed
]

# Add each WMS layer to the map
for layer_name, title in layer_info:
    wms_layer = folium.raster_layers.WmsTileLayer(
        url=wms_url,
        layers=layer_name,
        fmt='image/png',
        transparent=True,
        overlay=True,
        name=title,  # Set the title for the layer switcher
    )
    wms_layer.add_to(mymap)

# Create a custom HTML control for switching GeoServer layers
layer_select_html = """
<div style="position: fixed; top: 10px; right: 10px; z-index: 1000; background-color: white; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);">
    <select id="layer-select">
        <option value="" disabled selected>Select Layer</option>
        <option value="mastersthesis_2023:gba_lcr_1983_1993">Land Cover 1983-1993</option>
        <option value="mastersthesis_2023:gba_lcr_1993_2003">Land Cover 1993-2003</option>
        <option value="mastersthesis_2023:gba_lcr_2003_2013">Land Cover 2003-2013</option>
        <option value="mastersthesis_2023:gba_lcr_2013_2023">Land Cover 2013-2023</option>
        <option value="GMBLULC:gmb_lulc_2017_2018">Land Cover 2017-2018</option>
    </select>
</div>
<script>
    document.getElementById('layer-select').addEventListener('change', function() {
        var selectedLayer = this.value;
        var layers = document.querySelectorAll('.leaflet-control-layers-overlays input');
        layers.forEach(function(layer) {
            if (layer.value === selectedLayer) {
                layer.checked = true;
            } else {
                layer.checked = false;
            }
        });
    });
</script>
"""

# Add the custom HTML control to the map
mymap.get_root().html.add_child(folium.Element(layer_select_html))

# Add legend with colors matching the map layers
legend_html = """
<div style="position: fixed; bottom: 10px; right: 10px; z-index: 1000; background-color: white; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);">
    <h3>Legend</h3>
    <p><strong>Land Cover 1983-1993</strong>: <span style="background-color: #ff0000; padding: 2px 8px; border-radius: 3px; color: white;">Legend content for this layer</span></p>
    <p><strong>Land Cover 1993-2003</strong>: <span style="background-color: #00ff00; padding: 2px 8px; border-radius: 3px; color: white;">Legend content for this layer</span></p>
    <p><strong>Land Cover 2003-2013</strong>: <span style="background-color: #0000ff; padding: 2px 8px; border-radius: 3px; color: white;">Legend content for this layer</span></p>
    <p><strong>Land Cover 2013-2023</strong>: <span style="background-color: #ffff00; padding: 2px 8px; border-radius: 3px; color: white;">Legend content for this layer</span></p>
    <p><strong>Land Cover 2017-2018</strong>: <span style="background-color: #ff00ff; padding: 2px 8px; border-radius: 3px; color: white;">Legend content for this layer</span></p>
</div>
"""

# Add the legend HTML to the map
mymap.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
map_path = 'wms_map.html'
mymap.save(map_path)

print(f'Map saved to {map_path}')
