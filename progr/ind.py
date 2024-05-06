#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import sys


def display_trains(trains):
    """
    Отобразить список.
    """
    if trains:
        line = '+-{}-+-{}-+-{}-+-{}-+--{}--+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 13,
            '-' * 18,
            '-' * 14
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^13} | {:^18} | {:^14} |'.format(
                "№",
                "Пункт отправления",
                "Номер поезда",
                "Время отправления",
                "Пункт назначения"
            )
        )
        print(line)

        for idx, train in enumerate(trains, 1):
            print(
                '| {:>4} | {:<30} | {:<13} | {:>18} | {:^16} |'.format(
                    idx, train.get('departure_point', ''),
                    train.get('number_train', ''),
                    train.get('time_departure', ''),
                    train.get('destination', '')
                )
            )
            print(line)

    else:
        print("Список поездов пуст.")


def add_train(trains, departure_point, number_train, time_departure, destination):
    """
    Добавить данные о поезде.
    """
    trains.append(
        {
            "departure_point": departure_point,
            "number_train": number_train,
            "time_departure": time_departure,
            "destination": destination
        }
    )

    return trains


def save_trains(file_name, trains):
    """
    Сохранить в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(trains, fout, ensure_ascii=False, indent=4)


def load_trains(file_name):
    """
    Загрузить из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def select_trains(trains, point_user):
    """
    Выбор поезда.
    """
    result = []
    for train in trains:
        if point_user == str.lower(train['destination']):
            result.append(train)

    return result


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    parser = argparse.ArgumentParser("trains")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new train"
    )
    add.add_argument(
        "-dep",
        "--departure",
        action="store",
        required=True,
        help="The train's departure point"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        required=True,
        help="The train's number"
    )
    add.add_argument(
        "-t",
        "--time",
        action="store",
        required=True,
        help="The time departure of train"
    )
    add.add_argument(
        "-des",
        "--destination",
        action="store",
        required=True,
        help="The train's destination point"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all trains"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the trains"
    )
    select.add_argument(
        "-P",
        "--point",
        action="store",
        required=True,
        help="The required point"
    )

    args = parser.parse_args(command_line)

    is_dirty = False
    if os.path.exists(args.filename):
        trains = load_trains(args.filename)
    else:
        trains = []

    if args.command == "add":
        trains = add_train(
            trains,
            args.departure,
            args.number,
            args.time,
            args.destination
        )
        is_dirty = True

    elif args.command == "display":
        display_trains(trains)

    elif args.command == "select":
        selected = select_trains(trains, args.point)
        display_trains(selected)

    if is_dirty:
        save_trains(args.filename, trains)


if __name__ == "__main__":
    main()