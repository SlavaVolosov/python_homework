# Task 5

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __str__(self):
        return f'Point({self.x}, {self.y})'

    def __eq__(self, value):
        if isinstance(value, Point):
            return self.x == value.x and self.y == value.y
        return False

    def distance_to(self, other):
        if not isinstance(other, Point):
            raise TypeError('Argument must be a Point')
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Vector(Point):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __str__(self):
        return f'Vector({self.x}, {self.y})'

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError('Can only add another Vector')
        return Vector(self.x + other.x, self.y + other.y)

    # added a static method to create a Vector from two Points as it seemed to make sense
    @staticmethod
    def from_points(p1, p2):
        if not (isinstance(p1, Point) and isinstance(p2, Point)):
            raise TypeError('Arguments must be Point instances')
        return Vector(p2.x - p1.x, p2.y - p1.y)


# Demonstration
# Point class
p1 = Point(3, 4)
p2 = Point(0, 0)
print('p1:', p1)
print('p2:', p2)
print('p1 == p2:', p1 == p2)
print('Distance from p1 to p2:', p1.distance_to(p2))

# Vector class
v1 = Vector(1, 2)
v2 = Vector(3, 4)
print('v1:', v1)
print('v2:', v2)
print('v1 + v2:', v1 + v2)
print('v2 - v1:', v2 - v1)
print('v1 * 3:', v1 * 3)
print('v2 / 2:', v2 / 2)

# Demonstrate error handling
try:
    print('v1 + p1:', v1 + p1)
except Exception as e:
    print('Error:', e)
try:
    print('v1 / 0:', v1 / 0)
except Exception as e:
    print('Error:', e)

# Demonstrate from_points static method
v3 = Vector.from_points(p1, p2)
print('v3 (from p1 and p2):', v3)
v4 = Vector.from_points(p2, p1)
print('v4 (from p2 and p1):', v4)
