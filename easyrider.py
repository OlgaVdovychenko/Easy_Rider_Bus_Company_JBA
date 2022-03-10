import json
import re
import itertools


def dict_from_json(string):
    return json.loads(string)


def bus_id_ok(info):
    if isinstance(info, int):
        return True
    return False


def stop_id_ok(info):
    return True if isinstance(info, int) else False


def stop_name_ok(info):
    if not info:
        return False
    if not isinstance(info, str):
        return False
    template = r'[A-Z][a-z]+\s([A-Z][a-z]+\s)?(Avenue|Street|Boulevard|Road)$'
    if re.match(template, info):
        return True
    return False


def stop_type_ok(info):
    if not isinstance(info, str):
        return False
    if not info:
        return True
    return True if re.match("^(S|O|F)$", info) else False


def arrival_time_ok(info):
    if not info:
        return False
    if not isinstance(info, str):
        return False
    if not re.match("^([01][0-9]|[2][0-4]):[0-5][0-9]$", info):
        return False
    return True


def validity_check(lst_of_dicts):
    bus_id_error = 0
    stop_id_error = 0
    stop_name_error = 0
    next_stop_error = 0
    stop_type_error = 0
    arrival_time_error = 0
    for bus in lst_of_dicts:
        if not bus_id_ok(bus["bus_id"]):
            bus_id_error += 1
        if not stop_id_ok(bus["stop_id"]):
            stop_id_error += 1
        if not stop_name_ok(bus["stop_name"]):
            stop_name_error += 1
        if not stop_id_ok(bus["next_stop"]):
            next_stop_error += 1
        if not stop_type_ok(bus["stop_type"]):
            stop_type_error += 1
        if not arrival_time_ok(bus["a_time"]):
            # print(bus["a_time"])
            arrival_time_error += 1
    total_errors = stop_name_error + stop_type_error + arrival_time_error
    if not total_errors:
        '''print(f"Type and required field validation: {total_errors}")
        print(f"bus_id: {bus_id_error}")
        print(f"stop_id: {stop_id_error}")
        print(f"stop_name: {stop_name_error}")
        print(f"next_stop: {next_stop_error}")
        print(f"stop_type: {stop_type_error}")
        print(f"a_time: {arrival_time_error}")'''
        print(f'Format validation: {total_errors}')
        print(f"stop_name: {stop_name_error}")
        print(f"stop_type: {stop_type_error}")
        print(f"a_time: {arrival_time_error}")


def count_stops_number(lst_of_dicts):
    freq_stop_dict = {}
    for bus in lst_of_dicts:
        if bus_id_ok(bus["bus_id"]):
            freq_stop_dict.setdefault(bus["bus_id"], 0)
            freq_stop_dict[bus["bus_id"]] += 1
    print(freq_stop_dict)


def get_stops_dict(lst_of_dicts):
    res_dict = {}
    for bus in lst_of_dicts:
        res_dict.setdefault(bus["bus_id"], [])
        res_dict[bus["bus_id"]].append((bus["stop_name"], bus["stop_type"]))
    return res_dict


def start_finish_stops_ok(d):
    error = 0
    for bus in d:
        stops = [elem[1] for elem in d[bus]]
        if stops.count('S') != 1 or stops.count('F') != 1:
            print(f'There is no start or end stop for the line: {bus}')
            error += 1
    return False if error else True


def get_start_stops(stop_lst):
    res_list = [stop[0] for stop in stop_lst if stop[1] == 'S']
    res_list = set(res_list)
    return list(res_list)


def get_end_stops(stop_lst):
    res_list = [stop[0] for stop in stop_lst if stop[1] == 'F']
    res_list = set(res_list)
    return list(res_list)


def get_on_demand_stops(stop_lst):
    res_list = [stop[0] for stop in stop_lst if stop[1] == 'O']
    res_list = set(res_list)
    return list(res_list)


def get_transfer_stops(stop_lst):
    lst = [stop[0] for stop in stop_lst]
    res_list = [stop for stop in lst if lst.count(stop) >= 2]
    res_list = set(res_list)
    return list(res_list)


def get_arrival_time_dict(lst_of_dicts):
    res_dict = {}
    for bus in lst_of_dicts:
        res_dict.setdefault(bus["bus_id"], [])
        res_dict[bus["bus_id"]].append((bus["stop_name"], bus["a_time"]))
    return res_dict


def check_special_stops(d):
    stop_list = []
    for stop in d:
        stop_list.extend(d[stop])
    # print(stop_list)
    start_stop_list = get_start_stops(stop_list)
    print(f'Start stops: {len(start_stop_list)} {sorted(start_stop_list)}')
    transfer_stop_list = get_transfer_stops(stop_list)
    print(f'Transfer stops: {len(transfer_stop_list)} {sorted(transfer_stop_list)}')
    end_stop_list = get_end_stops(stop_list)
    print(f'Finish stops: {len(end_stop_list)} {sorted(end_stop_list)}')


def check_arrival_time(d):
    print("Arrival time test:")
    error = False
    for bus, stops in d.items():
        current_time = stops[0][1]
        for i in range(1, len(stops)):
            if stops[i][1] > current_time:
                current_time = stops[i][1]
            else:
                print(f'bus_id line {bus}: wrong time on station {stops[i][0]}')
                error = True
                break
    if not error:
        print('OK')


def check_on_demand_stops(d):
    print("On demand stop test:")
    stop_list = []
    for stop in d:
        stop_list.extend(d[stop])
    start_stop_list = get_start_stops(stop_list)
    # print(f'Start stops: {len(start_stop_list)} {sorted(start_stop_list)}')
    transfer_stop_list = get_transfer_stops(stop_list)
    # print(f'Transfer stops: {len(transfer_stop_list)} {sorted(transfer_stop_list)}')
    end_stop_list = get_end_stops(stop_list)
    # print(f'Finish stops: {len(end_stop_list)} {sorted(end_stop_list)}')
    on_demand_stop_list = get_on_demand_stops(stop_list)
    # print(f'On demand stops: {len(on_demand_stop_list)} {sorted(on_demand_stop_list)}')
    wrong_on_demand_stop_list = []
    for stop in on_demand_stop_list:
        if stop in itertools.chain(start_stop_list, transfer_stop_list, end_stop_list):
            wrong_on_demand_stop_list.append(stop)
    if wrong_on_demand_stop_list:
        print(f'Wrong stop type: {sorted(wrong_on_demand_stop_list)}')
    else:
        print('OK')


if __name__ == "__main__":
    user_input = input()
    info_dict = dict_from_json(user_input)
    # validity_check(info_dict)
    # count_stops_number(info_dict)
    stops_dict = get_stops_dict(info_dict)
    '''if start_finish_stops_ok(stops_dict):
        check_special_stops(stops_dict)'''
    '''a_time_dict = get_arrival_time_dict(info_dict)
    check_arrival_time(a_time_dict)'''
    check_on_demand_stops(stops_dict)
