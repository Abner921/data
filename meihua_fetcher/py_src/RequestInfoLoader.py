#!/usr/bin/env python

from pprint import pprint
import os, sys, datetime, StringIO, time

from Utility import Utility

class RequestInfoLoader:

  utility = None

  def __init__(self, utility):
    self.utility = utility

  def loadAddProductRequestFromFile(self, filename):
    """ Return a product object with mappings of property / value pair,
        and also read encode the image files.

        (siteInfo, productInfo) = loadAddProductRequestFromFile("product.txt")

        siteInfo = {
          "SITES": ["MADE_IN_CHINA", "ECVV"],
          "LOGIN": {
            "MADE_IN_CHINA" : {
              "USERNAME" : "abc",
              "PASSWORD" : "efg"
            },
            "ECVV" : {
              "USERNAME" : "abc",
              "PASSWORD" : "efg"
            },
          }
        }

    Product keys includes:
    PRODUCT_NAME
    KEYWORD1
    KEYWORD2
    KEYWORD3
    CATEGORY
    PRODUCT_IMAGE_FILE_PATH
    DESCRIPTION
    PAYMENT: 1 L/C  2 T/T  3 D/P  4 Paypal 5 Money Gram  6 Western Union Others
    """
    product = {}
    siteInfo = {
      "SITES": [],
      "LOGIN": {}
    }
    self.utility.printMessage("Loading product info from file: " + filename)
    request_file = open(filename)
    defaultPlatForm = None

    isParsingDescription = False

    for line in request_file:
      # Comments:
      if line.startswith("#") or line.startswith("//"):
        continue

      separatorIndex = line.find("=")
      if separatorIndex <= 0:
        if isParsingDescription:
          product["DESCRIPTION"] = product["DESCRIPTION"] + line
        else:
          self.utility.printError("Invalid product info. Should be key=value pair each line" + line)
        continue

      isParsingDescription = False

      key = line[ : separatorIndex]
      value = line[separatorIndex + 1 : ].strip()

      if key == "PLATFORM":
        siteInfo["SITES"].append(value)
        defaultPlatForm = value
        siteInfo["LOGIN"][defaultPlatForm] = {}
        continue
      
      if key == "USERNAME":
        if not defaultPlatForm:
          self.utility.printError("Find username but no platform settings." + line)
        else:
          siteInfo["LOGIN"][defaultPlatForm]["USERNAME"] = value
        continue

      if key == "PASSWORD":
        if not defaultPlatForm:
          self.utility.printError("Find password but no platform settings." + line)
        else:
          siteInfo["LOGIN"][defaultPlatForm]["PASSWORD"] = value
        continue

      if key == "DESCRIPTION":
        isParsingDescription = True

      if key.startswith("PLATFORM."):
        if len(key.split(".")) != 2 or len(value.split(":")) != 2:
          self.utility.printError("Invalid site login info. Should be LOGIN.SITENAME=USER:PASS pair each line" + line)

        site = key.split(".")[1]
        (username, password) = value.split(":")
        siteInfo["SITES"].append(site)
        siteInfo["LOGIN"][site] = {}
        siteInfo["LOGIN"][site]["USERNAME"] = username
        siteInfo["LOGIN"][site]["PASSWORD"] = password
      else:
        product[key.strip()] = value.strip()

    if product.has_key("PRODUCT_IMAGE_FILE_PATH") and product["PRODUCT_IMAGE_FILE_PATH"]:
      imageFilePath = self.utility.getProductRequestFilePath(product["PRODUCT_IMAGE_FILE_PATH"])
      lastSlashIndex = max(imageFilePath.rfind("\\"), imageFilePath.rfind("/"))
      imageFileName = imageFilePath[lastSlashIndex + 1:]

      imageData = ""
      with open(imageFilePath, "rb") as imageContent:
        imageData = imageContent.read()  # data.encode("base64")

      imageFileSize = len(imageData)
      product["PRODUCT_IMAGE_CONTENT"] = imageData
      self.utility.printMessage("Image file loaded: " + imageFilePath)
      product["PRODUCT_IMAGE_FILE_NAME"] = imageFileName
      self.utility.printMessage("Image file name: " + imageFileName)
      product["PRODUCT_IMAGE_FILE_SIZE"] = imageFileSize

    return siteInfo, product
