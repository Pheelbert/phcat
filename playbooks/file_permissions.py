class FilePermissions:
    def __init__(self, permissions_str):
        split_output = permissions_str.split(' ')
        self.permissions_str = split_output[0]
        self.owner_user = split_output[2]
        self.owner_group = split_output[3]
        self.is_directory = permissions_str[0] == 'd'
        self.owner_user_read = permissions_str[1] == 'r'
        self.owner_user_write = permissions_str[2] == 'w'
        self.owner_user_execute = permissions_str[3] == 'x'
        self.owner_group_read = permissions_str[4] == 'r'
        self.owner_group_write = permissions_str[5] == 'w'
        self.owner_group_execute = permissions_str[6] == 'x'
        self.others_read = permissions_str[7] == 'r'
        self.others_write = permissions_str[8] == 'w'
        self.others_execute = permissions_str[9] == 'x'

    def __str__(self):
        return f'{self.permissions_str} ({self.owner_user}:{self.owner_group})'

    def get_owner(self) -> str:
        return self.owner_user

    def get_group(self) -> str:
        return self.owner_group

    def can_owner_read(self) -> bool:
        return self.owner_user_read
    
    def can_owner_write(self) -> bool:
        return self.owner_user_write

    def can_owner_execute(self) -> bool:
        return self.owner_user_execute

    def can_group_read(self) -> bool:
        return self.owner_group_read
    
    def can_group_write(self) -> bool:
        return self.owner_group_write

    def can_group_execute(self) -> bool:
        return self.owner_group_execute

    def can_others_read(self) -> bool:
        return self.others_read
    
    def can_others_write(self) -> bool:
        return self.others_write

    def can_others_execute(self) -> bool:
        return self.others_execute
