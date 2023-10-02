import pytest
from hvss_calc import Metric, MetricGroup, ImpactType, ImpactTypes
from hvss_calc import metric_group_base as bmg

exp = bmg.metrics.get('EXP').metrics
xit = bmg.metrics.get('XIT').metrics


@pytest.mark.parametrize("object", [
    (bmg.metrics.get('EXP')),
    (exp.get('AV')),
    (exp.get('EAC')),
    (exp.get('PR')),
    (exp.get('UI')),
    (bmg.metrics.get('XIT')),
    (xit.get('XCIA')),
    (xit.get('XPS')),
    (xit.get('XSD')),
    (xit.get('XHB'))
])
def test_not_none(object):
    assert object is not None, 'Object is not loaded. Object type is None'


@pytest.mark.parametrize("metric, expected_type, expected_code, expected_name, expected_description", [
    (bmg.metrics.get('EXP'), MetricGroup, 'EXP', 'Exploitability', ''),
    (exp.get('AV'), MetricGroup, 'AV', 'Attack Vector', ''),
    (exp.get('EAC'), MetricGroup, 'EAC', 'Extended Attack Complexity', ''),
    (exp.get('PR'), MetricGroup, 'PR', 'Privileges Required', ''),
    (exp.get('UI'), MetricGroup, 'UI', 'User Interaction', ''),
    (bmg.metrics.get('XIT'), ImpactTypes, 'XIT', 'Impact Types', ''),
    (xit.get('XCIA'), ImpactType, 'XCIA', 'Original CIA', ''),
    (xit.get('XPS'), ImpactType, 'XPS', 'Patient Safety', ''),
    (xit.get('XSD'), ImpactType, 'XSD', 'Sensetive Data Exposure', ''),
    (xit.get('XHB'), ImpactType, 'XHB', 'Hospital Breach', '')
])
def test_group_type_code_name(metric, expected_type, expected_code, expected_name, expected_description):
    assert type(metric) is expected_type, f'Object is not an instance of {expected_type} type'
    assert metric.code == expected_code, f'Metric code do not match the expected code: {expected_code}'
    assert metric.name == expected_name, f'Metric name do not match the expected name: {expected_name}'
    # assert metric.description == expected_description, f'Metric name do not match the expected name: {expected_description}'
