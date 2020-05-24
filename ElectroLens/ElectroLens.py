"""
Communicate between Python and Javascript asynchronously using
inter-process messaging with the use of Javascript Bindings.
"""

from cefpython3 import cefpython as cef
import base64
import platform
import sys
import threading
import os
import json
import csv
from ase import Atoms
from ase.io.trajectory import TrajectoryReader
from sklearn.preprocessing import normalize

HTML_code = """
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
		<link href="static/css/main.css" rel="stylesheet" />
		<style type="text/css">
			* {
				.border-radius(0) !important;
			  }
			html, body {
			  height: 100%;
			  display: flex;
			  flex-direction: column;
			}
			.text-divider{margin: 1.2em 0; line-height: 0; text-align: center;}
			.text-divider span{background-color: #ffffff; padding: 0.5em;}
			.text-divider:before{ content: " "; display: block; border-top: 1px solid #e3e3e3; border-bottom: 1px solid #f7f7f7;}
			.load-window{overflow: scroll;height: 15%; width: 80%;left: 10%;align-items: center;}
			.config-window{overflow: scroll;height: 75%; width: 80%;left: 10%;align-items: center;}
		  </style>
		  <script>if (typeof module === 'object') {window.module = module; module = undefined;}</script>
		  <script src="vendor/jquery/jquery-3.4.1.js"></script>
		  <script src="vendor/bootstrap/js/bootstrap.js"></script>
		  <link href="vendor/bootstrap/css/bootstrap.css" rel="stylesheet">
		  <link href="static/css/main.css" rel="stylesheet" />
		
		  <script src="node_modules/es6/ES6.js"></script>
			
		  <script src="static/js/kdtree.js"></script>
		  <script src="static/js/progressbar.js"></script>
		  <script src="static/js/three.js"></script>

		  <script src="static/js/three-spritetext.js"></script>
		  <script src="static/js/jeezy.js"></script>
		  <script src="static/js/data2grid.js"></script>
		  <script src="static/js/effects/AnaglyphEffect.js"></script>
		  <link rel="stylesheet" type="text/css" href="static/js/loading-bar.css"/>
		  <script src="static/js/loading-bar.js"></script>
		
		  
		
		  <script src="static/js/jQuery.js"></script>
		 
		
		  
		
		  <script src="static/js/Detector.js"></script>
		  <script src="static/js/libs/stats.min.js"></script>
		  <script src="./MultiviewControl/customizeLut.js"></script>
		  <script src="static/js/controls/OrbitControls.js"></script>
		  <script src="static/js/controls/TrackballControls.js"></script>
		  <script src="static/js/libs/dat.gui.js"></script>
		  <script src="static/D3js/d3.min.js"></script>
		  <script src="static/D3js/d3-queue.v3.min.js"></script>
		
		  <link href="static/css/modify_datgui.css" rel="stylesheet">
		  
		  <script>if (window.module) module = window.module;</script>
	</head>
	<body>
		<div id="UI">
		</div>
		<div id="container"></div>
		
		

		<script src="<AbsolutePathToDirectory>/static/2D3D_connection_heatmap_test.js"></script>
		<script type="text/javascript">
			function defineData(datainput){
				
				//console.log(electroLensMain);
				console.log("start")
				data = datainput;
				//console.log("end")
				console.log(data);
                var loc = window.location.pathname;
                var dir = loc.substring(0, loc.lastIndexOf('/'));
                console.log(loc);
                console.log(dir);
				electroLensMain();
			}
		</script>
		
			


	</body>
</html>

"""
def html_to_data_uri(html, js_callback=None):
    # This function is called in two ways:
    # 1. From Python: in this case value is returned
    # 2. From Javascript: in this case value cannot be returned because
    #    inter-process messaging is asynchronous, so must return value
    #    by calling js_callback.
    html = html.encode("utf-8", "replace")
    b64 = base64.b64encode(html).decode("utf-8", "replace")
    ret = "data:text/html;base64,{data}".format(data=b64)
    if js_callback:
        js_print(js_callback.GetFrame().GetBrowser(),
                 "Python", "html_to_data_uri",
                 "Called from Javascript. Will call Javascript callback now.")
        js_callback.Call(ret)
    else:
        print("not js callback")
        print(ret)
        return ret

def check_versions():
    ver = cef.GetVersion()
    print("[ElectroLens] CEF Python {ver}".format(ver=ver["version"]))
    print("[ElectroLens] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[ElectroLens] CEF {ver}".format(ver=ver["cef_version"]))
    print("[ElectroLens] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"

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
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    settings = {
        "debug": True,
        "log_severity": cef.LOGSEVERITY_INFO,
        "log_file": "debug.log",
        "remote_debugging_port":8080,
    }
    cef.Initialize(settings=settings)
    cwd = os.getcwd()

    browser_setting = { "file_access_from_file_urls_allowed":True,\
                    "universal_access_from_file_urls_allowed": True,\
                    "web_security_disabled":True}
    dir_path = os.path.dirname(__file__).replace("\\","/")
    index_filepath = os.path.join(dir_path, 'static/index_cefpython_clean.html')
    print(index_filepath)
    browser = cef.CreateBrowserSync(url=index_filepath,#url=html_to_data_uri(HTML_code.replace("<AbsolutePathToDirectory>",dir_path)),
                                    window_title="ElectroLens", 
                                    settings = browser_setting)
    browser.SetClientHandler(LoadHandler(config))
    browser.ShowDevTools()
    bindings = cef.JavascriptBindings()
    #browser.SetJavascriptBindings(bindings)
    cef.MessageLoop()
    # del browser
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
    #def OnLoadEnd(self, browser, **_):
    #    browser.ExecuteFunction("defineData", self.config)
    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:
            # Loading is complete. DOM is ready.
            browser.ExecuteFunction("defineData", self.config)
