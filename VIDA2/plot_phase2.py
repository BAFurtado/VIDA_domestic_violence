""" Using python shapefile while ArcGis not available

"""
import os

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd


names = {'BRASILIA': {'name': 'Brasília',
                      'code': '53'},
         'CURITIBA': {'name': 'Curitiba',
                      'code': '41'},
         'BELO HORIZONTE': {'name': 'Belo Horizonte',
                            'code': '31'},
         'VITORIA': {'name': 'Vitória',
                     'code': '32'},
         'RIO DE JANEIRO': {'name': 'Rio de Janeiro',
                            'code': '21'},
         'RECIFE': {'name': 'Recife',
                    'code': '26'}}


def plot_maps(shape, data, col, leg=True, title='title'):
    # Read simulation data
    data = pd.read_csv(os.path.join('../output', data), sep=';')
    # Merge data with shapefile
    shape = pd.merge(shape, data)

    fig, ax = plt.subplots()
    shape.plot(column=col,
               legend=leg,
               ax=ax,
               scheme='quantiles',
               cmap='inferno',
               # missing_kwds={'color': 'lightgrey'},
               legend_kwds={'fmt': '{:,.0f}', 'frameon': False}
               )
    shape.boundary.plot(ax=ax, color='white', linewidth=.5, edgecolor='grey')
    ax.set_title(title)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # rms is a list of data to send over to merge along the shape and plot
    rms = list()
    for file in os.listdir('../output'):
        if '500' in file:
            rms.append(file)
    for rm in names:
        shps = gpd.read_file(f"../../censo2010/data/areas/{names[rm]['code']}_all_muns.shp")
        for f in rms:
            if rm in f:
                plot_maps(shps, f, 'Attacks per female')
                break
