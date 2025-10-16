import json
import logging

import gi

gi.require_version("Gtk", "3.0")
from dbus import Interface, SessionBus
from gi.repository import Gtk
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
        self.icon_search_obj = Gtk.IconTheme.get_default()

        self.logger = logging.getLogger(__name__)

    def get_combined_fuzzy_score(self, wm_class, title, query):
        query = query.lower().strip()
        wm_class = wm_class.lower().strip()
        title = title.lower().stip()

        wm_class_score = fuzz.ratio(query, wm_class)
        combined_score = fuzz.token_set_ratio(query, f"{wm_class} {title}")

        return (5 * wm_class_score) + combined_score

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
            key=lambda x: self.get_combined_fuzzy_score(
                x["wm_class"], x["title"], query
            ),
            reverse=True,
        )
        self.logger.debug(windows_data)

        items = []

        for window in windows_data:
            icon = self.icon_search_obj.lookup_icon(window["wm_class"], 48, 0)
            if icon:
                icon_name = icon.get_filename()
            else:
                icon_name = "images/icon.png"

            items.append(
                ExtensionResultItem(
                    icon=icon_name,
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
