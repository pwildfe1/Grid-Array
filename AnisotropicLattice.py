import rhinoscriptsyntax as rs
import math as m

def Main():
    cell = rs.GetObjects("please select polylines of cell",rs.filter.curve)
    attPt = rs.GetObject("please select attraction point",rs.filter.point)
    newCells = []
    cnts = []
    box = rs.BoundingBox(cell)
    cnt = rs.SurfaceAreaCentroid(box)[0]
    Z = rs.Distance(box[4],box[0])
    Y = rs.Distance(box[0],box[1])
    X = rs.Distance(box[0],box[3])
    vecXYZ = rs.VectorCreate(box[4],cnt)
    for i in range(len(10)):
        for j in range(len(10)):
            for k in range(len(10)):
                newCell01 = rs.CopyObjects(cell,[X*i,Y*j,Z*k])
                cnt01 = rs.PointAdd(cnt,[X*i,Y*j,Z*k])
                newCell02 = rs.CopyObjects(newCell01,vecXYZ)
                cnt02 = rs.PointAdd(cnt01,vecXYZ)
                newCells.append(newCell01)
                cnts.extend([cnt01,cnt02])
                newCells.append(newCell02)
    for i in range(len(newCells)):
        

Main()