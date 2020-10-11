"""electrolens plot"""

import json
from electrolens.embedded_browser import load_browser
from electrolens.view import View


class Plot(object):
    """
    electrolens Plot
    """
    def __init__(self):
        """
        initializes electrolens Plot object
        """
        self.__views__ = []
        self.input_configuration_file = None

    def add_view(self, plot_view: View) -> None:
        """
        adds view to the Plot

        :param plot_view: View object to be added
        :return: None
        """
        self.__views__.append(plot_view)

    def show(self) -> None:
        """
        shows electrolens visualization

        :return: None
        """
        load_browser(self.__create_configuration__())

    def save_configuration(self, output_json_file) -> None:
        """
        saves the visualization as electrolens configuration file

        :param output_json_file: path of the json file where the configuration will be saved to
        :return: None
        """
        configuration = self.__create_configuration__()
        with open(output_json_file, 'w') as fp:
            json.dump(configuration, fp, indent=4)

    def __create_configuration__(self) -> dict:
        """
        creates configuration for the plot
        :return: plot configuration dictionary
        """
        if self.input_configuration_file and len(self.__views__) > 0:
            raise TypeError('Please provide either views or configuration file but not both')

        configuration = {}
        if self.input_configuration_file:
            configuration = json.load(self.input_configuration_file)
        elif len(self.__views__) == 0:
            raise ValueError('No view or configuration file has been provided')
        else:
            # create configuration
            configuration = {
                'views': [],
                'plotSetup': {}
            }

            for view in self.__views__:
                view_configuration = view.get_configuration()
                configuration['views'].append(view_configuration['view'])
                for key in view_configuration['plot_setup'].keys():
                    configuration['plotSetup'][key] = view_configuration['plot_setup'][key]

        return configuration



