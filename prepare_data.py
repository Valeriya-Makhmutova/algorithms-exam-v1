def is_number(value):
    '''
    Функция - предикат.
    Определяет является ли числом переданное значение
    
    :param value: значение, 
    которое нужно проверить, 
    является ли оно числом (например, если число в виде строки)
    '''
    try:
        int(value)
        return True
    except ValueError:
        return False


def prepare_data(data):
    """
    Функция по обработки входных данных в удобную структуру в виде словаря
   
    :param data: полученные данные в сыром виде
    """
    dict_data = {}
    # Разделение по группам данных (cities, roads, requests)
    for elem in data:
        if elem.startswith("["):
            if elem[1:-1].lower() == 'cities':
                dict_data[elem[1:-1].lower()] = {}
            else:
                dict_data[elem[1:-1].lower()] = []
    # Группировка в словарь остальных данных
    for elem in data:
        if elem[0] != '[' and not is_number(elem[0]):
            request = {}
            elems = elem.split(' | ')

            request['from'] = elems[0].split(' -> ')[0]
            request['to'] = elems[0].split(' -> ')[1]
            request['prioritets'] = elems[1][1:-1].split(',')
            dict_data['requests'].append(request)

        if elem[1] == ':':
            id_ = int(elem.split(':')[0])
            city = (elem.split(':')[1]).strip()
            dict_data['cities'][id_] = city

        if elem[2] == '-':
            road_dict = {}
            road = elem.split(':')
      
            road_name = road[0]
     
            road_values = list(
                map(lambda x: int(x.strip()), road[1].split(',')))

            road_dict['from_id'] = int(road_name.split(' - ')[0])
            road_dict['to_id'] = int(road_name.split(' - ')[1])
            road_dict['values'] = {}
            road_dict['values']['Д'] = road_values[0]
            road_dict['values']['В'] = road_values[1]
            road_dict['values']['С'] = road_values[2]
            dict_data['roads'].append(road_dict)

    return (dict_data)
