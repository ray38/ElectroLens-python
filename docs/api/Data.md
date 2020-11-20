# Data

Data objects act as wrappers for data sets. These objects hold the data sets themselves as well as some metadata necessary for converting the sets to JSON configuration that ElectroLens can understand.

## MolecularData

### Initializer

```python
el.MolecularData(data: Union[str, Atoms, TrajcetoryReader, numpy.ndarray], np_atoms: list, ase_cell: cell)
```

### Parameters

| **Name** | **Type**                                                                                                                                                               | **Description**                                                               |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| data     | `str`, ASE [`Atoms`](https://wiki.fysik.dtu.dk/ase/ase/atoms.html), ASE [`TrajectoryReader`](https://wiki.fysik.dtu.dk/ase/ase/io/trajectory.html), or `numpy.ndarray` | The data set to visualize                                                     |
| np_atoms | `list`                                                                                                                                                                 | List of atom names for each row of data if 2D numpy array is passed into data |
| ase_cell | ASE `cell`                                                                                                                                                             | ASE cell object provided if data is passed in as a numpy array                |

#### data

*Type:* `str`, ASE [`Atoms`](https://wiki.fysik.dtu.dk/ase/ase/atoms.html), ASE [`TrajectoryReader`](https://wiki.fysik.dtu.dk/ase/ase/io/trajectory.html), or `numpy.ndarray`

The data set to visualize. The input must be one of the following types:

- `str`: a path to a CSV file containing the data

- [`Atoms`](https://wiki.fysik.dtu.dk/ase/ase/atoms.html): an ASE object containing molecular data such as coordiantes, atom names, cell information

- [`TrajectoryReader`](https://wiki.fysik.dtu.dk/ase/ase/io/trajectory.html): an ASE object used to hold framed molecular data

- `numpy.ndarray`: a 2D array of molecular data, in which each row represents data for a single atom, and the columns are properties as usual; for example:
  
  - ```python
    data = numpy.array([[2.96673, 2.64244, 5.63191, 1], [1, 2.64159, 5.63251, 2]])
    ```

#### np_atoms

*Type:* `list` *(Required only if data is of type `numpy.ndarray` and `'atom'` is not included in the plot's [`MolecularDataProperties`](./Properties.md#MolecularDataProperties) `columns` list and input data)*

A list of atom names corresponding to each row in the provided 2D array. Other molecular data formats will contain this data by default, but when using arrays to pass in data it must be explicitly stated. For example, for the sample data passed in above, the passed in list of atoms would look like the following:

```python
atoms = ['Fe', 'Fe']
```

#### ase_cell

*Type:* `cell` *(Required only if data is of type `numpy.ndarray`)*

An [ASE cell](https://wiki.fysik.dtu.dk/ase/ase/cell.html) object representing three lattice vectors forming a parallelepiped.

## SpatiallyResolvedData

### Initializer

```python
el.SpatiallyResolvedData(data: Union[str, numpy.ndarry], grid_points: list, grid_spacing: list, np_atoms: list, ase_cell: cell)
```

### Parameters

| **Name**     | **Type**                | **Description**                                                               |
| ------------ | ----------------------- | ----------------------------------------------------------------------------- |
| data         | `str` or `numpy.ndarry` | Spatially resolved data set to visualize                                      |
| grid_points  | `list`                  | `[x, y, z]` list of the number of grid points in each direction               |
| grid_spacing | `list`                  | `[x, y, z]` list of the spacing between grid points in each direction         |
| np_atoms     | `list`                  | List of atom names for each row of data if 2D numpy array is passed into data |
| ase_cell     | ASE `cell`              | ASE cell object provided if data is passed in as a numpy array                |

#### data

*Type:* `str` or `numpy.ndarry` 

The data set to visualize. The input must be one of the following types:

- `str`: a path to a CSV file containing the data

- `numpy.ndarray`: a 2D array of molecular data, in which each row represents data for a single atom, and the columns are properties as usual

#### grid_points

*Type:* `list` *(Optional)*

`[x, y, z]` list of the number of grid points in each direction

#### grid_spacing

*Type:* `list` *(Optional)*

`[x, y, z]` list of the spacing between grid points in each direction

#### np_atoms

*Type:* `list` *(Required only if data is of type `numpy.ndarray` and `'atom'` is not included in the plot's [`SpatiallyResolvedDataProperties`](./Properties.md#SpatiallyResolvedDataProperties) `columns` list and input data)*

A list of atom names corresponding to each row in the provided 2D array. Other molecular data formats will contain this data by default, but when using arrays to pass in data it must be explicitly stated. For example, for the sample data passed in above, the passed in list of atoms would look like the following:

```python
atoms = ['Fe', 'Fe']
```

#### ase_cell

*Type:* `cell` *(Required only if data is of type `numpy.ndarray`)*

An [ASE cell](https://wiki.fysik.dtu.dk/ase/ase/cell.html) object representing three lattice vectors forming a parallelepiped.
