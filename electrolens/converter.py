"""converter module contains classes for Spatially Resolved, Molecular and Framed Data conversions from input data"""

from enum import Enum
from ase import Atoms, cell
from ase.io.trajectory import TrajectoryReader
from sklearn.preprocessing import normalize
import typing
import csv
import os
import numpy as np


class DataFormat(Enum):
    """
    enumeration for electrolens acceptable data format
    """
    TRAJECTORY_DATA = 1
    ATOMS_DATA = 2
    SPATIALLY_RESOLVED_DATA = 3
    ARRAY_DATA = 4


class Converter(object):
    """
    base class for converters that convert input data to electrolens acceptable format
    """

    def __init__(self, input_data):
        """
        initializes a Converter object

        :param input_data: input data object to be converted by the Converter
        """
        self._input_data = input_data
        self._output_data = {'view': {}, 'plot_setup': {}}

    @staticmethod
    def create_converter(data_format: DataFormat, data, np_column_names: list, np_atoms: list, np_framed: bool,
                         np_frame_column: str, np_atoms_cell: cell.Cell):
        """
        creates new converter

        :param np_atoms_cell: ASE Cell object. The Cell object represents three lattice vectors forming the dimensions
                              of the system. Required only when converting from a numpy array of molecular data.
                              ASE Atoms and trajectory data implicitly have this information - when working with just
                              a 2D array of properties, it must be explicitly provided by the user
        :param np_frame_column: the name of the column representing the frame. Required only when converting from numpy.
                                electrolens needs to know the name of the property representing the frame in the simulation
                                in order to display atoms at each frame
        :param np_framed: boolean stating if numpy array data is framed. Default is false
        :param np_atoms: list of atom names for each row in 2D numpy array. when data is 2D array, each row contains
                         properties for a single atom - this list provides the name of each atom for every row
        :param np_column_names: list of column names corresponding to each column in the 2D numpy array. Need the column
                                names so they can be added to JSON configuration
        :param data_format: DataFormat enumeration value representing the type of converter to be created
        :param data: input data object. It can be of any supported type

        :return: newly created Converter object
        """
        if data_format == DataFormat.TRAJECTORY_DATA:
            return ASETrajectoryDataConverter(data)

        if data_format == DataFormat.ATOMS_DATA:
            return ASEAtomsDataConverter(data)

        if data_format == DataFormat.SPATIALLY_RESOLVED_DATA:
            return SpatiallyResolvedDataConverter(data)

        if data_format == DataFormat.ARRAY_DATA:
            return ArrayDataConverter(data, np_column_names, np_atoms, np_framed, np_frame_column, np_atoms_cell)

        raise TypeError("Unknown data format")

    def convert(self, output_file: typing.IO = None) -> dict:
        """
        converts input data to electrolens acceptable format

        :param output_file: an open file handle to write the configuration for converted data to
        :return: a dictionary containing electrolens configuration entries for converted data. The dictionary contains
        keys for view and plot setup as 'view' and 'plot_setup' respectively.
        """
        raise NotImplementedError()

    def _init_atoms(self, atoms_cell: cell.Cell, data_file: typing.IO) -> None:
        """
        fills up _output_data with common configurations for Atoms object

        :param atoms_cell: ASE cell that describes the system dimensions
        :param data_file: output data file
        :return: None
        """
        lattice_constants = atoms_cell.lengths()
        self._output_data['plot_setup'] = {
            'moleculePropertyList': ['atom']
        }

        self._output_data['view']['systemDimension'] = {
            'x': lattice_constants[0],
            'y': lattice_constants[1],
            'z': lattice_constants[2]
        }

        lattice_vector = normalize(atoms_cell, axis=1)
        self._output_data['view']['moleculeData'] = {
            'systemLatticeVectors': {
                'u11': lattice_vector[0][0], 'u12': lattice_vector[0][1], 'u13': lattice_vector[0][2],
                'u21': lattice_vector[1][0], 'u22': lattice_vector[1][1], 'u23': lattice_vector[1][2],
                'u31': lattice_vector[2][0], 'u32': lattice_vector[2][1], 'u33': lattice_vector[2][2]
            }
        }

        if data_file:
            abs_path = os.path.abspath(data_file.name)
            self._output_data['view']['moleculeData']['dataFilename'] = abs_path.replace('\\', '/')


class SpatiallyResolvedDataConverter(Converter):
    """
    Converter that converts input data to configuration related to Spatially Resolved Data
    """

    def convert(self, output_file: typing.IO = None) -> dict:
        pass


class ASEAtomsDataConverter(Converter):
    """
    Converter that converts input data to configuration related to Molecular Data
    """

    def convert(self, output_file: typing.IO = None) -> dict:
        if isinstance(self._input_data, Atoms):
            self.__convert_from_atoms__(output_file)
        else:
            raise TypeError('input data is not ASE molecular data')

        return self._output_data

    def __convert_from_atoms__(self, output_file: typing.IO) -> None:
        """
        converts Atoms object to Molecular Data configuration for electrolens and stores in _output_data

        :param output_file: an open file handle to write the configuration for converted data to
        :return: None
        """
        atoms = self._input_data
        super()._init_atoms(atoms.cell, output_file)

        if output_file:
            writer = csv.writer(output_file, delimiter=',')
            writer.writerow(['x', 'y', 'z', 'atom'])
            for atom in atoms:
                writer.writerow([atom.position[0], atom.position[1], atom.position[2], atom.symbol])
        else:
            self._output_data['view']['moleculeData']['data'] = []
            for atom in atoms:
                atom_data = {
                    'x': atom.position[0],
                    'y': atom.position[1],
                    'z': atom.position[2],
                    'atom': atom.symbol
                }
                self._output_data['view']['moleculeData']['data'].append(atom_data)


class ASETrajectoryDataConverter(Converter):
    """
    Converter that converts input data to configuration related to Framed Data
    """

    def convert(self, output_file: typing.IO = None) -> dict:
        if isinstance(self._input_data, TrajectoryReader):
            self.__convert_from_trajectory__(output_file)
        else:
            raise TypeError('input data is not trajectory data')

        return self._output_data

    def __convert_from_trajectory__(self, output_file: typing.IO) -> None:
        """
        converts Trajectory object to Framed Data configuration for electrolens and stores in _output_data
        :param output_file: an open file handle to write the configuration for converted data to
        :return: None
        """
        super()._init_atoms(self._input_data[0].cell, output_file)

        self._output_data['plot_setup']['frameProperty'] = 'frame'
        self._output_data['plot_setup']['moleculePropertyList'].append('frame')

        if output_file:
            writer = csv.writer(output_file, delimiter=',')
            writer.writerow(['x', 'y', 'z', 'atom', 'frame'])
            for i in range(len(self._input_data)):
                atoms = self._input_data[i]
                for atom in atoms:
                    writer.writerow([atom.position[0], atom.position[1], atom.position[2], atom.symbol, i])
        else:
            self._output_data['view']['moleculeData']['data'] = []
            for i in range(len(self._input_data)):
                atoms = self._input_data[i]
                for atom in atoms:
                    atom_data = {
                        'x': atom.position[0],
                        'y': atom.position[1],
                        'z': atom.position[2],
                        'atom': atom.symbol,
                        'frame': i
                    }
                    self._output_data['view']['moleculeData']['data'].append(atom_data)


class ArrayDataConverter(Converter):
    """
    Converter that converts a numpy array of data to JSON configuration
    Supports framed and non-framed data
    """

    def __init__(self, input_data, np_column_names, np_atoms, np_framed, np_frame_column, atoms_cell):
        super().__init__(input_data)
        self.np_column_names = np_column_names
        self.np_atoms = np_atoms
        self.np_framed = np_framed
        self.np_frame_column = np_frame_column
        self.cell = atoms_cell

    def convert(self, output_file: typing.IO = None) -> dict:
        if isinstance(self._input_data, np.ndarray):
            self.__convert_from_np_array__(output_file)
        else:
            raise TypeError('input data is not numpy array')

        return self._output_data

    def __convert_from_np_array__(self, output_file: typing.IO):
        """
        converts 2D numpy array to configuration for electrolens and stores in _output_data
        :param output_file: an open file handle to write the configuration for converted data to
        :return: None
        """
        # check if additional inputs are present
        if self.np_column_names is None:
            raise TypeError('missing column names for numpy array input data')
        if self.np_atoms is None:
            raise TypeError('missing atom names for numpy array input data')
        if self.cell is None:
            raise TypeError('missing cell configuration for numpy array input data')

        # check to make sure that the column name list contains 'x', 'y', and 'z' - electrolens expects those exactly
        if "x" not in self.np_column_names:
            raise ValueError("column 'x' not present in provided list of column names")
        elif "y" not in self.np_column_names:
            raise ValueError("column 'y' not present in provided list of column names")
        elif "z" not in self.np_column_names:
            raise ValueError("column 'z' not present in provided list of column names")

        # check if provided frame column name is actually present in the list of column names
        if self.np_framed and self.np_frame_column not in self.np_column_names:
            raise ValueError(f'defined frame column {self.np_frame_column} not in provided list of column names')

        super()._init_atoms(self.cell, output_file)

        # add additional properties (i.e. not the coordinates) to the list of molecule properties in the JSON config
        # this will also add the frame property if present
        additional_props = self.np_column_names.copy()
        additional_props.remove('x')
        additional_props.remove('y')
        additional_props.remove('z')
        for prop in additional_props:
            self._output_data['plot_setup']['moleculePropertyList'].append(prop)

        # add relevant frame metadata to JSON configuration
        if self.np_framed:
            # identify the property representing the frame
            # the name of the frame property has already been added to moleculePropertyList
            self._output_data['plot_setup']['frameProperty'] = self.np_frame_column

        if output_file:
            writer = csv.writer(output_file, delimiter=',')
            # if the data is framed, a column for the frame should be included in np_column_names
            col_names = self.np_column_names.copy()
            col_names.append('atom')
            writer.writerow(col_names)

            for atom in range(len(self._input_data)):
                # add all of the properties for current atom (including frame if it exists)
                atom_props = self._input_data[atom]
                row = []
                for column in self.np_column_names:
                    col_idx = self.np_column_names.index(column)
                    row.append(atom_props[col_idx])
                # atom is last in the list
                row.append(self.np_atoms[atom])
                writer.writerow(row)
        else:
            self._output_data['view']['moleculeData']['data'] = []
            # each row in the 2D array is a single atom and its properties
            for atom in range(len(self._input_data)):
                atom_props = self._input_data[atom]
                # add value from every column in the row (including the frame property if it exists)
                atom_data = {}
                for column in self.np_column_names:
                    col_idx = self.np_column_names.index(column)
                    atom_data[column] = atom_props[col_idx]
                # add the name of the atom
                atom_data["atom"] = self.np_atoms[atom]
                self._output_data['view']['moleculeData']['data'].append(atom_data)
