import math

from kivy3.math.vectors import Vector3
from kivy.graphics.transformation import Matrix

class Collider(object):
    """docstring for Collider"""
    def __init__(self, parent=None, callback=None):
        super(Collider, self).__init__()
        self.parent = parent
        self.callback = callback
        
    def check(self, player_pos, player_size):
        return False

    def transform(self, p):
        if self.parent is None:
            return p
        m = Matrix()
        m.translate(self.parent.pos.x, self.parent.pos.y, self.parent.pos.z)
        m.scale(*self.parent.scale.xyz)
        m.rotate(math.radians(self.parent.rot.x), 1,0,0)
        m.rotate(math.radians(self.parent.rot.y), 0,1,0)
        m.rotate(math.radians(self.parent.rot.z), 0,0,1)
        p = m.transform_point(*p)
        return Vector3(p)

class SphereCollider(Collider):
    """docstring for SphereCollider"""
    def __init__(self, position, radius, **kwargs):
        super(SphereCollider, self).__init__(**kwargs)
        self.position = position
        self.radius = radius

    def check(self, player_pos, player_size):
        p1 = self.transform(self.position)
        player_pos = Vector3(player_pos)

        if (p1-player_pos).length() < player_size + self.radius:
            return True
        return False

class LineCollider(Collider):
    """docstring for LineCollider"""
    def __init__(self, p1, p2, **kwargs):
        super(LineCollider, self).__init__(**kwargs)
        self.p1 = Vector3(p1)
        self.p2 = Vector3(p2)

    def distance(self, player_pos):
        p1 = self.transform(self.p1)
        p2 = self.transform(self.p2)
        player_pos = Vector3(player_pos)
        seg_v = p2 - p1
        pt_v = player_pos - p1
        if seg_v.length() <= 0:
            raise ValueError("Invalid segment length")
        seg_v_unit = seg_v * (1 / seg_v.length())
        proj = pt_v.dot(seg_v_unit)
        if proj <= 0:
            closest = Vector3(p1)
        elif proj >= seg_v.length():
            closest = Vector3(p2)
        else:
            proj_v = seg_v_unit * proj
            closest = proj_v + p1

        dist_v = player_pos - closest
        # print(dist_v, dist_v.length(), player_pos, closest)
        return dist_v.length()
        
    def check(self, player_pos, player_size):
        if self.distance(player_pos) > player_size:
            return False
        # offset = dist_v / dist_v.length() * (circ_rad - dist_v.length())
        return True

class BoxCollider(Collider):
    """docstring for BoxCollider"""
    def __init__(self, p1, p2, **kwargs):
        super(BoxCollider, self).__init__(**kwargs)
        self.p1 = p1
        self.p2 = p2

    def check(self, player_pos, player_size):
        p1 = self.transform(self.p1)
        p2 = self.transform(self.p2)
        player_pos = Vector3(player_pos)
        if p1.x > p2.x:
            p1.x, p2.x = p2.x, p1.x
        if p1.y > p2.y:
            p1.y, p2.y = p2.y, p1.y
        proj_v = player_pos.clamp(p1, p2)
        if (proj_v - player_pos).length() > player_size:
            return False
        return True

def test():
    c = LineCollider(p1 = Vector3([0,0,0]), p2 = Vector3([1,1,0]))
    print(c.check(Vector3([1,0,0]), 0.75))

if __name__ == '__main__':
    test()