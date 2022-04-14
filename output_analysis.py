import os
import pandas as pd
import matplotlib.pyplot as plt


def plotting(data, name='All'):
    fig, ax = plt.subplots()
    ax = data['Attacks per female'].plot(kind='hist', bins=40, alpha=.7, color='orange', ax=ax,
                                         label='Ataques por 100 mil mulheres')
    ax.set(xlabel='Ataques por 100 mil mulheres',
           ylabel='Frequência')
    y_min, y_max = ax.get_ylim()
    ax.vlines(data['Attacks per female'].median(), y_min, y_max, colors='red', alpha=.5,
              label=f"Mediana: {data['Attacks per female'].median():.02f}")
    for each in ['top', 'bottom', 'right', 'left']:
        ax.spines[each].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.legend(frameon=False)

    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.2)
    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)
    plt.savefig(f'{name}.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    p = 'output'
    files = os.listdir(p)
    d = pd.DataFrame()
    for f in files:
        if '2000' in f:
            d = d.append(pd.read_csv(os.path.join(p, f), sep=';'))
    plotting(d)
    for i, each in d.groupby(d.AREAP.astype(str).str[:2]):
        print(i, each)
        plotting(each, name=i)

