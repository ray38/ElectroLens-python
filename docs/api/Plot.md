# Plots

The `Plot` module represents the top-level container of all data sets being visualized. A `Plot` object will hold properties objects to be applied to data sets as well as the data sets themselves, containerized into `View`s.

## Plot (object)

### Initializer

```python
el.Plot(spatially_resolved_properties: SpatiallyResolvedDataProperties, molecular_properties: MolecularDataProperties, framed_properties: FramedDataProperties, configuration_file: str)
```

### Parameters

| **Name**                      | **Type**                                                              | **Description**                             |
| ----------------------------- | --------------------------------------------------------------------- | ------------------------------------------- |
| spatially_resolved_properties | [`SpatiallyResolvedDataProperties`](#SpatiallyResolvedDataProperties) | Properties for spatially resolved data sets |
| molecular_properties          | `MolecularDataProperties`                                             | Properties for molecular data sets          |
| framed_properties             | `FramedDataProperties`                                                | Frame property in data sets                 |
| configuration_file            | `str`                                                                 | JSON configuration file                     |

*If configuration_file provided, none of the properties parameters can be provided. Otherwise, ** at least one** of `SpatiallyResolvedDataProperties` and `MolecularDataProperties` must be provided*

#### spatially_resolved_properties

*Type:* `SpatiallyResolvedDataProperties`

Specifies the set of properties to be used for visualizing all spatially resolved data sets added to the plot

#### molecular_properties

*Type:* `MolecularDataProperties`

Specifies the set of properties to be used for visualizing all molecular data sets added to the plot

#### framed_properties

*Type:* `FramedDataProperties`

Specifies the column name of the frame property present in the atomic data property sets provided

*If this parameter is provided, the provided column name must be present in both of the provided sets of properties*

#### configuration_file

*Type:* `str`

A path to a JSON configuration file from a prior ElectroLens visualization. ElectroLens uses JSON files to hold all the data to be visualized as well as other settings of the visualization. This file is created from the provided data sets via a conversion process; if the user already has such a file, it can be directly provided.

### Methods

| **Name**                             | **Description**                              |
| ------------------------------------ | -------------------------------------------- |
| add_view(plot_view)                  | Add a view                                   |
| remove_view(plot_view)               | Remove a view                                |
| show()                               | Create the visualization for the plot's data |
| save_configuration(output_json_file) |                                              |

#### add_view(plot_view)

```python
def add_view(self, plot_view: View) -> None
```

*Parameters:*

- **plot_view**: `View`

*Returns: none*

Adds the provided view to the current plot. The data in the view will be visualized.

#### remove_view(plot_view)

```python
def remove_view(self, plot_view: View) -> None
```

*Parameters:*

- **plot_view**: `View`

*Returns: none*

Removes the provided view from the plot

#### show()

```python
def show(self) -> None
```

*Parameters: none*

*Returns: none*

Creates a visualization of all the views contained within the plot; creates a new browser window visualizing all provided data.

Invokes CEF-Python to create a browser window with embedded JavaScript (i.e. the main ElectroLens code)

#### save_configuration(output_json_file)

```python
def save_configuration(self, output_json_file: str) -> None
```

*Parameters:*

- **output_json_file**: `str` - File path where generated JSON configuration file will be saved

*Returns: none*

Saves the JSON configuration file created for data sets in the plot at the file specified by the provided path


