"""
electrolens example to view a single 3D View
"""

from ase.cluster.cubic import FaceCenteredCubic
import electrolens as el

# setup atoms object
surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
layers = [6, 9, 5]
lc = 3.61000
atoms = FaceCenteredCubic('Cu', surfaces, layers, latticeconstant=lc)

# create electrolens plot
plot = el.Plot()

# create and add a 3d view to the plot
# depending on the input data, the user will decide if it needs to be converted as framed,
# molecular or spatially resolved data
view = el.ThreeDView(input_data=atoms, data_format=el.DataFormat.MOLECULAR_DATA, molecule_name='Cu')

# add view to the plot
plot.add_view(view)

# show plot
plot.show()
