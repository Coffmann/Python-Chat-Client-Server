class Group():
    def __init__(self, name, owner)-> None:
        self.name = name
        self.owner = owner
        self.members = []
    
    def add_member(self, member)-> bool:
        if member not in self.members:
            self.members.append(member)
            return True
        return False
    
    def remove_member(self, member)-> bool:
        if member in self.members:
            self.members.remove(member)
            return True
        return False

class Client():
    def __init__(self,username, socket, address)-> None:
        self.username = username
        self.socket = socket
        self.address = address


clients : list[Client] = []
groups  : list[Group] = []
    