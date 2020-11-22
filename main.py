import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from matplotlib.ticker import PercentFormatter
from zipfile import ZipFile
from time import perf_counter
import os


def zad1():
    pd_list = []

    for filename in sorted(os.listdir("names/")):
        if filename.endswith('.txt'):
            with open('names/' + str(filename), 'r') as file:
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
    x = np.arange(1880, 2020)

    fig, axs = plt.subplots(2)
    fig.suptitle("Zadanie 5")
    axs[0].plot(x, table2['number'], 'r')
    axs[0].set_xlim(1880, 2020)
    axs[0].set_xticks(np.arange(1880, 2021, 20))
    axs[0].set_xlabel('Rok')
    axs[0].set_ylabel('Liczba urodzin')
    axs[0].grid()

    axs[1].plot(x, table2['diff'], 'b')
    axs[1].set_xlim(1880, 2020)
    axs[1].set_xticks(np.arange(1880, 2021, 20))
    axs[1].set_xlabel('Rok')
    axs[1].set_ylabel('Stosunek F do M')
    axs[1].grid()

    print("Rok najmniejszej roznicy urodzen: ", str(table2[abs(table2['diff'] - 1) == min(abs(table2['diff'] - 1))].index[0]))
    print("Rok najwiekszej roznicy urodzen: ", str(table2[table2['diff'] == max(table2['diff'])].index[0]))

    plt.subplots_adjust(hspace=0.5)
    plt.show()


def zad6(data):
    fem = data[data["sex"] == "F"]
    mel = data[data["sex"] == "M"]

    # female pivot
    table3_f = pd.pivot_table(fem, values='number', index=['year', 'name'], aggfunc=np.sum, fill_value=0)
    table3_f.sort_values(by=["year", "number"], inplace=True, ascending=False)

    # male pivot
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
    yy = sorted_f.iloc[0:1000, :]  # 1000 Najpopularniejszych imion zenskich

    stacked_m = list(zip(arr_names_m, arr_vals_m))
    top_data_m = pd.DataFrame(stacked_m, columns=['name', 'number'])
    sorted_m = top_data_m.groupby(by='name').sum().sort_values('number', ascending=False)
    xxy = sorted_m.iloc[0:1000, :]  # 1000 Najpopularniejszych imion meskich

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

    x1 = np.arange(1880, 2020)
    fig, axs = plt.subplots()
    fig.suptitle("Zadanie 7")
    axs.plot(x1, stacked['Harry'], 'r')
    axs.plot(x1, stacked['Marilin'], 'b')
    axs.plot(x1, stacked[Mel_1st], 'g')
    axs.plot(x1, stacked[Fem_1st], 'k')
    axs.legend(['Harry', 'Marilyn', Mel_1st, Fem_1st], loc='upper left')
    axs.set_xlim(1880, 2020)
    axs.set_xticks(np.arange(1880, 2021, 20))
    axs.grid()
    axs.set_xlabel('Rok')
    axs.set_ylabel('Ilosc')

    ax2 = axs.twinx()

    ax2.plot(x1, stacked['freq_harr'], '.c')
    ax2.plot(x1, stacked['freq_mar'], '.b')
    ax2.plot(x1, stacked['freq_mel'], '.y')
    ax2.plot(x1, stacked['freq_fem'], '.m')
    ax2.legend(['Harry', 'Marilyn', Mel_1st, Fem_1st], loc='upper right')
    ax2.set_ylabel('Popularnosc')

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
    x1 = []

    for i in data['year'].unique():
        x1.append(int(i))
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

    print("Najwieksza roznica: ", str(x1[ind]))

    fig, axs = plt.subplots()
    fig.suptitle("Zadanie 8")
    axs.plot(x1, arr_f, 'r')
    axs.plot(x1, arr_m, 'b')
    axs.legend(['Female', "Male"], loc='upper right')
    axs.set_xlim(1880, 2020)
    axs.set_xticks(np.arange(1880, 2021, 20))
    axs.yaxis.set_major_formatter(PercentFormatter(decimals=0))
    axs.grid()
    axs.set_xlabel('Rok')
    axs.set_ylabel('Procentowa wartosc imion z top1000')

    plt.show()


def zad9(data):
    table = pd.pivot_table(data, values='number', index=['year'], columns=['sex'], aggfunc=np.sum, fill_value=0)

    last_names = list(data['name'])
    for i in range(len(last_names)):
        last_names[i] = last_names[i][-1]

    data['lastnames'] = last_names
    data = pd.pivot_table(data, index=['year', 'sex', 'lastnames'], aggfunc=np.sum, fill_value=0)
    arr_f, arr_m = [], []

    for i in ['1910', '1960', '2015']:
        new_data_f = data.loc[(i, 'F')]
        new_data_m = data.loc[(i, 'M')]
        new_data_f['number'] = new_data_f['number'] / table['F'][i]
        new_data_m['number'] = new_data_m['number'] / table['M'][i]
        arr_f.append(new_data_f)
        arr_m.append(new_data_m)

    final = pd.merge(arr_f[0], arr_f[1], on='lastnames', how='right', suffixes=('_1910_f', '_1960_f'))
    final = pd.merge(final, arr_f[2], on='lastnames', how='right', suffixes=(None, '_2015_f'))
    final = pd.merge(final, arr_m[0], on='lastnames', how='right', suffixes=(None, '_1910_m'))
    final = pd.merge(final, arr_m[1], on='lastnames', how='right', suffixes=(None, '_1960_m'))
    final = pd.merge(final, arr_m[2], on='lastnames', how='right', suffixes=(None, '_2015_m'))
    final = final.fillna(0.0)

    final['diff'] = abs(final['number_2015_m'] - final['number_1910_m'])

    print('Najwiekszy wzrost/spadek wystapil dla litery: ', str(final[final['diff'] == max(final['diff'])].index[0]))

    fig, ax = plt.subplots(2)
    fig.suptitle("Zadanie 9")
    x = np.arange(len(final))
    width = 0.1

    ax[0].bar(x - 0.3, final['number_1910_m'], width, label='Man 1910')
    ax[0].bar(x - 0.2, final['number_1910_f'], width, label='Woman 1910 ')
    ax[0].bar(x - 0.1, final['number_1960_m'], width, label='Man 1960')
    ax[0].bar(x + 0.1, final['number_1960_f'], width, label='Woman 1960')
    ax[0].bar(x + 0.2, final['number_2015_m'], width, label='Man 2015')
    ax[0].bar(x + 0.3, final['number'], width, label='Woman 2015')
    ax[0].set_xlabel('Litera')
    ax[0].set_ylabel('Popularnosc')
    ax[0].legend()
    ax[0].grid(axis='y')


    ax[0].set_xticks(x)
    ax[0].set_xticklabels(final.index)
    ax[0].tick_params(axis='x')

    # Trend
    sorted_table = final.sort_values('diff', ascending=False)
    y1, y2, y3 = [], [], []
    x1 = np.arange(1880, 2020)

    for i in table.index:
        trend_data_1 = (data.loc[(i, 'M', sorted_table.index[0])] / data.loc[(i, 'M')].sum()) * 100
        trend_data_2 = (data.loc[(i, 'M', sorted_table.index[1])] / data.loc[(i, 'M')].sum()) * 100
        trend_data_3 = (data.loc[(i, 'M', sorted_table.index[2])] / data.loc[(i, 'M')].sum()) * 100
        y1.append(trend_data_1['number'])
        y2.append(trend_data_2['number'])
        y3.append(trend_data_3['number'])

    ax[1].plot(x1, y1, 'r')
    ax[1].plot(x1, y2, 'g')
    ax[1].plot(x1, y3, 'b')
    ax[1].legend([str(sorted_table.index[0]), str(sorted_table.index[1]), str(sorted_table.index[2])], loc='upper right')
    ax[1].set_xlim(1880, 2020)
    ax[1].set_xticks(np.arange(1880, 2021, 20))
    ax[1].set_ylim(0, 40)
    ax[1].yaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax[1].grid()
    ax[1].set_xlabel('Rok')
    ax[1].set_ylabel('Trend')
    plt.subplots_adjust(hspace=0.5)
    plt.show()


def zad10(data):
    table = pd.pivot_table(data, values='number', index=['name'], columns=['sex'], aggfunc=np.sum, fill_value=0)
    table = table.loc[(table['F'] > 0) & (table['M'] > 0), :]

    ind_f = table[table['F'] == max(table['F'])].index[0]
    ind_m = table[table['M'] == max(table['M'])].index[0]

    print('Najpopularniejsze imie zenskie: ', ind_f)
    print('Najpopularniejsze imie meskie: ', ind_m)

    return table


def zad11(data, data_10):
    table1 = data[data['name'].isin(list(data_10.index))]
    table = pd.pivot_table(table1, values='number', index=['name'], columns=['year', 'sex'], aggfunc=np.sum, fill_value=0)

    for i in range(1880, 2020):
        f = table[(str(i), 'F')] / (table[(str(i), 'F')] + table[(str(i), 'M')])
        m = table[(str(i), 'M')] / (table[(str(i), 'F')] + table[(str(i), 'M')])
        table[(str(i), 'F')] = f
        table[(str(i), 'M')] = m

    tab1 = table.loc[:, '1880':'1920']
    tab2 = table.loc[:, '2000':'2020']
    tab1 = tab1.mean(axis=1, level=1)
    tab2 = tab2.mean(axis=1, level=1)
    tab_1_2 = pd.merge(tab1, tab2, on='name').dropna()

    tab_1_2['diff'] = abs((tab_1_2['F_x'] - tab_1_2['F_y']) - (tab_1_2['M_x'] - tab_1_2['M_y']))
    tab_1_2.sort_values(by='diff', inplace=True, ascending=False)
    tab_1_2 = tab_1_2[tab_1_2['diff'] == 2.0]
    tab_1_2.sort_index(inplace=True)

    name1 = tab_1_2.index[0]
    name2 = tab_1_2.index[1]

    table_last = pd.pivot_table(table1, values='number', index=['year'], columns=['name', 'sex'], aggfunc=np.sum, fill_value=0)
    table_last = table_last.loc[:, [name1, name2]]

    first_f = table_last[(name1, 'F')]
    first_m = table_last[(name1, 'M')]
    sec_f = table_last[(name2, 'F')]
    sec_m = table_last[(name2, 'M')]

    x1 = np.arange(1880, 2020)
    fig, axs = plt.subplots(2)
    fig.suptitle("Zadanie 11")
    axs[0].plot(x1, first_f, 'r')
    axs[0].plot(x1, first_m, 'g')
    axs[0].legend(['Abell female', 'Abell male'], loc='upper left')
    axs[0].set_xlim(1880, 2020)
    axs[0].set_xticks(np.arange(1880, 2020, 10))
    axs[0].grid()
    axs[0].set_xlabel('Rok')
    axs[0].set_ylabel('Ilosc wystapien imienia pierwszego')

    axs[1].plot(x1, sec_f, 'b')
    axs[1].plot(x1, sec_m, 'k')
    axs[1].legend(['Abney female', 'Abney male'], loc='upper left')
    axs[1].set_xlim(1880, 2020)
    axs[1].set_xticks(np.arange(1880, 2020, 10))
    axs[1].grid()
    axs[1].set_xlabel('Rok')
    axs[1].set_ylabel('Ilosc wystapien imienia drugiego')
    plt.subplots_adjust(hspace=0.7)
    plt.show()


def zad12():
    conn = sqlite3.connect("USA_ltper_1x1.sqlite")
    c = conn.cursor()
    # c.execute('DROP TABLE sql_data_12')
    c.execute('CREATE TABLE sql_data_12 AS SELECT * FROM USA_fltper_1x1 UNION SELECT * FROM USA_mltper_1x1;')
    conn.commit()
    conn.close()


def zad13(data):
    table = pd.pivot_table(data, values='number', index=['year'], aggfunc=np.sum, fill_value=0)

    conn = sqlite3.connect("USA_ltper_1x1.sqlite")
    c = conn.cursor()
    arr_sql = []
    for row in c.execute('SELECT Year, dx FROM sql_data_12;'):
        arr_sql.append(row)
    conn.close()

    data_sql = pd.DataFrame(data=arr_sql, index=[f for f in range(len(arr_sql))], columns=['Year', 'Deaths'])
    data_sql = data_sql.groupby("Year").sum()

    x = np.arange(1959, 2018)
    fig, axs = plt.subplots()

    axs.plot(x, table["number"] - list(data_sql["Deaths"]), 'g')
    axs.set_xlim(1959, 2018)
    axs.set_xticks(np.arange(1959, 2019, 5))
    axs.grid()
    axs.set_xlabel('Rok')
    axs.set_ylabel('Przyrost naturalny')

    plt.show()


def zad14_15(data):
    # Task 14
    table = pd.pivot_table(data, values='number', index=['year'], aggfunc=np.sum, fill_value=0)

    conn = sqlite3.connect("USA_ltper_1x1.sqlite")
    c = conn.cursor()
    arr_sql = []
    for row in c.execute('SELECT Year, dx, Age FROM sql_data_12 WHERE Age >= 0 AND Age <= 4;'):
        arr_sql.append(row)
    conn.close()

    data_sql = pd.DataFrame(data=arr_sql, index=[f for f in range(len(arr_sql))], columns=['Year', 'Deaths', 'Age'])
    data_sql_14 = data_sql[data_sql['Age'] == 0].groupby("Year").sum()
    data_sql_14['wsp_1'] = (list(table['number']) - data_sql_14['Deaths']) / list(table['number'])

    # Task 15
    data_sql = data_sql.groupby(["Year", "Age"]).sum()

    arr_5 = []
    for i in data_sql_14.index:
        if i <= 2012:
            val = 0
            for j in range(5):
                val += data_sql.loc[pd.IndexSlice[i + j, j], 'Deaths']
            arr_5.append(val)

    for i in range(len(arr_5)):
        arr_5[i] = (table['number'][str(i + 1959)] - arr_5[i]) / table['number'][str(i + 1959)]

    x1 = np.arange(1959, 2018)
    x2 = np.arange(1959, 2013)
    fig, axs = plt.subplots()

    axs.plot(x1, data_sql_14['wsp_1'], 'r')
    axs.plot(x2, list(arr_5), 'g')
    axs.legend(["Wsp przezywalnosci w 1 roku zycia", "Wsp przezywalnosci w 5 latach zycia"], loc='upper left')
    axs.set_xlim(1959, 2018)
    axs.set_xticks(np.arange(1959, 2019, 5))
    axs.grid()
    axs.set_xlabel('Rok')
    axs.set_ylabel('Wartosc wspolczynnika')

    plt.show()


def data_13_14_15():
    pd_list = []

    for filename in sorted(os.listdir("names/")):
        if filename.endswith('.txt'):
            with open('names/' + str(filename), 'r') as file:
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

    return data


if __name__ == "__main__":
    start = perf_counter()
    data_1 = zad1()  # load data for further tasks
    # print(data_1)
    zad2(data_1)
    zad3(data_1)
    zad4(data_1)
    zad5(data_1)
    data_2 = zad6(data_1)
    # print(data_2)
    zad7(data_1, data_2)
    zad8(data_1)
    zad9(data_1)
    data_10 = zad10(data_1)
    zad11(data_1, data_10)
    zad12()
    data_3 = data_13_14_15()  # load data for further tasks
    zad13(data_3)
    zad14_15(data_3)
    stop = perf_counter()
    print('Elapsed time: ', str(stop - start))

