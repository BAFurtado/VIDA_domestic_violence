import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

if __name__ == '__main__':
    os.chdir('..')


def summary():
    pass


def generic(name, ax, x_label, y_label, title, legend):
    # Histograms
    # legend = ['sanctioned', 'not sanctioned', 'proposed']
    # colors = ['red', 'blue', 'grey']
    # for i, k in enumerate(legend):
    #     ax.hist([x.ideology for x in data if x.category == k], bins=50, alpha=.35, color=colors[i])

    ax = set_proper_ticks(ax, x_label, y_label, title, legend)

    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    # Remove the tick marks; they are unnecessary with the tick lines we just
    # plotted.
    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)

    plt.savefig(f'{name}.png', bbox_inches='tight')
    plt.show()


def set_proper_ticks(ax, x_label='', y_label='', title='', legend=''):

    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.5f}'.format))
    ax.legend = ([legend])
    return ax


def plot(data, group_col, plot_col):
    fig, ax = plt.subplots()
    data = data.groupby(group_col).agg('median').reset_index()
    ax.plot(data[group_col], data[plot_col], label='Pct Aggressors')
    ax.legend(loc='upper right', frameon=False)
    ax = set_proper_ticks(ax)
    plt.show()


def another_plot(data, col_interest, col_aggregate):
    # TODO: Border, Legend, Abbvr. Ticks
    fig, ax = plt.subplots()
    data = data.groupby(by=col_aggregate).agg('median').reset_index()
    data = data.sort_values(by=[col_interest])
    data[col_interest].plot(kind='bar', legend=col_aggregate, ylim=[min(data[col_interest]), max(data[col_interest])])
    sns.palplot(sns.color_palette("Blues"))
    fig = sns.barplot(data=data, x=col_aggregate, y=col_interest)
    fig.plot()
    plt.show()


if __name__ == '__main__':
    # df3 = pd.read_csv('output/bundled_together.csv', sep=';')
    # plot(df3, 'gender_stress', "aggressor_pct")

    df = pd.read_csv('output/output_metropolis.csv', sep=';')
    another_plot(df, 'aggressor_pct', 'metro')
