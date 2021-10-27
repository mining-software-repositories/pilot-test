class MyModifiedFile:
    def __init__(self, my_file):
        self.my_file = my_file

    def get_filename(self):
        return self.my_file.filename

    def get_change_type(self):
        return self.my_file.change_type.name

    def get_added_lines(self):
        return self.my_file.added_lines

    def get_deleted_lines(self):
        return self.my_file.deleted_lines

    def get_source_code(self):
        return self.my_file.source_code

    def get_nloc(self):
        return self.my_file.nloc

    def get_complexity(self):
        return self.my_file.complexity

    def get_modifications(self):
        added = self.my_file.added_lines
        deleted = self.my_file.deleted_lines
        return added + deleted

    def get_old_path(self):
        return self.my_file.old_path

    def get_new_path(self):
        return self.my_file.new_path

    def get_path(self):
        pass