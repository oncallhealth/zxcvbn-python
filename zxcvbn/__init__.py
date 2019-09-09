from datetime import datetime

from . import matching, scoring, time_estimates, feedback

from enum import Enum


class PasswordErrors(Enum):
    ROWS = 1
    SHORT = 2
    REPEAT_CHAR = 3
    REPEAT_SEQ = 4
    SEQUENCE = 5
    YEARS = 6
    DATE = 7
    TOP10 = 8
    TOP100 = 9
    COMMON = 10
    COMMON2 = 11
    SINGLE_WORD = 12
    NAME = 13
    COMMON_NAME = 14


def zxcvbn(password, user_inputs=None):
    try:
        # Python 2 string types
        basestring = (str, unicode)
    except NameError:
        # Python 3 string types
        basestring = (str, bytes)

    if user_inputs is None:
        user_inputs = []

    start = datetime.now()

    sanitized_inputs = []
    for arg in user_inputs:
        if not isinstance(arg, basestring):
            arg = str(arg)
        sanitized_inputs.append(arg.lower())

    ranked_dictionaries = matching.RANKED_DICTIONARIES
    ranked_dictionaries['user_inputs'] = matching.build_ranked_dict(sanitized_inputs)

    matches = matching.omnimatch(password, ranked_dictionaries)
    result = scoring.most_guessable_match_sequence(password, matches)
    result['calc_time'] = datetime.now() - start

    attack_times = time_estimates.estimate_attack_times(result['guesses'])
    for prop, val in attack_times.items():
        result[prop] = val

    result['feedback'] = feedback.get_feedback(result['score'],
                                               result['sequence'])

    return result
