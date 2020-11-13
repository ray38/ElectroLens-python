# ElectroLens

ElectroLens is an easy-to-use tool for visualizing highly dimensional atomic data sets. Originally written in JavaScript, this python application was built to serve as a wrapper to the main body of code and enable developers working with [ASE](https://wiki.fysik.dtu.dk/ase/index.html) to easily integrate ElectroLens into their projects and create fast, easy visualizations with their data sets.

## Installation

#### Requirements

- Python 3.6 or newer

- ASE

- NumPy

The simplest way to install ElectroLens is through pip:

```shell
pip install electrolens-python
```

## Getting Started

This section will provide a quick introduction into the ElectroLens API and how visualizations are created.

To start, let's examine this simple block of code that will create a 3D visualization using ASE atoms:

```python
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
```

#### ASE Atoms

This script makes use of the ASE `Atoms` object to create a set of molecules for visualization. For more information, please refer to the ASE documentation.

```python
# setup atoms object
surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
layers = [6, 9, 5]
lc = 3.61000
atoms = FaceCenteredCubic('Cu', surfaces, layers, latticeconstant=lc)
```

#### Plot

The `Plot` acts as the main canvas on which to create visualizations. We can visualize several data sets within a single plot. ElectroLens makes no assumptions about the structure of the data it receives, particularly the properties of the data set. The user must explicitly state the names of the properties that the data contains and that user wishes to visualize on the plot. *(Note: at the very minimum, the list of properties must contain 'x', 'y', and 'z' so that ElectroLens can actually create a plot of all of the atoms in space.*) An ASE `Atoms` object represents a set of atoms at a single point in time and all of their 3D coordinates, so this would fall under the category of `MolecularDataProperties`; we create the set of properties and add it to the plot. For all molecular data sets visualized on this plot, this set of properties will be used.

```python
# create electrolens plot
molecular_data_properties = el.MolecularDataProperties(columns=['x', 'y', 'z', 'atom'])
plot = el.Plot(molecular_properties=molecular_data_properties)
```

#### View

The `View` is what contains the data itself. Here the user passes in the data it wishes to be visualized, and the view is added to the plot. Just as we did in creating the plot, we must explicitly state the structure of the data. Data is passed from ElectroLens-python to ElectroLens-JS via JSON configuration files created through a conversion process within the python application. Different data formats undergo different conversion processes in order to create the appropriate JSON configuration file that the JS code can interpret, so it is necessary for the user to specify the data format so that the proper visualization is created. `Atoms` objects are a type of molecular data, so create a new `MolecularData` object, add it to the view, and add the view to the plot.

```python
# create 3D view and add data to it
view = el.ThreeDView(system_name='Cu')
molecular_data = el.MolecularData(data=atoms)
view.add_data(molecular_data)

# add view to the plot
plot.add_view(view)
```

#### Visualization

To start the visualization, simply execute `plot.show()` , which will create a new window containing all of the views added to the plots. This simple script will produce the following visualization:

<img src="/docs/images/single_view_example.png" />
