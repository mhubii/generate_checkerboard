import cairo
import argparse
import yaml

M2INCH = 39.3701

# checkerboard generator
# best used with https://github.com/sourishg/stereo-calibration

# DIN formats in units of m
SIZE = {"A0": [0.841, 1.189],
        "A1": [0.594, 0.841],
        "A2": [0.420, 0.594],
        "A3": [0.297, 0.420],
        "A4": [0.210, 0.297]}

if __name__ == "__main__":

    arg = argparse.ArgumentParser()
    arg.add_argument("--format", type=str, default="A4", help="Set checkerboard format, defaults to A4")
    arg.add_argument("--size", type=float, default=5e-2, help="Set checkerboard square size, defaults to 5e-2 m")

    parser = arg.parse_args()

    f = SIZE[parser.format]
    size = parser.size

    # number of points
    px = int(f[1]*M2INCH*72.) # width and height in points
    py = int(f[0]*M2INCH*72.) # 1 point == 1/72 inch, https://pycairo.readthedocs.io/en/latest/reference/surfaces.html#class-pdfsurface-surface

    # number of squares
    nx = f[1]/size
    ny = f[0]/size

    # scaling factor
    sx = int(px/nx)
    sy = int(py/ny)
    s = min(sx, sy)

    svg = cairo.SVGSurface("checkerboard.svg",
                           px,
                           py
    )
    pdf = cairo.PDFSurface("checkerboard.pdf",
                           px, 
                           py
    )

    for surface in [svg, pdf]:
        ctx = cairo.Context(surface)
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

        surface.show_page()

    # safe parameters
    dict_file = {'w': int(nx), 'h': int(ny), 's': size}
    with open(r'param.yaml', 'w') as file:
        yaml.dump(dict_file, file)
