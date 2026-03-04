import requests
import folium

url_parkings_static = "https://data.angers.fr/api/explore/v2.1/catalog/datasets/angers_stationnement/records?limit=20"
url_parkings_dynamic = "https://data.angers.fr/api/explore/v2.1/catalog/datasets/parking-angers/records?limit=20"
url_citiz_info = "https://backend.citiz.fr/public/provider/7/gbfs/v3.0/station_information.json"
url_citiz_status = "https://backend.citiz.fr/public/provider/7/gbfs/v3.0/station_status.json"

parkings_static = requests.get(url_parkings_static).json()['results']
parkings_dynamic = requests.get(url_parkings_dynamic).json()['results']
citiz_info = requests.get(url_citiz_info).json()['data']['stations']
citiz_status = requests.get(url_citiz_status).json()['data']['stations']

correspondance = [
    ("49007-P-006", "Ralliement"), ("49007-P-008", "Larrey"), ("49007-P-013", "Saint Serge Patinoire"),
    ("49007-P-017", "Quai"), ("49007-P-005", "Saint Laud 2"), ("49007-P-010", "Mail"),
    ("49007-P-015", "Leclerc"), ("49007-P-003", "Republique"), ("49007-P-004", "Confluences"),
    ("49007-P-007", "Mitterrand Maine"), ("49007-P-012", "Haras Public"), ("49007-P-014", "Moliere"),
    ("49007-P-018", "Maternite"), ("49007-P-001", "Berges De Maine"), ("49007-P-002", "Mitterrand Rennes"),
    ("49007-P-009", "Bressigny"), ("49007-P-011", "Saint Laud"), ("49007-P-016", "Marengo")
]

dict_parkings = {p['id']: p for p in parkings_static}
dict_dispo_p = {p['nom']: p['disponible'] for p in parkings_dynamic}
dict_dispo_c = {s['station_id']: s['num_vehicles_available'] for s in citiz_status}

angers_map = folium.Map(location=[47.471, -0.552], zoom_start=14)

for id_p, nom_d in correspondance:
    if id_p in dict_parkings and nom_d in dict_dispo_p:
        p = dict_parkings[id_p]
        dispo = dict_dispo_p[nom_d]
        color = 'green' if dispo > 50 else 'orange' if dispo >= 15 else 'red'
        
        folium.Marker(
            location=[float(p['ylat']), float(p['xlong'])],
            popup="Parking " + p['nom'] + " : " + str(dispo) + " places",
            tooltip=p['nom'],
            icon=folium.Icon(color=color, icon='square-parking', prefix='fa')
        ).add_to(angers_map)

for s in citiz_info:
    nb_dispo = dict_dispo_c.get(s['station_id'], 0)
    nom_c = s['name'][0]['text']
    color = 'blue' if nb_dispo > 0 else 'lightgray'
    
    folium.Marker(
        location=[s['lat'], s['lon']],
        popup="Station Citiz " + nom_c + " : " + str(nb_dispo) + " voitures disponibles.",
        tooltip=nom_c,
        icon=folium.Icon(color=color, icon='car', prefix='fa')
    ).add_to(angers_map)

angers_map.save('parking_angers_complet.html')