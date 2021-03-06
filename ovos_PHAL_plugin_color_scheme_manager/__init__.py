import os
from os.path import join
from mycroft_bus_client.message import Message
from ovos_plugin_manager.phal import PHALPlugin
from ovos_utils.log import LOG
from ovos_utils.xdg_utils import xdg_data_home

class ColorSchemeManager(PHALPlugin):

    def __init__(self, bus=None, config=None):
        super().__init__(bus=bus, name="ovos-PHAL-plugin-color-scheme-manager", config=config)
        self.theme_path = join(xdg_data_home(), "OVOS", "ColorSchemes")
        self.bus.on("ovos.shell.gui.color.scheme.generate", self.generate_theme)

    def generate_theme(self, message):
        if "primaryColor" not in message.data or "secondaryColor" not in message.data or "textColor" not in message.data:
            return

        if "theme_name" not in message.data:
            return

        theme_name = message.data["theme_name"]
        file_name = theme_name.replace(" ", "_").lower() + ".json"

        LOG.info(f"Creating ColorScheme For {theme_name}")

        if not os.path.exists(self.theme_path):
            os.makedirs(self.theme_path)

        if file_name in os.listdir(self.theme_path):
            os.remove(join(self.theme_path, file_name))

        theme_file = open(join(self.theme_path, file_name), "w")
        theme_file.write("{\n")
        theme_file.write('"name":"' + theme_name + '",\n')
        theme_file.write('"primaryColor":"' + message.data["primaryColor"] + '",\n')
        theme_file.write('"secondaryColor":"' + message.data["secondaryColor"] + '",\n')
        theme_file.write('"textColor":"' + message.data["textColor"] + '"\n')
        theme_file.write("}\n")
        theme_file.close()
        self.bus.emit(Message("ovos.shell.gui.color.scheme.generated", {"theme_name": theme_name, "theme_path": self.theme_path}))
