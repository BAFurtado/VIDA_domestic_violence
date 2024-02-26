import os
import pandas as pd
import matplotlib.pyplot as plt

def plotting(data: pd.DataFrame, name='All'):

    xlabel = 'Ataques por 100 mil mulheres'
    _, histogram = plt.subplots()
    histogram = data['Attacks per female'].plot(kind='hist', bins=40, alpha=.7, color='orange', ax=histogram,
                                         label=xlabel)
    
    histogram.set(xlabel=xlabel,
           ylabel='Frequência')
    
    y_min, y_max = histogram.get_ylim()

    histogram.vlines(data['Attacks per female'].median(), y_min, y_max, colors='red', alpha=.5,
              label=f"Mediana: {data['Attacks per female'].median():.02f}")
    
    for position in ['top', 'bottom', 'right', 'left']:
        histogram.spines[position].set_visible(False)

    histogram.get_xaxis().tick_bottom()
    histogram.get_yaxis().tick_left()
    histogram.legend(frameon=False)
    histogram.set_title(f'Histograma Frequência / {xlabel}')

    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.2)
    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)
    plt.savefig(f'{name}.png', bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    output_dir  = 'output'
    files       = os.listdir(output_dir)
    dataframe   = pd.DataFrame()
    for file in files:
        if '2000' in file:
            dataframe = dataframe._append(pd.read_csv(os.path.join(output_dir, file), sep=';'))
    plotting(dataframe)
    for i, each in dataframe.groupby(dataframe.AREAP.astype(str).str[:2]):
        print(i, each)
        plotting(each, name=i)

