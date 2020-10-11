"""
converter module contains classes for Spatially Resolved, Molecular and Framed Data conversions from input data
"""

from ase import Atoms
from ase.io.trajectory import TrajectoryReader
from sklearn.preprocessing import normalize
import typing
import csv


class Converter(object):
    def __init__(self, input_data):
        self._input_data = input_data
        self._output_data = {'view': {}, 'plot_setup': {}}

    def convert(self, output_file: typing.IO = None) -> dict:
        raise NotImplementedError()

    def _init_atoms(self, atoms: Atoms) -> None:
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


class SpatiallyResolvedDataConverter(Converter):
    def convert(self, output_file: typing.IO = None) -> dict:
        pass


class MolecularDataConverter(Converter):
    def convert(self, output_file: typing.IO = None) -> dict:
        if isinstance(self._input_data, Atoms):
            self.__convert_from_atoms__(output_file)
        else:
            raise TypeError('input data is not molecular data')

        return self._output_data

    def __convert_from_atoms__(self, output_file: typing.IO) -> None:
        atoms = self._input_data
        super()._init_atoms(atoms)

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
    def convert(self, output_file: typing.IO = None) -> dict:
        if isinstance(self._input_data, TrajectoryReader):
            self.__convert_from_trajectory__(output_file)
        else:
            raise TypeError('input data is not framed data')

        return self._output_data

    def __convert_from_trajectory__(self, output_file: typing.IO) -> None:
        super()._init_atoms(self._input_data[0])

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
