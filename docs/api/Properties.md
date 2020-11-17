# Properties

Properties are used to define the structure of the data being visualized. Because ElectroLens can handle so many different data formats, the application cannot make any assumptions about the structure of the data--that is, ElectroLens needs to be told what each column in a data set represents (i.e. is this column the x coordinate of the atom, is it the name of the atom, etc). 

At a minimum, each properties object will include three properties for physical coordinates to actually visualize atoms in space, but data sets could contain additional properties which the user must define.

A properties object is created and used at the [`Plot`](./Plot.md#Plot) level, so a set of properties for a given data type will apply to all data sets of the corresponding type in that plot (i.e. all molecular data sets should have the columns defined in the plot's `MolecularDataProperties` object).

## MolecularDataProperties

### Initializer

```python
el.MolecularDataProperties(columns: list)
```

### Parameters

| **Name** | **Type** | **Description**                                |
| -------- | -------- | ---------------------------------------------- |
| columns  | `list`   | A list of column names for molecular data sets |

#### columns

*Type:* `list` *(Optional, default: `['x', 'y', 'z']`)*

Specifies a list of column names for properties to be visualized for all molecular data sets in the plot. If a list is provided, it must contain at least the default xyz coordinates.

## SpatiallyResolvedDataProperties

### Initializer

```python
el.SpatiallyResolvedDataProperties(columns: list, density_property: str, density_lower_limit: float, density_upper_limit: float)
```

### Parameters

| **Name**            | **Type** | **Description**                                                     |
| ------------------- | -------- | ------------------------------------------------------------------- |
| columns             | `list`   | A list of column names for spatially resolved data sets             |
| density_property    | `str`    | Column/property in columns corresponding to the density of the atom |
| density_lower_limit | `float`  | Lower limit of the density_property                                 |
| density_upper_limit | `float`  | Upper limit of the density_property                                 |

#### columns

*Type:* `list` *(Optional, default: `['x', 'y', 'z', 'rho']`)*

Specifies a list of column names for properties to be visualized for all spatially resolved data sets in the plot. If a list is provided, it must contain at least the default xyz coordinates as well as the provided density_property.

#### density_property

*Type:* `str` *(Optional, default: `'rho'`)*

Columns name in columns list corresponding to the density of the atom. If a value is provided it must appear in the columns list provided.

#### density_lower_limit

*Type:* `float` *(Optional, default: `1e-3`)*

Lower limit of the density_property.

#### density_upper_limit

*Type:* `float` *(Optional, default: `1e6`)*

Lower limit of the density_property.

## FramedDataProperties

Framed data represents data that changes over time in a dynamic system. A "frame" represents a single point in time in a simulation. Framed data sets contain atomic data (either molecular or spatially resolved) for each atom in the system at each point in time.

To show the behavior of a system over time, a [`Plot`](./Plot.md#Plot) must be provided with the name of the column in data sets corresponding to the frame. ElectroLens can then gather and visualize the atomic data at each unique frame.

The `FramedDataProperties` object is unique in that, unlike the previous 2 sets of properties, there is no corresponding 'framed data' type. Either molecular or spatially resolved data can be framed, and ElectroLens will automatically check to see if the data is framed using the `frame_column` provided by the user.

### Initializer

```python
el.FramedDataProperties(frame_column: str)
```

### Parameters

| **Name**     | **Type** | **Description**                                  |
| ------------ | -------- | ------------------------------------------------ |
| frame_column | `str`    | Name of the column representing the frame number |

#### frame_column

*Type:* `str` *(Optional, default: `'frame'`)*

Name of the column in the data set that corresponds to the frame number in a molecular simulation over time
