"""
electrolens example to show plot that takes full configuration from a file
"""

import electrolens as el

# create electrolens plot
plot = el.Plot(configuration_file='input_plot_configuration.json')

# addition of views is not supported when plot configuration file is provided

# show plot
plot.show()
