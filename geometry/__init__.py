import random


def square_grid_diagonal(dimension):
    distance = 10
    coordinates = []
    offset = (dimension / 2 - 0.5) * distance
    for x in range(dimension):
        coordinates.append(((x * distance) + -offset, (x * distance) + -offset, 0))
        for y in range(1, x+1):
            coordinates.append(((x * distance) + -offset, (x * distance) + -offset + -(y * distance), 0))
        for y in range(x):
            coordinates.append(((x - y) * distance - distance + -offset, (x * distance) + -offset, 0))
    return coordinates


def square_grid_zigzag(dimension, resolution, space):
    coords = []
    distance = 10 / resolution * space
    offset = (dimension / 2 - (0.5 / resolution)) * distance * resolution
    for x in range(dimension * resolution):
        for j in range(dimension * resolution):
            # coords.append((j * distance - offset, x * distance - offset, random.randrange(0, 0)))
            coords.append((j * distance - offset, x * distance - offset, 0))
    return coords


def poi_from_coords_zigzag(coords, dimension, resolution):
    _coords = []
    size = dimension * resolution
    for x in range(dimension * resolution):
        for j in range(dimension * resolution):
            if x == 0:
                prev = coords[x + j]
                _coords.append((
                    prev[0] - ((prev[0] - coords[x + j + 1][0]) / 2),
                    prev[1] - ((prev[1] - coords[x + j + size + 1][1]) / 2),
                    .5
                ))
            else:
                prev = coords[x * (dimension+1) + j]
                _coords.append((
                    prev[0] - ((prev[0] - coords[x * (dimension+1) + j + 1][0]) / 2),
                    prev[1] - ((prev[1] - coords[x * (dimension+1) + j + size + 1][1]) / 2),
                    .5
                ))
    return _coords


def edges_grid_diagonal(dimension):
    distance = 10
    edges = []
    odd_nums = get_odd_numbers([x for x in range(dimension * dimension)])
    for x in range(dimension - 1):
        if x == 0:
            edges.append((x, x + 1))
            edges.append((x + 1, x + 2))
            edges.append((x + 2, x))
            edges.append((x + 1, x + 3))
            edges.append((x + 3, x))
        else:
            edges.append((x * x, x * x + odd_nums[x]))
            current = x * x + odd_nums[x]
            for y in range(x + 1):
                edges.append((current + y, current + y + 1))
                edges.append((current + y + 1, x * x + y))
                if y < x:
                    edges.append((current + y + 1, x * x + y + 1))
            for y in range(x + 1):
                if y == 0:
                    edges.append((current, current + x + 2))
                    edges.append((current + x + 2, x * x))
                    # print((current + x + 2, x * x + x + 1))
                    # print((current, current + x + 2))
                else:
                    edges.append((current + x + y + 1, current + x + y + 2))
                # else:
                #     edges.append((current + y, current + y + 1))
                # if y < x:
                #     edges.append((current + y + 1, x * x + y + 1))
    return edges


def edges_grid_zigzag(dimension, resolution):
    edges = []
    dimension = dimension * resolution
    for y in range(dimension):
        mod = y * dimension
        if y == 0:
            for x in range(dimension):
                if x < dimension-1:
                    edges.append((x, x + 1))
                    edges.append((x, x + dimension))
                    edges.append((x, x + dimension + 1))
                else:
                    edges.append((x, x + dimension))
        elif y < dimension-1:
            for x in range(dimension):
                t = x + mod
                if x < dimension-1:
                    edges.append((t, t + 1))
                    edges.append((t, t + dimension))
                    edges.append((t, t + dimension + 1))
                else:
                    edges.append((t, t + dimension))
        else:
            for x in range(0, dimension-1):
                t = x + mod
                edges.append((t, t + 1))
    return edges


def faces_grid_zigzag(dimension, resolution):
    faces = []
    dimension = dimension * resolution
    for y in range(dimension):
        mod = y * dimension
        if y == 0:
            for x in range(dimension):
                if x < dimension - 1:
                    faces.append((x, x + 1, x + dimension + 1))
                    faces.append((x, x + dimension + 1, x + dimension))
        elif y < dimension-1:
            for x in range(dimension):
                if x < dimension - 1:
                    faces.append((x + mod, x + mod + 1, x + mod + dimension + 1))
                    faces.append((x + mod, x + mod + dimension + 1, x + mod + dimension))
    return faces


def get_odd_numbers(numbers):
    odd_numbers = []
    for number in numbers:
        if number % 2 == 1:
            odd_numbers.append(number)

    return odd_numbers


def get_even_numbers(numbers):
    odd_numbers = []
    for number in numbers:
        if number % 2 == 0:
            odd_numbers.append(number)

    return odd_numbers
