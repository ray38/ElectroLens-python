"""
converter module contains classes for source formats to target formats
"""
from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum
from ase import Atoms, cell
from ase.io.trajectory import TrajectoryReader
from sklearn.preprocessing import normalize
from typing.io import IO
from typing import Union
import csv
import os
import numpy as np

from electrolens import SpatiallyResolvedDataProperties, MolecularDataProperties, FramedDataProperties
from . import message


class DataFormat(Enum):
    """
    input and output data format
    """
    MOLECULAR_DATA = 1
    SPATIALLY_RESOLVED_DATA = 2
    TRAJECTORY_DATA = 3
    ATOMS_DATA = 4
    ARRAY_DATA = 5
    FILE_DATA = 6


def _init_atoms_(output: dict, atoms_cell: cell.Cell) -> None:
    """
    performs common tasks for atoms input data format
    Args:
        output: output dictionary to be updated
        atoms_cell: ASE atoms cell object

    Returns: None
    """
    if 'systemDimension' in output:
        message.warning(f"{output['moleculeName']}: System Dimensions are overridden by user provided values")
    else:
        lattice_constants = atoms_cell.lengths()
        output['systemDimension'] = {
            'x': lattice_constants[0],
            'y': lattice_constants[1],
            'z': lattice_constants[2]
        }

    if 'systemLatticeVectors' in output:
        message.warning(f"{output['moleculeName']}: System Lattice Vectors are overridden by user provided values")
    else:
        lattice_vector = normalize(atoms_cell, axis=1)
        output['systemLatticeVectors'] = {
            'u11': lattice_vector[0][0], 'u12': lattice_vector[0][1], 'u13': lattice_vector[0][2],
            'u21': lattice_vector[1][0], 'u22': lattice_vector[1][1], 'u23': lattice_vector[1][2],
            'u31': lattice_vector[2][0], 'u32': lattice_vector[2][1], 'u33': lattice_vector[2][2]
        }


def _set_data_filename_(output: dict, data_output_file: IO):
    """
    adds dataFilename element if file is to be used for data
    Args:
        output: output dictionary to be updated
        data_output_file: file path containing data

    Returns: None
    """
    abs_path = os.path.abspath(data_output_file.name)
    output['dataFilename'] = abs_path.replace('\\', '/')


class Converter(ABC):
    """
    base converter class
    """
    def __init__(self, data):
        """
        initializes converter class
        Args:
            data: input data
        """
        self.data = data

    @staticmethod
    def __get_data_format__(data: Union[str, Atoms, TrajectoryReader, np.ndarray]) -> DataFormat:
        """
        provides format of input data
        Args:
            data: input data whose format is to be identified

        Returns: format of the data
        """
        if isinstance(data, str):
            return DataFormat.FILE_DATA

        if isinstance(data, Atoms):
            return DataFormat.ATOMS_DATA

        if isinstance(data, TrajectoryReader):
            return DataFormat.TRAJECTORY_DATA

        if isinstance(data, np.ndarray):
            return DataFormat.ARRAY_DATA

        raise ValueError("Unsupported data format")

    @staticmethod
    def create_converter(data: Union[str, Atoms, TrajectoryReader, np.ndarray], target_format: DataFormat):
        """
        creates converter for provided data and target format combination
        Args:
            data: input data to be converted
            target_format: target data format

        Returns: converter object
        """
        source_format = Converter.__get_data_format__(data)
        if source_format == DataFormat.TRAJECTORY_DATA and target_format == DataFormat.MOLECULAR_DATA:
            return ASETrajectoryToMolecularDataConverter(data)

        if source_format == DataFormat.ATOMS_DATA and target_format == DataFormat.MOLECULAR_DATA:
            return ASEAtomsToMolecularDataConverter(data)

        if source_format == DataFormat.ARRAY_DATA:
            if target_format == DataFormat.MOLECULAR_DATA:
                return ArrayToMolecularDataConverter(data)

            if target_format == DataFormat.SPATIALLY_RESOLVED_DATA:
                return ArrayToSpatiallyResolvedDataConverter(data)

        if source_format == DataFormat.FILE_DATA:
            return FileToAnyDataConverter(data, target_format)

        raise TypeError("Unsupported data format conversion")

    @abstractmethod
    def convert(self,
                output: dict,
                properties: Union[SpatiallyResolvedDataProperties, MolecularDataProperties],
                framed_properties: FramedDataProperties = None,
                extra_properties: namedtuple = None,
                data_output_file: IO = None) -> None:
        """
        converts data and updates output dictionary
        Args:
            output: the output dictionary to be updated
            properties: spatially resolved or molecular properties provided at plot level
            framed_properties: framed properties provided at plot level
            extra_properties: any extra properties required by the converter
            data_output_file: filepath for storing data instead of being stored in configuration

        Returns: None
        """
        raise NotImplementedError()


class ASEAtomsToMolecularDataConverter(Converter):
    """
    ASE Atoms data to molecular data converter
    """
    def __init__(self, data: Atoms):
        """
        initializes the converter
        Args:
            data: input data
        """
        super().__init__(data)

    def convert(self,
                output: dict,
                properties: Union[SpatiallyResolvedDataProperties, MolecularDataProperties],
                framed_properties: FramedDataProperties = None,
                extra_properties: namedtuple = None,
                data_output_file: IO = None) -> None:
        """
        converts data and updates output dictionary
        Args:
            output: the output dictionary to be updated
            properties: spatially resolved or molecular properties provided at plot level
            framed_properties: framed properties provided at plot level
            extra_properties: any extra properties required by the converter
            data_output_file: filepath for storing data instead of being stored in configuration

        Returns: None
        """
        if framed_properties is not None:
            raise ValueError("Atoms data does not support frames")

        if isinstance(self.data, Atoms):
            self.__convert__(output, properties, data_output_file)
        else:
            raise TypeError('input data is not ASE molecular data')

    def __convert__(self, output: dict, properties: MolecularDataProperties, data_output_file: IO) -> None:
        atoms = self.data
        _init_atoms_(output, atoms.cell)

        output['moleculeData'] = {}
        output = output['moleculeData']

        columns = properties.columns.copy()
        if 'atom' not in columns:
            columns.append('atom')
        x_index = columns.index('x')
        y_index = columns.index('y')
        z_index = columns.index('z')
        atom_index = columns.index('atom')

        if data_output_file is not None:
            _set_data_filename_(output, data_output_file)
            writer = csv.writer(data_output_file, delimiter=',')
            writer.writerow(columns)
            for atom in atoms:
                row = [''] * len(columns)
                row[x_index] = atom.position[0]
                row[y_index] = atom.position[1]
                row[z_index] = atom.position[2]
                row[atom_index] = atom.symbol
                writer.writerow(row)
        else:
            output['data'] = []
            other_columns = set(columns) - {'x', 'y', 'z', 'atom'}
            for atom in atoms:
                atom_data = {
                    'x': atom.position[0],
                    'y': atom.position[1],
                    'z': atom.position[2],
                    'atom': atom.symbol
                }
                for column in other_columns:
                    atom_data[column] = ''
                output['data'].append(atom_data)


class ASETrajectoryToMolecularDataConverter(Converter):
    """
    ASE Trajectory to molecular data converter
    """
    def __init__(self, data: TrajectoryReader):
        """
        initializes the converter
        Args:
            data: input data
        """
        super().__init__(data)

    def convert(self,
                output: dict,
                properties: Union[SpatiallyResolvedDataProperties, MolecularDataProperties],
                framed_properties: FramedDataProperties = None,
                extra_properties: namedtuple = None,
                data_output_file: IO = None) -> None:
        """
        converts data and updates output dictionary
        Args:
            output: the output dictionary to be updated
            properties: spatially resolved or molecular properties provided at plot level
            framed_properties: framed properties provided at plot level
            extra_properties: any extra properties required by the converter
            data_output_file: filepath for storing data instead of being stored in configuration

        Returns: None
        """
        if isinstance(self.data, TrajectoryReader):
            self.__convert__(output, properties, framed_properties, data_output_file)
        else:
            raise TypeError('input data is not ASE Trajectory Reader')

    def __convert__(self, output: dict, properties: MolecularDataProperties,
                    framed_properties: FramedDataProperties, data_output_file: IO) -> None:
        _init_atoms_(output, self.data[0].cell)

        output['moleculeData'] = {}
        output = output['moleculeData']

        columns = properties.columns.copy()
        if 'atom' not in columns:
            columns.append('atom')

        x_index = columns.index('x')
        y_index = columns.index('y')
        z_index = columns.index('z')
        atom_index = properties.columns.index('atom')
        frame_index: int = 0
        if framed_properties is not None:
            frame_index = columns.index(framed_properties.frame_column)

        if data_output_file is not None:
            _set_data_filename_(output, data_output_file)
            writer = csv.writer(data_output_file, delimiter=',')
            writer.writerow(columns)
            for i in range(len(self.data)):
                atoms = self.data[i]
                for atom in atoms:
                    row = [''] * len(columns)
                    row[x_index] = atom.position[0]
                    row[y_index] = atom.position[1]
                    row[z_index] = atom.position[2]
                    row[atom_index] = atom.symbol
                    if framed_properties is not None:
                        row[frame_index] = i
                    writer.writerow(row)
        else:
            output['data'] = []
            for i in range(len(self.data)):
                atoms = self.data[i]
                for atom in atoms:
                    atom_data = {
                        'x': atom.position[0],
                        'y': atom.position[1],
                        'z': atom.position[2],
                        'atom': atom.symbol
                    }
                    if framed_properties is not None:
                        atom_data[framed_properties.frame_column] = i
                    output['data'].append(atom_data)


class ArrayToMolecularDataConverter(Converter):
    """
    Converter that converts a numpy array of data to JSON configuration
    Supports framed and non-framed data
    """
    def __init__(self, data: np.ndarray):
        """
        initializes the converter
        Args:
            data: input numpy array
        """
        super().__init__(data)

    def convert(self,
                output: dict,
                properties: Union[SpatiallyResolvedDataProperties, MolecularDataProperties],
                framed_properties: FramedDataProperties = None,
                extra_properties: namedtuple = None,
                data_output_file: IO = None) -> None:
        """
        converts data and updates output dictionary
        Args:
            output: the output dictionary to be updated
            properties: spatially resolved or molecular properties provided at plot level
            framed_properties: framed properties provided at plot level
            extra_properties: any extra properties required by the converter
            data_output_file: filepath for storing data instead of being stored in configuration

        Returns: None
        """
        if isinstance(self.data, np.ndarray):
            self.__convert__(output, properties, extra_properties, data_output_file)
        else:
            raise TypeError('input data is not numpy array')

    def __convert__(self, output: dict, properties: MolecularDataProperties,
                    extra_properties: namedtuple, data_output_file: IO):
        # check if additional inputs are present
        if extra_properties.np_atoms is None:
            raise TypeError('missing atom names for numpy array input data')
        if extra_properties.cell is None:
            raise TypeError('missing cell configuration for numpy array input data')

        _init_atoms_(output, extra_properties.cell)

        output['moleculeData'] = {}
        output = output['moleculeData']

        if data_output_file is not None:
            _set_data_filename_(output, data_output_file)
            writer = csv.writer(data_output_file, delimiter=',')
            writer.writerow(properties.columns)

            for atom in range(len(self.data)):
                # add all of the properties for current atom (including frame if it exists)
                atom_props = self.data[atom]
                row = []
                for column in properties.columns:
                    col_idx = properties.columns.index(column)
                    row.append(atom_props[col_idx])
                # atom is last in the list
                row.append(extra_properties.np_atoms[atom])
                writer.writerow(row)
        else:
            output['data'] = []
            # each row in the 2D array is a single atom and its properties
            for atom in range(len(self.data)):
                atom_props = self.data[atom]
                # add value from every column in the row (including the frame property if it exists)
                atom_data = {}
                for column in properties.columns:
                    col_idx = properties.columns.index(column)
                    atom_data[column] = atom_props[col_idx]
                # add the name of the atom
                atom_data["atom"] = extra_properties.np_atoms[atom]
                output['data'].append(atom_data)


class ArrayToSpatiallyResolvedDataConverter(Converter):
    """
    converts numpy array to spatially resolved data json
    """
    def __init__(self, data: np.ndarray):
        """
        initializes the converter
        Args:
            data: input data as numpy array
        """
        super().__init__(data)

    def convert(self,
                output: dict,
                properties: Union[SpatiallyResolvedDataProperties, MolecularDataProperties],
                framed_properties: FramedDataProperties = None,
                extra_properties: namedtuple = None,
                data_output_file: IO = None) -> None:
        """
        converts data and updates output dictionary
        Args:
            output: the output dictionary to be updated
            properties: spatially resolved or molecular properties provided at plot level
            framed_properties: framed properties provided at plot level
            extra_properties: any extra properties required by the converter
            data_output_file: filepath for storing data instead of being stored in configuration

        Returns: None
        """
        if isinstance(self.data, np.ndarray):
            self.__convert__(output, properties, data_output_file)
        else:
            raise TypeError('input data is not numpy array')

    def __convert__(self, output: dict, properties: SpatiallyResolvedDataProperties, data_output_file: IO):
        pass


class FileToAnyDataConverter(Converter):
    """
    uses file which contains data for spatially resolved and molecular data conversion
    """
    def __init__(self, data: str, target_format: DataFormat):
        """
        initializes the converter
        Args:
            data: input file path
            target_format: target format to convert into
        """
        super().__init__(data)
        self.target_format = target_format

    def convert(self,
                output: dict,
                properties: Union[SpatiallyResolvedDataProperties, MolecularDataProperties],
                framed_properties: FramedDataProperties = None,
                extra_properties: namedtuple = None,
                data_output_file: IO = None) -> None:
        """
        converts data and updates output dictionary
        Args:
            output: the output dictionary to be updated
            properties: spatially resolved or molecular properties provided at plot level
            framed_properties: framed properties provided at plot level
            extra_properties: any extra properties required by the converter
            data_output_file: filepath for storing data instead of being stored in configuration

        Returns: None
        """
        if isinstance(self.data, str):
            self.__convert__(output)
        else:
            raise TypeError('input data is not file path')

    def __convert__(self, output: dict):
        node = ''
        if self.target_format == DataFormat.MOLECULAR_DATA:
            node = 'moleculeData'
        elif self.target_format == DataFormat.SPATIALLY_RESOLVED_DATA:
            node = 'spatiallyResolvedData'
        else:
            raise ValueError("Unsupported data format conversion")

        output[node] = {}
        with open(self.data) as file:
            _set_data_filename_(output[node], file)
