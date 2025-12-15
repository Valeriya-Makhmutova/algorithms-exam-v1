from prepare_data import prepare_data
from utils import get_graph, find_all_optimal_paths, get_one_optimal_path
from formatter import format_data


def main():
    with open('input.txt', encoding='utf-8') as f:
        data = f.read().split('\n')
        result_data_list = []

        normalized_data = prepare_data(data)

        for request in normalized_data['requests']:
            routes_results = {}
            city_from = request['from']
            city_finish = request['to']

            graph = get_graph(normalized_data)

            all_suitable_paths = find_all_optimal_paths(
                graph, city_from, city_finish, normalized_data['cities'])

            optimal_path = get_one_optimal_path(
                all_suitable_paths, request['prioritets'])

            routes_results['all_paths'] = all_suitable_paths
            routes_results['optimal_path'] = optimal_path

            result_data_list.append(routes_results)

        total = format_data(result_data_list)
        file = open('output.txt', 'w', encoding='utf-8')
        file.write('\n'.join(total))
    print('Успешно! Результат в файле output.txt :)')
    pass


if __name__ == "__main__":
    main()
