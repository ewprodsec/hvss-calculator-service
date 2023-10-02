from .hvss_10_ml import Hvss10ML
from .hvss_common import HvssBaseResult
from .hvss_utils import get_rating

class Hvss:
    def __init__(self):
        self.calc = Hvss10ML()

    def calculate(self, hvss_vector: str) -> HvssBaseResult:
        """'
        Calculate the Basic Score from provided 'hvss_vector' and
        return the result as an instance of the class HvssBaseResult:
          HvssBaseResult(vector, base, rating, impactTypeName, impactTypeCode, impactScore, exploitability)
        or in case of error:
          HvssBaseResult(errorMessage)

        See below an example of the expected HvssBaseResult
        """
        hvss_result: HvssBaseResult = self.calc.calculate(hvss_vector)
        if (hvss_result.errorMessage is None):
            hvss_result.rating = get_rating(hvss_result)
        return hvss_result
