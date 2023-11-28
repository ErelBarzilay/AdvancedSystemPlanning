from PIL import Image
import numpy as np
import crypt_image
import io
import struct
class Card:
    def __init__(self, name, creator, image, riddle, solution = None):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution
    def __repr__(self):
        return "<name: " + self.name + " creator:" + self.creator + " >"
    def __str__(self):
        str = "Card " + self.name + " by " + self.creator + "\n"
        str = str + "riddle: " + self.riddle + "\n"
        if self.solution == None:
            return str + "Solution: None"
        return str + "Solution:"  + self.solution
    
    @classmethod
    def create_from_path(cls, name, creator, path, riddle, solution):
        card = Card(name, creator, crypt_image.CryptImage(Image.open(path)), riddle, solution)
        return card
    
    def serialize(self):
        len_name = (len(self.name)) 
        len_creator = (len(self.creator))
        height_pic = (self.image.image.size[0]) 
        len_pic = (self.image.image.size[1])
        len_rid = (len(self.riddle))
        img = list(self.image.image.getdata())
        img = [bytes(x) for x in img]
        x = img[0]
        for i in range(1,len(img)):
            x = x + img[i]
        img = x
        img = bytearray(img)
        serialized = struct.pack("I"+str(len_name)+'s'+"I"+str(len_creator)+'s'+"I"+"I"+str(len(img)) + 's' + "I" + str(len_rid) + 's', len_name,bytes(self.name,'utf-8'),len_creator,bytearray(self.creator,'utf-8'), height_pic, len_pic, img, len_rid, bytearray(self.riddle,'utf-8'))
        return serialized
    
    @classmethod
    def deserialize(cls, serialized):
        len_name = struct.unpack_from("I",serialized)[0]
        name = struct.unpack_from(str(len_name)+ "s",serialized, 4)[0]
        len_creator = struct.unpack_from("I" + str(len_name) + "s" + "I", serialized)[2]
        creator = struct.unpack_from("I" + str(len_name) + "s" + "I" + str(len_creator) + "s", serialized)[3]
        height_pic = struct.unpack_from("I" + str(len_name) + "s" + "I" + str(len_creator) + "s" + "I", serialized)[4]
        len_pic = struct.unpack_from("I" + str(len_name) + "s" + "I" + str(len_creator) + "s" + "I" + "I", serialized)[5]
        img_data =  struct.unpack_from("I" + str(len_name) + "s" + "I" + str(len_creator) + "s" + "I" + "I" + str(len_pic * height_pic * 3) + "s", serialized)[6]
        len_riddle = struct.unpack_from("I" + str(len_name) + "s" + "I" + str(len_creator) + "s" + "I" + "I" + str(len_pic * height_pic * 3) + "s" + "I", serialized)[7]
        riddle = struct.unpack_from("I" + str(len_name) + "s" + "I" + str(len_creator) + "s" + "I" + "I" + str(len_pic * height_pic * 3) + "s" + "I" +str(len_riddle) + "s", serialized)[8]
        img = Image.frombytes('RGB', size = (height_pic, len_pic), data = img_data)
        return Card((name.decode('utf-8')),(creator.decode('utf-8')),crypt_image.CryptImage(img),(riddle.decode('utf-8')))
        
