"""electrolens plot"""

import json
from electrolens.embedded_browser import load_browser
from electrolens.view import View


class Plot(object):
    def __init__(self):
        self.__views__ = []
        self.input_configuration_file = None

    def add_view(self, plot_view: View) -> None:
        self.__views__.append(plot_view)

    def show(self) -> None:
        load_browser(self.__create_configuration__())

    def save_configuration(self, output_json_file) -> None:
        configuration = self.__create_configuration__()
        with open(output_json_file, 'w') as fp:
            json.dump(configuration, fp, indent=4)

    def __create_configuration__(self) -> dict:
        if self.input_configuration_file and len(self.__views__) > 0:
            raise TypeError('Please provide either views or configuration file but not both')

        configuration = {}
        if self.input_configuration_file:
            configuration = json.load(self.input_configuration_file)
        elif len(self.__views__) == 0:
            raise ValueError('No view or configuration file has been provided')
        else:
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



