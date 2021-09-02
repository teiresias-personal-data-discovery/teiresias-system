from fuzzywuzzy import process, fuzz


def process_proximity(item, personal_data_key_words, **kwargs):
    proximity_threshold = kwargs.get("proximity_threshold", 60)
    ordered_proximities = process.extract(item,
                                          personal_data_key_words,
                                          scorer=fuzz.token_sort_ratio)
    if proximity_threshold:
        return [
            proximity for proximity in ordered_proximities
            if proximity[1] >= proximity_threshold
        ]
    return ordered_proximities


def process_proximity_of_items(items, key_words):
    proximities = {}
    if isinstance(items, list):
        for item in items:
            ordered_proximities = process_proximity(item, key_words)
            proximities = {
                **proximities,
                **({
                    item: ordered_proximities
                } if len(ordered_proximities) else {})
            }
    if isinstance(items, dict):
        for name, item in items.items():
            ordered_proximities = process_proximity(item, key_words)
            proximities = {
                **proximities,
                **({
                    name: ordered_proximities
                } if len(ordered_proximities) else {})
            }
    return proximities
