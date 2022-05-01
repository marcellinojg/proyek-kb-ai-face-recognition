from email.mime import image
import face_recognition
import os


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
        
    
    # def loadUploadedImage(self,url):
    #     self.image = face_recognition.load_image_file(url)
    #     self.url = url
        
        
    def loadLocalImage(self,url):
        self.image = face_recognition.load_image_file(url)
        self.url = url
        
    def findEncode(self):
        self.location = face_recognition.face_locations(self.image)
        self.encoding = face_recognition.face_encodings(self.image)[0]
        
    def findPerson(self):
        faces = KnownPeople()
        name = "Unknown"
        for i in range(0,len(faces.faces)):
            isFound = face_recognition.compare_faces([faces.faces[i].encoding],self.encoding)
            if isFound[0]:
                name = faces.faces[i].name
                self.name = name
                break
        
        print("This is " + name)
        return name        
        
        
    
class KnownPeople:
    faces = []
    folder_names = []
    
    def __init__(self):
        self.folder_names = os.listdir("KnownImages")
        self.addFaces()
        
    def addFaces(self):
        for i in range(0,len(self.folder_names)):
            image_names = os.listdir("KnownImages/" + self.folder_names[i])
            for j in range(0,len(image_names)):
                self.faces.append(Face(self.folder_names[i],"KnownImages/" + self.folder_names[i] + "/" + image_names[j]))
    
if __name__ == "__main__":
    listFaces = KnownPeople()
    testElon = Face("","testelon1.jpg")
    testBill = Face("","testbill1.jpg")
    testMark = Face("","testmark1.jpg")
    testElon.findPerson()
    testBill.findPerson()
    testMark.findPerson()