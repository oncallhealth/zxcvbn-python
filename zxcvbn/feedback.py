from . import PasswordErrors


def get_feedback(score, sequence):
    if len(sequence) == 0:
        return {
            'warning': '',
            'suggestions': []
        }

    if score > 2:
        return {
            'warning': '',
            'suggestions': [],
        }

    longest_match = sequence[0]
    for match in sequence[1:]:
        if len(match['token']) > len(longest_match['token']):
            longest_match = match

    feedback = get_match_feedback(longest_match, len(sequence) == 1)
    if feedback:
        if not feedback['warning']:
            feedback['warning'] = ''
    else:
        feedback = {
            'warning': '',
            'suggestions': []
        }

    return feedback


def get_match_feedback(match, is_sole_match):
    if match['pattern'] == 'dictionary':
        return get_dictionary_match_feedback(match, is_sole_match)
    elif match['pattern'] == 'spatial':
        if match['turns'] == 1:
            warning = PasswordErrors.ROWS
        else:
            warning = PasswordErrors.SHORT

        return {
            'warning': warning,
            'suggestions': [
            ]
        }
    elif match['pattern'] == 'repeat':
        if len(match['base_token']) == 1:
            warning = PasswordErrors.REPEAT_CHAR
        else:
            warning = PasswordErrors.REPEAT_SEQ
        return {
            'warning': warning,
            'suggestions': [
            ]
        }
    elif match['pattern'] == 'sequence':
        return {
            'warning': PasswordErrors.SEQUENCE,
            'suggestions': [
            ]
        }
    elif match['pattern'] == 'regex':
        if match['regex_name'] == 'recent_year':
            return {
                'warning': PasswordErrors.YEARS,
                'suggestions': []
            }
    elif match['pattern'] == 'date':
        return {
            'warning': PasswordErrors.DATE,
            'suggestions': [],
        }


def get_dictionary_match_feedback(match, is_sole_match):
    warning = ''
    suggestions = []
    if match['dictionary_name'] == 'passwords':
        if is_sole_match and not match.get('l33t', False) and not \
                match['reversed']:
            if match['rank'] <= 10:
                warning = PasswordErrors.TOP10
            elif match['rank'] <= 100:
                warning = PasswordErrors.TOP100
            else:
                warning = PasswordErrors.COMMON
        elif match['guesses_log10'] <= 4:
            warning = PasswordErrors.COMMON2
    elif match['dictionary_name'] == 'english':
        if is_sole_match:
            warning = PasswordErrors.SINGLE_WORD
    elif match['dictionary_name'] in ['surnames', 'male_names',
                                      'female_names', ]:
        if is_sole_match:
            warning = PasswordErrors.NAME
        else:
            warning = PasswordErrors.COMMON_NAME
    else:
        warning = ''

    return {
        'warning': warning,
        'suggestions': suggestions,
    }
