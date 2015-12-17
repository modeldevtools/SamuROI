from .polyroi import PolygonRoi
from .segmentroi import SegmentRoi

from dumb.util import bicycle

class BranchRoi(PolygonRoi):
    """
        Extend the PolygonRoi with children, splitting and segment selection.
    """

    @PolygonRoi.active.setter
    def active(self,active):
        """
        Extend the polyroi _set_active property, to also deactivate contained segments.
        """
        if active == False:
            self.active_segment = None
        else:
            self.next_segment()
        # call the baseclass property setter
        PolygonRoi.active.fset(self,active)

    def __init__(self, data, axes, **kwargs):
        super(BranchRoi,self).__init__(data, axes = axes, **kwargs)
        self.children = []
        self.__active_segment = None
        self.__children_cycle = bicycle(self.children)

    def next_segment(self):
        if len(self.children) > 0:
            self.active_segment = self.__children_cycle.next()

    def previous_segment(self):
        if len(self.children) > 0:
            self.active_segment = self.__children_cycle.prev()

    @property
    def active_segment(self):
        return self.__active_segment

    @active_segment.setter
    def active_segment(self,s):
        # hide artists of previous branch
        if self.active_segment is not None:
            self.active_segment.active = False

        self.__active_segment = s
        if s is not None:
            self.active_segment.active = True

    def split(self, length):
        """Only supported if self is a root item."""
        for child in self.children:
            child.artist.remove()

        # split branch and ist insert childrens
        # do list insertion because this will keep the children_cycle updated
        self.children[:] = [SegmentRoi(child.data,
                                parent = self,
                                axes = self.axes)
                            for child in super(BranchRoi, self).split(length = length)]
        if self.active:
            self.active_segment = self.children[0]
