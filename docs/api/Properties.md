# Properties

*Insert description later!!!!!!!!*

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

#### Initialization

```python
framed_properties = el.FramedDataProperties(frame_column="frame")
```

Parameters:

- `frame_column` (optional): name of the column in the data set that corresponds to the frame number in a molecular simulation over time
  
  - If none provided, default is `'frame'`
