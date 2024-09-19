import logging


class StageFuncs:
    def main_menu(self):
        if hasattr(self, 'state') and hasattr(self, 'unload'):
            if self.state == -1:
                self.unload()
            elif self.state == 0:
                pass
            elif self.state == 1:
                pass
        else:
            logging.critical(f' Failed to run StageFunc \'main_menu\':'
                             f' At least one required attribute from class {self.__class__.__name__} is missing')

    def test_scene(self):
        if hasattr(self, 'state') and hasattr(self, 'unload') and hasattr(self, 'assets'):
            if self.state == -1:
                pass
            elif self.state == 0:
                for asset in self.assets:
                    asset.add_to_scene()
            elif self.state >= 1:
                self.state = 0
        else:
            logging.critical(f' Failed to run StageFunc \'main_menu\':'
                             f' At least one required attribute from class {self.__class__.__name__} is missing')

    def test_scene_3d(self):
        if hasattr(self, 'state') and hasattr(self, 'unload') and hasattr(self, 'assets'):
            if self.state == -1:
                pass
            elif self.state == 0:
                for asset in self.assets:
                    asset.add_to_scene()
            elif self.state >= 1:
                self.state = 0
        else:
            logging.critical(f' Failed to run StageFunc \'main_menu\':'
                             f' At least one required attribute from class {self.__class__.__name__} is missing')