"""
Communicate between Python and Javascript asynchronously using
inter-process messaging with the use of Javascript Bindings.
"""

from cefpython3 import cefpython as cef
import os
import json
import csv
from ase import Atoms
from ase.io.trajectory import TrajectoryReader
from sklearn.preprocessing import normalize


# def view(data):
#     #print type(data)
#     if isinstance(data, Atoms):
#         config = atomsToConfig(data)
#     elif isinstance(data, TrajectoryReader):
#         config = trajToConfig(data)
#     else:
#         config = data
#     cef.Initialize()
#     # cwd = os.getcwd()
#     # try:
#     #     os.chdir("ElectroLens-python")
#     # except:
#     #     pass
    
#     dir_path = os.path.dirname(__file__)
#     # index_filepath = 'file://' + os.path.join(dir_path, 'index_cefpython.html')
#     index_filepath = os.path.join(dir_path, 'static/index_cefpython.html')
#     print(index_filepath)

#     browser_setting = { "file_access_from_file_urls_allowed":True,\
#                     "universal_access_from_file_urls_allowed": True,\
#                     "web_security_disabled":True}
                    
#     browser = cef.CreateBrowserSync(url=index_filepath,
#                                     window_title="ElectroLens", settings = browser_setting)
#     # os.chdir(cwd)
#     browser.SetClientHandler(LoadHandler(config))
#     bindings = cef.JavascriptBindings()
#     browser.SetJavascriptBindings(bindings)
#     cef.MessageLoop()
#     del browser
#     cef.Shutdown()
#     return 

def view(data):
    #print type(data)
    #config = trajToConfig2(data)
    print("start")
    if isinstance(data, Atoms):
        config = atomsToConfig(data)
    elif isinstance(data, TrajectoryReader):
        config = trajToConfig(data)
    else:
        config = data
    with open('temp_data.json', 'w') as fp:
        json.dump(config , fp, indent=4)
    settings = {
        "debug": True,
        "log_severity": cef.LOGSEVERITY_INFO,
        "log_file": "debug.log",
    }
    cef.Initialize(settings=settings)
    cwd = os.getcwd()
    # try:
    #     os.chdir("ElectroLens-python")
    # except:
    #     pass
    browser_setting = { "file_access_from_file_urls_allowed":True,\
                    "universal_access_from_file_urls_allowed": True,\
                    "web_security_disabled":True}
    dir_path = os.path.dirname(__file__)
    index_filepath = os.path.join(dir_path, 'static/index_cefpython.html')
    browser = cef.CreateBrowserSync(url=index_filepath,
                                    window_title="ElectroLens", settings = browser_setting)
    os.chdir(cwd)
    browser.SetClientHandler(LoadHandler(config))
    bindings = cef.JavascriptBindings()
    browser.SetJavascriptBindings(bindings)
    cef.MessageLoop()
    del browser
    cef.Shutdown()
    return 

def atomsToConfig(a):
    #print "converting atoms to config"
    systemDimension = {}
    lattice_constants = a.cell.lengths()
    systemDimension["x"] = lattice_constants[0]
    systemDimension["y"] = lattice_constants[1]
    systemDimension["z"] = lattice_constants[2]

    config = {}

    config["views"] = []
    temp = {}
    temp["viewType"] = "3DView"
    temp["moleculeName"] = "test"
    temp["moleculeData"] = {}

    lattice_vector = normalize(a.cell,axis=1)
    print(lattice_vector)
    # temp["systemLatticeVectors"] = {
    #     "u11": lattice_vector[0][0],
    #     "u12": lattice_vector[0][1],
    #     "u13": lattice_vector[0][2],
    #     "u21": lattice_vector[1][0],
    #     "u22": lattice_vector[1][1],
    #     "u23": lattice_vector[1][2],
    #     "u31": lattice_vector[2][0],
    #     "u32": lattice_vector[2][1],
    #     "u33": lattice_vector[2][2]
    #   },

    temp["systemLatticeVectors"] = {}
    temp["systemLatticeVectors"]["u11"] = lattice_vector[0][0]
    temp["systemLatticeVectors"]["u12"] = lattice_vector[0][1]
    temp["systemLatticeVectors"]["u13"] = lattice_vector[0][2]
    temp["systemLatticeVectors"]["u21"] = lattice_vector[1][0]
    temp["systemLatticeVectors"]["u22"] = lattice_vector[1][1]
    temp["systemLatticeVectors"]["u23"] = lattice_vector[1][2]
    temp["systemLatticeVectors"]["u31"] = lattice_vector[2][0]
    temp["systemLatticeVectors"]["u32"] = lattice_vector[2][1]
    temp["systemLatticeVectors"]["u33"] = lattice_vector[2][2]

    print(temp["systemLatticeVectors"])

    temp["moleculeData"]["data"] = []
    for atom in a:
        temp_atom = {}
        temp_atom["x"] = atom.position[0]
        temp_atom["y"] = atom.position[1]
        temp_atom["z"] = atom.position[2]
        temp_atom["atom"] = atom.symbol
        temp["moleculeData"]["data"].append(temp_atom)
    temp["systemDimension"] = systemDimension
    config["views"].append(temp)
    config["plotSetup"] = {}
    config["plotSetup"]["moleculePropertyList"] = ["atom"]
    return config


def trajToConfig(a):
    #print "converting traj to config"
    systemDimension = {}
    systemDimension["x"] = [0,a[0].cell[0][0]]
    systemDimension["y"] = [0,a[0].cell[1][1]]
    systemDimension["z"] = [0,a[0].cell[2][2]]

    length = len(a) * len(a[0])

    if length < 10000000:
        config = {}

        config["views"] = []
        temp = {}
        temp["viewType"] = "3DView"
        temp["moleculeName"] = "test"
        temp["moleculeData"] = {}
        temp["moleculeData"]["data"] = []
        for i in range(len(a)):
            atoms = a[i]
            for atom in atoms:
                temp_atom = {}
                temp_atom["x"] = atom.position[0]
                temp_atom["y"] = atom.position[1]
                temp_atom["z"] = atom.position[2]
                temp_atom["atom"] = atom.symbol
                temp_atom["frame"] = i
                temp["moleculeData"]["data"].append(temp_atom)
        temp["moleculeData"]["gridSpacing"] = {"x":0.1,"y":0.1,"z":0.1}
        temp["systemDimension"] = systemDimension
        config["views"].append(temp)
        config["plotSetup"] = {}
        config["plotSetup"]["frameProperty"] = "frame"
        config["plotSetup"]["moleculePropertyList"] = ["atom","frame"]

    else:
        config = {}

        config["views"] = []
        temp = {}
        temp["viewType"] = "3DView"
        temp["moleculeName"] = "test"
        temp["moleculeData"] = {}
        temp["moleculeData"]["dataFilename"] = os.getcwd() + "/__ElectroLens_View_Intermediate__.csv"

        with open('__ElectroLens_View_Intermediate__.csv', mode='w') as file:
            writer = csv.writer(file, delimiter=',')

            writer.writerow(['x', 'y','z','atom','frame'])

            for i in range(len(a)):
                atoms = a[i]
                for atom in atoms:
                    temp_row = []
                    temp_row.append(atom.position[0])
                    temp_row.append(atom.position[1])
                    temp_row.append(atom.position[2])
                    temp_row.append(atom.symbol)
                    temp_row.append(i)
                    writer.writerow(temp_row)

        temp["moleculeData"]["gridSpacing"] = {"x":0.1,"y":0.1,"z":0.1}
        temp["systemDimension"] = systemDimension
        config["views"].append(temp)
        config["plotSetup"] = {}
        config["plotSetup"]["frameProperty"] = "frame"
        config["plotSetup"]["moleculePropertyList"] = ["atom","frame"]



    return config

def trajToConfig2(data):
    a, fingerprint = data
    #print "converting traj to config"
    systemDimension = {}
    systemDimension["x"] = [0,a.cell[0][0]]
    systemDimension["y"] = [0,a.cell[1][1]]
    systemDimension["z"] = [0,a.cell[2][2]]


    config = {}

    config["views"] = []
    temp = {}
    temp["viewType"] = "3DView"
    temp["moleculeName"] = "test"
    temp["moleculeData"] = {}
    temp["moleculeData"]["data"] = []
    atoms = a
    for i, atom in enumerate(atoms):
        temp_atom = {}
        temp_atom["x"] = atom.position[0]
        temp_atom["y"] = atom.position[1]
        temp_atom["z"] = atom.position[2]
        temp_atom["atom"] = atom.symbol
        temp_atom["p1"] = fingerprint[i][1][0]
        temp_atom["p2"] = fingerprint[i][1][1]
        temp_atom["p3"] = fingerprint[i][1][2]
        temp["moleculeData"]["data"].append(temp_atom)
    temp["moleculeData"]["gridSpacing"] = {"x":0.1,"y":0.1,"z":0.1}
    temp["systemDimension"] = systemDimension
    config["views"].append(temp)
    config["plotSetup"] = {}
    config["plotSetup"]["moleculePropertyList"] = ["atom","p1","p2","p3"]



    return config

class LoadHandler(object):

    def __init__(self, config):
        self.config = config
    def OnLoadEnd(self, browser, **_):
        browser.ExecuteFunction("defineData", self.config)
