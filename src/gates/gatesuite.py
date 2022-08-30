from src.gates.branching.ifthenelsegate import if_then_else_gate


class GateSuite():

    def __init__(self, group):
        self.group = group
    
    def if_then_else(self, condition_wire, if_wire, else_wire):
        return if_then_else_gate(condition_wire, if_wire, else_wire)
