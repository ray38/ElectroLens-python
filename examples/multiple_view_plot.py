"""
electrolens example to view multiple 3D Views
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
plot.add_view(view)

# you can add multiple views (3D or 2D) to a plot
# adding same view again
plot.add_view(view)

# will have to figure out the correct values but this will be the api to add a TwoDHeatmap
# not sure about the parameters here. It does show the 2D panel though.
# view2 = el.TwoDHeatmap(plot_x="0", plot_y="0", plot_x_transform="linear", plot_y_transform="linear")
# plot.add_view(view2)

# show plot
plot.show()
