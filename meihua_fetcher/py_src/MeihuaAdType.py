#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utility import enum

MeihuaAdType = enum(MAGAZINE = "1", TV = "2", OUTDOOR = "3", ONLINE = "4", PROMOTION = "5", RADIO = "6")

MeihuaAdTypeNameMap = {
  MeihuaAdType.MAGAZINE : "magazine",
  MeihuaAdType.TV : "tv",
  MeihuaAdType.OUTDOOR : "outdoor",
  MeihuaAdType.ONLINE : "online",
  MeihuaAdType.PROMOTION : "promotion",
  MeihuaAdType.RADIO : "radio",
}
