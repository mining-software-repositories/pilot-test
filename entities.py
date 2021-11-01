class MyCommit:
    def __init__(self, my_commit):
        self.my_commit = my_commit

    #hash of the commit 1
    #hash (str): 
    def get_hash(self):
        return self.my_commit.hash

    #commit message 2
    #msg (str): 
    def get_msg(self):
        return self.my_commit.msg

    # commit author (name, email) 3
    # author (Developer): 
    def get_(self):
        return self.my_commit.author

    #commit committer (name, email) 4
    #committer (Developer): 
    def get_committer(self):
        return self.my_commit.committer

    #authored date 5
    #author_date (datetime): 
    def get_author_date(self):
        return self.my_commit.author_date

    #author timezone (expressed in seconds from epoch) 6
    #author_timezone (int): 
    def get_author_timezone(self):
        return self.my_commit.author_timezone

    #commit date 7
    #committer_date (datetime): 
    def get_committer_date(self):
        return self.my_commit.committer_date

    # commit timezone (expressed in seconds from epoch) 8
    #committer_timezone (int): 
    def get_committer_timezone(self):
        return self.my_commit.committer_timezone

    #List of branches that contain this commit 9
    #branches (List[str]): 
    def get_branches(self):
        return self.my_commit.branches

    # True if the commit is in the main branch 10
    #in_main_branch (Bool): 
    def get_in_main_branch(self):
        return self.my_commit.in_main_branch

    # True if the commit is a merge commit 11
    #merge (Bool): 
    def get_merge(self):
        return self.my_commit.merge

    # list of modified files in the commit (see modifications_toplevel) 12
    #modified_files (List[ModifiedFile]): 
    def get_modified_files(self):
        return self.my_commit.modified_files

    # list of the commit parents 13
    #parents (List[str]): 
    def get_parents(self):
        return self.my_commit.parents

    # project name 14
    #project_name (str): 
    def get_project_name(self):
        return self.my_commit.project_name

    # project path 15
    #project_path (str): 
    def get_project_path(self):
        return self.my_commit.project_path

    # number of deleted lines in the commit (as shown from –shortstat). 16
    #deletions (int): 
    def get_deletions(self):
        return self.my_commit.deletions

    # number of added lines in the commit (as shown from –shortstat). 17
    #insertions (int): 
    def get_insertions(self):
        return self.my_commit.insertions

    #total number of added + deleted lines in the commit (as shown from –shortstat). 18
    #lines (int): 
    def get_lines(self):
        return self.my_commit.lines

    # number of files changed in the commit (as shown from –shortstat). 19
    #files (int): 
    def get_files(self):
        return self.my_commit.files

    # DMM metric value for the unit size property. 20
    #dmm_unit_size (float): 
    def get_dmm_unit_size(self):
        return self.my_commit.dmm_unit_size

    # DMM metric value for the unit complexity property. 21
    #dmm_unit_complexity (float): 
    def get_dmm_unit_complexity(self):
        return self.my_commit.dmm_unit_complexity

    # DMM metric value for the unit interfacing property. 22
    #dmm_unit_interfacing (float): 
    def get_dmm_unit_interfacing(self):
        return self.my_commit.dmm_unit_interfacing

class MyModifiedFile:
    def __init__(self, my_file):
        self.my_file = my_file

    # old_path: old path of the file (can be _None_ if the file is added)
    def get_old_path(self):
        return self.my_file.old_path

    #new_path: new path of the file (can be _None_ if the file is deleted)
    def get_new_path(self):
        return self.my_file.new_path

    def get_path(self):
        pass

    #filename: 
    # return only the filename 
    # (e.g., given a path-like-string such as “/Users/dspadini/pydriller/myfile.py” returns “myfile.py”)
    def get_filename(self):
        return self.my_file.filename

    # change_type: type of the change: 
    # can be Added, Deleted, Modified, or Renamed.
    def get_change_type(self):
        return self.my_file.change_type.name

    # diff: diff of the file as Git presents it (e.g., starting with @@ xx,xx @@).
    def get_diff(self):
        return self.my_file.diff
    
    # diff_parsed: diff parsed in a dictionary containing the added and deleted lines. The dictionary has 2 keys: “added” and “deleted”, each containing a list of Tuple (int, str) corresponding to (number of line in the file, actual line).
    def get_diff_parsed(self):
        return self.my_file.diff_parsed

    # added_lines: number of lines added
    def get_added_lines(self):
        return self.my_file.added_lines

    # deleted_lines: number of lines removed
    def get_deleted_lines(self):
        return self.my_file.deleted_lines

    # source_code: source code of the file (can be _None_ if the file is deleted or only renamed)
    def get_source_code(self):
        return self.my_file.source_code

    # source_code_before: source code of the file before the change (can be _None_ if the file is added or only renamed)
        def get_source_code_before(self):
            return self.my_file.source_code_before

    # methods: list of methods of the file. The list might be empty if the programming language is not supported or if the file is not a source code file. These are the methods after the change.
    def get_methods(self):
        return self.my_file.methods

    # methods_before: list of methods of the file before the change (e.g., before the commit.)
    def get_methods_before(self):
        return self.my_file.methods_before

    # changed_methods: subset of _methods_ containing only the changed methods.
    def get_changed_methods(self):
        return self.my_file.changed_methods
    
    # nloc: Lines Of Code (LOC) of the file
    def get_nloc(self):
        return self.my_file.nloc

    #complexity: Cyclomatic Complexity of the file
    def get_complexity(self):
        return self.my_file.complexity

    # token_count: Number of Tokens of the file
    def get_token_count(self):
        return self.my_file.token_count

    def get_modifications(self):
        added = self.my_file.added_lines
        deleted = self.my_file.deleted_lines
        return added + deleted