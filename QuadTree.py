# coding : utf-8



class CQuadEnum():
    """
            ┊
      UL(1) ┊  UR(0)
       -------------
      DL(2) ┊  DR(3)
            ┊
    """
    INVALID = -1
    UR = 0
    UL = 1
    DL = 2
    DR = 3

class CQuadTree(object):
    def __init__(self):
        self.m_nDepth = 0
        self.m_nMaxObjs = 0
        self.m_RootNode = None

    def InitQuadTree(self, nDepth, nMaxObjs):
        pass

    def InitQuadTreeNode(self, rect):
        pass

    def CreateQuadTreeNode(self, nDepth, rect, oQuadTreeNode):
        pass
    
    def Split(self, oQuadTreeNode):
        pass

    def Insert(self, rect, oQuadTreeNode):
        pass

    def GetIndex(self, rect, oQuadTreenNode):
        pass

    def Remove(self, rect, oQuadTreenNode):
        pass
    
    def Find(self, rect, oBeganNode, oEndNode):
        pass

    def PrintAllNode(self, oQuadTreenNode):
        pass

    def Search(self):
        pass

    def GetTreeRoot(self):
        return self.m_RootNode

    def GetDepth(self):
        return self.m_nDepth

    def GetMaxObjects(self):
        return self.m_nMaxObjs


class CQuadTreeNode(object):
    def __init__(self, rect):
        pass


if __name__ == '__main__':
    pass