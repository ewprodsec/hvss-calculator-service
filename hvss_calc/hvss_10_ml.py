import os
import pickle
import numpy as np
from .hvss_common import HvssBaseResult
from .hvss_metrics import metric_codes as c, metric_group_base as bmg


class Hvss10ML:
    def __init__(self):
        self.hvss_metrics = self.get_hvss_metrics()
        self.models = self.load_models()

    @staticmethod
    def get_model_file_names():
        return {
            c.EXP: 'exploitability_model.pkl',
            c.XCIA: 'xcia_model.pkl',
            c.XPS: 'xps_model.pkl',
            c.XSD: 'xsd_model.pkl',
            c.XHB: 'xhb_model.pkl'
        }

    def load_model(self, file_name):
        # Get the current script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the file in the "Models" subfolder
        file_path = os.path.join(script_dir, 'Models', file_name)
        print(f'\nDEBUG:\t  Loading model from the file: {file_path}')
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                print(f'DEBUG:\t  Loaded data from file: {file_name}')
                return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None

    def load_models(self):
        models: dict = {}
        for code, file in self.get_model_file_names().items():
            models[code] = self.load_model(file)
        return models

    def predict(self, arr: list, model_code: str) -> float:
        input = np.array(arr)
        prediction = self.models.get(model_code).predict([input])[0]
        if prediction > 10:
            prediction = 10
        elif prediction < 0:
            prediction = 0
        else:
            prediction = round(prediction, 1)
        return prediction

    def calc_exploitability(self, arr) -> float:
        if len(arr) != 4:
            return {'error': 'Input array for exploitability calculation must have 4 values'}
        if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1):
            prediction = 10
        elif (arr[0] == 4 and arr[1] == 6 and arr[2] == 3 and arr[3] == 2):
            prediction = 0.1
        else:
            input = np.array(arr)
            prediction = self.models.get(c.EXP).predict([input])[0]
            if (prediction > 10):
                prediction = 10
            elif (prediction < 0):
                prediction = 0
            else:
                prediction = round(prediction, 1)
        return prediction

    def calc_xcia(self, arr) -> float:
        if len(arr) != 7:
            return {'error': 'Input array for XCIA calculation must have 7 values'}
        if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1
                and arr[4] == 3 and arr[5] == 3 and arr[6] == 3):
            prediction = 10
        elif (arr[4] == 1 and arr[5] == 1 and arr[6] == 1):
            prediction = 0
        else:
            prediction = self.predict(arr, c.XCIA)
        return prediction

    def calc_xps(self, arr) -> float:
        if len(arr) != 5:
            return {'error': 'Input array for XPS calculation must have 5 values'}
        if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1 and arr[4] == 5):
            prediction = 10
        elif (arr[4] == 1):
            prediction = 0
        else:
            prediction = self.predict(arr, c.XPS)
        return prediction

    def calc_xsd(self, arr) -> float:
        if len(arr) != 5:
            return {'error': 'Input array for XSD calculation must have 5 values'}
        if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1 and arr[4] == 5):
            prediction = 10
        elif (arr[4] == 1):
            prediction = 0
        else:
            prediction = self.predict(arr, c.XSD)
        return prediction

    def calc_xhb(self, arr) -> float:
        if len(arr) != 5:
            raise ValueError('Input array for XHB calculation must have 5 values')
        if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1 and arr[4] == 4):
            prediction = 10
        elif (arr[4] == 1):
            prediction = 0
        else:
            prediction = self.predict(arr, c.XHB)
        return prediction

    def get_calc_function(self, model_code):
        calcs = {
            c.EXP: self.calc_exploitability,
            c.XCIA: self.calc_xcia,
            c.XPS: self.calc_xps,
            c.XSD: self.calc_xsd,
            c.XHB: self.calc_xhb
        }
        return calcs.get(model_code)

    def calculate_arr(self, metric_code: str, input_arr: list) -> float:
        return self.get_calc_function(metric_code)(input_arr)

    def split_vector(self, hvss_vector: str) -> dict:
        return dict(x.split(':') for x in hvss_vector.split('/'))

    def get_hvss_metrics(self):
        hvss_metrics = {
            **bmg.metrics.get(c.EXP).metrics,
            **bmg.metrics.get(c.XIT).metrics,
            **bmg.metrics.get(c.XIT).metrics.get(c.XCIA).metrics,
        }
        del hvss_metrics[c.XCIA]
        return hvss_metrics

    def get_index_arr(self, vector_dict) -> list:
        arr = list()
        for k, v in vector_dict.items():
            if k in self.hvss_metrics:
                m = self.hvss_metrics.get(k).metrics.get(v)
                arr.append(m.index)
        print(f'DEBUG:\t  Indexed HVSS vector: {arr}')
        return arr

    def calculate(self, hvss_vector: str) -> HvssBaseResult:
        print(f'DEBUG:\t  Received HVSS vector: {hvss_vector}')
        vector_dict = self.split_vector(hvss_vector)
        print(f'DEBUG:\t  Splited HVSS vector: {vector_dict}')
        impact_code = vector_dict.get(c.XIT)
        impact_type_name = bmg.metrics.get(c.XIT).metrics.get(impact_code).name
        # Calculate impact
        arr = self.get_index_arr(vector_dict)
        base_score = self.calculate_arr(impact_code, arr)
        # Calculate exploitability
        exp_score = self.calculate_arr(c.EXP, arr[:4])
        print(f'DEBUG:\t  Exploitability subscore: {exp_score}  {arr[:4]}')
        # Handle error case
        error_message = None
        if (type(base_score) == dict) and ('error' in base_score):
            error_message = base_score.get('error')
            base_score = None
            exp_score = None

        hvssResult = HvssBaseResult(
            vector=hvss_vector,
            base=base_score,
            rating=None,  # FIXME: add
            impactTypeName=impact_type_name,
            impactTypeCode=impact_code,
            impactScore=None,
            exploitability=exp_score,
            errorMessage=error_message
        );
        return hvssResult
