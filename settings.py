class Settings:
    def __init__(self, filename):
        # Create a list of line strings from settings file
        with open(filename) as self.file:
            self.file = self.file.readlines()

        # Remove white spaces and new lines
        for i in range(len(self.file)):
            self.file[i] = self.file[i].strip('\n')
            self.file[i] = self.file[i].replace('\t', '')
            self.file[i] = self.file[i].replace(' ', '')

        # Extract data from lines
        settings_category_list = ['screenwidth', 'screenheight', 'fullscreen', 'fps', 'vsync']
        settings_data_list = []
        categories = []
        for i in range(len(self.file)):
            if not self.file[i] == '':
                # Find line center
                assert '=' in self.file[i], filename + ', line ' + str(i) + ': No \'=\' found'
                equal_index = self.file[i].index('=')
                assert len(self.file[i]) > equal_index + 1, filename + ', line ' + str(i) + ': No data after \'=\' found'

                # Break up line string around '='
                category, settings_data = self.file[i][:equal_index], self.file[i][equal_index + 1:]
                assert category in settings_category_list, (filename + ', line ' + str(i) +
                                                            ': Category \'' + category + '\' not a valid settings category')
                settings_data_list.append([category, settings_data])
                categories.append(category)
        assert all(elem in categories for elem in settings_category_list), filename + ': At least one category in settings not found'

        # Process data from lines
        for category, settings_data in settings_data_list:
            if category == 'screenwidth':
                self.widthSetting = int(settings_data)

            elif category == 'screenheight':
                self.heightSetting = int(settings_data)

            elif category == 'fullscreen':
                if int(settings_data) == 0:
                    self.fullscreenSetting = False
                else:
                    self.fullscreenSetting = True

            elif category == 'fps':
                self.fpsSetting = int(settings_data)

            elif category == 'vsync':
                if int(settings_data) == 0:
                    self.vsyncSetting = False
                else:
                    self.vsyncSetting = True

            else:
                pass
