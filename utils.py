import heapq


def get_graph(normal_data):
    graph = {}
    cities = normal_data['cities'].keys()

    # Инициализируем пустые списки смежности для всех городов
    for city_id in cities:
        graph[city_id] = {}

    # Добавляем все дороги (дороги двусторонние)
    for road in normal_data['roads']:
        from_id = road['from_id']
        to_id = road['to_id']
        values = road['values']

        # Добавляем связь в обе стороны
        graph[from_id][to_id] = values
        graph[to_id][from_id] = values

    return graph


def get_road_by_metric(graph, start_id, end_id, metric_char, cities_dict):

    # Проверка существования городов
    if start_id not in graph or end_id not in graph:
        return None

    # Инициализация
    distances = {city_id: float('inf') for city_id in graph}
    distances[start_id] = 0

    previous = {city_id: None for city_id in graph}

    # Для хранения всех трех метрик (все равно с русскими ключами)
    total_metrics = {
        city_id: {'Д': 0, 'В': 0, 'С': 0}
        for city_id in graph
    }

    # Очередь с приоритетом
    pq = [(0, start_id)]

    while pq:
        current_dist, current_city = heapq.heappop(pq)

        # Если достигли конечного города
        if current_city == end_id:
            break

        # Если текущее расстояние больше известного
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

                heapq.heappush(pq, (new_dist, neighbor))

    # Если путь не найден
    if distances[end_id] == float('inf'):
        return None

    # Восстанавливаем путь
    path_ids = []
    current = end_id
    while current is not None:
        path_ids.append(current)
        current = previous[current]
    path_ids.reverse()

    # Преобразуем ID в названия
    path_names = [cities_dict[city_id] for city_id in path_ids]

    return {
        'path': path_names,
        'path_ids': path_ids,
        'Д': total_metrics[end_id]['Д'],
        'В': total_metrics[end_id]['В'],
        'С': total_metrics[end_id]['С']
    }


def find_all_optimal_paths(graph, start_name, end_name, cities_dict):

    # Нужно найти ID городов по названию
    reverse_cities = {v: k for k, v in cities_dict.items()}

    start_id = reverse_cities.get(start_name)
    end_id = reverse_cities.get(end_name)

    if start_id is None or end_id is None:
        print(f"Город не найден: {start_name} или {end_name}")
        return {}

    results = {}
    metrics = ['Д', 'В', 'С']

    for metric_char in metrics:
        result = get_road_by_metric(
            graph, start_id, end_id, metric_char, cities_dict)
        if result:
            results[metric_char] = result
        else:
            print(f"Путь по критерию '{metric_char}' не найден")

    return results


def get_one_optimal_path(paths, prioritets):

    paths_in_order = []
    for priority in prioritets:
        if priority in paths:
            paths_in_order.append(paths[priority])

    best_path = paths_in_order[0]

    for current_path in paths_in_order[1:]:
        for element in prioritets:
            if current_path[element] < best_path[element]:
                best_path = current_path[element]
                break
            elif current_path[element] > best_path[element]:
                break

    return best_path
