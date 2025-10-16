import json
import logging
import subprocess

from dbus import Interface, SessionBus
from rapidfuzz import fuzz
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class DemoExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def __init__(self):
        BUS_NAME = "org.gnome.Shell"
        OBJECT_PATH = "/org/gnome/Shell/Extensions/Windows"
        INTERFACE = "org.gnome.Shell.Extensions.Windows"

        self.bus = SessionBus()
        self.obj = self.bus.get_object(BUS_NAME, OBJECT_PATH)
        self.obj_interface = Interface(self.obj, INTERFACE)
        self.logger = logging.getLogger(__name__)

    def get_windows(self):
        try:
            windows_json = self.obj_interface.List()
            windows_data = json.loads(windows_json)

            return windows_data
        except KeyError:
            print("DBUS ERROR")
        except Exception as e:
            print(f"ERROR: {e}")

    def move_to_window(self, window_data):
        self.obj_interface.Activate(window_data["id"])

    def on_event(self, event, extension):
        query = event.get_argument() or ""
        self.logger.info("INITIALIZING QUERY: ", query)

        windows_data = self.get_windows()
        windows_data.sort(
            key=lambda x: fuzz.ratio(query, x["title"] + x["wm_class"]), reverse=True
        )
        self.logger.debug(windows_data)

        items = []

        for window in windows_data:
            items.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"{window['wm_class']}: {window['title']}",
                    on_enter=RunScriptAction(
                        f"gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell/Extensions/Windows --method org.gnome.Shell.Extensions.Windows.Activate {window['id']}"
                    ),
                )
            )

        self.logger.info("OBJECTS CREATED")

        return RenderResultListAction(items)


if __name__ == "__main__":
    DemoExtension().run()
