"""electrolens view definitions"""

from electrolens.converter import Converter, DataFormat


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
        """
        super().__init__("3DView")
        self.input_data = input_data
        self.data_format = data_format
        self.molecule_name = molecule_name
        self.grid_spacing = grid_spacing
        self.output_data_file = output_data_file

        # create converter for the view
        self.__converter__ = Converter.create_converter(self.data_format, self.input_data)

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
