#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bisect
import json
import os
import sys
import click


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
        click.echo(line)
        click.echo(
            '| {:^4} | {:^30} | {:^13} | {:^18} | {:^14} |'.format(
                "№",
                "Пункт отправления",
                "Номер поезда",
                "Время отправления",
                "Пункт назначения"
            )
        )
        click.echo(line)
        for idx, train in trains:
            click.echo(
                '| {:>4} | {:<30} | {:<13} | {:>18} | {:^16} |'.format(
                    idx, train.get('departure_point', ''),
                    train.get('number_train', ''),
                    train.get('time_departure', ''),
                    train.get('destination', '')
                )
            )
        click.echo(line)
    else:
        click.echo("Список поездов пуст.")


def add_train(trains, departure_point, number_train, time_departure, destination):
    """
    Добавить данные.
    """
    is_dirty = False
    train = {
        "departure_point": departure_point,
        "number_train": number_train,
        "time_departure": time_departure,
        "destination": destination
    }
    if train not in trains:
        bisect.insort(
            trains,
            train,
            key=lambda item: item.get("time_departure"),
        )
        is_dirty = True
    else:
        click.echo("Данный поезд уже добавлен.")
    return trains, is_dirty



def select_trains(trains, point_user):
    """
    Выбор поезда.
    """
    selected = []
    for train in trains:
        if point_user == str.lower(train['destination']):
            selected.append(train)

    return selected


def save_trains(file_name, trains):
    """
    Сохранить в файл JSON.
    """
    with open(file_name, "w") as file_out:
        json.dump(trains, file_out, ensure_ascii=False, indent=4)


def load_trains(file_name):
    """
    Загрузить из файла JSON.
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


@click.group()
def command():
    pass


@command.command()
@click.argument("filename")
@click.option("-dep", "--departure_point", required=True, help="The departure point train")
@click.option("-n", "--number_train", required=True, help="The number train")
@click.option("-t", "--time_departure", required=True, help="The time departure of train")
@click.option("-des", "--destination", required=True, help="The destination of train")
def add(filename, departure_point, number_train, time_departure, destination):
    """
    Добавить поезд.
    """

    filename = os.path.join("data", filename)
    trains = load_trains(filename)

    routes, is_dirty = add_train(trains, departure_point.lower(), number_train.lower(), time_departure.lower(), destination.lower())
    if is_dirty:
        save_trains(filename, trains)


@command.command()
@click.argument("filename")
@click.option("-p", "--point_user", required=True, help="Destination train")
def select(filename, point_user):
    """
    Выбрать
    """
    filename = os.path.join("data", filename)
    point_user = point_user.lower()
    trains = load_trains(filename)
    selected_trains = select_trains(trains, point_user)
    display_trains(selected_trains)


@command.command()
@click.argument("filename")
def display(filename):
    """
    Отобразить
    """
    filename = os.path.join("data", filename)
    trains = load_trains(filename)
    display_trains(trains)


if __name__ == "__main__":
    command()