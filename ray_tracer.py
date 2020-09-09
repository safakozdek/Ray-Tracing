from PIL import Image
import numpy as np

objects = []
epsilon = 1e-3
z_min = 200
z_max = 1000
light_position = [500, 500, 500]
ambient_component = 0.05
ambient_color = [255, 255, 255]
max_depth = 2


class Plane:

    def __init__(self, point, normal, color, k_diffuse, k_reflect):
        self.normal = convert_unit_vector(normal)
        self.point = point
        self.color = color
        self.k_diffuse = k_diffuse
        self.k_reflect = k_reflect

    def getNormal(self, surfacePoint):
        return self.normal


class Sphere:

    def __init__(self, center, radius, color, k_diffuse, k_reflect):
        self.center = center
        self.radius = radius
        self.color = color
        self.k_diffuse = k_diffuse
        self.k_reflect = k_reflect

    def getNormal(self, surfacePoint):
        return np.subtract(surfacePoint, self.center) / self.radius


class Ray:

    def __init__(self, point, dir):
        self.point = point
        self.dir = dir


def take_input():
    print("Taking input from input.txt")
    file = open("input.txt", "r")
    numberOfSpheres = int(file.readline())

    # add spheres as objects
    for i in range(numberOfSpheres):
        color = [int(x) for x in file.readline().split(",")]
        center = [int(x) for x in file.readline().split(",")]
        radius = int(file.readline())
        k_diffuse = float(file.readline())
        k_reflect = float(file.readline())
        sphere = Sphere(center, radius, color, k_diffuse, k_reflect)
        objects.append(sphere)

    numberOfPlanes = int(file.readline())
    # add planes as objects
    for i in range(numberOfPlanes):
        color = [int(x) for x in file.readline().split(",")]
        point = [int(x) for x in file.readline().split(",")]
        normal = [int(x) for x in file.readline().split(",")]
        k_diffuse = float(file.readline())
        k_reflect = float(file.readline())

        plane = Plane(point, normal, color, k_diffuse, k_reflect)
        objects.append(plane)

    print("Input has been successfully taken")



# algebraic_method
def find_intersection_plane(ray, plane):
    normalDotRayDir = np.dot(plane.normal, ray.dir)
    if np.abs(normalDotRayDir) < epsilon:
        return None  # no intersection or in the plane
    t = np.dot(convert_unit_vector(plane.normal), (np.subtract(plane.point, ray.point))) / np.dot(ray.dir, plane.normal)
    return t if t > epsilon else None


def find_intersection_sphere(ray, sphere):
    distance = np.subtract(ray.point, sphere.center)
    a = np.dot(ray.dir, ray.dir)
    b = 2 * np.dot(distance, ray.dir)
    c = np.dot(distance, distance) - sphere.radius ** 2
    delta = b ** 2 - 4 * a * c

    if delta < 0:
        return None, None
    elif delta == 0:
        point = - b / (2 * a)
        return point, None
    else:
        t1 = (-b - np.sqrt(delta)) / (2 * a)
        t2 = (-b + np.sqrt(delta)) / (2 * a)
        return t1, t2  # t2>t1


def is_visible(t_to_check, t_max, ray):
    z_point = ray.point[2] + t_to_check * ray.dir[2]  # index 2 is z value
    return epsilon < t_to_check < t_max and z_min < z_point < z_max


def find_closest_object(ray):
    closest = [99999999, None]  # index 0 = t , index 1 = object

    for object in objects:
        if type(object) is Sphere:
            t1, t2 = find_intersection_sphere(ray, object)

            if t1 is None:
                pass
            elif is_visible(t1, closest[0], ray):
                closest = [t1, object]
            elif is_visible(t2, closest[0], ray):
                closest = [t2, object]

        elif type(object) is Plane:
            t = find_intersection_plane(ray, object)
            if t is None:
                pass
            elif is_visible(t, closest[0], ray):
                closest = [t, object]

    return closest  # return the object and t


def convert_unit_vector(vector):
    magnitude = np.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    return np.divide(vector, magnitude)


def reflect_ray(ray, surface_normal, point):
    new_dir = ray.dir - 2 * (np.dot(ray.dir, surface_normal)) * surface_normal
    new_dir = convert_unit_vector(new_dir)

    return Ray(point + epsilon * surface_normal, new_dir)


def cast_ray(ray, depth):
    # find the closest object
    color = [0, 0, 0]
    intersection = find_closest_object(ray)  # index 0 = t , index 1 = object
    if intersection[1] is not None and depth < max_depth:
        # check if it is under shadow by generating a ray to light source
        intersection_point = ray.point + np.multiply(ray.dir, intersection[0])
        light_dir = np.subtract(light_position, intersection_point)
        unit_light_dir = convert_unit_vector(light_dir)
        light_ray = Ray(intersection_point, unit_light_dir)
        light_intersection = find_closest_object(light_ray)

        light = 1
        if type(light_intersection[1]) is Sphere and light_intersection[1] != intersection[1]:
            light = 0

        ambient_col = np.multiply(ambient_color, ambient_component, np.divide(intersection[1].color, 256))
        unit_normal = convert_unit_vector(intersection[1].getNormal(intersection_point))
        diffuse_col = np.multiply(intersection[1].k_diffuse * max(0, np.dot(unit_light_dir, unit_normal)),
                                  intersection[1].color)

        new_ray = reflect_ray(ray, intersection[1].getNormal(intersection_point), intersection_point)
        color = ambient_col + diffuse_col * light
        color += np.multiply(intersection[1].k_reflect, cast_ray(new_ray, depth + 1)) / (depth + 1)

    return color


def generate_pixel_color(x, y):
    pixel_x = -49.95 + x * 0.1
    pixel_y = (999 - y) * 0.1 - 49.95
    pixel_z = 100

    dir = [pixel_x, pixel_y, pixel_z]
    eye_point = [0, 0, 0]
    depth = 0
    initialRay = Ray(eye_point, dir)
    color = cast_ray(initialRay, depth)

    return color


def generate_image():
    print("Calculating image")
    image = np.zeros((1000, 1000, 3))

    for x in range(1000):
        for y in range(1000):
            color = generate_pixel_color(x, y)

            image[y][x][0] = int(min(color[0], 255))
            image[y][x][1] = int(min(color[1], 255))
            image[y][x][2] = int(min(color[2], 255))

    print("Image calculation is done.")

    return image


def print_image(image):
    print("Generating Image")
    im = Image.fromarray(image.astype('uint8'))
    im.save('output.png')
    print("Image has been generated successfully")


def main():
    take_input()
    image = generate_image()
    print_image(image)


if __name__ == "__main__":
    main()