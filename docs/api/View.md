# Views

The `View` module serves as the container for the actual data set. ElectroLens creates visualizations at `View` granularity; each view added to a plot has its data visualized in the browser window. Multiple views in a plot results in multiple visualizations of different molecular systems. 

Views hold all atomic data as well as the metadata associated with a particular visualization, such as the dimensions of the system in which the atoms exist. A single view can simulatenously hold both molecular data and spatially resolved data.

## ThreeDView

A `ThreeDView` is used to show ball-and-stick molecules and atoms in the system. The coordiantes provided in the data set are used to place atoms and molecules in 3D space.

### Initializer

```python
el.ThreeDView(system_name: str, system_dimensions: list, system_lattice_vectors: list)
```

### Parameters

| **Name**               | **Type** | **Description**                              |
| ---------------------- | -------- | -------------------------------------------- |
| system_name            | `str`    | The name of this view/molecular system       |
| system_dimensions      | `list`   | Dimensions of cell in which atoms are placed |
| system_lattice_vectors | `list`   | Nested lists for lattice vectors             |

#### system_name

*Type:* `str` 

The name of this view/molecular system.

#### system_dimensions

*Type:* `list` *(Optional, default: `[10, 10, 10]`)*

List of xyz values representing the size of the 3D system.

#### system_lattice_vectors

*Type:* `list` *(Optional, default: `[[1,0,0], [0, 1, 0], [0, 0, 1]]`)*

Nested lists of coordiantes used to construct a lattice in which atoms are placed.

### Methods

| **Name**                         | **Description**           |
| -------------------------------- | ------------------------- |
| add_data(data, output_data_file) | Adds a data set to a view |

#### add_data(data, output_data_file)

```python
def add_data(self, data: Union[SpatiallyResolvedData, MolecularData], output_data_file) -> None
```

*Parameters:*

- **data**: [`SpatiallyResolvedData`](./Data.md#SpatiallyResolvedData) or [`MolecularData`](./Data.md#MolecularData)

- **output_data_file**: `str` *(Optional, default is `None`)*

*Returns: none*

Adds a data set to the view, enabling it to be visualized. If output_data_file is provided, the data passed in is written to a CSV file at the specified path; the generated JSON configuration will hold a path to this file rather than the data itself. This feature is useful in the case of extremely large data sets. 

*Note: If the data passed in is a CSV file itself, an output file path cannot be provided.*
