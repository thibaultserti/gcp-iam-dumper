class Member:
    def __init__(self, name) -> None:
        self.roles = set()
        self.name = name

    def add_role(self, role: str) -> None:
        self.roles.add(role)

    def is_user(self)-> bool:
        return self.name.startswith("user:")

    def is_sa(self)-> bool:
        return self.name.startswith("serviceAccount:")
    
    def is_group(self) -> bool:
        return self.name.startswith("group:")
    
    def is_physical(self) -> bool:
        return self.is_group() or self.is_user()
    
    def __repr__(self) -> str:
        return str(list(self.roles))
        

class Role:
    def __init__(self, name) -> None:
        self.members = set()
        self.name = name
    
    def add_member(self, member: str) -> None:
        self.members.add(member)
    
    def __repr__(self) -> str:
        return str(list(self.members))
