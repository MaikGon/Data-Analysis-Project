import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandasgui
import sqlite3
import requests
import json
from statistics import *
from matplotlib.ticker import PercentFormatter
from zipfile import ZipFile
from time import perf_counter


def zad1():
    pd_list = []

    with ZipFile('names.zip', 'r') as zippp:
        for filename in zippp.namelist():
            if filename.endswith('.txt'):
                with zippp.open(filename) as file:
                    frame = pd.read_csv(file, delimiter=',', names=['name', 'sex', 'number'])
                    # Dodaj kolumne z rokiem
                    frame['year'] = filename[3:-4]
                    pd_list.append(frame)

                    # Jesli sa 2 elementy - sklej je
                    if len(pd_list) == 2:
                        new_frame = pd.concat([pd_list[0], pd_list[1]])
                        pd_list.clear()
                        pd_list.append(new_frame)

    data = pd.DataFrame(data=pd_list[0])
    arr_years = [f for f in range(len(data))]
    data = data.set_index([pd.Index(arr_years)])
    return data


def zad2(data):
    print("Ilosc unikalnych imion: ", str(len(data['name'].unique())))


def zad3(data):
    table = pd.pivot_table(data, values='number', index=['name'], columns=['sex'], aggfunc=np.sum, fill_value=0)
    F = table[table['F'] != 0].count()['F']
    M = table[table['M'] != 0].count()['M']
    print("Ilosc unikalnych imion zenskich: ", str(F))
    print("Ilosc unikalnych imion meskich: ", str(M))

    # print(data[data['sex'] == 'M'].groupby(by='name').count()['sex'])
    # print(data[data['sex'] == 'F'].groupby(by='name').count()['sex'])


def zad4(data):
    table = pd.pivot_table(data, values='number', index=['name'], columns=['sex'], aggfunc=np.sum, fill_value=0)
    data['frequency_female'] = 0.0
    data['frequency_male'] = 0.0

    for ind in range(len(data)):
        find_year = data['year'][ind]
        print(data['name'][ind], ' ', find_year)
        if data['sex'][ind] == 'F':
            data['frequency_female'][ind] = data['number'][ind] / table[data['sex'][ind]][find_year]
        elif data['sex'][ind] == 'M':
            data['frequency_male'][ind] = data['number'][ind] / table[data['sex'][ind]][find_year]

    # data.to_csv("data_names.csv")


def zad5(data):
    table = pd.pivot_table(data, values='number', index=['year'], columns=['sex'], aggfunc=np.sum, fill_value=0)
    table2 = pd.pivot_table(data, values='number', index=['year'], aggfunc=np.sum, fill_value=0)

    table2['diff'] = table['F'] / table['M']
    arr = []

    for i in table.index:
        arr.append(int(i))

    fig, axs = plt.subplots(2)
    axs[0].plot(arr, table2['number'], '.r')
    axs[0].set_title('Liczba urodzin', fontsize=12)
    axs[0].set_xlim(1880, 2020)
    axs[0].set_xticks(np.arange(1880, 2021, 20))
    axs[0].set_xlabel('Rok')
    axs[0].set_ylabel('Wartosc')
    axs[0].grid()

    axs[1].plot(arr, table2['diff'], '.b')
    axs[1].set_title('Stosunek F do M', fontsize=12)
    axs[1].set_xlim(1880, 2020)
    axs[1].set_xticks(np.arange(1880, 2021, 20))
    axs[1].set_xlabel('Rok')
    axs[1].set_ylabel('Wartosc')
    axs[1].grid()

    print("Rok najmniejszej roznicy urodzen: ", str(table2[abs(table2['diff'] - 1) == min(abs(table2['diff'] - 1))].index[0]))
    print("Rok najwiekszej roznicy urodzen: ", str(table2[table2['diff'] == max(table2['diff'])].index[0]))

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def zad6(data):
    fem = data[data["sex"] == "F"]
    mel = data[data["sex"] == "M"]

    table3_f = pd.pivot_table(fem, values='number', index=['year', 'name'], aggfunc=np.sum, fill_value=0)
    table3_f.sort_values(by=["year", "number"], inplace=True, ascending=False)

    table3_m = pd.pivot_table(mel, values='number', index=['year', 'name'], aggfunc=np.sum, fill_value=0)
    table3_m.sort_values(by=["year", "number"], inplace=True, ascending=False)

    arr_names_f = []
    arr_vals_f = []
    arr_names_m = []
    arr_vals_m = []

    for i in data['year'].unique():
        x = table3_f.loc[i]
        x = x.iloc[0:1000, :]
        for j in range(len(x)):
            arr_names_f.append(x.index[j])
            arr_vals_f.append(x.values[j][0])

        y = table3_m.loc[i]
        y = y.iloc[0:1000, :]
        for k in range(len(y)):
            arr_names_m.append(y.index[k])
            arr_vals_m.append(y.values[k][0])

    stacked_f = list(zip(arr_names_f, arr_vals_f))
    top_data_f = pd.DataFrame(stacked_f, columns=['name', 'number'])
    sorted_f = top_data_f.groupby(by='name').sum().sort_values('number', ascending=False)
    yy = sorted_f.iloc[0:1000, :]
    print("1000 Najpopularniejszych imion zenskich: ", list(yy.index))
    # yy.to_csv("top_1000_fem.csv")

    stacked_m = list(zip(arr_names_m, arr_vals_m))
    top_data_m = pd.DataFrame(stacked_m, columns=['name', 'number'])
    sorted_m = top_data_m.groupby(by='name').sum().sort_values('number', ascending=False)
    xxy = sorted_m.iloc[0:1000, :]
    print("1000 Najpopularniejszych imion meskich: ", list(xxy.index))
    # xxy.to_csv("top_1000_mel.csv")


def zad7(data):
    pass


if __name__ == "__main__":
    # zad1()
    # zad2(zad1())
    # zad3(zad1())
    # zad4(zad1())
    # zad5(zad1())
    # zad6(zad1())
    zad7(data)
    # zad8()
