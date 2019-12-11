import numpy as np
np.set_printoptions(precision=3)
from commonfunctions import *
import cv2

def normalize(Array):
    Array = np.copy(Array)
    Sum = (Array**2).sum()
    Divisor = math.sqrt(Sum.sum())
    if Divisor != 0:
        Array /= Divisor
    return Array

def getHOG(Img, BlockSize=(8,8), CellSize=(8,8), NumBins=9):
    BlockSize = ( int(BlockSize[0]) , int(BlockSize[1]) )
    CellSize = ( int(CellSize[0]) , int(CellSize[1]) )
    NumBins = int( NumBins )

    ImgShape = Img.shape
    NumCellsX = int( (Img.shape[0] / CellSize[0]) )
    NumCellsY = int( (Img.shape[1] / CellSize[1]) )
    NumCells = int( NumCellsX * NumCellsY )
    NumBlocksX = int( (Img.shape[0] - BlockSize[0] + CellSize[0]) / CellSize[0] )
    NumBlocksY = int( (Img.shape[1] - BlockSize[1] + CellSize[1]) / CellSize[1] )
    NumBlocks = ( NumBlocksX * NumBlocksY )
    NumCellsInBlockX = int( BlockSize[0] / CellSize[0] )
    NumCellsInBlockY = int( BlockSize[1] / CellSize[1] )
    NumCellsInBlock = NumCellsInBlockX * NumCellsInBlockY
    OrientationStep = 180 / NumBins;
    Gradient = np.ones(ImgShape)
    GradientOrientation = np.ones(ImgShape)

    # Compute Gradients and GradientOrientation
    Img = np.int64(Img)
    Gx = np.zeros(ImgShape)
    Gy = np.zeros(ImgShape)
    Gx[:, 1:-1] = Img[:, 2:] - Img[:, :-2]
    Gy[1:-1, :] = Img[2:, :] - Img[:-2, :]
    Gradient = np.sqrt(Gx**2 + Gy**2)
    GradientOrientation = ( ( ( np.arctan2(Gy, Gx) ) / math.pi ) * 180 ) % 180
    
    # Compute Bins For Every Pixel
    Bin = [ np.floor(( (GradientOrientation[:,:] + OrientationStep/2) / OrientationStep ) - 1) % NumBins,
                      np.floor( (GradientOrientation[:,:] + OrientationStep/2) / OrientationStep ) % NumBins]
    Bin = np.int16(Bin)

    # Compute Ratios For Every Pixel
    Ratio = [ ( 1 - ( ( (GradientOrientation[:, :] + OrientationStep/2) / OrientationStep ) - ( (GradientOrientation[:, :] + OrientationStep/2) // OrientationStep ) ) ),
             ( ( (GradientOrientation[:, :] + OrientationStep/2) / OrientationStep ) - ( (GradientOrientation[:, :] + OrientationStep/2) // OrientationStep ) )]
    Ratio = np.array(Ratio).astype(float)

    # Compute All Bins For Every Pixel
    HOGPX = np.zeros((Img.shape[0],Img.shape[1],9))
    for bin in range(NumBins):
        HOGPX[:,:,bin] += np.where(np.array(Bin[0]) == bin,np.array(Ratio[0]),0)
        HOGPX[:,:,bin] += np.where(np.array(Bin[1]) == bin,np.array(Ratio[1]),0)
    Gradient = np.repeat(Gradient[:,:],NumBins).reshape((Img.shape[0],Img.shape[1],NumBins))
    HOGPX = HOGPX * Gradient
    
    # Compute HOG For Cells
    HOGCells = np.zeros((NumCellsX, NumCellsY,9))
    for x in range(NumCellsX):
        for y in range(NumCellsY):
            HOGCells[x,y] = np.sum(np.sum(HOGPX[  x*CellSize[0]:(x+1)*CellSize[0], y*CellSize[1]:(y+1)*CellSize[1]], axis=0),axis=0)
            
    ## Normalization
    HOGVector = []
    Counter = 0
    for x in range(NumBlocksX):
        for y in range(NumBlocksY):
            HOGVector.extend(list(np.concatenate( 
                normalize( HOGCells[x : x+NumCellsInBlockX, y : y+NumCellsInBlockY] )
                ).ravel()))
            Counter += 1
            
    return Gradient, GradientOrientation, HOGVector

# img = cv2.imread('test.png', 0)
# img = cv2.resize(img, (50,50))
# Gradient, GradientOrientation, HOGVector = getHOG(img, (16,16))
# print(len(HOGVector))
# print(HOGVector)

#img = cv2.imread('C:/Users/samir/source/repos/PythonApplication1/PythonApplication1/Datasets/Images/AF0305_1100_00F.jpg',0)
#img = cv2.resize(img, (250,250))
#Gradient, GradientOrientation, HOGVector = getHOG(img, (16,16))
#print(len(HOGVector))
#print(HOGVector)