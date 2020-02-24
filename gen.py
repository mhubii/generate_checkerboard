import cairo
import argparse
import yaml

# checkerboard generator
# best used with https://github.com/sourishg/stereo-calibration

M2INCH = 39.3701

# DIN formats in units of inch
SIZE = {"A0": [33.1, 46.8],
        "A1": [23.4, 33.1],
        "A2": [16.5, 23.4],
        "A3": [11.7, 16.5],
        "A4": [8.3, 11.7]}

if __name__ == "__main__":

    arg = argparse.ArgumentParser()
    arg.add_argument("--format", type=str, default="A4", help="Set checkerboard format, defaults to A4")
    arg.add_argument("--size", type=float, default=5e-2, help="Set checkerboard square size, defaults to 5e-2 m")

    parser = arg.parse_args()

    f = SIZE[parser.format]
    size = parser.size

    # number of points
    px = int(f[1]*72.) # width and height in points
    py = int(f[0]*72.) # 1 point == 1/72 inch, https://pycairo.readthedocs.io/en/latest/reference/surfaces.html#class-pdfsurface-surface

    # number of squares
    nx = f[1]/(size*M2INCH)
    ny = f[0]/(size*M2INCH)

    # scaling factor
    sx = int(px/nx)
    sy = int(py/ny)
    s = min(sx, sy)

    ps = cairo.PSSurface("checkerboard.ps",
                           px, 
                           py
    )

    ctx = cairo.Context(ps)
    ctx.scale(s, s)

    # create white surface
    ctx.rectangle(0, 0, nx*sx, ny*sy)
    ctx.set_source_rgb(1., 1., 1.)
    ctx.fill()

    # fill white surface with black squares
    for x in range(int(nx+1)):
        for y in range(int(ny+1)):
            if x % 2 == 0 and y % 2 == 0 or x % 2 == 1 and y % 2 == 1:
                ctx.rectangle(x, y, 1, 1)
                ctx.set_source_rgb(0., 0., 0.)
                ctx.fill()

    ps.show_page()

    # safe parameters
    dict_file = {'w': int(nx), 'h': int(ny), 's': size}
    with open(r'param.yaml', 'w') as file:
        yaml.dump(dict_file, file)
