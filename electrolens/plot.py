"""
electrolens plot module
"""

import json
from typing import List

from electrolens.embedded_browser import load_browser


class SpatiallyResolvedDataProperties(object):
    """
    electrolens Plot properties for Spatially Resolved Data
    """
    required_columns = {'x', 'y', 'z'}

    def __init__(self,
                 columns: List[str],
                 density_property: str = 'rho',
                 density_lower_limit: float = 1e-3,
                 density_upper_limit: float = 1e6):
        """
        Spatially Resolved Data properties setup for the plot
        Args:
         columns: list of columns for spatially resolved data
         density_property: column that denotes density
         density_lower_limit: density lower limit
         density_upper_limit: density upper limit
        """
        self.columns = columns
        self.density_property = density_property
        self.density_lower_limit = density_lower_limit
        self.density_upper_limit = density_upper_limit

        # validate columns
        if self.columns is None:
            self.columns = list(SpatiallyResolvedDataProperties.required_columns)
            self.columns.append(self.density_property)
        else:
            if density_property not in self.columns:
                raise ValueError("density_property should be available in columns list")
            elif len(set(SpatiallyResolvedDataProperties.required_columns) - set(self.columns)) > 0:
                raise ValueError("columns list should contain 'x', 'y', 'z' and the density property at least")

    def add_plot_setup(self, configuration: dict) -> None:
        """
        adds plot setup elements for spatially resolved data
        Args:
            configuration: configuration dictionary to add elements in

        Returns: None
        """
        # add 'atom' to list of properties in JSON config if not already present in the columns list
        # create a copy of the list so 'atom' does not get added to self.columns
        cols_copy = self.columns.copy()
        if 'atom' not in cols_copy:
            cols_copy.append('atom')
        configuration['spatiallyResolvedPropertyList'] = cols_copy

        configuration['pointcloudDensity'] = self.density_property
        configuration['densityCutoffLow'] = self.density_lower_limit
        configuration['densityCutoffUp'] = self.density_upper_limit


class MolecularDataProperties(object):
    """
    electrolens Plot properties for Molecular Data
    """
    required_columns = {'x', 'y', 'z'}

    def __init__(self, columns: List[str]):
        """
        Molecular Data properties setup for the plot
        Args:
            columns: list of columns for molecular data
        """
        self.columns = columns

        # validate columns
        if self.columns is None:
            self.columns = list(MolecularDataProperties.required_columns)
        elif len(MolecularDataProperties.required_columns - set(self.columns)) > 0:
            raise ValueError("columns list should contain 'x','y','z' columns at least")

    def add_plot_setup(self, configuration: dict) -> None:
        """
        adds plot setup elements for molecular data
        Args:
            configuration: configuration dictionary to add elements in

        Returns: None
        """
        # add 'atom' to list of properties in JSON config if not already present in the columns list
        # create a copy of the list so 'atom' does not get added to self.columns
        cols_copy = self.columns.copy()
        if 'atom' not in cols_copy:
            cols_copy.append('atom')
        configuration['moleculePropertyList'] = cols_copy


class FramedDataProperties(object):
    """
    electrolens Plot properties for Framed Data
    """
    def __init__(self, frame_column: str = 'frame'):
        """
        Framed Data properties setup for the plot
        Args:
            frame_column: framed column name
        """
        self.frame_column = frame_column

    def add_plot_setup(self, configuration: dict) -> None:
        """
        adds plot setup elements for framed data
        Args:
            configuration: configuration dictionary to add elements in

        Returns: None
        """
        configuration['frameProperty'] = self.frame_column


class Plot(object):
    """
    electrolens Plot
    """
    def __init__(self,
                 spatially_resolved_properties: SpatiallyResolvedDataProperties = None,
                 molecular_properties: MolecularDataProperties = None,
                 framed_properties: FramedDataProperties = None,
                 configuration_file: str = None):
        """
        initializes electrolens Plot

        Args:
            spatially_resolved_properties: spatially resolved data properties
            molecular_properties: molecular data properties
            framed_properties: framed data properties
            configuration_file: input configuration file to be used for plot. Other arguments are not required if this
            argument is provided. If this is not provided then at least one of the spatially_resolved_properties and
            molecular_properties arguments need to be provided
        """
        # validate arguments
        if configuration_file is None:
            if spatially_resolved_properties is None and molecular_properties is None:
                raise ValueError("Either spatially resolved or molecular properties should be provided \
                when configuration_file is not provided")
            else:
                if framed_properties is not None:
                    # check if frame column is available in spatially resolved properties
                    if (spatially_resolved_properties is not None and
                            framed_properties.frame_column not in spatially_resolved_properties.columns):
                        raise ValueError(f"Frame column, {framed_properties.frame_column}, should be available \
                        in spatially resolved properties list")

                    # check if frame column is available in molecular properties
                    if (molecular_properties is not None and
                            framed_properties.frame_column not in molecular_properties.columns):
                        raise ValueError(f"Frame column, {framed_properties.frame_column}, should be available \
                        in molecular properties list")
        else:
            # other arguments are not required if configuration_file is provided
            if (spatially_resolved_properties is not None or
                    molecular_properties is not None or
                    framed_properties is not None):
                raise ValueError("Other arguments should not be provided when configuration_file is provided")

        self.__views__ = []
        self.spatially_resolved_properties = spatially_resolved_properties
        self.molecular_properties = molecular_properties
        self.framed_properties = framed_properties
        self.input_configuration_file = configuration_file

    def add_view(self, plot_view) -> None:
        """
        adds view to the plot
        Args:
            plot_view: view object to be added to the plot

        Returns: None
        """
        if self.input_configuration_file is not None:
            raise ValueError("View cannot be added when configuration file has been provided")

        self.__views__.append(plot_view)

    def remove_view(self, plot_view) -> None:
        """
        removes a view from the plot
        Args:
            plot_view: existing view object in the plot

        Returns: None
        """
        self.__views__.remove(plot_view)

    def show(self) -> None:
        """
        displays electrolens plot
        Returns: None
        """
        load_browser(self.__create_configuration__())

    def save_configuration(self, output_json_file) -> None:
        """
        saves plot configuration file
        Args:
            output_json_file: file path where plot configuration will be saved

        Returns: None
        """
        configuration = self.__create_configuration__()
        with open(output_json_file, 'w') as fp:
            json.dump(configuration, fp, indent=4)

    def __create_configuration__(self) -> dict:
        """
        creates plot configuration
        Returns: configuration dictionary
        """
        configuration = {}
        if self.input_configuration_file:
            with open(self.input_configuration_file, 'r') as file:
                configuration = json.load(file)
        elif len(self.__views__) == 0:
            raise ValueError("No view found")
        else:
            # create configuration
            configuration = {
                'views': [],
                'plotSetup': self.__get_plot_setup__()
            }

            for view in self.__views__:
                view_configuration = view.get_configuration(
                    spatially_resolved_properties=self.spatially_resolved_properties,
                    molecular_properties=self.molecular_properties,
                    framed_properties=self.framed_properties)
                configuration['views'].append(view_configuration)

        return configuration

    def __get_plot_setup__(self) -> dict:
        """
        returns plot setup element of the configuration
        Returns: plot setup dictionary
        """
        configuration = {}
        if self.spatially_resolved_properties is not None:
            self.spatially_resolved_properties.add_plot_setup(configuration)

        if self.molecular_properties is not None:
            self.molecular_properties.add_plot_setup(configuration)

        if self.framed_properties is not None:
            self.framed_properties.add_plot_setup(configuration)

        return configuration
