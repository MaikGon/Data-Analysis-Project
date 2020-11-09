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


def main():
    start = perf_counter()
    pd_list = []

    # Zadanie 1
    with ZipFile('names.zip', 'r') as zip:
        for filename in zip.namelist():
            if filename.endswith('.txt'):
                with zip.open(filename) as file:
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

    # # Zadanie 2
    # table = pd.pivot_table(data, values='number', index=['name'], columns=['sex'], aggfunc=np.sum, fill_value=0)
    # print("Ilosc unikalnych imion: ", str(len(table)))
    #
    # # print("Ilosc unikalnych imion: ", str(len(data['name'].unique())))
    # # print(data[data['sex'] == 'M'].groupby(by='name').count()['sex'])
    # # print(data[data['sex'] == 'F'].groupby(by='name').count()['sex'])
    #
    # # Zadanie 3
    # F = table[table['F'] != 0].count()['F']
    # M = table[table['M'] != 0].count()['M']
    # print("Ilosc unikalnych imion zenskich: ", str(F))
    # print("Ilosc unikalnych imion meskich: ", str(M))

    # Zadanie 4
    # data['frequency_female'] = 0.0
    # data['frequency_male'] = 0.0
    #
    table2 = pd.pivot_table(data, values='number', index=['year'], columns=['sex'],  aggfunc=np.sum,
                            fill_value=0)
    #
    # for ind in range(len(data)):
    #     find_year = data['year'][ind]
    #     print(data['name'][ind], ' ', find_year)
    #     if data['sex'][ind] == 'F':
    #         data['frequency_female'][ind] = data['number'][ind] / table2[data['sex'][ind]][find_year]
    #     elif data['sex'][ind] == 'M':
    #         data['frequency_male'][ind] = data['number'][ind] / table2[data['sex'][ind]][find_year]
    #
    # data.to_csv("data_names.csv")

    # Zadanie 5

    table3 = pd.pivot_table(data, values='number', index=['year'], aggfunc=np.sum,
                            fill_value=0)
    table3['diff'] = table2['F'] / table2['M']

    arr = []
    for i in table3.index:
        arr.append(int(i))

    fig, axs = plt.subplots(2)
    axs[0].plot(arr, table3['number'], '.r')
    axs[0].set_title('Liczba urodzin', fontsize=12)
    axs[0].set_xlim(1880, 2020)
    axs[0].set_xticks(np.arange(1880, 2021, 20))
    axs[0].set_xlabel('Rok')
    axs[0].set_ylabel('Wartosc')
    axs[0].grid()

    axs[1].plot(arr, table3['diff'], '.b')
    axs[1].set_title('Stosunek F do M', fontsize=12)
    axs[1].set_xlim(1880, 2020)
    axs[1].set_xticks(np.arange(1880, 2021, 20))
    axs[1].set_xlabel('Rok')
    axs[1].set_ylabel('Wartosc')
    axs[1].grid()

    print("Rok najmniejszej roznicy urodzen: ", str(table3[abs(table3['diff'] - 1) == min(abs(table3['diff'] - 1))].index[0]))
    print("Rok najwiekszej roznicy urodzen: ", str(table3[table3['diff'] == max(table3['diff'])].index[0]))

    plt.subplots_adjust(hspace=0.5)
    plt.show()

    stop = perf_counter()
    print("Elapsed time: ", str(stop - start))


if __name__ == "__main__":
    main()
