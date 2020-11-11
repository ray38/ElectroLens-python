"""
electrolens example to plot spatially resolved data from a file
"""
import electrolens as el

# create electrolens plot
spatially_resolved_properties = el.SpatiallyResolvedDataProperties(
    columns=['x', 'y', 'z', 'rho', "gamma", "epxc", "deriv1", "deriv2"],
    density_property='rho', density_lower_limit=0.00001, density_upper_limit=1000000)

plot = el.Plot(spatially_resolved_properties=spatially_resolved_properties)

# create 3D view and add data to it
view = el.ThreeDView(system_name='C6H6')
spatially_resolved_data = el.SpatiallyResolvedData(data="C6H6_data.csv", grid_points=[30, 30, 30],
                                                   grid_spacing=[0.4, 0.3, 0.3])
view.add_data(spatially_resolved_data)

# add view to the plot
plot.add_view(view)

# show plot
plot.show()

