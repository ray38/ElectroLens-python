import numpy as np
import electrolens as el
from ase import cell

property_names = ['x', 'y', 'z', 'frame']
atoms = ['Fe', 'Fe']
data = np.array([[2.96673, 2.64244, 5.63191, 1], [1, 2.64159, 5.63251, 2]])
cell = cell.Cell([[0.0, 2.04, 2.04], [2.04, 0.0, 2.04], [2.04, 2.04, 0.0]])

plot = el.Plot()

view = el.ThreeDView(input_data=data, data_format=el.DataFormat.ARRAY_DATA, molecule_name='Cu', np_column_names=property_names,
                     np_atoms=atoms, np_framed=True, np_cell=cell)

plot.add_view(view)

# show plot
plot.show()

# save configuration
plot.save_configuration(output_json_file='config.json')

