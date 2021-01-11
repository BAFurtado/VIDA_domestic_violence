import os
import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter

if __name__ == '__main__':
    os.chdir('..')


def summary():
    files = os.listdir('output/')
    for file in files:
        data = pd.read_csv(os.path.join('output', file), sep=';')
        try:
            group_col = re.findall("\['(.*)'\]", file)[0]
            data = data.groupby(group_col).agg('median').reset_index()
            print(data[[group_col, 'aggressor_pct']].head(8))
        except IndexError:
            num_steps = int(re.findall("_(.*).", file)[0].split('.')[0].split('_')[-1])
            print(f'Número steps {num_steps}')
            print(data.loc[num_steps - 1, 'Stress'])


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
    ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.4f}'.format))
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
    fig, ax = plt.subplots()
    ax = set_proper_ticks(ax)
    data = data.groupby(by=col_aggregate).agg('mean').reset_index()
    data = data.sort_values(by=[col_interest])

    ax = sns.barplot(x="metro", y="Attacks per female", data=data, palette="Blues_d", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
    # ax.axes.set_title("Notificações simuladas médias de ataques por cem mil mulheres por ACPs", fontsize=10)
    ax.set_xlabel("Brazilian metropolises", fontsize=9)
    ax.set_ylabel("Cases per 100,000 women", fontsize=8)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.tick_params(labelsize=6)
    plt.ylim(min(data[col_interest]) - .0005, max(data[col_interest]))
    plt.savefig('output/metropolis.png', transparent=True, bbox_inches='tight', dpi=360, width=800)
    plt.savefig('output/figura2_EPS.eps', format='eps', transparent=True, bbox_inches='tight', dpi=360)
    plt.show()


if __name__ == '__main__':
    # df3 = pd.read_csv('output/bundled_together.csv', sep=';')
    # plot(df3, 'gender_stress', "aggressor_pct")

    df = pd.read_csv("output/output_200_dict_keys(['metro']).csv", sep=';')
    another_plot(df, 'Attacks per female', 'metro')

    # summary()
