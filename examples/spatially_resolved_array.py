"""
electrolens example to plot spatially resolved data from a file
"""
import electrolens as el
import numpy as np
from ase import cell

# create electrolens plot
spatially_resolved_properties = el.SpatiallyResolvedDataProperties(
    columns=['x', 'y', 'z', 'rho', 'gamma', 'epxc', 'deriv1', 'deriv2', 'atom'],
    density_property='rho', density_lower_limit=0.00001, density_upper_limit=1000000)

plot = el.Plot(spatially_resolved_properties=spatially_resolved_properties)

# data setup
atoms = ['Fe', 'Fe']
data = np.array([[2.96673, 2.64244, 5.63191, 1, 1, 1, 1, 1, 'Fe'], [1, 2.64159, 5.63251, 2, 2, 2, 2, 2, 'Fe']])
cell = cell.Cell([[0.0, 2.04, 2.04], [2.04, 0.0, 2.04], [2.04, 2.04, 0.0]])

# create 3D view and add data to it
view = el.ThreeDView(system_name='C6H6')
spatially_resolved_data = el.SpatiallyResolvedData(data=data, np_atoms=atoms, ase_cell=cell, grid_points=[30, 30, 30],
                                                   grid_spacing=[0.4, 0.3, 0.3])
view.add_data(spatially_resolved_data, output_data_file='spat_data.csv')

# add view to the plot
plot.add_view(view)

# show plot
#plot.show()

plot.save_configuration('spat_resolved_config.json')
