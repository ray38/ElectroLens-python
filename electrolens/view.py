"""
electrolens view module
"""
from abc import ABC, abstractmethod
from collections import namedtuple
from typing import Union, List
from ase import Atoms, cell
from ase.io.trajectory import TrajectoryReader
from electrolens.converter import Converter, DataFormat
from electrolens import SpatiallyResolvedDataProperties, MolecularDataProperties, FramedDataProperties
import numpy as np


class SpatiallyResolvedData(object):
    """
    spatially resolved data
    """
    def __init__(self,
                 data: Union[str, np.ndarray],
                 grid_points: list = None,
                 grid_spacing: list = None,
                 np_atoms: List[str] = None,
                 ase_cell: cell = None):
        """
        initializes spatially resolved data
        Args:
            data: spatially resolved data. it can be a file path or a numpy array
            grid_points: list of grid_points. e.g. [10,10,10] represents [x,y,z]
            grid_spacing: list of grid spacing. e.g. [0.2,0.2,0.2] represents [x,y,z]
        """
        self.data = data
        self.grid_points = grid_points
        self.grid_spacing = grid_spacing
        self.np_atoms = np_atoms
        self.ase_cell = ase_cell

    def add_configuration(self,
                          configuration: dict,
                          properties: SpatiallyResolvedDataProperties,
                          framed_properties: FramedDataProperties,
                          data_output_file: str) -> None:
        """
        adds spatially resolved data configuration
        Args:
            configuration: the configuration dictionary to add elements in
            properties: spatially resolved data properties provided at plot level
            framed_properties: framed data properties provided at plot level
            data_output_file: filepath if data is to be stored in a file instead of configuration

        Returns: None
        """
        # add additional properties for numpy array
        ExtraProperties = namedtuple('ExtraProperties', ['np_atoms', 'cell'])
        extra_properties = ExtraProperties(np_atoms=self.np_atoms, cell=self.ase_cell)

        # create converter
        converter = Converter.create_converter(data=self.data, target_format=DataFormat.SPATIALLY_RESOLVED_DATA)

        # add configuration
        if data_output_file is not None:
            with open(data_output_file, mode='w', newline='') as file:
                converter.convert(output=configuration,
                                  properties=properties,
                                  extra_properties=extra_properties,
                                  framed_properties=framed_properties,
                                  data_output_file=file)
        else:
            converter.convert(output=configuration,
                              properties=properties,
                              extra_properties=extra_properties,
                              framed_properties=framed_properties)

        # grid points
        configuration['spatiallyResolvedData'] = {}
        srd_config = configuration['spatiallyResolvedData']
        if self.grid_points is not None:
            srd_config['numGridPoints'] = {
                "x": self.grid_points[0],
                "y": self.grid_points[1],
                "z": self.grid_points[2]
            }

        # grid spacing
        if self.grid_spacing is not None:
            srd_config['gridSpacing'] = {
                "x": self.grid_spacing[0],
                "y": self.grid_spacing[1],
                "z": self.grid_spacing[2]
            }


class MolecularData(object):
    """
    electrolens molecular data
    """
    def __init__(self,
                 data: Union[str, Atoms, TrajectoryReader, np.ndarray],
                 np_atoms: List[str] = None,
                 ase_cell: cell = None):
        """
        initializes molecular data
        Args:
            data: molecular data. It can be a file path, an Atoms object, a TrajectoryReader object or a numpy array
            np_atoms: list of columns in case of the data being passed as numpy array
            ase_cell: ASE cell object in case of the data being passed as numpy array
        """
        self.data = data
        self.np_atoms = np_atoms
        self.ase_cell = ase_cell

    def add_configuration(self,
                          configuration: dict,
                          properties: MolecularDataProperties,
                          framed_properties: FramedDataProperties,
                          data_output_file: str) -> None:
        """
        adds molecular data configuration
        Args:
            configuration: configuration dictionary to add elements in
            properties: molecular data properties provided at plot level
            framed_properties: framed data properties provided at plot level
            data_output_file: filepath if data is to be stored in a file instead of configuration

        Returns: None
        """
        # add additional properties for numpy array
        ExtraProperties = namedtuple('ExtraProperties', ['np_atoms', 'cell'])
        extra_properties = ExtraProperties(np_atoms=self.np_atoms, cell=self.ase_cell)

        # create converter
        converter = Converter.create_converter(data=self.data, target_format=DataFormat.MOLECULAR_DATA)

        # add configuration
        if data_output_file is not None:
            with open(data_output_file, mode='w', newline='') as file:
                converter.convert(output=configuration,
                                  properties=properties,
                                  framed_properties=framed_properties,
                                  extra_properties=extra_properties,
                                  data_output_file=file)
        else:
            converter.convert(output=configuration,
                              properties=properties,
                              framed_properties=framed_properties,
                              extra_properties=extra_properties)


class View(ABC):
    """
    base class of electrolens views
    """
    def __init__(self, view_type: str) -> None:
        """
        initializes view object
        Args:
            view_type: type of view. "3DView" or "2DHeatmap"
        """
        self.view_type = view_type

    @abstractmethod
    def get_configuration(self,
                          spatially_resolved_properties: SpatiallyResolvedDataProperties = None,
                          molecular_properties: MolecularDataProperties = None,
                          framed_properties: FramedDataProperties = None) -> dict:
        """
        provides configuration for the complete view
        Args:
            spatially_resolved_properties: spatially resolved data properties provided at plot level
            molecular_properties: molecular data properties provided at plot level
            framed_properties: framed data properties provided at plot level

        Returns: dictionary containing view configuration
        """
        raise NotImplementedError()


class ThreeDView(View):
    """
    3D View
    """
    def __init__(self, system_name: str, system_dimensions: list = None, system_lattice_vectors: list = None):
        """
        initializes electrolens 3D view
        Args:
            system_name: system name or molecule name
            system_dimensions: system dimensions e.g. [1,1,1] represents [x,y,z] values
            system_lattice_vectors: nested lists for lattice vectors e.g. [[1,0,0],[0,1,0],[0,0,1]] represents
            [[u11,u12,u13],[u21,u22,u23],[u31,u32,u33]]
        """
        super().__init__("3DView")

        # system name
        self.system_name = system_name

        # system dimensions
        self.system_dimensions = None
        if system_dimensions is not None:
            self.system_dimensions = {
                'x': system_dimensions[0],
                'y': system_dimensions[1],
                'z': system_dimensions[2]
            }

        # system lattice vectors
        self.system_lattice_vectors = None
        if system_lattice_vectors is not None:
            vectors = system_lattice_vectors
            self.system_lattice_vectors = {
                'u11': vectors[0][0], 'u12': vectors[0][1], 'u13': vectors[0][2],
                'u21': vectors[1][0], 'u22': vectors[1][1], 'u23': vectors[1][2],
                'u31': vectors[2][0], 'u32': vectors[2][1], 'u33': vectors[2][2]
            }

        # input data
        self.spatially_resolved_data = None
        self.molecular_data = None
        self.spatially_resolved_output_file = None
        self.molecular_output_file = None

    def add_data(self, data: Union[SpatiallyResolvedData, MolecularData], output_data_file: str = None):
        """
        adds data to view
        Args:
            data: spatially resolved or molecular data to be added
            output_data_file: filepath if the data is to be written in a file instead of configuration. This is not
            required if input data is already a file

        Returns: None
        """
        if isinstance(data, SpatiallyResolvedData) or isinstance(data, MolecularData):
            if isinstance(data.data, str) and output_data_file is not None:
                raise ValueError("output_data_file is not supported when input is already a file")

            if isinstance(data, SpatiallyResolvedData):
                self.spatially_resolved_data = data
                self.spatially_resolved_output_file = output_data_file
            elif isinstance(data, MolecularData):
                self.molecular_data = data
                self.molecular_output_file = output_data_file
            else:
                raise ValueError("Unknown data format")

    def get_configuration(self,
                          spatially_resolved_properties: SpatiallyResolvedDataProperties = None,
                          molecular_properties: MolecularDataProperties = None,
                          framed_properties: FramedDataProperties = None) -> dict:
        """
        provides configuration for the complete view
        Args:
            spatially_resolved_properties: spatially resolved data properties provided at plot level
            molecular_properties: molecular data properties provided at plot level
            framed_properties: framed data properties provided at plot level

        Returns: dictionary containing view configuration
        """
        configuration = {
            'viewType': self.view_type,
            'moleculeName': self.system_name
        }

        if self.system_dimensions is not None:
            configuration['systemDimension'] = self.system_dimensions

        if self.system_lattice_vectors is not None:
            configuration['systemLatticeVectors'] = self.system_lattice_vectors

        if spatially_resolved_properties is not None:
            self.spatially_resolved_data.add_configuration(configuration, spatially_resolved_properties,
                                                           framed_properties, self.spatially_resolved_output_file)

        if molecular_properties is not None:
            self.molecular_data.add_configuration(configuration, molecular_properties,
                                                  framed_properties, self.molecular_output_file)

        # default system dimensions and lattice vectors
        if 'systemDimension' not in configuration:
            configuration['systemDimension'] = {'x': 10, 'y': 10, 'z': 10}

        if 'systemLatticeVectors' not in configuration:
            configuration['systemLatticeVectors'] = {
                'u11': 1, 'u12': 0, 'u13': 0,
                'u21': 0, 'u22': 1, 'u23': 0,
                'u31': 0, 'u32': 0, 'u33': 1,
            }

        return configuration


class TwoDHeatmap(View):
    """
    2D Heatmap view
    """
    def __init__(self, plot_x: str, plot_y: str, plot_x_transform: str, plot_y_transform: str):
        """
        initializes 2D Heatmap view
        Args:
            plot_x: plot_x value
            plot_y: plot_y value
            plot_x_transform: plot_x transform value
            plot_y_transform: plot_y transform value
        """
        super().__init__('2DHeatmap')
        self.plot_x = plot_x
        self.plot_y = plot_y
        self.plot_x_transform = plot_x_transform
        self.plot_y_transform = plot_y_transform

    def get_configuration(self,
                          spatially_resolved_properties: SpatiallyResolvedDataProperties = None,
                          molecular_properties: MolecularDataProperties = None,
                          framed_properties: FramedDataProperties = None) -> dict:
        """
        provides configuration for the complete view
        Args:
            spatially_resolved_properties: spatially resolved data properties provided at plot level
            molecular_properties: molecular data properties provided at plot level
            framed_properties: framed data properties provided at plot level

        Returns: dictionary containing view configuration
        """
        configuration = {
            'view': {
                'viewType': self.view_type,
                'plotX': self.plot_x,
                'plotY': self.plot_y,
                'plotXTransform': self.plot_x_transform,
                'plotYTransform': self.plot_y_transform
            },
            'plot_setup': {
            }
        }

        return configuration
