from ase.cluster.cubic import FaceCenteredCubic
import electrolens as el

# setup atoms object
surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
layers = [6, 9, 5]
lc = 3.61000
atoms = FaceCenteredCubic('Cu', surfaces, layers, latticeconstant=lc)

# create electrolens plot
molecular_data_properties = el.MolecularDataProperties(columns=['x', 'y', 'z', 'atom'])
plot = el.Plot(molecular_properties=molecular_data_properties)

# create 3D view and add data to it
view = el.ThreeDView(system_name='Cu')
molecular_data = el.MolecularData(data=atoms)
view.add_data(molecular_data)

# add view to the plot
plot.add_view(view)

# show plot
plot.show()
