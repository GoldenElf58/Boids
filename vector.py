import math


class Vector:
    def __init__(self, x: float = 0, y: float = 0):
        self.x: float = x
        self.y: float = y
    
    def to_tuple(self):
        return self.x, self.y
    
    def limit(self, x_limit: float, y_limit: float):
        return Vector(max(min(self.x, x_limit), -x_limit), max(min(self.y, y_limit), -y_limit))
    
    def distance(self, other) -> float:
        return (self - other).__len__()
    
    def distance_squared(self, other) -> float:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2
    
    def to_polar(self):
        angle = math.atan2(self.y, self.x)
        speed = (self.x ** 2 + self.y ** 2) ** 0.5
        return PolarVector(angle, speed)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self == other
    
    def __len__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of range")
    
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Index out of range")
    
    def __iter__(self):
        return iter([self.x, self.y])
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __pos__(self):
        return Vector(self.x, self.y)
    
    def __abs__(self):
        return len(self)
    
    def __invert__(self):
        return Vector(-self.x, -self.y)
    
    def __round__(self, ndigits=None):
        return Vector(round(self.x, ndigits), round(self.y, ndigits))


class Point(Vector):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)


class PolarVector(Vector):
    def __init__(self, angle=0.0, speed=0.0):
        # Indicate that initialization is in progress
        self._initializing = True
        
        # Initialize angle and speed
        self._angle = float(angle)
        self._speed = float(speed)
        
        # Compute x and y based on angle and speed
        x = self._speed * math.cos(self._angle)
        y = self._speed * math.sin(self._angle)
        
        # Initialize the base Vector class without invoking __setattr__
        super().__init__(x, y)
        
        # Initialization complete
        self._initializing = False
    
    def limit(self, speed_limit: float, angle_limit: float = None) -> 'PolarVector':
        if angle_limit is not None:
            return PolarVector(max(min(self.angle, angle_limit), -angle_limit),
                               max(min(self.speed, speed_limit), -speed_limit)).limit(angle_limit)
        return PolarVector(self.angle, max(min(self.speed, speed_limit), -speed_limit))
    
    @property
    def angle(self):
        """Angle in radians."""
        # Update angle based on current x and y
        self._angle = math.atan2(self.y, self.x)
        return self._angle
    
    @angle.setter
    def angle(self, value):
        self._angle = float(value)
        # Update x and y based on new angle and current speed
        self._update_cartesian()
    
    @property
    def speed(self):
        """Magnitude of the vector."""
        # Update speed based on current x and y
        self._speed = math.hypot(self.x, self.y)
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = float(value)
        # Update x and y based on new speed and current angle
        self._update_cartesian()
    
    def _update_cartesian(self):
        """Update x and y based on the current angle and speed."""
        x = self._speed * math.cos(self._angle)
        y = self._speed * math.sin(self._angle)
        super().__setattr__('x', x)
        super().__setattr__('y', y)
    
    def _update_polar(self):
        """Update angle and speed based on the current x and y."""
        self._angle = math.atan2(self.y, self.x)
        self._speed = math.hypot(self.x, self.y)
    
    def __setattr__(self, name, value):
        if name in ('x', 'y'):
            super().__setattr__(name, value)
            # Only update polar coordinates if initialization is complete
            if not getattr(self, '_initializing', False):
                self._update_polar()
        else:
            super().__setattr__(name, value)
    
    # Override methods to ensure they return PolarVector instances
    def __add__(self, other):
        result = super().__add__(other)
        return PolarVector.from_cartesian(result.x, result.y)
    
    def __sub__(self, other):
        result = super().__sub__(other)
        return PolarVector.from_cartesian(result.x, result.y)
    
    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return PolarVector(self.angle, self.speed * scalar)
        else:
            raise TypeError("Multiplication with non-scalar is not supported.")
    
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            return PolarVector(self.angle, self.speed / scalar)
        else:
            raise TypeError("Division by non-scalar is not supported.")
    
    @classmethod
    def from_cartesian(cls, x, y):
        """Create a PolarVector from x and y components."""
        angle = math.atan2(y, x)
        speed = math.hypot(x, y)
        return cls(angle, speed)
    
    def dot(self, other):
        """Compute the dot product with another vector."""
        return self.x * other.x + self.y * other.y
    
    def cross(self, other):
        """Compute the cross product with another vector (in 2D)."""
        return self.x * other.y - self.y * other.x
    
    def magnitude(self):
        """Return the magnitude of the vector."""
        return self.speed
    
    def normalize(self):
        """Return a unit vector with the same angle."""
        return PolarVector(self.angle, 1.0)
    
    def __repr__(self):
        return f"PolarVector(angle={self.angle}, speed={self.speed})"
    
    def to_degrees(self):
        """Return the angle in degrees."""
        return math.degrees(self.angle)
    
    # Override other methods to ensure they return PolarVector instances
    def __neg__(self):
        result = super().__neg__()
        return PolarVector.from_cartesian(result.x, result.y)
    
    def __pos__(self):
        return PolarVector(self.angle, self.speed)
    
    def __abs__(self):
        return self.speed
    
    def __invert__(self):
        result = super().__invert__()
        return PolarVector.from_cartesian(result.x, result.y)
    
    def __round__(self, ndigits=None):
        result = super().__round__(ndigits)
        return PolarVector.from_cartesian(result.x, result.y)
