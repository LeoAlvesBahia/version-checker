class LibClass:
    def __init__(self, complete_value):
        self.complete_value = complete_value
        self.name = None
        self.version = None
        self.operator = None

    def separate_values(self):
        temp_object = self

        if '==' in temp_object.complete_value:
            splited_values = temp_object.complete_value.split('==')
            temp_object.name = splited_values[0]
            temp_object.version = splited_values[1] if len(splited_values) > 1 else None
            temp_object.operator = '=='
        elif '>=' in temp_object.complete_value:
            splited_values = temp_object.complete_value.split('>=')
            temp_object.name = splited_values[0]
            temp_object.version = splited_values[1] if len(splited_values) > 1 else None
            temp_object.operator = '>='
        elif '<=' in temp_object.complete_value:
            splited_values = temp_object.complete_value.split('<=')
            temp_object.name = splited_values[0]
            temp_object.version = splited_values[1] if len(splited_values) > 1 else None
            temp_object.operator = '<='
        else:
            temp_object.name = temp_object.complete_value

        # uvicorn probably is a exception when come to libs name. Standard
        # in this case indicates to install package not on minimal
        if 'uvicorn' in temp_object.name:
            temp_object.name = 'uvicorn'

        return temp_object

    def check_version(self, latest_version):
        if not self.version:
            return False
        # create list for version numbers and convert string to int
        file_version = [int(a) for a in self.version.split('.')]
        latest_version = [int(a) for a in latest_version.split('.')]

        # check if a list is bigger than other than fill with 0 the smaller
        if len(file_version) > len(latest_version):
            for i in range(latest_version, file_version):
                latest_version.append(0)
        elif len(latest_version) > len(file_version):
            for i in range(file_version, latest_version):
                file_version.append(0)

        for i in range(len(file_version)):
            if latest_version[i]>file_version[i]:
                return True
        return False