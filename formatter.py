def get_string(parameters):
    head, cities, values = parameters

    if head == 'Д':
        head_word = 'ДЛИНА:'

    if head == 'В':
        head_word = 'ВРЕМЯ:'

    if head == 'С':
        head_word = 'СТОИМОСТЬ:'

    if head == 'К':
        head_word = 'КОМПРОМИСС:'

    result = f"{head_word}"

    city_string = ''
    for i, city in enumerate(cities):
        if i != len(cities) - 1:
            city_string += f"{city} -> "
        else:
            city_string += f"{city}"

    result = f"{result} {city_string} | Д={values['Д']}, В={values['В']}, С={values['С']}"
    return result


def format_data(all_requests_data):
    result = []
    for request in all_requests_data:
        all_paths = request['all_paths']  # несколько путей
        for key, value in all_paths.items():
            data_formatter = []

            data_formatter.append(key)
            data_formatter.append(all_paths[key]['path'])

            values = {}

            values['Д'] = all_paths[key]['Д']
            values['В'] = all_paths[key]['В']
            values['С'] = all_paths[key]['С']
            data_formatter.append(values)

            string = get_string(data_formatter)
            result.append(string)

        optimal_path = request['optimal_path']

        head = 'К'
        cities = optimal_path['path']

        values = {}
        values['Д'] = optimal_path['Д']
        values['В'] = optimal_path['В']
        values['С'] = optimal_path['С']

        string = get_string([head, cities, values])

        result.append(string)
        result.append('  ')

    return result
