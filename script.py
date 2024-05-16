### code was written by brych92 (on github - https://github.com/brych92, email: brych92@gmail.com)

import json, requests
from qgis.core import QgsProject, QgsFeature, QgsJsonExporter, QgsVectorLayer, QgsJsonUtils, QgsTask, QgsMessageLog, Qgis, QgsApplication
from qgis.utils import iface
from requests.structures import CaseInsensitiveDict

#коди з API від 26-04-2024
SRID_list_api = {            
        'EPSG:4284': 4284,#СК-42 (B, L)
        
        'EPSG:9831': 700001,#МСК-01 (АР Крим)
        'EPSG:9832': 700002,#МСК-05 (Вінницька область)
        'EPSG:9833': 700003,#МСК-07 (Волинська область)
        'EPSG:9834': 700004,#МСК-12 (Дніпропетровська область)
        'EPSG:9835': 700005,#МСК-14 (Донецька область)
        'EPSG:9836': 700006,#МСК-18 (Житомирська область)
        'EPSG:9837': 700007,#МСК-21 (Закарпатська область)
        'EPSG:9838': 700008,#МСК-23 (Запорізька область)
        'EPSG:9839': 700009,#МСК-26 (Івано-Франківська область)
        'EPSG:9840': 700010,#МСК-35 (Кіровоградська область)
        'EPSG:9821': 700011,#МСК-32 (Київська область)
        'EPSG:9864': 700012,#МСК-80 (м. Київ)
        'EPSG:9841': 700013,#МСК-44 (Луганська область)
        'EPSG:9851': 700014,#МСК-46 (Львівська область)
        'EPSG:9852': 700015,#МСК-48 (Миколаївська область)
        'EPSG:9853': 700016,#МСК-51 (Одеська область)
        'EPSG:9854': 700017,#МСК-53 (Полтавська область)
        'EPSG:9855': 700018,#МСК-56 (Рівненська область)
        'EPSG:9856': 700019,#МСК-59 (Сумська область)
        'EPSG:9857': 700020,#МСК-61 (Тернопільська область)
        'EPSG:9858': 700021,#МСК-63 (Харківська область)
        'EPSG:9859': 700022,#МСК-65 (Херсонська область)
        'EPSG:9860': 700023,#МСК-68 (Хмельницька область)
        'EPSG:9861': 700024,#МСК-71 (Черкаська область)
        'EPSG:9862': 700025,#МСК-73 (Чернівецька область)
        'EPSG:9863': 700026,#МСК-74 (Чернігівська область)
        'EPSG:9865': 700027,#МСК-84 (м. Севастополь)
        
        'EPSG:28404': 28404,#СК-42 GK6 зона 4 осьовий меридіан 21°
        'EPSG:28405': 28405,#СК-42 GK6 зона 5 осьовий меридіан 27°
        'EPSG:28406': 28406,#СК-42 GK6 зона 6 осьовий меридіан 33°
        'EPSG:28407': 28407,#СК-42 GK6 зона 7 осьовий меридіан 39°
        
        'EPSG:2582': 2582,#СК-42 GK3 осьовий меридіан 21°
        'EPSG:2583': 2583,#СК-42 GK3 осьовий меридіан 24°
        'EPSG:2584': 2584,#СК-42 GK3 осьовий меридіан 27°
        'EPSG:2585': 2585,#СК-42 GK3 осьовий меридіан 30°
        'EPSG:2586': 2586,#СК-42 GK3 осьовий меридіан 33°
        'EPSG:2587': 2587,#СК-42 GK3 осьовий меридіан 36°
        'EPSG:2588': 2588,#СК-42 GK3 осьовий меридіан 39°
        
        'EPSG:28404': 28404,#СК-42 GK6 зона 4 осьовий меридіан 21°
        'EPSG:28405': 28405,#СК-42 GK6 зона 5 осьовий меридіан 27°
        'EPSG:28406': 28406,#СК-42 GK6 зона 6 осьовий меридіан 33°
        'EPSG:28407': 28407,#СК-42 GK6 зона 7 осьовий меридіан 39°
        
        'EPSG:7825': 7825,#СК-63 район X 1 зона
        'EPSG:7826': 7826,#СК-63 район X 2 зона
        'EPSG:7827': 7827,#СК-63 район X 3 зона
        'EPSG:7828': 7828,#СК-63 район X 4 зона
        'EPSG:7829': 7829,#СК-63 район X 5 зона
        'EPSG:7830': 7830,#СК-63 район X 6 зона
    }

#коди з старого калькулятора
SRID_list_old = {
        'EPSG:9832': 700002,#'msk2000 МСК-05 (Вінницька область)'
        'EPSG:9833': 700003,#'msk2000 МСК-07 (Волинська область)'
        'EPSG:9834': 700004,#'msk2000 МСК-12 (Дніпропетровська область)'
        'EPSG:9835': 700005,#'msk2000 МСК-14 (Донецька область)'
        'EPSG:9836': 700006,#'msk2000 МСК-18 (Житомирська область)'
        'EPSG:9837': 700007,#'msk2000 МСК-21 (Закарпатська область)'
        'EPSG:9838': 700008,#'msk2000 МСК-23 (Запорізька область)'
        'EPSG:9839': 700009,#'msk2000 МСК-26 (Івано-Франківська область)'
        'EPSG:9821': 700011,#'msk2000 МСК-32 (Київська область)'
        'EPSG:9840': 700010,#'msk2000 МСК-35 (Кіровоградська область)'
        'EPSG:9841': 700013,#'msk2000 МСК-44 (Луганська область)'
        'EPSG:9851': 700014,#'msk2000 МСК-46 (Львівська область)'
        'EPSG:9852': 700015,#'msk2000 МСК-48 (Миколаївська область)'
        'EPSG:9853': 700016,#'msk2000 МСК-51 (Одеська область)'
        'EPSG:9854': 700017,#'msk2000 МСК-53 (Полтавська область)'
        'EPSG:9855': 700018,#'msk2000 МСК-56 (Рівненська область)'
        'EPSG:9856': 700019,#'msk2000 МСК-59 (Сумська область)'
        'EPSG:9857': 700020,#'msk2000 МСК-61 (Тернопільська область)'
        'EPSG:9858': 700021,#'msk2000 МСК-63 (Харківська область)'
        'EPSG:9859': 700022,#'msk2000 МСК-65 (Херсонська область)'
        'EPSG:9860': 700023,#'msk2000 МСК-68 (Хмельницька область)'
        'EPSG:9861': 700024,#'msk2000 МСК-71 (Черкаська область)'
        'EPSG:9862': 700025,#'msk2000 МСК-73 (Чернівецька область)'
        'EPSG:9863': 700026,#'msk2000 МСК-74 (Чернігівська область)'
        'EPSG:9864': 700012,#'msk2000 МСК-80 (м. Київ)'
        
        'EPSG:2582': 2582,#'sk423 СК-42 GK3 осьовий меридіан 21°'
        'EPSG:2583': 2583,#'sk423 СК-42 GK3 осьовий меридіан 24°'
        'EPSG:2584': 2584,#'sk423 СК-42 GK3 осьовий меридіан 27°'
        'EPSG:2585': 2585,#'sk423 СК-42 GK3 осьовий меридіан 30°'
        'EPSG:2586': 2586,#'sk423 СК-42 GK3 осьовий меридіан 33°'
        'EPSG:2587': 2587,#'sk423 СК-42 GK3 осьовий меридіан 36°'
        'EPSG:2588': 2588,#'sk423 СК-42 GK3 осьовий меридіан 39°'
        
        'EPSG:28404': 28404,#'sk426 СК-42 GK6 зона 4 осьовий меридіан 21°'
        'EPSG:28405': 28405,#'sk426 СК-42 GK6 зона 5 осьовий меридіан 27°'
        'EPSG:28406': 28406,#'sk426 СК-42 GK6 зона 6 осьовий меридіан 33°'
        'EPSG:28407': 28407,#'sk426 СК-42 GK6 зона 7 осьовий меридіан 39°'
        
        'EPSG:7825': 500001,#'sk63 район X 1 зона'
        'EPSG:7826': 500002,#'sk63 район X 2 зона'
        'EPSG:7827': 500003,#'sk63 район X 3 зона'
        'EPSG:7828': 500004,#'sk63 район X 4 зона'
        'EPSG:7829': 500005,#'sk63 район X 5 зона'
        'EPSG:7830': 500006,#'sk63 район X 6 зона'
        
        'EPSG:5577': 702582,#'usk20003 УСК-2000 GK3 осьовий меридіан 21°'
        'EPSG:5578': 702583,#'usk20003 УСК-2000 GK3 осьовий меридіан 24°'
        'EPSG:5579': 702584,#'usk20003 УСК-2000 GK3 осьовий меридіан 27°'
        'EPSG:5580': 702585,#'usk20003 УСК-2000 GK3 осьовий меридіан 30°'
        'EPSG:5581': 702586,#'usk20003 УСК-2000 GK3 осьовий меридіан 33°'
        'EPSG:5582': 702587,#'usk20003 УСК-2000 GK3 осьовий меридіан 36°'
        'EPSG:5583': 702588,#'usk20003 УСК-2000 GK3 осьовий меридіан 39°'
        
        'EPSG:5562': 728404,#'usk20006 УСК-2000 GK6 зона 4 осьовий меридіан 21°'
        'EPSG:5563': 728405,#'usk20006 УСК-2000 GK6 зона 5 осьовий меридіан 27°'
        'EPSG:5564': 728406,#'usk20006 УСК-2000 GK6 зона 6 осьовий меридіан 33°'
        'EPSG:5565': 728407,#'usk20006 УСК-2000 GK6 зона 7 осьовий меридіан 39°'
    }

#коди які дійсно працюють
SRID_list_correct = {
        'EPSG:9831': 700001,#МСК-01 (АР Крим)
        'EPSG:9832': 700002,#МСК-05 (Вінницька область)
        'EPSG:9833': 700003,#МСК-07 (Волинська область)
        'EPSG:9834': 700004,#МСК-12 (Дніпропетровська область)
        'EPSG:9835': 700005,#МСК-14 (Донецька область)
        'EPSG:9836': 700006,#МСК-18 (Житомирська область)
        'EPSG:9837': 700007,#МСК-21 (Закарпатська область)
        'EPSG:9838': 700008,#МСК-23 (Запорізька область)
        'EPSG:9839': 700009,#МСК-26 (Івано-Франківська область)
        'EPSG:9840': 700010,#МСК-35 (Кіровоградська область)
        'EPSG:9821': 700011,#МСК-32 (Київська область)
        'EPSG:9864': 700012,#МСК-80 (м. Київ)
        'EPSG:9841': 700013,#МСК-44 (Луганська область)
        'EPSG:9851': 700014,#МСК-46 (Львівська область)
        'EPSG:9852': 700015,#МСК-48 (Миколаївська область)
        'EPSG:9853': 700016,#МСК-51 (Одеська область)
        'EPSG:9854': 700017,#МСК-53 (Полтавська область)
        'EPSG:9855': 700018,#МСК-56 (Рівненська область)
        'EPSG:9856': 700019,#МСК-59 (Сумська область)
        'EPSG:9857': 700020,#МСК-61 (Тернопільська область)
        'EPSG:9858': 700021,#МСК-63 (Харківська область)
        'EPSG:9859': 700022,#МСК-65 (Херсонська область)
        'EPSG:9860': 700023,#МСК-68 (Хмельницька область)
        'EPSG:9861': 700024,#МСК-71 (Черкаська область)
        'EPSG:9862': 700025,#МСК-73 (Чернівецька область)
        'EPSG:9863': 700026,#МСК-74 (Чернігівська область)
        'EPSG:9865': 700027,#МСК-84 (м. Севастополь)
        
        'EPSG:7825': 7825,#СК-63 район X 1 зона
        'EPSG:7826': 7826,#СК-63 район X 2 зона
        'EPSG:7827': 7827,#СК-63 район X 3 зона
        'EPSG:7828': 7828,#СК-63 район X 4 зона
        'EPSG:7829': 7829,#СК-63 район X 5 зона
        'EPSG:7830': 7830,#СК-63 район X 6 зона
        
        'EPSG:5577': 702582,#УСК-2000 GK3 осьовий меридіан 21°
        'EPSG:5578': 702583,#УСК-2000 GK3 осьовий меридіан 24°
        'EPSG:5579': 702584,#УСК-2000 GK3 осьовий меридіан 27°
        'EPSG:5580': 702585,#УСК-2000 GK3 осьовий меридіан 30°
        'EPSG:5581': 702586,#УСК-2000 GK3 осьовий меридіан 33°
        'EPSG:5582': 702587,#УСК-2000 GK3 осьовий меридіан 36°
        'EPSG:5583': 702588,#УСК-2000 GK3 осьовий меридіан 39°
        
        'EPSG:5562': 728404,#УСК-2000 GK6 зона 4 осьовий меридіан 21°
        'EPSG:5563': 728405,#УСК-2000 GK6 зона 5 осьовий меридіан 27°
        'EPSG:5564': 728406,#УСК-2000 GK6 зона 6 осьовий меридіан 33°
        'EPSG:5565': 728407,#УСК-2000 GK6 зона 7 осьовий меридіан 39°
    }

list_types = {
    'api': SRID_list_api,
    'old': SRID_list_old,
    'correct': SRID_list_correct
    }

MESSAGE_CATEGORY = "DGM API Конвертер"

class convertTask(QgsTask):
    def __init__(self, description, layers, outCRS, only_selected = True, list_type='api', include_parameters = False, batch_size = 100, inCode = True, outCode = True, skip_other = True):
        super().__init__(description, QgsTask.CanCancel)
        
        self.layers = layers
        self.outCRS = outCRS
        self.only_selected = only_selected
        self.list_type = list_type
        self.include_parameters = include_parameters
        self.batch_size = batch_size
        self.inCode = inCode
        self.outCode = outCode
        self.skip_other = skip_other
        
        self.exception = None
        self.warnings = []
        self.new_layers = []
        
        self.total_layers = len(layers)
        self.layers_processed = 0
        
        self.total_features = self.features_count(layers)
        self.features_skipped = 0
        
        if self.total_features == 0:
            self.step = 0
            # self.cancel()
        else:
            self.step = batch_size/self.total_features
            self.progress = 0
        
    
    def features_count(self, layers):
        features_qty = 0
        SRID_list = list_types[self.list_type]
        for layer in layers:
            inCRS = layer.crs()

            if inCRS == self.outCRS:
                self.warnings.append(f"СК шару «{layer.name()}» співпадає з цільовою СК, перерахунок шару пропущено.")
                QgsMessageLog.logMessage(f"СК шару «{layer.name()}» співпадає з цільовою СК, перерахунок шару пропущено.", MESSAGE_CATEGORY, Qgis.Warning)
                continue
            
            if inCRS.authid() not in SRID_list and self.skip_other:
                self.warnings.append(f"СК Шару «{layer.name()}»({layer.crs().authid()}) - не підтримується API. Перерахунок шару буде пропущено.")
                QgsMessageLog.logMessage(f"СК Шару «{layer.name()}»({layer.crs().authid()}) - не підтримується API. Перерахунок шару буде пропущено.", MESSAGE_CATEGORY, Qgis.Warning)
                continue
                
            if not self.only_selected or len(layer.selectedFeatures()) == 0:
                features_qty += len(list(layer.getFeatures()))
            else:
                features_qty += len(layer.selectedFeatures())
        
        return features_qty
    
    def run(self):
        QgsMessageLog.logMessage(f'Переахунок через DGM API запущено! Кількість шарів до обробки: {len(self.layers)}', MESSAGE_CATEGORY, Qgis.Info)
        
        layers = self.layers
        outCRS = self.outCRS
        only_selected = self.only_selected
        list_type = self.list_type
        include_parameters = self.include_parameters
        batch_size = self.batch_size
        
        if list_type not in list_types:
            self.exception = ValueError("Тип службових кодів list_type може бути тільки 'api' - коди зі списку API, 'old' - коди старого калькулятора або 'correct' - то шо ми підібрали")
            QgsMessageLog.logMessage("Невідповідний тип списку кодів для перерахунку. Тип службових кодів list_type може бути тільки 'api' - коди зі списку API, 'old' - коди старого калькулятора або 'correct' - то шо ми підібрали", MESSAGE_CATEGORY, Qgis.Critical)
            return False
        
        SRID_list = list_types[list_type]
        
        if len(layers) == 0:
            self.exception = Exception('Не вибрані шари для перерахунку!')

            return False
        
        
        self.setProgress(0)
        for layer in layers:
            inCRS = layer.crs()
            
            if inCRS == outCRS:
                self.warnings.append(f"СК шару «{layer.name()}» співпадає з цільовою СК, перерахунок шару пропущено.")
                QgsMessageLog.logMessage(f"СК шару «{layer.name()}» співпадає з цільовою СК, перерахунок шару пропущено.", MESSAGE_CATEGORY, Qgis.Warning)
                continue
            
            if inCRS.authid() not in SRID_list and self.skip_other:
                self.warnings.append(f"СК Шару «{layer.name()}»({layer.crs().authid()}) - не підтримується API. Перерахунок шару буде пропущено.")
                QgsMessageLog.logMessage(f"СК Шару «{layer.name()}»({layer.crs().authid()}) - не підтримується API. Перерахунок шару буде пропущено.", MESSAGE_CATEGORY, Qgis.Warning)
                continue
                
            features_to_process = layer.selectedFeatures()
            
            if len(features_to_process) == 0 or not only_selected:
                features_to_process = list(layer.getFeatures())
            
            if len(features_to_process) == 0:
                self.warnings.append(f"В шарі «{layer.name()}» відсутні об'єкти для перерахунку, перерахунок шару пропущено.")
                QgsMessageLog.logMessage(f"В шарі «{layer.name()}» відсутні об'єкти для перерахунку, перерахунок шару пропущено.", MESSAGE_CATEGORY, Qgis.Warning)
                continue 
                
            json_features = json.loads(QgsJsonExporter().exportFeatures(features_to_process))
            
            geom_type = json_features["features"][0]["geometry"]["type"]

            new_layer = QgsVectorLayer(f'{geom_type}?crs={outCRS.authid()}', f"{layer.name()} - конвертоване в {outCRS.authid()}", "memory")
            
            fields = QgsJsonUtils.stringToFields(QgsJsonExporter().exportFeatures(features_to_process))
            
            if ("properties" in json_features["features"][0]) and (json_features["features"][0]["properties"] != None) and "id" not in json_features["features"][0]["properties"].keys():
                id_index = fields.indexOf('id')
                if id_index > -1:
                    fields.remove(id_index)
                    
            new_layer.dataProvider().addAttributes(fields.toList())
            new_layer.updateFields()
            
            if inCRS.authid() in SRID_list and self.inCode:
                inSRID = SRID_list[inCRS.authid()]
            else:
                inSRID = int(inCRS.authid().split(":")[1])

            if outCRS.authid() in SRID_list and self.outCode:
                outSRID = SRID_list[outCRS.authid()]
            else:
                outSRID = int(outCRS.authid().split(":")[1])
            
            features_batches = [features_to_process[i:i + batch_size] for i in range(0, len(features_to_process), batch_size)]
            
            for num, batch in enumerate(features_batches):
                
                if self.isCanceled():
                    return False
                json_features = json.loads(QgsJsonExporter().exportFeatures(batch))
                
                json_object = {
                    "geojson": {
                        "type": "FeatureCollection",
                        "name": layer.name(),
                        "features": json_features["features"]
                        },
                    "outSRID": str(outSRID), 
                    "inSRID": str(inSRID)
                    }
                
                status_code, json_out = self.send_request(json_object, parameters = include_parameters)
                
                
                if status_code == 400:
                    self.warnings.append(f"Сервер повернув помилку {status_code} для шару «{layer.name()}»(пакет {num}): Неправильно сформований запит від клієнта. Спробуйте запустити процес з іншими вхідними параметрами.")
                    self.features_skipped += self.batch_size
                    continue
                    
                if status_code == 401:
                    self.warnings.append(f"Сервер повернув помилку {status_code} для шару «{layer.name()}»(пакет {num}): API потребує аутентифікації. Можливо до нього добралися кляті капіталісти...")
                    self.features_skipped += self.batch_size
                    continue
                
                if status_code == 403:
                    self.warnings.append(f"Сервер повернув помилку {status_code} для шару «{layer.name()}»(пакет {num}): Відмова запиту. Напевно сьогодні не ваш день...")
                    self.features_skipped += self.batch_size
                    continue
                
                if status_code == 404:
                    self.warnings.append(f"Сервер повернув помилку {status_code} для шару «{layer.name()}»(пакет {num}): Інформації не знайдено. Навіть не знаю, що вам сказати...")
                    self.features_skipped += self.batch_size
                    continue
                
                if status_code == 500:
                    self.warnings.append(f"Сервер повернув помилку {status_code} для шару «{layer.name()}»(пакет {num}): Помилка на стороні сервера. Недокодили...")
                    self.features_skipped += self.batch_size
                    continue
                    
                if status_code == 503:
                    self.warnings.append(f"Сервер повернув помилку {status_code} для шару «{layer.name()}»(пакет {num}): Сервер тимчасово не може опрацьовувати запити з технічних причин. Вихідний в нього...")
                    self.features_skipped += self.batch_size
                    continue
                
                if "features" not in json_out:
                    self.warnings.append(f"У відповіді сервера для шару «{layer.name()}», відсутні об'єкти...")
                    self.features_skipped += self.batch_size
                    continue
                
                
                json_string = json.dumps(json_out)
                
                new_features = QgsJsonUtils.stringToFeatureList(json_string, fields)

                new_layer.dataProvider().addFeatures(new_features)
                
                self.progress += self.step*100
                
                if self.progress > 100:
                    self.progress = 100
                
                self.setProgress(int(self.progress))
                
                QgsMessageLog.logMessage(f"Партія {num+1} з {len(features_batches)}, шару «{layer.name()}» - Виконана. Прогрес - {self.progress}", MESSAGE_CATEGORY, Qgis.Info)
                
                
            self.layers_processed += 1
            
            self.new_layers.append(new_layer)
            QgsMessageLog.logMessage(f"Шар «{new_layer.name()}» - додано", MESSAGE_CATEGORY, Qgis.Info)
        QgsMessageLog.logMessage("Фініш", MESSAGE_CATEGORY, Qgis.Info)
        return True
    
    def finished(self, result):
        if len(self.warnings) != 0:
            for warning in self.warnings:
                iface.messageBar().pushWarning("Увага", warning)
        
        
        if result:
            QgsMessageLog.logMessage(
                f"Задача по конвертації об'єктів завершена успішно!\nКонвертовано {self.layers_processed} з {self.total_layers} шарів(в них пропущено {self.features_skipped} з {self.total_features} об'єктів)",
                MESSAGE_CATEGORY, Qgis.Success)
            
            project = QgsProject.instance()
            
            for new_layer in self.new_layers:
                
                project.addMapLayer(new_layer)

                iface.mapCanvas().refresh()
            
        else:
            if self.exception is None:
                QgsMessageLog.logMessage(
                    '"{name}" not successful but without '\
                    'exception (probably the task was manually '\
                    'canceled by the user)'.format(
                        name=self.description()),
                    MESSAGE_CATEGORY, Qgis.Warning)
            else:
                QgsMessageLog.logMessage(
                    'RandomTask "{name}" Exception: {exception}'.format(
                        name=self.description(),
                        exception=self.exception),
                    MESSAGE_CATEGORY, Qgis.Critical)
                raise self.exception

    def cancel(self):
        QgsMessageLog.logMessage(
            f'Задача була відмінена користувачем',
            MESSAGE_CATEGORY, Qgis.Info)
        super().cancel()
    
    def send_request(self, json_object, parameters = True):
        inSRID = json_object['inSRID']
        outSRID = json_object['outSRID']
        
        if parameters:
            url = f"https://dgm.gki.com.ua/api-user/transform-file?inSRID={inSRID}&outSRID={outSRID}"
        else:
            url = f"https://dgm.gki.com.ua/api-user/transform-file"
        

        token_headers = CaseInsensitiveDict()
        token_headers["Accept"] = "application/json"

        response = requests.post(url, headers = token_headers, json = json_object, timeout=15)#, stream=True, timeout=60)
        if response.status_code == 200:
            json_out = response.json()
        else:
            json_out = None
        return response.status_code, json_out
    


def convert(layers, outCRS, only_selected = True, list_type='correct', include_parameters = False, batch_size = 100, inCode = True, outCode = True, skip_other = True):
    def finished(status):
        self = task
        if status == 3:
            if len(self.warnings) != 0:
                for warning in self.warnings:
                    iface.messageBar().pushWarning("Увага", warning)
            
            if True:
                QgsMessageLog.logMessage(
                    f"Задача по конвертації об'єктів завершена успішно!\nКонвертовано {self.layers_processed} з {self.total_layers} шарів(в них пропущено {self.features_skipped} з {self.total_features} об'єктів)",
                    MESSAGE_CATEGORY, Qgis.Success)
                
                project = QgsProject.instance()
                
                for new_layer in self.new_layers:
                    
                    project.addMapLayer(new_layer)

                    iface.mapCanvas().refresh()
                
            else:
                if self.exception is None:
                    QgsMessageLog.logMessage(
                        '"{name}" not successful but without '\
                        'exception (probably the task was manually '\
                        'canceled by the user)'.format(
                            name=self.description()),
                        MESSAGE_CATEGORY, Qgis.Warning)
                else:
                    QgsMessageLog.logMessage(
                        'RandomTask "{name}" Exception: {exception}'.format(
                            name=self.description(),
                            exception=self.exception),
                        MESSAGE_CATEGORY, Qgis.Critical)
                    raise self.exception
        if status == 4:
            QgsMessageLog.logMessage(
            f'Задача була відмінена користувачем',
            MESSAGE_CATEGORY, Qgis.Info)
            task.cancel()
    
    task = convertTask("Конвертація шарів через DGM API", layers, outCRS, list_type = list_type)#, only_selected, list_type, include_parameters, batch_size, inCode, outCode, skip_other)
    task.statusChanged.connect(finished)

    QgsApplication.taskManager().addTask(task)

    

