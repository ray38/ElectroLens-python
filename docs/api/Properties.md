# Properties

Properties are used to define the structure of the data being visualized. Because ElectroLens can handle so many different data formats, the application cannot make any assumptions about the structure of the data--that is, ElectroLens needs to be told what each column in a data set represents (i.e. is this column the x coordinate of the atom, is it the name of the atom, etc). 

At a minimum, each `Properties` object will include three properties for physical coordinates to actually visualize atoms in space, but data sets could contain additional properties which the user must define.

A `Properties` object is created and used at the `Plot` level, so a set of properties for a given data type will apply to all data sets of the corresponding type in that plot (i.e. all molecular data sets should have the columns defined in the plot's `MolecularDataProperties` object).

## MolecularDataProperties (object)

### Initialization

```python
molecular_data_properties = el.MolecularDataProperties(columns=['x', 'y', 'z', 'atom'])
```

Parameters:

- `columns` (optional): a list of properties to be plotted in the visualization
  
  - If none provided, the default is `['x', 'y', 'z']`
  
  - Otherwise, if a list is provided, it must contain the 3D coordinates at a minimum

## SpatiallyResolvedDataProperties (object)

#### Initialization

```python
spatially_resolved_properties = el.SpatiallyResolvedDataProperties(
    columns=['x', 'y', 'z', 'rho', "gamma", "epxc", "deriv1", "deriv2"],
    density_property='rho', density_lower_limit=0.00001,  density_upper_limit=1000000)
```

Parameters:

- `columns` (optional): a list of properties to be plotted in the visualization
  
  - If none provided, the default is `['x', 'y', 'z', 'rho']`
  
  - Otherwise, if a list is provided, it must contain the 3D coordinates and the `density_property` at a minimum

- `density_property` (optional): column in `columns` corresponding to the density of the atom
  
  - If none provided, default is `'rho'`
  
  - Provided value must be in `columns`

- `density_lower_limit` (optional): lower limit of the `density_property`
  
  - If none provided, default is `1e-3`

- `density_upper_limit` (optional): lower limit of the`density_property`
  
  - If none provided, default is `1e6`

## FramedDataProperties (object)

Framed data represents data that changes over time in a dynamic system. A "frame" represents a single point in time in a simulation. Framed data sets contain atomic data (either molecular or spatially resolved) for each atom in the system at each point in time.

To show the behavior of a system over time, a `Plot` must be provided with the name of the column in data sets corresponding to the frame. ElectroLens can then gather and visualize the atomic data at each unique frame.

The `FramedDataProperties` object is unique in that, unlike the previous 2 sets of properties, there is no corresponding 'framed data' type. Either molecular or spatially resolved data can be framed, and ElectroLens will automatically check to see if the data is framed using the `frame_column` provided by the user.

#### Initialization

```python
framed_properties = el.FramedDataProperties(frame_column="frame")
```

Parameters:

- `frame_column` (optional): name of the column in the data set that corresponds to the frame number in a molecular simulation over time
  
  - If none provided, default is `'frame'`
