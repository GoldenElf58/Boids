class Area:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def contains(self, item):
        return self.x <= item.pos.x <= self.x + self.w and self.y <= item.pos.y <= self.y + self.h
    
    def __repr__(self):
        return f"Area({self.x}, {self.y}, {self.w}, {self.h})"
