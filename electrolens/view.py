"""view definitions"""

from enum import Enum

from electrolens import converter


class DataFormat(Enum):
    FRAMED_DATA = 1
    MOLECULAR_DATA = 2
    SPATIALLY_RESOLVED_DATA = 3


class View(object):
    def __init__(self, view_type: str):
        self.view_type = view_type

    def get_configuration(self) -> dict:
        raise NotImplementedError()


class ThreeDView(View):
    def __init__(self,
                 input_data,
                 data_format: DataFormat,
                 molecule_name: str,
                 grid_spacing: dict = None,
                 output_data_file: str = None):
        super().__init__("3DView")
        self.input_data = input_data
        self.data_format = data_format
        self.molecule_name = molecule_name
        self.grid_spacing = grid_spacing
        self.output_data_file = output_data_file
        self.__converter__ = self.__get_converter__()

    def __get_converter__(self) -> converter.Converter:
        if self.data_format == DataFormat.FRAMED_DATA:
            return converter.FramedDataConverter(self.input_data)

        if self.data_format == DataFormat.MOLECULAR_DATA:
            return converter.MolecularDataConverter(self.input_data)

        if self.data_format == DataFormat.SPATIALLY_RESOLVED_DATA:
            return converter.SpatiallyResolvedDataConverter(self.input_data)

        raise TypeError("Unknown data format")

    def get_configuration(self) -> dict:
        configuration = {
            'view': {
                'viewType': self.view_type,
                'moleculeName': self.molecule_name
            }
        }
        if self.grid_spacing:
            configuration['view']['gridSpacing'] = self.grid_spacing

        if self.output_data_file:
            configuration['view']['dataFilename'] = self.output_data_file
            with open(self.output_data_file, mode='w') as file:
                converted_data = self.__converter__.convert(file)
        else:
            converted_data = self.__converter__.convert()

        for key in converted_data['view'].keys():
            configuration['view'][key] = converted_data['view'][key]

        configuration['plot_setup'] = converted_data['plot_setup']

        return configuration


class TwoDView(View):
    def __init__(self, plot_x: str, plot_y: str, plot_x_transform: str, plot_y_transform: str):
        super().__init__('2DHeatmap')
        self.plot_x = plot_x
        self.plot_y = plot_y
        self.plot_x_transform = plot_x_transform
        self.plot_y_transform = plot_y_transform

    def get_configuration(self) -> dict:
        configuration = {
            'viewType': self.view_type,
            'plotX': self.plot_x,
            'plotY': self.plot_y,
            'plotXTransform': self.plot_x_transform,
            'plotYTransform': self.plot_y_transform,
        }

        return configuration
