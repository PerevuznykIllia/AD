from spyre import server
import pandas as pd
import os
import numpy as np

class SetData(server.App):
    title = "Візуалізація Даних"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'NOAA',
            "options": [{"label": "VCI", "value": "VCI"},
                        {"label": "TCI", "value": "TCI"},
                        {"label": "VHI", "value": "VHI"}],
            "key": 'NOAA',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Region',
            "options": [{"label": "Вінницька", "value": "Вінницька"},
                        {"label": "Волинська", "value": "Волинська"},
                        {"label": "Дніпропетровська", "value": "Дніпропетровська"},
                        {"label": "Донецька", "value": "Донецька"},
                        {"label": "Житомирська", "value": "Житомирська"},
                        {"label": "Закарпатська", "value": "Закарпатська"},
                        {"label": "Запорізька", "value": "Запорізька"},
                        {"label": "Івано-Франківська", "value": "Івано-Франківська"},
                        {"label": "Київська", "value": "Київська"},
                        {"label": "Кіровоградська", "value": "Кіровоградська"},
                        {"label": "Луганська", "value": "Луганська"},
                        {"label": "Львівська", "value": "Львівська"},
                        {"label": "Миколаївська", "value": "Миколаївська"},
                        {"label": "Одеська", "value": "Одеська"},
                        {"label": "Полтавська", "value": "Полтавська"},
                        {"label": "Рівенська", "value": "Рівенська"},
                        {"label": "Сумська", "value": "Сумська"},
                        {"label": "Тернопільська", "value": "Тернопільська"},
                        {"label": "Харківська", "value": "Харківська"},
                        {"label": "Херсонська", "value": "Херсонська"},
                        {"label": "Хмельницька", "value": "Хмельницька"},
                        {"label": "Черкаська", "value": "Черкаська"},
                        {"label": "Чернівецька", "value": "Чернівецька"},
                        {"label": "Чернігівська", "value": "Чернігівська"},
                        {"label": "Республіка Крим", "value": "Республіка Крим"}],
            "key": 'region',
            "action_id": "update_data"
        },
        {

            "type":'slider',
            "label": 'year',
            "key": 'year',
            "value" : 2000,
            "min" : 1999,
            "max" : 2024,
            "action_id" : "update_data",
        },

        {
            "type": 'text',
            "label": 'Week min',
            "key": 'week_min',
            "value": '',
            "action_id": "update_data"
        },

        {
            "type": 'text',
            "label": 'Week max',
            "key": 'week_max',
            "value": '',
            "action_id": "update_data"
        }
    ]

    controls = [{
        "type": "hidden",
        "id": "update_data"
    }]

    tabs = ["Table", "Plot"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        current_directory = os.getcwd()
        filename = "all.csv"
        full_path = os.path.join(current_directory, filename)
        df = pd.read_csv(full_path)
        return df

    def getTable(self, params):
        df = self.getData(params)
        region = params['region']
        year = int(params['year'])
        week_min = int(params['week_min'])
        week_max = int(params['week_max'])
        if week_max > 52:
            return pd.DataFrame({'message': ['Будь ласка, введіть значення для Week max менше або рівне 52.']})
        if week_max < week_min:
            return pd.DataFrame({'message': ['Будь ласка, введіть правильні дані для Week min і Week max.']})
        data = df[(df['area'] == region) & (df['Year'] == year) & (df['Week'] >= week_min) & (df['Week'] <= week_max)]
        columns = ['Year', 'Week', params['NOAA'], 'area']
        return data.loc[:, columns]


    def getPlot(self, params):
        region = params['region']
        year = int(params['year'])
        ticker = params['NOAA']
        week_min = int(params['week_min'])
        week_max = int(params['week_max'])
        df = self.getData(params)
        data = df[(df['area'] == region) & (df['Year'] == year) & (df['Week'] >= week_min) & (df['Week'] <= week_max)]
        plt_obj = data.plot(x='Week', y=ticker)
        plt_obj.set_ylabel("NOAA дані")
        plt_obj.set_xlabel("Тиждень")
        plt_obj.set_title(f"Графік для регіону {region} у {year} році для вказаних тижнів")
        plt_obj.set_xticks(np.arange(week_min, week_max + 1, 1))
        plot = plt_obj.get_figure()
        return plot
if __name__ == '__main__':
    app = SetData()
    app.launch(port=8008)




