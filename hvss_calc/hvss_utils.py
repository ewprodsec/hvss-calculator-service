from .hvss_common import HvssBaseResult


def get_rating(hvss_result: HvssBaseResult) -> str:
    base_score = hvss_result.base;
    if base_score == 0:
        return 'None'
    elif base_score < 4.0:
        return 'Low'
    elif base_score < 7.0:
        return 'Medium'
    elif base_score < 9.0:
        return 'High'
    else:
        return 'Critical'
