"""converter module contains classes for Spatially Resolved, Molecular and Framed Data conversions from input data"""

from enum import Enum
from ase import Atoms
from ase.io.trajectory import TrajectoryReader
from sklearn.preprocessing import normalize
import typing
import csv
import os


class DataFormat(Enum):
    """
    enumeration for electrolens acceptable data format
    """
    FRAMED_DATA = 1
    MOLECULAR_DATA = 2
    SPATIALLY_RESOLVED_DATA = 3


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
    def create_converter(data_format: DataFormat, data):
        """
        creates new converter

        :param data_format: DataFormat enumeration value representing the type of converter to be created
        :param data: input data object. It can be of any supported type

        :return: newly created Converter object
        """
        if data_format == DataFormat.FRAMED_DATA:
            return FramedDataConverter(data)

        if data_format == DataFormat.MOLECULAR_DATA:
            return MolecularDataConverter(data)

        if data_format == DataFormat.SPATIALLY_RESOLVED_DATA:
            return SpatiallyResolvedDataConverter(data)

        raise TypeError("Unknown data format")

    def convert(self, output_file: typing.IO = None) -> dict:
        """
        converts input data to electrolens acceptable format

        :param output_file: an open file handle to write the configuration for converted data to
        :return: a dictionary containing electrolens configuration entries for converted data. The dictionary contains
        keys for view and plot setup as 'view' and 'plot_setup' respectively.
        """
        raise NotImplementedError()

    def _init_atoms(self, atoms: Atoms, data_file: typing.IO) -> None:
        """
        fills up _output_data with common configurations for Atoms object

        :param atoms: Atoms object containing input data
        :param data_file: output data file
        :return: None
        """
        lattice_constants = atoms.cell.lengths()
        self._output_data['plot_setup'] = {
            'moleculePropertyList': ['atom']
        }

        self._output_data['view']['systemDimension'] = {
            'x': lattice_constants[0],
            'y': lattice_constants[1],
            'z': lattice_constants[2]
        }

        lattice_vector = normalize(atoms.cell, axis=1)
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


class MolecularDataConverter(Converter):
    """
    Converter that converts input data to configuration related to Molecular Data
    """

    def convert(self, output_file: typing.IO = None) -> dict:
        if isinstance(self._input_data, Atoms):
            self.__convert_from_atoms__(output_file)
        else:
            raise TypeError('input data is not molecular data')

        return self._output_data

    def __convert_from_atoms__(self, output_file: typing.IO) -> None:
        """
        converts Atoms object to Molecular Data configuration for electrolens and stores in _output_data

        :param output_file: an open file handle to write the configuration for converted data to
        :return: None
        """
        atoms = self._input_data
        super()._init_atoms(atoms, output_file)

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


class FramedDataConverter(Converter):
    """
    Converter that converts input data to configuration related to Framed Data
    """

    def convert(self, output_file: typing.IO = None) -> dict:
        if isinstance(self._input_data, TrajectoryReader):
            self.__convert_from_trajectory__(output_file)
        else:
            raise TypeError('input data is not framed data')

        return self._output_data

    def __convert_from_trajectory__(self, output_file: typing.IO) -> None:
        """
        converts Trajectory object to Framed Data configuration for electrolens and stores in _output_data
        :param output_file: an open file handle to write the configuration for converted data to
        :return: None
        """
        super()._init_atoms(self._input_data[0], output_file)

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
