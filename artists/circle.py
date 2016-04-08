import itertools

from matplotlib.patches import Circle

from .artist import MaskArtist


class CircleArtist(MaskArtist, Circle):
    """
    Fake a circle shaped roi by creating a n-faced circle like polygon.
    """
    # use thin lines for inactive artists, and thick lines for active ones.
    thin = 1
    thick = 5

    colors = {'red', 'green', 'blue', 'cyan', 'purple'}
    colorcycle = itertools.cycle(colors)

    # @Artist.active.setter
    # def active(self, a):
    #     """ Extend the roi setter to also change linewidth of active artist."""
    #     if a is True:
    #         self.circle.set_linewidth(self.thick)
    #         self.circle.set_edgecolor(self.color)
    #     else:
    #         self.circle.set_linewidth(self.thin)
    #         self.circle.set_edgecolor('gray')
    #     Artist.active.fset(self, a)

    @MaskArtist.selected.setter
    def selected(self, a):
        """ Extend the roi setter to also change linewidth of active artist."""
        if a is True:
            self.set_linewidth(self.thick)
            self.set_edgecolor(self.color)
        else:
            self.set_linewidth(self.thin)
            self.set_edgecolor('gray')

    @property
    def color(self):
        return self.__color

    def __init__(self, mask):
        MaskArtist.__init__(self, mask)
        Circle.__init__(self,
                        mask.center,
                        mask.radius,
                        fill=False,
                        picker=True,
                        lw=self.thin,
                        color='gray')
        # self.circle.roi = self

        self.__color = CircleArtist.colorcycle.next()

        # parent.aximage.add_artist(self.circle)
