#!/usr/bin/env python
import argparse
import math
import os

import matplotlib.cm
import matplotlib.colors
import matplotlib.pyplot


def gamma_to_linear(value, gamma=2.2):
    # type: (float, float) -> float
    return math.pow(value, gamma)


def cmap_to_cube(colormap):
    # type: (matplotlib.colors.Colormap) -> list[str]

    result = [
        'TITLE "{}"'.format(colormap.name),
        "LUT_1D_SIZE {}".format(colormap.N),
    ]

    result.extend(
        [
            "{:.5f} {:.5f} {:.5f}".format(
                *[gamma_to_linear(x) for x in colormap(sample)]
            )
            for sample in range(colormap.N)
        ]
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    maps_group = group.add_mutually_exclusive_group()
    maps_group.add_argument("--colormap", nargs="+")
    maps_group.add_argument("--all", action="store_true")
    group.add_argument("--list", action="store_true")
    parser.add_argument("--output-dir", default=os.curdir)

    args = parser.parse_args()

    if args.list:
        print("\n".join(matplotlib.pyplot.colormaps()))
        return

    if args.all:
        cmap_names = matplotlib.pyplot.colormaps()
    else:
        cmap_names = args.colormap

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for colormap in (matplotlib.cm.get_cmap(cmap_name) for cmap_name in cmap_names):
        with open(
            os.path.join(args.output_dir, "{}.cube".format(colormap.name)), "w"
        ) as lut_file:
            print("Writing {} ...".format(lut_file.name))
            lut_file.write("\n".join(cmap_to_cube(colormap)))


if __name__ == "__main__":
    main()
