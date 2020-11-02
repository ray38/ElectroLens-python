"""
electrolens example to show framed and molecular data plotted from numpy array
"""
import numpy as np
import electrolens as el
from ase import cell

property_names = ['x', 'y', 'z', 'frame']
atoms = ['Fe', 'Fe']
data = np.array([[2.96673, 2.64244, 5.63191, 1], [1, 2.64159, 5.63251, 2]])
cell = cell.Cell([[0.0, 2.04, 2.04], [2.04, 0.0, 2.04], [2.04, 2.04, 0.0]])

# create electrolens plot
molecular_data_properties = el.MolecularDataProperties(columns=property_names)
framed_data_properties = el.FramedDataProperties(frame_column='frame')
plot = el.Plot(molecular_properties=molecular_data_properties, framed_properties=framed_data_properties)

# create 3D view and add data to it
view = el.ThreeDView(system_name='Cu')
molecular_data = el.MolecularData(data=data, np_atoms=atoms, ase_cell=cell)
view.add_data(molecular_data)

# add view to the plot
plot.add_view(view)

# show plot
plot.show()

