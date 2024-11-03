import pygame


class Quadtree:
    def __init__(self, x, y, w, h, max_objects=4):
        self.x = x  # X-coordinate of the node's top-left corner
        self.y = y  # Y-coordinate of the node's top-left corner
        self.w = w  # Width of the node
        self.h = h  # Height of the node
        self.objects = []  # Objects contained directly in this node
        self.nodes = []  # Child nodes (subdivisions)
        self.divided = False  # Flag indicating whether the node is subdivided
        self.max_objects = max_objects  # Max objects before subdivision

    def subdivide(self):
        w = self.w / 2
        h = self.h / 2
        self.nodes = [
            Quadtree(self.x, self.y, w, h, self.max_objects),              # Top-left
            Quadtree(self.x + w, self.y, w, h, self.max_objects),          # Top-right
            Quadtree(self.x, self.y + h, w, h, self.max_objects),          # Bottom-left
            Quadtree(self.x + w, self.y + h, w, h, self.max_objects)       # Bottom-right
        ]
        self.divided = True

        # Redistribute objects into child nodes
        for obj in self.objects:
            self.insert(obj)
        self.objects = []  # Clear objects after redistributing

    def insert(self, obj):
        if not self.contains(obj):
            return False  # Object does not belong in this node

        if self.divided:
            # Insert into appropriate child node
            for node in self.nodes:
                if node.insert(obj):
                    return True
            return False  # Should not reach here
        else:
            self.objects.append(obj)
            if len(self.objects) > self.max_objects:
                self.subdivide()
            return True

    def contains(self, obj):
        # Check if the point is within the node's boundaries
        return (self.x <= obj.pos.x < self.x + self.w and
                self.y <= obj.pos.y < self.y + self.h)

    def intersects(self, area):
        # Check if the node intersects with a given rectangular area
        return not (area.x > self.x + self.w or area.x + area.w < self.x or
                    area.y > self.y + self.h or area.y + area.h < self.y)

    def query(self, area):
        results = []
        if not self.intersects(area):
            return results  # No intersection, return empty list

        # Check objects at the current node
        for obj in self.objects:
            if area.contains(obj):
                results.append(obj)

        # Recurse into child nodes
        if self.divided:
            for node in self.nodes:
                results.extend(node.query(area))
        return results

    def query_all(self):
        results = []
        results.extend(self.objects)
        if self.divided:
            for node in self.nodes:
                results.extend(node.query_all())
        return results

    def show(self, screen):
        if self.divided:
            for node in self.nodes:
                node.show(screen)
        else:
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 1)
    
    def __repr__(self):
        return f"Quadtree(x={self.x}, y={self.y}, w={self.w}, h={self.h})"
