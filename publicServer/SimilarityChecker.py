from difflib import SequenceMatcher


def find_most_similar_strings(input_string, string_list):
    ratios = []
    for string in string_list:
        ratio = SequenceMatcher(None, input_string, string).ratio()
        ratios.append((string, ratio))
    sorted_strings = sorted(ratios, key=lambda x: x[1], reverse=True)
    most_similar_strings = [sorted_strings[0][0]]
    for string, ratio in sorted_strings[1:]:
        if ratio == sorted_strings[0][1]:
            if len(most_similar_strings) >= 3:
                break
            most_similar_strings.append(string)
        else:
            break
    return most_similar_strings
