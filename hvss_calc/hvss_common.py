from dataclasses import dataclass


@dataclass
class Metric:
    code: str
    name: str
    index: int = 0
    weight: float = 0.0
    description: str = None


@dataclass
class MetricGroup:
    code: str
    name: str
    metrics: dict
    description: str = None


@dataclass
class ImpactType(MetricGroup):
    pass


@dataclass
class ImpactTypes(ImpactType):
    pass


@dataclass
class MetricCode:
    EXP: str
    XIT: str
    XCIA: str
    XPS: str
    XSD: str
    XHB: str


@dataclass
class HvssBaseResult:
    """
    Do not change this naming convention to PEP-8 style!
    This is an interface contract with JavaScript based web UI.
    """
    vector: str
    base: float
    rating: str
    impactTypeName: str
    impactTypeCode: str
    impactScore: float
    exploitability: float
    errorMessage: str = None
