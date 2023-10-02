import pytest
from sklearn.neural_network import MLPRegressor
from hvss_calc import metric_codes as c
from hvss_calc import Hvss10ML, HvssBaseResult

TEST_FILE_NAMES = {
    c.EXP: 'exploitability_model.pkl',
    c.XCIA: 'xcia_model.pkl',
    c.XPS: 'xps_model.pkl',
    c.XSD: 'xsd_model.pkl',
    c.XHB: 'xhb_model.pkl'}

MODEL_FILE_NAMES_PARAM = list(TEST_FILE_NAMES.items())


@pytest.fixture(scope="module")
def test_calc():
    return Hvss10ML()


@pytest.fixture(scope="module")
def test_expected_model_type():
    return MLPRegressor


@pytest.fixture(scope="module")
def test_file_names():
    return TEST_FILE_NAMES


def assert_model_type(model, model_code, test_expected_model_type):
    assert model is not None, f'Model "{model_code}" is not loaded. Model type is None'
    assert type(model) is test_expected_model_type, \
        f'Loaded Model "{model_code}" is not an instance of {test_expected_model_type}'


def assert_score(actual_score, expected_score):
    assert actual_score == expected_score, 'Calculated Score not equal to expected'


def assert_hvss_result(actual, expected):
    if (isinstance(actual, expected)):
        a = actual.__dict__
        e = expected.__dict__
        assert a == a
    else:
        return False


def test_constructor():
    calc = Hvss10ML()
    assert type(calc) is Hvss10ML, 'Constructed object is not an instance of Hvss10ML'


@pytest.mark.parametrize("model_code, expected_model_file_name", MODEL_FILE_NAMES_PARAM)
def test_get_model_file_names(test_calc, model_code, expected_model_file_name):
    file_name = test_calc.get_model_file_names()[model_code]
    assert file_name == expected_model_file_name, f'Model file names do not match the expected names: {expected_model_file_name}'


@pytest.mark.parametrize("model_code, file_name", MODEL_FILE_NAMES_PARAM)
def test_load_model(test_calc, model_code, file_name, test_expected_model_type):
    model = test_calc.load_model(file_name)
    assert_model_type(model, model_code, test_expected_model_type)


def test_load_models(test_calc, test_file_names, test_expected_model_type):
    models = test_calc.load_models()
    for model_code in test_file_names.keys():
        model = models.get(model_code)
        assert_model_type(model, model_code, test_expected_model_type)


@pytest.mark.parametrize("hvssVector, expected_chunks", [
    ('HVSS:1.0/AV:N/EAC:N/PR:N/UI:N/XIT:XCIA/C:H/I:L/A:N',
     {'HVSS': '1.0', 'AV': 'N', 'EAC': 'N', 'PR': 'N', 'UI': 'N', 'XIT': 'XCIA', 'C': 'H', 'I': 'L', 'A': 'N'}),
    ('HVSS:1.0/AV:A/EAC:L/PR:L/UI:R/XIT:XPS/XPS:MD',
     {'HVSS': '1.0', 'AV': 'A', 'EAC': 'L', 'PR': 'L', 'UI': 'R', 'XIT': 'XPS', 'XPS': 'MD'}),
    ('HVSS:1.0/AV:P/EAC:H/PR:H/UI:R/XIT:XSD/XSD:SG',
     {'HVSS': '1.0', 'AV': 'P', 'EAC': 'H', 'PR': 'H', 'UI': 'R', 'XIT': 'XSD', 'XSD': 'SG'}),
    ('HVSS:1.0/AV:P/EAC:C/PR:H/UI:R/XIT:XHB/XHB:NA',
     {'HVSS': '1.0', 'AV': 'P', 'EAC': 'C', 'PR': 'H', 'UI': 'R', 'XIT': 'XHB', 'XHB': 'NA'}),
])
def test_split_vector(test_calc, hvssVector, expected_chunks: dict):
    chunks = test_calc.split_vector(hvssVector)
    assert chunks == expected_chunks


@pytest.mark.skip(reason="no way of currently testing this")  # FIXME: REMOVE SKIP TEST
@pytest.mark.parametrize("metric_code, vector_dict, expected_metric_dict", [
    (c.EXP, {'HVSS': '1.0', 'AV': 'N', 'EAC': 'N', 'PR': 'N', 'UI': 'N', 'XIT': 'XCIA', 'C': 'H', 'I': 'L', 'A': 'N'},
     {'AV': 'N', 'EAC': 'N', 'PR': 'N', 'UI': 'N'}),
    (c.EXP, {'HVSS': '1.0', 'AV': 'A', 'EAC': 'L', 'PR': 'L', 'UI': 'N', 'XIT': 'XPS', 'XPS': 'MD'},
     {'AV': 'A', 'EAC': 'L', 'PR': 'L', 'UI': 'N'}),
    (c.EXP, {'HVSS': '1.0', 'AV': 'L', 'EAC': 'M', 'PR': 'H', 'UI': 'N', 'XIT': 'XSD', 'XSD': 'SG'},
     {'AV': 'L', 'EAC': 'M', 'PR': 'H', 'UI': 'N'}),
    (c.EXP, {'HVSS': '1.0', 'AV': 'P', 'EAC': 'H', 'PR': 'N', 'UI': 'R', 'XIT': 'XHB', 'XHB': 'NA'},
     {'AV': 'P', 'EAC': 'H', 'PR': 'N', 'UI': 'R'}),
    (c.EXP, {'HVSS': '1.0', 'AV': 'P', 'EAC': 'C', 'PR': 'L', 'UI': 'R', 'XIT': 'XHB', 'XHB': 'NA'},
     {'AV': 'P', 'EAC': 'C', 'PR': 'L', 'UI': 'R'}),
    (c.EXP, {'HVSS': '1.0', 'AV': 'P', 'EAC': 'E', 'PR': 'H', 'UI': 'R', 'XIT': 'XHB', 'XHB': 'NA'},
     {'AV': 'P', 'EAC': 'E', 'PR': 'H', 'UI': 'R'}),

    # (c.XIT, {'HVSS': '1.0', 'AV': 'N', 'EAC': 'N', 'PR': 'N', 'UI': 'N', 'XIT': 'XCIA', 'C': 'H', 'I': 'L', 'A': 'N'}),
    # (c.XIT, {'HVSS': '1.0', 'AV': 'A', 'EAC': 'L', 'PR': 'L', 'UI': 'R', 'XIT': 'XPS', 'XPS': 'MD'}),
    # (c.XIT, {'HVSS': '1.0', 'AV': 'P', 'EAC': 'H', 'PR': 'H', 'UI': 'R', 'XIT': 'XSD', 'XSD': 'SG'}),
    # (c.XIT, {'HVSS': '1.0', 'AV': 'P', 'EAC': 'C', 'PR': 'H', 'UI': 'R', 'XIT': 'XHB', 'XHB': 'NA'}),
])
def test_get_metric_dict(test_calc, metric_code, vector_dict, expected_metric_dict):
    metric_dict = test_calc.get_metric_dict(metric_code, vector_dict)
    assert metric_dict == expected_metric_dict


@pytest.mark.skip(reason="no way of currently testing this")  # FIXME: REMOVE SKIP TEST
@pytest.mark.parametrize("vector_dict, metric_code, expected_arr", [
    # EXP - Exploitability
    ({'HVSS': '1.0', 'AV': 'N', 'EAC': 'N', 'PR': 'N', 'UI': 'N', 'XIT': 'XCIA', 'C': 'H', 'I': 'L', 'A': 'N'}, c.EXP,
     [1, 1, 1, 1]),
    ({'HVSS': '1.0', 'AV': 'A', 'EAC': 'L', 'PR': 'L', 'UI': 'R', 'XIT': 'XPS', 'XPS': 'MD'}, c.EXP, [2, 2, 2, 2]),
    ({'HVSS': '1.0', 'AV': 'L', 'EAC': 'M', 'PR': 'H', 'UI': 'R', 'XIT': 'XPS', 'XPS': 'C'}, c.EXP, [3, 3, 3, 2]),
    ({'HVSS': '1.0', 'AV': 'P', 'EAC': 'H', 'PR': 'H', 'UI': 'R', 'XIT': 'XSD', 'XSD': 'SG'}, c.EXP, [4, 4, 3, 2]),
    ({'HVSS': '1.0', 'AV': 'P', 'EAC': 'C', 'PR': 'H', 'UI': 'R', 'XIT': 'XHB', 'XHB': 'NA'}, c.EXP, [4, 5, 3, 2]),
    ({'HVSS': '1.0', 'AV': 'P', 'EAC': 'E', 'PR': 'H', 'UI': 'R', 'XIT': 'XHB', 'XHB': 'UI'}, c.EXP, [4, 6, 3, 2]),
    # XPS
    # XSD
    # XHB
])
def test_get_index_arr(test_calc, vector_dict, metric_code, expected_arr):
    # metric_dict = test_calc.get_metric_dict(metric_code, vector_dict)
    # def get_index_arr(self, metric_code, vector_dict)
    arr = test_calc.get_index_arr(metric_code, vector_dict)
    assert arr == expected_arr


@pytest.mark.skip(reason="no way of currently testing this")  # FIXME: REMOVE SKIP TEST
@pytest.mark.parametrize("model_code, input_arr, expected_score", [
    (c.EXP, [1, 1, 1, 2], 7.8),
    (c.XCIA, [1, 3, 1, 2, 1, 2, 2], 5.1),
    (c.XPS, [1, 3, 1, 2, 2], 4.3),
    (c.XSD, [1, 3, 1, 2, 2], 4.4),
    (c.XHB, [1, 3, 2, 1, 1, 2, 1], 6.2),
])
def test_calculate_arr(test_calc, model_code, input_arr, expected_score):
    score = test_calc.calculate_arr(model_code, input_arr)
    assert_score(score, expected_score)


# @pytest.mark.skip(reason="no way of currently testing this") # FIXME: REMOVE SKIP TEST
@pytest.mark.parametrize("hvssVector, expected_result", [
    ('HVSS:1.0/AV:N/EAC:N/PR:N/UI:N/XIT:XCIA/C:H/I:L/A:N', 7.9), # 7.8 | CVSS = 8.2

])
def test_calculate(test_calc, hvssVector, expected_result):
    hvss_result: HvssBaseResult = test_calc.calculate(hvssVector)
    # assert_hvss_result(hvss_result, expected_result)
    assert type(hvss_result) is HvssBaseResult
    # assert hvss_result == expected_result
    assert hvss_result.base == expected_result
    # assert hvss_result.exploitability == expected_exp

# ================================================================================================

# @pytest.mark.parametrize("hvssVector, expected_arr", [
#     ('HVSS:1.0/AV:N/EAC:N/PR:N/UI:N/XIT:XCIA/C:H/I:L/A:N', [1, 1, 1, 1]),
#     ('HVSS:1.0/AV:A/EAC:L/PR:L/UI:R/XIT:XPS/XPS:MD', [2, 2, 2, 2]),
#     ('HVSS:1.0/AV:L/EAC:M/PR:H/UI:R/XIT:XPS/XPS:C', [3, 3, 3, 2]),
#     ('HVSS:1.0/AV:P/EAC:H/PR:H/UI:R/XIT:XSD/XSD:SG', [4, 4, 3, 2]),
#     ('HVSS:1.0/AV:P/EAC:C/PR:H/UI:R/XIT:XHB/XHB:NA', [4, 5, 3, 2]),
#     ('HVSS:1.0/AV:P/EAC:E/PR:H/UI:R/XIT:XHB/XHB:UI', [4, 6, 3, 2]),
#     ('HVSS:1.0/AV:N/EAC:L/PR:H/UI:R/XIT:XPS/XPS:MD', [1, 2, 3, 2]),
#     ('HVSS:1.0/AV:P/EAC:M/PR:L/UI:N/XIT:XSD/XSD:SG', [4, 3, 2, 1]),
#     ('HVSS:1.0/AV:P/EAC:E/PR:H/UI:R/XIT:XHB/XHB:UI', [4, 6, 3, 2]),
# ])
# @pytest.mark.parametrize("hvssVector, expected_arr", [
#     (c.EXP, [1, 1, 1, 2], 7.8),
#     (c.XCIA, [1, 3, 1, 2, 1, 2, 2], 5.1),
#     (c.XPS, [1, 3, 1, 2, 2], 4.3),
#     (c.XSD, [1, 3, 1, 2, 2], 4.4),
#     (c.XHB, [1, 3, 2, 1, 1, 2, 1], 6.2),
# ])

