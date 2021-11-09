from bpy.utils import previews
import os


class VlanderSettings:
    icons_collection = {}
    # the classes to register/unregister
    VLANDER_classes = []

    def setup(self):
        icons = previews.new()
        icons_dir = os.path.join(os.path.dirname(__file__), "icons")
        for icon in os.listdir(icons_dir):
            name, ext = os.path.splitext(icon)
            icons.load(name, os.path.join(icons_dir, icon), 'IMAGE')
        self.icons_collection["main"] = icons

    def destroy(self):
        for icons in self.icons_collection.values():
            previews.remove(icons)
        self.icons_collection.clear()
