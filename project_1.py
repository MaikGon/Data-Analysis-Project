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
import math


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
    fem = data[data["sex"] == "F"].groupby(by='year').sum()
    mel = data[data["sex"] == "M"].groupby(by='year').sum()

    data_1 = pd.merge(data, fem, on='year')
    data_1 = pd.merge(data_1, mel, on='year')

    data['frequency_female'] = (data_1[data_1["sex"] == "F"]['number_x'] / data_1['number_y']).fillna(0.0)
    data['frequency_male'] = (data_1[data_1["sex"] == "M"]['number_x'] / data_1['number']).fillna(0.0)

    print(data)


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


def zad8(data):
    fem = data[data["sex"] == "F"]
    mel = data[data["sex"] == "M"]

    table3_f = pd.pivot_table(fem, values='number', index=['year', 'name'], aggfunc=np.sum, fill_value=0)
    table3_f.sort_values(by=["year", "number"], inplace=True, ascending=False)

    table3_m = pd.pivot_table(mel, values='number', index=['year', 'name'], aggfunc=np.sum, fill_value=0)
    table3_m.sort_values(by=["year", "number"], inplace=True, ascending=False)

    arr_all_f = [f for f in table3_f['number'].groupby(by='year').count()]
    arr_all_m = [f for f in table3_m['number'].groupby(by='year').count()]

    arr_f, arr_m = [], []
    ind = 0
    arr = []

    for i in data['year'].unique():
        arr.append(int(i))
        x = table3_f.loc[i]
        x = x.iloc[0:1000, :]
        arr_f.append(len(x)*100 / arr_all_f[ind])

        y = table3_m.loc[i]
        y = y.iloc[0:1000, :]
        arr_m.append(len(y) * 100 / arr_all_m[ind])
        ind += 1

    diff_arr = []
    for i in range(len(arr_f)):
        diff_arr.append(abs(arr_f[i] - arr_m[i]))
    ind = diff_arr.index(max(diff_arr))

    print("Najwieksza roznica: ", str(arr[ind]))

    fig, axs = plt.subplots()

    axs.plot(arr, arr_f, 'r')
    axs.plot(arr, arr_m, 'b')
    axs.legend(['Female', "Male"], loc='upper right')
    axs.set_xlim(1880, 2020)
    axs.set_xticks(np.arange(1880, 2021, 20))
    axs.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    axs.grid()

    plt.show()


def zad9(data):
    last_names = list(data['name'])
    for i in range(len(last_names)):
        last_names[i] = last_names[i][-1]

    data['lastnames'] = last_names
    data = data.groupby(by=['year', 'sex', 'lastnames']).sum()
    arr = []

    for i in data.index:
        if i[0] == '1910' or i[0] == '1960' or i[0] == '2015':
            new_data = data.loc[i[0]]
            arr.append(new_data)

    new_frame = pd.concat([arr[0], arr[1], arr[2]])
    data2 = pd.DataFrame(data=new_frame)
    print(data2)

    #table = pd.pivot_table(data, values='number', index=['year'], columns=['sex', 'name'], aggfunc=np.sum, fill_value=0)
    #print(table)


def zad10(data):
    table = pd.pivot_table(data, values='number', index=['name'], columns=['sex'], aggfunc=np.sum, fill_value=0)
    names_arr = []
    f_arr, m_arr = [], []

    for i in table.index:
        if table['F'][i] > 0 and table['M'][i] > 0:
            names_arr.append(i)
            f_arr.append(table['F'][i])
            m_arr.append(table['M'][i])

    ind_f = f_arr.index(max(f_arr))
    ind_m = m_arr.index(max(m_arr))

    print('Wszystkie imiona: ', names_arr)
    print('Najpopularniejsze imie zenskie: ', str(names_arr[ind_f]))
    print('Najpopularniejsze imie meskie: ', str(names_arr[ind_m]))


def zad11():
    pass


def zad12():
    conn = sqlite3.connect("USA_ltper_1x1.sqlite")
    c = conn.cursor()
    c.execute('DROP TABLE data')
    c.execute('DROP TABLE sql_data_12')
    c.execute('CREATE TABLE sql_data_12 AS SELECT * FROM USA_fltper_1x1 UNION SELECT * FROM USA_mltper_1x1;')
    conn.commit()
    for row in c.execute('SELECT * FROM sql_data_12'):
        print(row)
    conn.close()


def zad13():
    pd_list = []

    with ZipFile('names.zip', 'r') as zippp:
        for filename in zippp.namelist():
            if filename.endswith('.txt'):
                with zippp.open(filename) as file:
                    frame = pd.read_csv(file, delimiter=',', names=['name', 'sex', 'number'])
                    if 2017 >= int(filename[3:-4]) >= 1959:
                        frame['year'] = filename[3:-4]

                        pd_list.append(frame)

                        if len(pd_list) == 2:
                            new_frame = pd.concat([pd_list[0], pd_list[1]])
                            pd_list.clear()
                            pd_list.append(new_frame)

    data = pd.DataFrame(data=pd_list[0])
    arr_years = [f for f in range(len(data))]
    data = data.set_index([pd.Index(arr_years)])

    table = pd.pivot_table(data, values='number', index=['year'], aggfunc=np.sum, fill_value=0)

    conn = sqlite3.connect("USA_ltper_1x1.sqlite")
    c = conn.cursor()
    arr = []
    for row in c.execute('SELECT Year, dx FROM sql_data_12;'):
        arr.append(row)
    conn.close()

    data_sql = pd.DataFrame(data=arr, index=[f for f in range(len(arr))], columns=['Year', 'Deaths'])
    data_sql = data_sql.groupby("Year").sum()

    arr = []
    for i in data['year'].unique():
        arr.append(int(i))
        
    fig, axs = plt.subplots()

    axs.plot(arr, table["number"] - list(data_sql["Deaths"]), 'g')
    axs.legend(["Przyrost naturalny"], loc='upper right')
    axs.set_xlim(1959, 2018)
    axs.set_xticks(np.arange(1959, 2019, 5))
    axs.grid()

    plt.show()


def zad14_15():
    pd_list = []

    with ZipFile('names.zip', 'r') as zippp:
        for filename in zippp.namelist():
            if filename.endswith('.txt'):
                with zippp.open(filename) as file:
                    frame = pd.read_csv(file, delimiter=',', names=['name', 'sex', 'number'])
                    if 2017 >= int(filename[3:-4]) >= 1959:
                        frame['year'] = filename[3:-4]

                        pd_list.append(frame)

                        if len(pd_list) == 2:
                            new_frame = pd.concat([pd_list[0], pd_list[1]])
                            pd_list.clear()
                            pd_list.append(new_frame)

    data = pd.DataFrame(data=pd_list[0])
    arr_years = [f for f in range(len(data))]
    data = data.set_index([pd.Index(arr_years)])

    table = pd.pivot_table(data, values='number', index=['year'], aggfunc=np.sum, fill_value=0)

    conn = sqlite3.connect("USA_ltper_1x1.sqlite")
    c = conn.cursor()
    arr = []
    for row in c.execute('SELECT Year, dx FROM sql_data_12 WHERE Age = 0;'):
        arr.append(row)
    conn.close()

    data_sql = pd.DataFrame(data=arr, index=[f for f in range(len(arr))], columns=['Year', 'Deaths'])
    data_sql = data_sql.groupby("Year").sum()

    data_sql['wsp'] = (list(table['number']) - data_sql['Deaths']) / list(table['number'])

    arr = []
    for i in data['year'].unique():
        arr.append(int(i))

    fig, axs = plt.subplots()

    axs.plot(arr, data_sql['wsp'], 'g')
    axs.legend(["Wspolczynnik przezywalnosci"], loc='upper right')
    axs.set_xlim(1959, 2018)
    axs.set_xticks(np.arange(1959, 2019, 5))
    axs.grid()

    plt.show()


if __name__ == "__main__":
    # print(zad1())
    # zad2(zad1())
    # zad3(zad1())
    # zad4(zad1())
    # zad5(zad1())
    # print(zad6(zad1()))
    # zad7(zad1(), zad6(zad1()))
    # zad8(zad1())
    zad9(zad1())
    # zad10(zad1())
    # zad11()
    # zad12()
    # zad13()
    #zad14_15()

