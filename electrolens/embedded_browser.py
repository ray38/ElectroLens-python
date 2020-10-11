"""handles cefpython browser"""

import sys
import os
import platform
from cefpython3 import cefpython as cef


def check_versions():
    ver = cef.GetVersion()
    print("[ElectroLens] CEF Python {ver}".format(ver=ver["version"]))
    print("[ElectroLens] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[ElectroLens] CEF {ver}".format(ver=ver["cef_version"]))
    print("[ElectroLens] Python {ver} {arch}".format(
        ver=platform.python_version(),
        arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


def load_browser(configuration) -> None:
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    settings = {
        # "debug": True,
        # "log_severity": cef.LOGSEVERITY_INFO,
        # "log_file": "debug.log",
        # "remote_debugging_port":8080,
    }
    cef.Initialize(settings=settings)
    cwd = os.getcwd()

    browser_setting = {"file_access_from_file_urls_allowed": True,
                       "universal_access_from_file_urls_allowed": True,
                       "web_security_disabled": True}
    dir_path = os.path.dirname(__file__).replace("\\", "/")
    index_filepath = "file://" + os.path.join(dir_path, 'static/index_cefpython_clean.html')
    print(index_filepath)
    browser = cef.CreateBrowserSync(url=index_filepath,
                                    window_title="ElectroLens",
                                    settings=browser_setting)
    browser.SetClientHandler(LoadHandler(configuration))
    # if show_dev_tools:
    #    browser.ShowDevTools()
    cef.MessageLoop()
    # del browser
    cef.Shutdown()


class LoadHandler(object):

    def __init__(self, config):
        self.config = config

    # def OnLoadEnd(self, browser, **_):
    #    browser.ExecuteFunction("defineData", self.config)
    def OnLoadingStateChange(self, browser, is_loading, **_):
        """Called when the loading state has changed."""
        if not is_loading:
            # Loading is complete. DOM is ready.
            browser.ExecuteFunction("defineData", self.config)
