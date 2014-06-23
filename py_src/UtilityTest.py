#!/usr/bin/env python

from Utility import Utility

utility = Utility()

imagePayLoad = """------WebKitFormBoundary9Vj7shUQsQewcabN
Content-Disposition: form-data; name="%==>FILE_NAME<==%"; filename="%==>FILE_NAME<==%"
Content-Type: image/jpeg
------WebKitFormBoundary9Vj7shUQsQewcabN--
"""

dataPayLoad = {
  'data_params' : {
    'action' : "post using %==>CONTENT_TYPE<==%",
  },
}

input = {
  'STRINGKEY1' : "AFSL",
  'OBJECTKEY1' : {'test' : 'zzxv'},
  'OBJECTKEY2' : {'test' : 'zzxv'},
  'HOST_NAME' : 'www.test.com',
  'FILE_NAME' : 'test.jpg',
  'CONTENT_TYPE' : 'JPEG',
  'IMAGE_PAY_LOAD' : imagePayLoad,
  'DATA_PAY_LOAD' : dataPayLoad
}

value1 = "asdfa asdf%==>STRINGKEY1<==%weurou"
value2 = "asdfa asdf%==>STRINGKEY2<==%weurou"
value3 = "%-->OBJECTKEY<--%"


testProductImage = {
  'url' : 'http://%==>HOST_NAME<==%/upload?image=%==>FILE_NAME<==%',
  'headers' : {
    'Content-Type' : "%==>CONTENT_TYPE<==%",
  },
  'image' : "%-->IMAGE_PAY_LOAD<--%",
  'data' : "%-->DATA_PAY_LOAD<--%"
}


print utility.getMacroKey("%==>STRINGKEY1<==%")
print utility.getMacroKey("asdfa asdf%==>STRINGKEY2<==%weurou")
print utility.getMacroKey("%-->OBJECTKEY<--%")
print utility.getMacroKey("asdfa%-->OBJECTKEY<--%asdf")

print utility.replaceMacro(input, value1, "STRINGKEY1", True)
print utility.replaceMacro(input, value1, "STRINGKEY3", True)
print utility.replaceMacro(input, value2, "STRINGKEY1", True)
print utility.replaceMacro(input, value3, "OBJECTKEY1", False)
print utility.replaceMacro(input, value3, "OBJECTKEY2", False)
print utility.replaceMacro(input, value3, "OBJECTKEY3", False)


utility.processSiteData(testProductImage, input)
print testProductImage