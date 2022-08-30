"""
Contains residue groups.
"""
from src.groups.group import Group


class Residue():
    """
    Residue class.
    """

    @classmethod
    def create(cls, value, modulus) -> 'Residue':
        """
        Creates a residue of given value with given modulus.

        :param value: Value of the residue.
        :type value: int
        :param modulus: Modulus of the residue.
        :type modulus: int
        :return: Residue of given value with given modulus
        :rtype: Residue
        """
        residue = Residue()
        residue.value = int(value)
        residue.modulus = modulus
        return residue

    def __init__(self):
        self.value = None
        self.modulus = None

    def __int__(self):
        return self.value

    def __repr__(self):
        return f'Residue <{self.__str__()}>'

    def __str__(self):
        return str(int(self))

    def __eq__(self, other):
        return int(self) % self.modulus == int(other) % self.modulus

    def __add__(self, other) -> 'Residue':
        other_val = int(other)
        s = (self.value + other_val) % self.modulus
        return Residue.create(s, self.modulus)

    def __radd__(self, other) -> 'Residue':
        return self + other

    def __sub__(self, other) -> 'Residue':
        other_val = int(other)
        s = (self.value - other_val) % self.modulus
        return Residue.create(s, self.modulus)

    def __rsub__(self, other) -> 'Residue':
        return Residue.create(int(other), self.modulus).__sub__(self)

    def __neg__(self):
        return Residue.create(self.modulus - int(self), self.modulus)

    def __mul__(self, other) -> 'Residue':
        other_val = int(other)
        s = (self.value * other_val) % self.modulus
        return Residue.create(s, self.modulus)

    def __rmul__(self, other) -> 'Residue':
        return self * other

    def __pow__(self, other) -> 'Residue':
        other_val = int(other)
        s = pow(self.value, other_val, self.modulus)
        return Residue.create(s, self.modulus)

    def __floordiv__(self, other) -> 'Residue':
        other_val = Residue.create(int(other), self.modulus)
        other_val_inv = other_val.invert()
        return self * other_val_inv

    def __rfloordiv__(self, other) -> 'Residue':
        return Residue.create(int(other), self.modulus).__floordiv__(self)

    def __truediv__(self, other) -> 'Residue':
        other_val = Residue.create(int(other), self.modulus)
        other_val_inv = other_val.invert()
        return self * other_val_inv

    def __rtruediv__(self, other) -> 'Residue':
        return Residue.create(int(other), self.modulus).__truediv__(self)

    def invert(self):
        inv_val = pow(self.value, -1, self.modulus)
        return Residue.create(inv_val, self.modulus)


class ResidueGroup(Group):

    @classmethod
    def create(cls, modulus) -> 'ResidueGroup':
        group = ResidueGroup()
        group.modulus = modulus
        return group

    def __init__(self):
        self.modulus = None

    def gen(self, x: int) -> Residue:
        return Residue.create(x, self.modulus)

    def inv(self, x) -> Residue:
        residue = self.gen(int(x))
        return residue.invert()
