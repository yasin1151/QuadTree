# -*- coding:utf-8 -*-
# author : Pengyao
# time   : 2018/7/28


class CQuadEnum():
    """
    节点的类型枚举
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


class Rectangle(object):
    """
        用于记录rect位置变化
    """
    def __init__(self, tRect):
        # 记录移动前处于那一个节点
        self.m_iLastIndex = -1
        # 记录移动后处于哪一个节点
        self.m_iNowIndex = -1

        # 父节点
        self.m_ParentNode = None

        self.m_tRect = tRect

    def GetRect(self):
        """
            获取矩形区域
        """
        return self.m_tRect

class CQuadTreeNode(object):
    def __init__(self, nDepth, rect):
        # 节点的矩形区域
        self.m_tRect = rect
        # 节点对象的数组
        self.m_ObjLst = []
        # 子节点数量
        self.m_nChildCount = 0
        # 子节点数组
        self.m_ChildLst = [None, None, None, None]
        # 深度
        self.m_nDepth = nDepth
    
    def SetDepth(self, nDepth):
        """
            设置深度
        """
        self.m_nDepth = nDepth

    def GetDepth(self):
        """
            获取深度
        """
        return self.m_nDepth

    def SetRect(self, rect):
        """
            设置矩形区域
        """
        self.m_tRect = rect

    def GetRect(self):
        """
            返回节点的矩形区域
        """
        return self.m_tRect

    def GetObjLst(self):
        """
            返回节点的对象数组
        """
        return self.m_ObjLst

    def GetObjNum(self):
        """
            返回当前节点保存的对象的数量
        """
        return len(self.m_ObjLst)

    def SetChildNum(self, nNum):
        """
            设置子节点数量
        """
        self.m_nChildCount = nNum

    def GetChildNum(self):
        """
            返回子节点的数目
        """
        return self.m_nChildCount

    def GetAllChild(self):
        """
            返回所有子节点的数组
        """
        return self.m_ChildLst

    def Insert(self, obj):
        """
            插入节点
        """
        self.m_ObjLst.append(obj)

    def Remove(self, obj):
        """
            移除节点
        """
        self.m_ObjLst.remove(obj)

    def ClearObjLst(self):
        """
            清理对象数组
        """
        self.m_ObjLst = []


class CQuadTree(object):
    """
        只保存抽象的区域
        与实体无关
    """
    def __init__(self, nMaxObjNum, nMaxDepth, rect):
        self.m_nDepth = nMaxDepth
        self.m_nMaxObjs = nMaxObjNum
        self.m_RootNode = CQuadTreeNode(0, rect)
    

    # ====================外部接口=====================

    def GetTreeRoot(self):
        """
            获取根节点
        """
        return self.m_RootNode

    def SetMaxDepth(self, nMaxDepth):
        """
            设置节点创建的最大深度
        """
        self.m_nDepth = nMaxDepth

    def GeMaxtDepth(self):
        """
            获取节点创建的最大深度
        """
        return self.m_nDepth

    def SetNOdeMaxObjects(self, nMaxNum):
        """
            设置单个节点最大的对象数目
        """
        self.m_nMaxObjs = nMaxNum

    def GetNodeMaxObjects(self):
        """
            获取单个节点最大的对象数目
        """
        return self.m_nMaxObjs

    def Insert(self, tRect):
        """
            插入节点
        """
        self._Insert(tRect, self.m_RootNode)

    def Remove(self, tRect):
        """
            删除节点
        """
        self._Remove(tRect, self.m_RootNode)

    def Print(self):
        """
            输出内部结构
        """
        self._PrintAllNode(self.m_RootNode)

    def GetRectAllNode(self, tRect):
        """
            获取区域内的全部节点
        """
        retLst = []
        self._Search(tRect, self.m_RootNode, retLst)
        return retLst

    def AdjustNode(self, tRect):
        pass
    # ===========================内部接口=========================

    def _Split(self, oQuadTreeNode):
        """
            划分节点的四个区域
        """
        if oQuadTreeNode is None:
            return

        posX, posY, width, height = oQuadTreeNode.GetRect()
        newWidth = width / 2
        newHeight = height / 2

        newNodeUR = CQuadTreeNode(oQuadTreeNode.GetDepth() + 1, (posX + newWidth, posY + newHeight, newWidth, newHeight))
        newNodeUL = CQuadTreeNode(oQuadTreeNode.GetDepth() + 1, (posX, posY + newHeight, newWidth, newHeight))
        newNodeDL = CQuadTreeNode(oQuadTreeNode.GetDepth() + 1, (posX, posY, newWidth, newHeight))
        newNodeDR = CQuadTreeNode(oQuadTreeNode.GetDepth() + 1, (posX + newWidth, posY + newHeight, newWidth, newHeight))

        childLst = oQuadTreeNode.GetAllChild()
        childLst[0] = newNodeUR
        childLst[1] = newNodeUL
        childLst[2] = newNodeDL
        childLst[3] = newNodeDR

        oQuadTreeNode.SetChildNum(4)

    def _Insert(self, rect, oQuadTreeNode):
        """
            插入节点到四叉树中
        """
        
        if oQuadTreeNode is None:
            return

        if oQuadTreeNode.GetChildNum() > 0:
            # 如果有子节点
            nIndex = self._GetIndex(rect, oQuadTreeNode)
            if CQuadEnum.UR <= nIndex <= CQuadEnum.DR:
                # 如果被子节点包含
                self._Insert(rect, oQuadTreeNode.GetAllChild()[nIndex])
        else:
            # 如果是叶子节点, 但是最大对象数量超过限制
            if oQuadTreeNode.GetObjNum() >= self.m_nMaxObjs and oQuadTreeNode.GetDepth() < self.m_nDepth:
                self._Split(oQuadTreeNode)
                for each in oQuadTreeNode.GetObjLst():
                    self._Insert(each, oQuadTreeNode)

                oQuadTreeNode.ClearObjLst()
                self._Insert(rect, oQuadTreeNode)
            else:
                # 最大数量未超过限制
                oQuadTreeNode.Insert(rect)    

    def _Remove(self, tRect, oQuadTreeNode):
        if oQuadTreeNode is None:
            return

        if oQuadTreeNode.GetChildNum() == 0 and oQuadTreeNode.GetObjNum() > 0:
            objLst = oQuadTreeNode.GetObjLst()
            for each in objLst[:]:
                if tRect == each:
                    # Remove
                    objLst.remove(each)
            return

        nIndex = self._GetIndex(tRect, oQuadTreeNode)
        childLst = oQuadTreeNode.GetAllChild()
        if CQuadEnum.UR <= nIndex <= CQuadEnum.DR:
            if childLst[nIndex] != None:
                self._Remove(tRect, childLst[nIndex])
            return

    def _GetIndex(self, rect, oQuadTreeNode):
        """
            获取Rect在oQuadTreeNode中的象限
            如果与两个以上相交，会存储在父节点
        """
        posX, posY, width, height = oQuadTreeNode.GetRect()
        subWidth = width / 2
        subHeight = height / 2

        rX, rY, rW, rH = rect

        # UR 0
        if posX + subWidth <= rX < posX + width and \
            posY + subHeight <= rY < posY + height:
            return CQuadEnum.UR
        # UL 1
        elif posX <= rX < posX + subWidth and \
            posY + subHeight <= rY < posY + height:
            return CQuadEnum.UL
        # DL 2
        elif posX <= rX < posX + subWidth and \
            posY <= rY < posY + subHeight:
            return CQuadEnum.DL
        # DR 3
        elif posX + subWidth <= rX < posX + width and \
            posY <= rY < posY + subHeight:
            return CQuadEnum.DR
        else:
            return CQuadEnum.INVALID

    def _PrintAllNode(self, oQuadTreeNode):
        """
            输出所有叶子节点的信息
        """
        if oQuadTreeNode is None:
            return
        print " " * oQuadTreeNode.GetDepth() * 2, "Node Rect:[ %s ], Depth : %s, ObjNum : %s" % (oQuadTreeNode.GetRect(), oQuadTreeNode.GetDepth(), oQuadTreeNode.GetObjNum())
        if oQuadTreeNode.GetChildNum() == 0:
            if oQuadTreeNode.GetObjNum() > 0:
                print " " * oQuadTreeNode.GetDepth() * 2, "{"
                for each in oQuadTreeNode.GetObjLst():
                    print " " * oQuadTreeNode.GetDepth() * 3, "[ %s ]" % str(each)
                print " " * oQuadTreeNode.GetDepth() * 2, "}"
        else:
            print " " * oQuadTreeNode.GetDepth() * 2, "{"            
            for each in oQuadTreeNode.GetAllChild():
                self._PrintAllNode(each)
            print " " * oQuadTreeNode.GetDepth() * 2, "}"

    def _Search(self, tRect, oQuadTreeNode, retLst):
        if oQuadTreeNode is None:
            return

        if oQuadTreeNode.GetChildNum() == 0:
            if oQuadTreeNode.GetObjNum() > 0:
                retLst += oQuadTreeNode.GetObjLst()
            return

        nIndex = self._GetIndex(tRect, oQuadTreeNode)
        childLst = oQuadTreeNode.GetAllChild()
        if CQuadEnum.UR <= nIndex <= CQuadEnum.DR:
            if childLst[nIndex] != None:
                self._Search(tRect, childLst[nIndex], retLst)
            return
            
        for i in xrange(0, 4):
            if nIndex != i and childLst[i] != None:
                self._Search(tRect, childLst[i], retLst)


if __name__ == '__main__':
    import random
    rectLst = []
    for i in xrange(0, 10):
        randX = random.randint(0, 500)
        randY = random.randint(0, 500)
        randW = random.randint(0, 100)
        randH = random.randint(0, 100)
        rectLst.append((randX, randY, randX +randW, randY + randH))

    oQuadTree = CQuadTree(5, 5, (0, 0, 1000, 1000))
    for each in rectLst:
        print "NodeRect :", each
        oQuadTree.Insert(each)

    lst = oQuadTree.GetRectAllNode((300, 300, 300, 300))
    for each in lst:
        print "Area Node :", each
        oQuadTree.Remove(each)
    

    lst = oQuadTree.GetRectAllNode((300, 300, 300, 300))
    for each in lst:
        print "Remove Node :", each
    
