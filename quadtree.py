class Quadtree:
    def __init__(self, x, y, w, h, max_objects=4):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.objects = []
        self.nodes = []
        self.divided = False
        self.max_objects = max_objects
    
    def subdivide(self):
        w = self.w / 2
        h = self.h / 2
        self.nodes.append(Quadtree(self.x, self.y, w, h))
        self.nodes.append(Quadtree(self.x + w, self.y, w, h))
        self.nodes.append(Quadtree(self.x, self.y + h, w, h))
        self.nodes.append(Quadtree(self.x + w, self.y + h, w, h))
        for obj in self.objects:
            for node in self.nodes:
                node.insert(obj)
        self.objects = []
        self.divided = True

    def insert(self, obj):
        if len(self.nodes) >= self.max_objects:
            if not self.divided:
                self.subdivide()
            for node in self.nodes:
                node.insert(obj)
            return
        if self.contains(obj):
            self.objects.append(obj)
        return

    def contains(self, obj, point=True):
        if point:
            return self.x <= obj.pos.x <= self.x + self.w and self.y <= obj.pos.y <= self.y + self.h
        return ((self.x <= obj.x <= self.x + self.w or self.x <= obj.x + obj.w <= self.x + self.w) and
                (self.y <= obj.y <= self.y + self.h or self.y <= obj.y + obj.h <= self.y + self.h))

    def query(self, area) -> list:
        results = []
        if not self.contains(area):
            return results
        if self.divided:
            for node in self.nodes:
                if node.contains(area, False):
                    results.extend(node.query(area))
            return results
        for obj in self.objects:
            if area.contains(obj):
                results.append(obj)
        return results
