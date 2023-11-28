"""Execute Commands"""
from settings import AUTHENTICATION_SUCCESSFUL, SESSIONS_FILE, USER_DIR
from globals import users

INVALID_COMMAND_SYNTAX = 'Invalid Comand Syntax'
INVALID_COMMAND = 'Invalid Command'

class Executor:
    """Handles Command Execution for a specific username"""
    username = ""
    def execute(self, command):
        """Main Command Handler"""
        if self.username:
            with open(USER_DIR / self.username / 'history.txt', 'a', encoding='utf-8') as f:
                print(command, file=f)

        args = command.split()

        if len(args) < 1:
            return INVALID_COMMAND

        commands = {
            'list': self.ls,
            'change_folder': self.change_folder,
            'read_file': self.read_file,
            'write_file': self.write_file,
            'create_folder': self.create_folder,
            'login': self.login,
            'register': self.register,
            'commands': self.commands
        }

        if args[0] not in commands.keys():
            return INVALID_COMMAND

        return commands[args[0]](*args)


    def login(self, *args):
        """login <username> <password> -- Handles Login Process"""
        if len(args) != 3: return INVALID_COMMAND_SYNTAX
        [_, username, password] = args
        try:
            if users[username]['logged_in']:
                return 'User Already logged in'
            if users[username]['password'] == password:
                if self.username:
                    users[self.username]['logged_in'] = False
                self.username = username
                return AUTHENTICATION_SUCCESSFUL
            return 'Password Invalid'
        except KeyError:
            return 'User not Registered'


    def register(self, *args):
        """register <username> <password> -- Handles Registration Process, USer Directory Creation"""
        if len(args) != 3: return INVALID_COMMAND_SYNTAX
        [_, username, password] = args

        if username in users.keys():
            return 'Username Already Exists'

        user_dir = USER_DIR / username
        user_dir.mkdir(parents=True)

        users[username] = {
            'password': password,
            'cwd': user_dir,
            'logged_in': True
        }
        with open(SESSIONS_FILE, 'a', encoding='utf-8') as session_file:
            print(f'{username},{password},{user_dir}', file=session_file)

        self.username = username
        return AUTHENTICATION_SUCCESSFUL


    def ls(self, *args):
        """list -- Lists Contents in Current Working Directory"""
        if len(args) != 1: return INVALID_COMMAND_SYNTAX
        files = [file.name for file in users[self.username]['cwd'].iterdir()]
        if len(files) == 0: return 'Nothing in Current Directory'
        return '\n'.join(files)


    def change_folder(self, *args):
        """change_folder <folder> -- Changes Folder to Given Directory"""
        if len(args) != 2: return INVALID_COMMAND_SYNTAX
        cwd = users[self.username]['cwd']
        change_to_dir = cwd / args[1]
        change_to_dir = change_to_dir.resolve()
        if change_to_dir.exists() and\
        change_to_dir.is_dir() and\
        self.username in str(change_to_dir):
            users[self.username]['cwd'] = change_to_dir
            return f'Directory Changed'
        return 'No Such Directory Exists'


    def read_file(self, *args):
        """read_file <file> -- Reads File and shows contents"""
        if len(args) != 2: return INVALID_COMMAND_SYNTAX
        cwd = users[self.username]['cwd']
        file = cwd / args[1]
        if file.exists() and file.is_file():
            return file.read_text()
        return 'File does not exist'


    def write_file(self, *args):
        """write_file <file> <content> -- Writes in File"""
        if len(args) < 3: return INVALID_COMMAND_SYNTAX
        cwd = users[self.username]['cwd']
        file = cwd / args[1]
        if file.is_dir():
            return "Is a Directory"
        with open(file, 'a', encoding='utf-8') as f:
            f.write(*args[2:])
        return 'Done Writing'


    def create_folder(self, *args):
        """create_folder <folder> -- Creates Folder"""
        if len(args) != 2: return INVALID_COMMAND_SYNTAX
        cwd = users[self.username]['cwd']
        creation_dir = cwd / args[1]
        creation_dir = creation_dir.resolve()
        if creation_dir.exists() and self.username not in str(creation_dir):
            return 'File/Directory Already Exists'

        creation_dir.mkdir(parents=True)
        return 'Made Directory'
    
    def _quit(self):
        """quit - Quit Connection"""

    def commands(self, *args):
        """commands -- Help for All Commands"""
        cmds = {
            'list': self.ls,
            'change_folder': self.change_folder,
            'read_file': self.read_file,
            'write_file': self.write_file,
            'create_folder': self.create_folder,
            'login': self.login,
            'register': self.register,
            'quit': self._quit,
            'commands': self.commands
        }
        help_list = [x.__doc__ for x in cmds.values()]
        return '\n'.join(help_list)
