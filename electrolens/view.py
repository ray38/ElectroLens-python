"""electrolens view definitions"""

from electrolens.converter import Converter, DataFormat
from ase import cell


class View(object):
    """
    base class for electrolens views
    """

    def __init__(self, view_type: str):
        """
        initializes new View object

        :param view_type: string representing type of the view
        """
        self.view_type = view_type

    def get_configuration(self) -> dict:
        """
        returns electrolens configuration for the view
        :return: dictionary containing configuration for the view and associated plot setup data
        """
        raise NotImplementedError()


class ThreeDView(View):
    """
    electrolens 3DView
    """

    def __init__(self,
                 input_data,
                 data_format: DataFormat,
                 molecule_name: str,
                 np_column_names: list = None,
                 np_atoms: list = None,
                 np_framed: bool = False,
                 np_frame_column: str = "frame",
                 np_cell: cell.Cell = None,
                 grid_spacing: dict = None,
                 output_data_file: str = None):
        """
        initializes electrolens 3DView

        :param input_data: input data for the view. It can have any of the supported types
        :param data_format: DataFormat enumeration value representing the electrolens configuration format for the view
        for example: framed, molecular or spatially resolved
        :param molecule_name: molecule name string
        :param grid_spacing: grid spacing dictionary in format {'x': value, 'y': value, 'z': value}
        :param output_data_file: path to the file that will store the data. The data will be part of configuration
        itself if this parameter is None or not provided
        :param np_cell: ASE Cell object. The Cell object represents three lattice vectors forming the dimensions
                              of the system. Required only when converting from a numpy array of molecular data
        :param np_frame_column: the name of the column representing the frame. Required only when converting from numpy
        :param np_framed: boolean stating if numpy array data is framed. Default is false
        :param np_atoms: list of atom names for each row in 2D numpy array. when data is 2D array, each row contains
                         properties for a single atom - this list provides the name of each atom for every row
        :param np_column_names: list of column names corresponding to each column in the 2D numpy array. Need the column
                                names so they can be added to JSON configuration
        """
        super().__init__("3DView")
        self.input_data = input_data
        self.data_format = data_format
        self.molecule_name = molecule_name

        # user input needed to support creating views with numpy arrays
        self.np_column_names = np_column_names
        self.np_atoms = np_atoms
        self.np_framed = np_framed
        self.np_frame_column = np_frame_column
        self.np_cell = np_cell

        self.grid_spacing = grid_spacing
        self.output_data_file = output_data_file

        # create converter for the view
        self.__converter__ = Converter.create_converter(self.data_format, self.input_data, self.np_column_names,
                                                        self.np_atoms, self.np_framed, self.np_frame_column, self.np_cell)

    def get_configuration(self) -> dict:
        configuration = {
            'view': {
                'viewType': self.view_type,
                'moleculeName': self.molecule_name
            }
        }

        # add grid spacing if provided by user
        if self.grid_spacing:
            configuration['view']['gridSpacing'] = self.grid_spacing

        # write configuration
        if self.output_data_file:
            configuration['view']['dataFilename'] = self.output_data_file
            with open(self.output_data_file, mode='w', newline='') as file:
                converted_data = self.__converter__.convert(file)
        else:
            converted_data = self.__converter__.convert()

        for key in converted_data['view'].keys():
            configuration['view'][key] = converted_data['view'][key]

        configuration['plot_setup'] = converted_data['plot_setup']

        return configuration


class TwoDHeatmap(View):
    """
    electrolens 2DHeatmap view
    """
    def __init__(self, plot_x: str, plot_y: str, plot_x_transform: str, plot_y_transform: str):
        """
        initializes electrolens 2D Heatmap view

        :param plot_x: plot X
        :param plot_y: plot Y
        :param plot_x_transform: plot X transform
        :param plot_y_transform: plot Y transform
        """
        super().__init__('2DHeatmap')
        self.plot_x = plot_x
        self.plot_y = plot_y
        self.plot_x_transform = plot_x_transform
        self.plot_y_transform = plot_y_transform

    def get_configuration(self) -> dict:
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
