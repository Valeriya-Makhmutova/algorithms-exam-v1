import heapq  # Встроенный модуль Python для работы с кучами


def get_graph(normal_data):
    """
    Функция для построения графа по нормализованным данным

    :param normal_data: нормализованные данные для построения графа
    """
    graph = {}
    cities = normal_data['cities'].keys()

    # Инициализируем пустые списки для всех городов
    for city_id in cities:
        graph[city_id] = {}

    # Добавляем все дороги (дороги двусторонние)
    for road in normal_data['roads']:
        from_id = road['from_id']
        to_id = road['to_id']
        values = road['values']

        # Добавляем связь между узлами в обе стороны
        graph[from_id][to_id] = values
        graph[to_id][from_id] = values

    return graph


def get_road_by_metric(graph, start_id, end_id, metric_char, cities_dict):
    """
    Алгоритм Дейкстры для поиска кротчайшего пути по заданному 1 параметру

    :param graph: готовый граф по узлам и рёбрам
    :param start_id: ID города, из которого начинается путь
    :param end_id: ID города-назначения 
    :param metric_char: параметр (метрика), по которой идёт поиск кротчайшего пути
    :param cities_dict: словарь соответствия ID городов их названиям
    """
    # Проверка существования городов
    if start_id not in graph or end_id not in graph:
        return None

    # Инициализация структур данных, необходимых для работы алгоритма:
    # Cловарь минимальных расстояний от start_id до каждого города
    # (изначально все расстояния бесконечны, кроме начального города)
    distances = {city_id: float('inf') for city_id in graph}
    distances[start_id] = 0

    # Cловарь для восстановления пути (хранит родителей)
    previous = {city_id: None for city_id in graph}

    # Для хранения значений всх трех метрик,
    # аккумулируем все данные для достоверного конечного подсчёта
    total_metrics = {
        city_id: {'Д': 0, 'В': 0, 'С': 0}
        for city_id in graph
    }

    # Определяем очередь с приоритетом
    # (необходимо в Алгоритме Дейкстры, эффективная структура данных)
    pq = [(0, start_id)]
    # Пока есть города в очереди, продолжаем обрабатывать граф
    while pq:
        # Извлекаем город с минимальным текущим расстоянием из очереди
        current_dist, current_city = heapq.heappop(pq)

        if current_city == end_id:
            break

        if current_dist > distances[current_city]:
            continue

        # Перебираем соседей
        for neighbor, metrics in graph[current_city].items():
          # Получаем вес по выбранной метрике
            weight = metrics[metric_char]
            new_dist = current_dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_city

              # Обновляем ВСЕ три метрики
                total_metrics[neighbor]['Д'] = (
                    total_metrics[current_city]['Д'] + metrics['Д']
                )
                total_metrics[neighbor]['В'] = (
                    total_metrics[current_city]['В'] + metrics['В']
                )
                total_metrics[neighbor]['С'] = (
                    total_metrics[current_city]['С'] + metrics['С']
                )
                # Добавляем соседа в очередь с приоритетом для дальнейшей обработки
                heapq.heappush(pq, (new_dist, neighbor))

    # Если расстояние до конечного города осталось бесконечным,
    # значит путь не был найден (граф несвязный или нет подходящего пути)
    if distances[end_id] == float('inf'):
        return None

    # Восстанавливаем путь от конечного города к начальному,
    # используя словарь previous (идем по цепочке родителей)
    path_ids = []
    current = end_id
    while current is not None:
        path_ids.append(current)
        current = previous[current]
    # Путь восстановлен в обратном порядке (от конца к началу),
    # поэтому нужно развернуть его
    path_ids.reverse()

    # Преобразуем список ID городов в список их названий
    path_names = [cities_dict[city_id] for city_id in path_ids]

    return {
        'path': path_names,
        'path_ids': path_ids,
        'Д': total_metrics[end_id]['Д'],
        'В': total_metrics[end_id]['В'],
        'С': total_metrics[end_id]['С']
    }


def find_all_optimal_paths(graph, start_name, end_name, cities_dict):
    """
    Функция поиска трёх маршрутов по заданным параметрам (запускает внутри себя алгоритм Дейкстры)

    :param graph: граф
    :param start_name: названия города отправления 
    :param end_name: город назначения 
    :param cities_dict: словарь ID городов и их названий
    """

    # Создаем обратный словарь для быстрого поиска ID по названию города
    reverse_cities = {value: key for key, value in cities_dict.items()}

    start_id = reverse_cities.get(start_name)
    end_id = reverse_cities.get(end_name)

    if start_id is None or end_id is None:
        print(f"Город не найден: {start_name} или {end_name}")
        return {}

    results = {}
    metrics = ['Д', 'В', 'С']
    # Для каждого критерия ищем оптимальный маршрут
    for metric_char in metrics:
        # Вызываем алгоритм Дейкстры для поиска пути по текущему критерию
        result = get_road_by_metric(
            graph, start_id, end_id, metric_char, cities_dict)
        if result:
            results[metric_char] = result
        else:
            print(f"Путь по критерию '{metric_char}' не найден")

    return results


def get_one_optimal_path(paths, prioritets):
    """
    Выбирает один компромиссный маршрут из трех найденных оптимальных маршрутов
    на основе заданных приоритетов среди метрик

    :param paths: все найденные пути
    :param prioritets: заданные приоритеты метрик
    """

    paths_in_order = []
    for priority in prioritets:
        if priority in paths:
            paths_in_order.append(paths[priority])
    # Определяем первый путь как лучший
    best_path = paths_in_order[0]
    # Проходим по всем остальным, кроме первого и сравнимаем
    for current_path in paths_in_order[1:]:
        for element in prioritets:
            # Если текущий маршрут лучше по критерию (значение меньше),
            # то меняемм на новый
            if current_path[element] < best_path[element]:
                best_path = current_path[element]
                break
            elif current_path[element] > best_path[element]:
                break

    return best_path
