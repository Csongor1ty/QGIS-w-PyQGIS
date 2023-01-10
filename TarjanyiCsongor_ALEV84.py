#Tarjanyi Csongor - ALEV84
#7. feladat

#a)
varosLayer = QgsProject.instance().mapLayersByName("varosokMasolt")[0]
pontokLayer = QgsProject.instance().mapLayersByName("OsszevontVonalakMerged")[0]

varosLayer.startEditing()
varosLayer.addAttribute(QgsField('Palyaudvar', QVariant.Int, 'int', 10))
varosLayer.updateFields()

for varos in varosLayer.getFeatures():
    count = 0
    for pont in pontokLayer.getFeatures():
        if (pont["addr_city"] == varos["NAME"] and pont["amenity"] == "bus_station"):
            count += 1
    if (count > 0):
        varos["Palyaudvar"] = count
        varosLayer.updateFeature(varos)

varosLayer.commitChanges()
iface.vectorLayerTools().stopEditing(varosLayer)
#NOTE: Sajnos az általam választott témában az OSM adatai elég hiányosak, emiatt a szkript is hiányos adatokkal tud csak dolgozni.

#b)
rules = (
    ('car_rental', '"amenity" LIKE \'car_rental\'', 'green'),
    ('bus_station', '"amenity" LIKE \'bus_station\'', 'red'),
    ('driving_school', '"amenity" LIKE \'driving_school\'', 'blue')
)

symbol = QgsSymbol.defaultSymbol(pontokLayer.geometryType())
renderer = QgsRuleBasedRenderer(symbol)

root_rule = renderer.rootRule()

for label, expression, color_name in rules:
    rule = root_rule.children()[0].clone()
    rule.setLabel(label)
    rule.setFilterExpression(expression)
    symbol = QgsSymbol.defaultSymbol(pontokLayer.geometryType())
    symbol.setColor(QColor(color_name))
    if label == 'car_rental':
        car_symbol_layer = QgsSimpleMarkerSymbolLayer.create({"name": "circle", "color": "red", "size": "5"})
        symbol.changeSymbolLayer(0, car_symbol_layer)
    elif label == 'bus_station':
        bus_symbol_layer = QgsSimpleMarkerSymbolLayer.create({"name": "square", "color": "blue", "size": "5"})
        symbol.changeSymbolLayer(0, bus_symbol_layer)
    elif label == 'driving_school':
        steering_wheel_symbol_layer = QgsSimpleMarkerSymbolLayer.create({"name": "triangle", "color": "green", "size": "5"})
        symbol.changeSymbolLayer(0, steering_wheel_symbol_layer)
    rule.setSymbol(symbol)
    root_rule.appendChild(rule)

root_rule.removeChildAt(0)
pontokLayer.setRenderer(renderer)
pontokLayer.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(pontokLayer.id())