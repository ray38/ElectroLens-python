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

# show plot
plot.show()

# save configuration
plot.save_configuration(output_json_file='config.json')
