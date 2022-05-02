from email.mime import image
import face_recognition
import os
import numpy


class Face:
    name = ""
    image = None
    location = None
    encoding = None
    url = None
    
    def __init__(self,name,url):
        self.name = name
        self.url = url
        self.loadLocalImage(self.url)
        self.findEncode()     
        
    def loadLocalImage(self,url):
        self.image = face_recognition.load_image_file(url)
        self.url = url
        
    def findEncode(self):
        self.location = face_recognition.face_locations(self.image)
        self.encoding = face_recognition.face_encodings(self.image,num_jitters=10)[0]
        
    def findPerson(self):
        faces = KnownPeople()
        name = "Unknown"
        for i in range(0,len(faces.faces)):
            isFound = face_recognition.compare_faces(faces.faces[i],self.encoding,tolerance=0.4)
            if isFound[0]:
                name = faces.peopleName[i]
                self.name = name
                break
        
        print("This is " + name)
        return name        
        
        
    
class KnownPeople:
    faces = []
    peopleName = []
    folder_names = []
    
    def __init__(self):
        self.folder_names = os.listdir("KnownImages")
        self.addFaces()
    
    def addFaces(self):
        for people in self.folder_names:
            dataList = os.listdir("KnownImages/" + people)
            self.peopleName.append(people)
            tempArr = []
            for data in dataList:
                tempArr1 = numpy.load("KnownImages/" + people + "/" + data)
                tempArr.append(tempArr1)
            self.faces.append(tempArr)
                
    
if __name__ == "__main__":
    listFaces = KnownPeople()
    testElon = Face("","testelon1.jpg")
    testBill = Face("","testbill1.jpg")
    testMark = Face("","testmark1.jpg")
    testElon.findPerson()
    testBill.findPerson()
    testMark.findPerson()