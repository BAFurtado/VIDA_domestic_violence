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
                            'code': '33'},
         'RECIFE': {'name': 'Recife',
                    'code': '26'},
         'PORTO ALEGRE': {'name': 'Porto Alegre',
                          'code': '43'}
         }


def plot_maps(shape, boundaries, col, leg=True, title='title'):
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
    plt.savefig(f'data/{title}.png', dpi=300)
    plt.show()


def prepair_data(plot=False):
    brasil = gpd.read_file("../../PolicySpace2/input/shapes/mun_ACPS_ibge_2014_latlong_wgs1984_fixed.shp")
    shapes, files = list(), list()
    # rms is a list of data to send over to merge along the shape and plot
    for file in os.listdir('../output'):
        if '500' in file:
            files.append(file)
    for rm in names:
        shps = gpd.read_file(f"../../censo2010/data/areas/{names[rm]['code']}_all_muns.shp")
        if rm == 'BRASILIA':
            shps.append(gpd.read_file(f"../../censo2010/data/areas/52_all_muns.shp"))
        for file in files:
            if rm in file:
                # Read simulation data
                data = pd.read_csv(os.path.join('../output', file), sep=';')
                data.to_excel(f'data/{rm}.xlsx')
                # Merge data with shapefile
                shape = pd.merge(shps, data)
                shape.to_file(f'data/{rm}.shp')
                shapes.append(shape)
                # Municipalities boundaries
                muns = data.AREAP.astype(str).str[:7]
                rm_subset = brasil[brasil.CD_GEOCMU.isin(muns)]
                if plot:
                    plot_maps(shape, rm_subset, 'Attacks per female', title=names[rm]['name'])
                break
    return shapes, files


if __name__ == '__main__':
    p = True
    shp, fs = prepair_data(plot=p)
