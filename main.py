import math
import os

import matplotlib.cm
import matplotlib.colors
import matplotlib.pyplot


def gamma_to_linear(value, gamma=2.2):
    # type: (float, float) -> flost
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
    if not os.path.exists("lut"):
        os.makedirs("lut")

    for colormap in (matplotlib.cm.get_cmap(cmap_name) for cmap_name in ["jet", "plasma", "viridis"]):
        with open(os.path.join("lut", "{}.cube".format(colormap.name)), "w") as lut_file:
            lut_file.write("\n".join(cmap_to_cube(colormap)))


if __name__ == "__main__":
    main()
