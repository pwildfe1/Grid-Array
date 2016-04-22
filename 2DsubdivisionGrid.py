import rhinoscriptsyntax as rs
import random as r
import math as m

class tile:
    def __init__(self,VERTICIES):
        self.vert = VERTICIES
        self.x = rs.VectorCreate(self.vert[1],self.vert[0])
        self.y = rs.VectorCreate(self.vert[3],self.vert[0])
    def gen(self):
        pts = []
        pts.extend(self.vert)
        pts.append(self.vert[0])
        profile = rs.AddCurve(pts,1)
        return profile
    def subDiv(self):
        profile = self.gen()
        divTiles = []
        startPtX = rs.PointAdd(self.vert[0],self.x/2)
        startPtY = rs.PointAdd(self.vert[0],self.y/2)
        endPtX = rs.PointAdd(self.vert[2],-self.x/2)
        endPtY = rs.PointAdd(self.vert[2],-self.y/2)
        cnt = self.cntPt()
        divTiles.append(tile([self.vert[0],startPtX,cnt,startPtY]))
        divTiles.append(tile([startPtX,self.vert[1],endPtY,cnt]))
        divTiles.append(tile([cnt,endPtY,self.vert[2],endPtX]))
        divTiles.append(tile([startPtY,cnt,endPtX,self.vert[3]]))
        for i in range(len(divTiles)):
            divTiles[i].gen()
        return divTiles
    def perforate(self,factor):
        profile = self.gen()
        if factor>0:
            newPts = []
            cnt = self.cntPt()
            if factor<1:
                for i in range(len(self.vert)):
                    vec = rs.VectorCreate(cnt,self.vert[i])
                    newPts.append(rs.PointAdd(self.vert[i],factor*vec))
            perforatedCell = tile(newPts)
            return perforatedCell.gen()
        else:
            return profile
    def cntPt(self):
        sum = [0,0,0]
        for i in range(len(self.vert)):
            sum=rs.PointAdd(self.vert[i],sum)
        cntPt = sum/len(self.vert)
        return cntPt

def SortCurvesByPt(curves,pt):
    indexes = []
    distances = []
    sorted = []
    min = 1000000000
    for i in range(len(curves)):
        param = rs.CurveClosestPoint(curves[i],pt)
        crvPt = rs.EvaluateCurve(curves[i],param)
        distances.append(rs.Distance(crvPt,pt))
    for i in range(len(curves)):
        for j in range(len(distances)):
            if distances[j]<min:
                min = distances[j]
                index = j
        indexes.append(index)
        sorted.append(curves[index])
        distances[index] = 1000000000
        min = 1000000000
    return sorted


def collectIntersections(set,cuts):
    intersectPts = []
    for i in range(len(cuts)):
        intersect = rs.CurveCurveIntersection(set,cuts[i])
        if intersect!=None:
            intersectPts.append(intersect[0][1])
    return intersectPts

def createTiles(sets,cuts,attPts,perfPts,strength):
    pts = []
    myTiles = []
    profiles = []
    for i in range(len(sets)):
        pts.append(collectIntersections(sets[i],cuts))
    for i in range(len(pts)-1):
        if len(pts[i])<len(pts[i+1]):
            min = len(pts[i])
        else:
            min = len(pts[i+1])
        for j in range(min-1):
            myTiles.append(tile([pts[i][j],pts[i+1][j],pts[i+1][j+1],pts[i][j+1]]))
    for i in range(len(myTiles)):
        cntPt = myTiles[i].cntPt()
        sum = 0
        sumP = 0
        for j in range(len(attPts)):
            sum = sum + rs.Distance(cntPt,attPts[j])
        for j in range(len(perfPts)):
            sumP = sumP + rs.Distance(cntPt,perfPts[j])
        valSub = sum/len(attPts)/strength
        valPerf = sumP/len(perfPts)/strength
        if valPerf>.8:
            valPerf = 0
        factor = r.random()
        if valSub<factor: 
            smallTiles = myTiles[i].subDiv()
            if valSub<factor/2:
                for k in range(len(smallTiles)):
                    smallerTiles = smallTiles[k].subDiv()
                if valSub<factor/3:
                    for n in range(len(smallerTiles)):
                        smallestTiles = smallerTiles[n].subDiv()
                        #smallestTiles[n].perforate(valPerf)
                else:
                    for k in range(len(smallerTiles)):
                        smallerTiles[k].perforate(valPerf)
            else:
                for k in range(len(smallTiles)):
                    smallTiles[k].perforate(valPerf)
        else:
            profiles.append(myTiles[i].perforate(valPerf))
    return profiles

def Main():
    crvs = rs.GetObjects("please select grid curves",rs.filter.curve)
    refPt = rs.GetObject("please select reference pt",rs.filter.point)
    attPts = rs.GetObjects("please select attPts",rs.filter.point)
    perfPts = rs.GetObjects("please select perforationPts",rs.filter.point)
    strength = rs.GetReal("please enter attPt range",300)
    crvX = []
    crvY = []
    vecX = rs.VectorCreate(rs.CurveEndPoint(crvs[0]),rs.CurveStartPoint(crvs[0]))
    for i in range(len(crvs)):
        vec = rs.VectorCreate(rs.CurveEndPoint(crvs[i]),rs.CurveStartPoint(crvs[i]))
        if rs.VectorAngle(vec,vecX)<1:
            crvX.append(crvs[i])
        else:
            crvY.append(crvs[i])
    crvX = SortCurvesByPt(crvX,refPt)
    crvY = SortCurvesByPt(crvY,refPt)
    createTiles(crvX,crvY,attPts,perfPts,strength)
    rs.DeleteObjects(crvX)
    rs.DeleteObjects(crvY)

Main()