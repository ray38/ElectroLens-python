"""
electrolens example to show molecular and spatially resolved data addition in a single view
"""
from ase.cluster.cubic import FaceCenteredCubic
import electrolens as el

# setup atoms object
surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
layers = [6, 9, 5]
lc = 3.61000
atoms = FaceCenteredCubic('Cu', surfaces, layers, latticeconstant=lc)

# set plot data properties
molecular_data_properties = el.MolecularDataProperties(columns=['x', 'y', 'z', 'atom'])
spatially_resolved_properties = el.SpatiallyResolvedDataProperties(
    columns=['x', 'y', 'z', 'rho', "gamma", "epxc", "deriv1", "deriv2"],
    density_property='rho', density_lower_limit=0.00001, density_upper_limit=1000000)

# create Plot
plot = el.Plot(molecular_properties=molecular_data_properties,spatially_resolved_properties=spatially_resolved_properties)

# create 3D view and add data to it
view = el.ThreeDView(system_name='C6H6')

# add molecular data
molecular_data = el.MolecularData(data=atoms)
view.add_data(molecular_data)

# add spatially resolved data
spatially_resolved_data = el.SpatiallyResolvedData(data="C6H6_data.csv", grid_points=[30, 30, 30], grid_spacing=[0.4, 0.3, 0.3])
view.add_data(spatially_resolved_data)

# add view to the plot
plot.add_view(view)

# show plot
plot.show()

