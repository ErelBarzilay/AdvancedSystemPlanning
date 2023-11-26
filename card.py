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
        height_pic = (self.image.image.shape[0]) 
        len_pic = (self.image.image.shape[1])
        len_rid = (len(self.riddle))
        img = Image.open(self.image.image, mode='r')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        serialized = struct.pack("I"+str(len_name)+"s"+"I"+str(len_creator)+"s"+"I"+"I"+str(len(img_byte_arr)) + "I" + str(len_rid) + "s", len_name,self.name,len_creator,self.creator, height_pic, len_pic, img_byte_arr, len_rid, self.riddle)
        return serialized
    @classmethod

    def deserialize(cls, serialized):
        len_name = struct.unpack_from("I",serialized)[0]
        name = struct.unpack_from(str(len_name)+ "s",serialized, 4)[0]
        len_creator = struct.unpack_from("I", serialized, 4 + len_name)[0]
        creator = struct.unpack_from(str(len_creator) + "s", serialized, 8 + len_name)[0]
        height_pic = struct.unpack_from("I",serialized, 8 + len_name + len_creator)[0]
        len_pic = struct.unpack_from("I",serialized, 12 + len_name + len_creator)[0]
        img_data = struct.unpack_from(str(height_pic * len_pic * 3) +"s", serialized, 20 + len_name + len_creator)[0]
        len_riddle = struct.unpack_from("I", serialized, 20 + len_name + len_creator + height_pic * len_pic * 3)[0]
        riddle = struct.unpack_from(str(len_riddle) + "s", serialized, 20 + len_name + len_creator + height_pic * len_pic * 3 + 4)[0]
        img = Image.frombytes('RGB', size = (len_pic, height_pic), data = img_data)
        return Card(name,creator,crypt_image.CryptImage(img),riddle)
        
