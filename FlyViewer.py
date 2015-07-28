#!/usr/bin/python3
# coding:utf-8

import sys,os
from PyQt5 import QtWidgets,QtGui

homePath='/mnt/Shmopbox'

pixdir=homePath+'/Science/Thesis/Abdominal Pigmentation/'
VERSION='0.0'

def main():    
    app=QtWidgets.QApplication(sys.argv)
    screen=Form(pixdir)
    screen.show()

    sys.exit(app.exec_())

class PicPanel(QtWidgets.QWidget):
    def __init__(self,pix=None,pixdir='',parent=None):
        super().__init__(parent)
        self.cursel=[0,0,0]
        self.pix=self._populatepix(pixdir) if pix==None else pix
        self._initLayout()

    def _populatepix(self):
        pix={}
        for f0 in os.listdir(pixdir):
            f0d=os.path.join(pixdir,f0)
            pix[f0]={}
            for f1 in os.listdir(f0d):
                f1d=os.path.join(f0d,f1)
                pix[f0][f1]={}
                for f2 in os.listdir(f1d):
                    f2d=os.path.join(f1d,f2)
                    pix[f0][f1][f2]=[os.path.join(f2d,s) for s in os.listdir(f2d)]
                    if len(pix[f0][f1][f2])>1:
                        print('Warning: Ignored second file in same folder:\n\t','\n\t'.join(pix[f0][f1][f2]))
        return pix

    def getCursel(self):
        return [self.lists[0].currentItem(),self.lists[1].currentItem(),self.lists[2].currentItem()]

    def updateList0(self):
        self.lists[0].clear()
        self.lists[0].addItems(sorted([s for s in self.pix]))
        self.lists[0].setCurrentRow(0)

    def updateList1(self):
        self.lists[1].clear()
        self.lists[1].addItems(sorted([s for s in self.pix[self.lists[0].currentItem().text()]]))
        self.lists[1].setCurrentRow(0)

    def updateList2(self):
        self.lists[2].clear()
        [t1,t2]=[self.lists[0].currentItem().text(),
                 self.lists[1].currentItem().text()]
        self.lists[2].addItems(sorted([s for s in self.pix[t1][t2]]))
        self.lists[2].setCurrentRow(0)

    def updateImage(self):
        [t1,t2,t3]=[self.lists[0].currentItem().text(),
                    self.lists[1].currentItem().text(),
                    self.lists[2].currentItem().text()]
        self.txt.setText(self.pix[t1][t2][t3][0])
        limg=QtGui.QPixmap(self.pix[t1][t2][t3][0])
        limg.scaledToWidth(True)
        self.img.setPixmap(limg)
        
    def _initLayout(self):
        def updateList1(row):
            if row!=-1:
                self.updateList1()
            
        def updateList2(row):
            if row!=-1:
                self.updateList2()

        def updateImage(row):
            if row!=-1:
                self.updateImage()

        self.txt=QtWidgets.QLineEdit()
        self.lists=[]
        for y in range(3):   # a/b/c
            self.lists.append(QtWidgets.QListWidget())
        self.img=QtWidgets.QLabel()
        self.img.setScaledContents(True)

        self.updateList0()
        self.updateList1()
        self.updateList2()
        self.updateImage()
        
        VB0=QtWidgets.QVBoxLayout()
        HB1=QtWidgets.QHBoxLayout()
        for i in range(3):
            HB1.addWidget(self.lists[i])
        VB0.addWidget(self.img)
        VB0.addWidget(self.txt)
        VB0.addLayout(HB1)
        
        self.lists[0].currentRowChanged.connect(updateList1)
        self.lists[1].currentRowChanged.connect(updateList2)
        self.lists[2].currentRowChanged.connect(updateImage)
        self.setLayout(VB0)
        self.setWindowTitle('Fly Viewer v. {}'.format(VERSION))
                    
                
class Form(QtWidgets.QWidget):
    def __init__(self,pixdir='',parent=None):
        super(Form,self).__init__(parent)
        self.pixdir=pixdir
        self.pix=self.populatepix()
        self.initLayout()

    def initLayout(self):
        self.panels=[PicPanel(self.pix,self.pixdir,self),PicPanel(self.pix,self.pixdir,self)]

        HB0=QtWidgets.QHBoxLayout()
        HB0.addWidget(self.panels[0])
        HB0.addWidget(self.panels[1])
            
        self.setLayout(HB0)
        self.setWindowTitle('Fly Viewer v. 0')

    def populatepix(self):
        pix={}
        for f0 in os.listdir(pixdir):
            f0d=os.path.join(pixdir,f0)
            pix[f0]={}
            for f1 in os.listdir(f0d):
                f1d=os.path.join(f0d,f1)
                pix[f0][f1]={}
                for f2 in os.listdir(f1d):
                    f2d=os.path.join(f1d,f2)
                    pix[f0][f1][f2]=[os.path.join(f2d,s) for s in os.listdir(f2d)]
                    if len(pix[f0][f1][f2])>1:
                        print('Warning: Ignored second file in same folder:\n\t','\n\t'.join(pix[f0][f1][f2]))
        return pix
        

if __name__=='__main__':
    main()
