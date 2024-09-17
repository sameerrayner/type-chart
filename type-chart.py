import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
from matplotlib import font_manager as fm, rcParams

prop = fm.FontProperties(fname = r"C:\Users\Sameer\OneDrive\Documents\Pokemon Classic.ttf")

types_df = pd.read_csv('PKMNDB/types.csv', usecols = ['id','identifier'], index_col = 'id', nrows = 18)

effectiveness_df = pd.read_csv('PKMNDB/type_efficacy.csv')

matrix_df = effectiveness_df.join(types_df, on = 'damage_type_id')
matrix_df.rename(columns = {'identifier' : 'attacking_type'}, inplace = True)

matrix_df = matrix_df.join(types_df, on = 'target_type_id')
matrix_df.rename(columns = {'identifier' : 'defending_type'}, inplace = True)

matrix_df.drop(['damage_type_id', 'target_type_id'], axis = 1, inplace = True)

matrix_df = matrix_df.pivot(index = 'defending_type', columns = 'attacking_type', values = 'damage_factor')

matrix_df = matrix_df.apply(lambda x:x/100)

typelist = ['normal','grass','water','fire','flying', 'fighting', 'bug', 'electric','ground', 'rock', 'ice','poison','psychic','ghost', 'dragon','dark','steel','fairy']
matrix_df.index = pd.CategoricalIndex(matrix_df.index, categories = typelist)
matrix_df.sort_index(inplace = True)
matrix_df = matrix_df[typelist]

fig, ax = plt.subplots(figsize = (17,17))

cmap = colors.ListedColormap(['black', '#fc6b6b', 'white', '#61ff5f'])
bounds = [0, 0.5, 1, 1.5, 2]
norm = colors.BoundaryNorm(bounds, cmap.N)

cax = ax.imshow(matrix_df, cmap=cmap)

ax.set_xticks(np.arange(matrix_df.values.shape[1]), labels = typelist, fontproperties = prop, fontsize = 12)
ax.set_yticks(np.arange(matrix_df.values.shape[0]), labels = typelist, fontproperties = prop, fontsize = 12)

ax.set_ylabel('Defending Type', fontproperties = prop, fontsize = 15)
ax.set_xlabel('Attacking Type', fontproperties = prop, fontsize = 15)
ax.set_title('Pokemon Type Effectiveness Chart', pad = 65, fontproperties = prop, fontsize = 25)

ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
plt.setp(ax.get_xticklabels(), rotation =45, ha = 'left', va = 'bottom', rotation_mode = 'anchor')

ax.set_xticks(np.arange(matrix_df.values.shape[1])-.5, minor = True)
ax.set_yticks(np.arange(matrix_df.values.shape[0])-.5, minor = True)
ax.grid(which = 'minor', color = 'gray', linestyle = '-', linewidth = 3)

cbar = fig.colorbar(cax, ticks = [1.75, 1.25, 0.75, 0.25], orientation = 'horizontal', location = 'top', shrink = 0.8, aspect = 50, pad = 0.085)
cbar.ax.set_xticklabels(['Super Effective (2x)', 'Neutral (1x)', 'Not Very Effective (0.5x)', 'No Effect (0x)'], fontproperties = prop, fontsize = 13)

plt.tight_layout()

plt.savefig('type_chart.png', bbox_inches = 'tight')