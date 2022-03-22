""" Using python shapefile while ArcGis not available

"""
import os

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

from matplotlib import cm

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
                          'code': '43'},
         'FORTALEZA': {'name': 'Fortaleza',
                       'code': '23'},
         'GOIANIA': {'name': 'Goiânia',
                     'code': '52'},
         'SAO PAULO': {'name': 'São Paulo',
                       'code': '35'},
         'SALVADOR': {'name': 'Salvador',
                      'code': '29'},
         'PORTO VELHO': {'name': 'Porto Velho',
                         'code': '11'},
         'JI-PARANA': {'name': 'Ji-Paraná',
                       'code': '11'},
         'CAMPO GRANDE': {'name': 'Campo Grande',
                          'code': '50'}
         }


def plot_maps(shape, boundaries, col, leg=True, title='title'):
    fig, ax = plt.subplots()
    cmap_reversed = cm.get_cmap('viridis_r')

    boundaries.boundary.plot(ax=ax, color='black', linewidth=1, edgecolor='grey', alpha=.7, label='')
    boundaries.apply(lambda x: ax.annotate(text=x['NM_MUNICIP'],
                                           xy=x.geometry.centroid.coords[0],
                                           ha='center',
                                           fontsize=7), axis=1)
    shape.plot(column=col,
               legend=leg,
               ax=ax,
               scheme='quantiles',
               cmap=cmap_reversed,
               alpha=.5,
               # missing_kwds={'color': 'lightgrey'},
               legend_kwds={'fmt': '{:,.0f}', 'frameon': False, 'loc': 'best', 'framealpha': 1}
               )
    shape.boundary.plot(ax=ax, color='white', linewidth=.3, edgecolor='grey')
    ax.set_title(title)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(f'data/{title}.png', dpi=300)
    plt.show()


def prepair_data(plot=False, runs='2000'):
    brasil = gpd.read_file("../../PolicySpace2/input/shapes/mun_ACPS_ibge_2014_latlong_wgs1984_fixed.shp")
    brasil = brasil.to_crs('EPSG:4674')
    files = list()
    # rms is a list of data to send over to merge along the shape and plot
    for file in os.listdir('../output'):
        if runs in file:
            files.append(file)
    for rm in names:
        shps = gpd.read_file(f"../../censo2010/data/areas/{names[rm]['code']}_all_muns.shp")
        if rm == 'BRASILIA':
            shps = shps.append(gpd.read_file(f"../../censo2010/data/areas/52_all_muns.shp"))
        if rm == 'PORTO VELHO':
            ro = gpd.read_file('data/RO_Municipios_2020.shp')
            ro = ro.to_crs('EPSG:4674')
        for file in files:
            if rm in file:
                # Read simulation data
                data = pd.read_csv(os.path.join('../output', file), sep=';')
                data = data[['AREAP', 'females', 'Attacks per female', 'Denounces per female']]
                # Merge data with shapefile
                shape = pd.merge(shps, data)
                shape = shape.rename(columns={'Attacks per female': 'ataque_fem',
                                              'Denounces per female': 'denunc_fem'})
                shape.to_file(f'data/{rm}.shp')
                # To save file
                data.loc[:, 'AREAP'] = data['AREAP'].astype(str)
                data.to_excel(f'data/{rm}.xlsx')

                # Municipalities boundaries
                muns = data.AREAP.astype(str).str[:7]
                if rm == 'PORTO VELHO':
                    ro = ro.rename(columns={'NM_MUN': 'NM_MUNICIP'})
                    rm_subset = ro[ro.CD_MUN.isin(muns)]

                else:
                    rm_subset = brasil[brasil.CD_GEOCMU.isin(muns)]
                if plot:
                    plot_maps(shape, rm_subset, 'ataque_fem', title=names[rm]['name'])
                break
    return shps, files


if __name__ == '__main__':
    p = False
    sps, fs = prepair_data(plot=p)
