class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.textcoords = []
        self.normals = []
        self.faces = []

        for line in self.lines:
            try:
                prefix, value = line.split(" ", 1)
                prefix = prefix.strip()
                value = value.strip()
            except:
                continue

            if prefix == "v":
                self.vertices.append(list(map(float, value.split(" "))))
            elif prefix == "vt":
                self.textcoords.append(list(map(float, value.split(" "))))
            elif prefix == "vn":
                self.normals.append(list(map(float, value.split(" "))))
            elif prefix == "f":
                self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ")])

    def normalize(self, v):
        """Devuelve el vector normalizado."""
        norm = (v[0]**2 + v[1]**2 + v[2]**2)**0.5
        if norm == 0:
            return v
        return [v[i] / norm for i in range(3)]

    def assemble(self) -> list[float]:
        transform_verts = []

        for face in self.faces:
            vert_count = len(face)
            v0 = self.vertices[face[0][0] - 1]
            v1 = self.vertices[face[1][0] - 1]
            v2 = self.vertices[face[2][0] - 1]

            vt0 = self.textcoords[face[0][1] - 1]
            vt1 = self.textcoords[face[1][1] - 1]
            vt2 = self.textcoords[face[2][1] - 1]

            if len(self.normals) != 0:
                vn0 = self.normals[face[0][2] - 1]
                vn1 = self.normals[face[1][2] - 1]
                vn2 = self.normals[face[2][2] - 1]
            else:
                vn0 = self.normalize(v0)
                vn1 = self.normalize(v1)
                vn2 = self.normalize(v2)

            transform_verts.extend(v0 + [vt0[0], vt0[1]] + vn0)
            transform_verts.extend(v1 + [vt1[0], vt1[1]] + vn1)
            transform_verts.extend(v2 + [vt2[0], vt2[1]] + vn2)

            if vert_count == 4:
                v3 = self.vertices[face[3][0] - 1]
                vt3 = self.textcoords[face[3][1] - 1]
                vn3 = self.normals[face[3][2] - 1] if len(self.normals) != 0 else self.normalize(v3)

                transform_verts.extend(v0 + [vt0[0], vt0[1]] + vn0)
                transform_verts.extend(v2 + [vt2[0], vt2[1]] + vn2)
                transform_verts.extend(v3 + [vt3[0], vt3[1]] + vn3)

        return transform_verts
