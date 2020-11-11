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
    # print("1000 Najpopularniejszych imion zenskich: ", list(yy.index))
    # yy.to_csv("top_1000_fem.csv")

    stacked_m = list(zip(arr_names_m, arr_vals_m))
    top_data_m = pd.DataFrame(stacked_m, columns=['name', 'number'])
    sorted_m = top_data_m.groupby(by='name').sum().sort_values('number', ascending=False)
    xxy = sorted_m.iloc[0:1000, :]
    # print("1000 Najpopularniejszych imion meskich: ", list(xxy.index))
    # xxy.to_csv("top_1000_mel.csv")
    return list(yy.index), list(xxy.index)


def zad7(data, top_data):
    Fem_1st = top_data[0][0]
    Mel_1st = top_data[1][0]

    harr_arr_num = []
    harr_arr_popul = []
    harr_arr_year = []
    Marilin_arr_num = []
    Marilin_arr_popul = []
    Marilin_arr_year = []
    Fem_1st_arr_num = []
    Fem_1st_arr_popul = []
    Fem_1st_arr_year = []
    Mel_1st_arr_num = []
    Mel_1st_arr_popul = []
    Mel_1st_arr_year = []

    table = pd.pivot_table(data, values='number', index=['name'], columns=['year'], aggfunc=np.sum, fill_value=0)

    for ind in data['year'].unique():
        harr_arr_num.append(table[str(ind)]['Harry'])
        harr_arr_year.append(str(ind))
        Marilin_arr_num.append(table[str(ind)]['Marilin'])
        Marilin_arr_year.append(str(ind))
        Fem_1st_arr_num.append(table[str(ind)][Fem_1st])
        Fem_1st_arr_year.append(str(ind))
        Mel_1st_arr_num.append(table[str(ind)][Mel_1st])
        Mel_1st_arr_year.append(str(ind))

    stacked = list(zip(harr_arr_year, harr_arr_num, Marilin_arr_num, Fem_1st_arr_num, Mel_1st_arr_num))
    stacked = pd.DataFrame(stacked, columns=['year', 'Harry', 'Marilin', str(Fem_1st), str(Mel_1st)])

    table1 = pd.pivot_table(data, values='number', index=['year'], aggfunc=np.sum, fill_value=0)

    # Frequency
    for i in data['year'].unique():
        all_numbers = table1.loc[i]

        val = table[str(i)]['Harry'] / all_numbers
        harr_arr_popul.append(val)
        val = table[str(i)]['Marilin'] / all_numbers
        Marilin_arr_popul.append(val)
        val = table[str(i)][Fem_1st] / all_numbers
        Fem_1st_arr_popul.append(val)
        val = table[str(i)][Mel_1st] / all_numbers
        Mel_1st_arr_popul.append(val)

    stacked['freq_harr'] = harr_arr_popul
    stacked['freq_mar'] = Marilin_arr_popul
    stacked['freq_fem'] = Fem_1st_arr_popul
    stacked['freq_mel'] = Mel_1st_arr_popul

    print('Ilosc imienia Harry w 1940: ', table['1940']['Harry'])
    print('Ilosc imienia Harry w 1980: ', table['1980']['Harry'])
    print('Ilosc imienia Harry w 2019: ', table['2019']['Harry'])
    print('Ilosc imienia Marilyn w 1940: ', table['1940']['Marilin'])
    print('Ilosc imienia Marilyn w 1980: ', table['1980']['Marilin'])
    print('Ilosc imienia Marilyn w 2019: ', table['2019']['Marilin'])
    print('Ilosc imienia ', Fem_1st, ' w 1940: ', table['1940'][Fem_1st])
    print('Ilosc imienia ', Fem_1st, ' w 1980: ', table['1980'][Fem_1st])
    print('Ilosc imienia ', Fem_1st, ' w 2019: ', table['2019'][Fem_1st])
    print('Ilosc imienia ', Mel_1st, ' w 1940: ', table['1940'][Mel_1st])
    print('Ilosc imienia ', Mel_1st, ' w 1980: ', table['1980'][Mel_1st])
    print('Ilosc imienia ', Mel_1st, ' w 2019: ', table['2019'][Mel_1st])

    arr = []

    for i in data['year'].unique():
        arr.append(int(i))

    fig, axs = plt.subplots(2)

    axs[0].plot(arr, stacked['Harry'], 'r')
    axs[0].plot(arr, stacked['Marilin'], 'b')
    axs[0].plot(arr, stacked[Mel_1st], 'g')
    axs[0].plot(arr, stacked[Fem_1st], 'k')
    axs[0].legend(['Harry', 'Marilyn', Mel_1st, Fem_1st], loc='upper right')
    axs[0].set_xlim(1880, 2020)
    axs[0].set_xticks(np.arange(1880, 2021, 20))
    axs[0].grid()

    axs[1].plot(arr, stacked['freq_harr'], 'r')
    axs[1].plot(arr, stacked['freq_mar'], 'b')
    axs[1].plot(arr, stacked['freq_mel'], 'g')
    axs[1].plot(arr, stacked['freq_fem'], 'k')
    axs[1].legend(['Harry', 'Marilyn', Mel_1st, Fem_1st], loc='upper right')
    axs[1].set_xlim(1880, 2020)
    axs[1].set_xticks(np.arange(1880, 2021, 20))
    axs[1].grid()

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def zad10(data):
    pass


if __name__ == "__main__":
    # zad1()
    # zad2(zad1())
    # zad3(zad1())
    # zad4(zad1())
    # zad5(zad1())
    # zad6(zad1())
    zad7(zad1(), zad6(zad1()))
    # zad8()
    # zad9()
    # zad10(zad1())
