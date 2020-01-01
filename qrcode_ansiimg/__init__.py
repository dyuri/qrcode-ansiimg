from qrcode.image.base import BaseImage


class AImg:
    def __init__(self, border, width, box_size, fgcolor=None, bgcolor=None):
        self.border = border
        self.width = width
        self.half = box_size < 2

        if fgcolor is None:
            self.fgcolor = 0
        else:
            self.fgcolor = fgcolor

        if bgcolor is None:
            self.bgcolor = 15
        else:
            self.bgcolor = bgcolor

        self._img = []
        for _ in range(self.width):
            line = []
            for _ in range(self.width):
                line.append(0)
            self._img.append(line)

    def draw(self, row, col):
        self._img[row][col] = 1

    def _empty(self):
        return f"\x1b[48;5;{self.fgcolor}m  \x1b[0m"

    def _full(self):
        return f"\x1b[48;5;{self.bgcolor}m  \x1b[0m"

    def write(self, target=None):
        # TODO half

        buf = []

        # top border
        for _ in range(self.border):
            for _ in range(self.border * 2 + self.width):
                buf.append(self._full())
            buf.append("\n")

        # content
        for l in self._img:
            # left border
            for _ in range(self.border):
                buf.append(self._full())

            for v in l:
                buf.append(self._empty() if v else self._full())

            # right border
            for _ in range(self.border):
                buf.append(self._full())

            buf.append("\n")

        # bottom border
        for _ in range(self.border):
            for _ in range(self.border * 2 + self.width):
                buf.append(self._full())
            buf.append("\n")

        if target is None:
            print(''.join(buf))
        elif isinstance(target, str):
            with open(target, 'w') as f:
                f.write(''.join(buf))
        elif hasattr(target, 'write'):
            target.write(''.join(buf).encode())


class AnsiImage(BaseImage):
    """ANSI image output
    """

    def new_image(self, **kwargs):
        fgcolor = kwargs.get("fill_color", None)
        bgcolor = kwargs.get("back_color", None)
        return AImg(self.border, self.width, self.box_size, fgcolor, bgcolor)

    def drawrect(self, row, col):
        self._img.draw(row, col)

    def save(self, stream, kind=None):
        self._img.write(stream)
