from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

import subprocess

class DemoExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or ''

        output = subprocess.run(f'wmctrl -l | awk \'$2 != "-1"\' | cut -d " " -f 5- | fzf -f \'{query}\'', shell=True, text=True, capture_output=True).stdout
        windows = output.strip().split("\n")

        items = []

        for window in windows:
            items.append(ExtensionSmallResultItem(icon='images/icon.png',
                                             name=window,
                                             on_enter=RunScriptAction(f'wmctrl -a \'{window}\'')))

        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()