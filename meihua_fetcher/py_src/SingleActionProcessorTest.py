import unittest

from Utility import Utility
from ErrorCode import ErrorCode
from FallbackType import FallbackType
from SingleActionProcessor import *

class SingleActionProcessorTest(unittest.TestCase):
  
  sap = SingleActionProcessor()
  
  TEST_INPUT_INFO = {
    'USERNAME' : "user1",
    'PASSWORD' : "pass1",
    'KEYWORD1' : "keyword1 text1 text2",
    'KEYWORD2' : "keyword2 text1 text2",
    'PLATFORM' : "eccv"
  }
    
  TEST_ACTION_INFO = {
    'action_name' : 'Login on MadeInChina',
    'url' : 'http://url',
    'headers' : {
      'Accept' : "text/html",
      'Content-Type' : "application/x-www-form-urlencoded",
      'Host' : "http://host",
      'Origin' : "http://origin",
      'Referer' : "http://referer",
      'User-Agent' : "agent"
    },
    'url_params' : {
      'param1' : "test1",
      'param2' : "1"
    },
    'data' : {
      'logonInfo.logUserName' : '%==>USERNAME<==%',
      'logonInfo.logPassword' : '%==>PASSWORD<==%',
    },
    'result' : [{
      'result_regex' : "result1",
      'output_key' : "RESULT1"
    }, {
      'result_regex' : "result2",
      'output_key' : "RESULT2",
      'case_sensitive' : False
    }],
    'error_handling' : [{
      'error_regex' : "no result need retry",
      'error_message' : "%==>USERNAME<==% : %==>PASSWORD<==% ",
      'error_code' : ErrorCode.ACTION_RETRY_NO_RESULT
      }, {
      'error_regex' : "timeout",
      'error_message' : "%==>USERNAME<==% : %==>PASSWORD<==% ",
      'error_code' : ErrorCode.ACTION_RETRY_TIMEOUT
      }, {
      'error_regex' : "no result error",
      'error_message' : "%==>USERNAME<==% : %==>PASSWORD<==% ",
      'error_code' : ErrorCode.ACTION_NO_RESULT
      }
    ],
    'retry_fallback' : [{
      'data_key' : 'KEYWORD1',
      'fallback_type' : FallbackType.REPLACE_WITH_SUBSTRING,
      'data_value' : 'all1'
    }, {
      'data_key' : 'KEYWORD2',
      'fallback_type' : FallbackType.REPLACE_WITH_FIXED_VALUE,
      'data_value' : 'all2'
    }]
  }

  _utility = Utility()
  _inputInfo = {}
  _actionInfo = {}

  def setUp(self):
    self._inputInfo = copy.deepcopy(self.TEST_INPUT_INFO)
    self._actionInfo = copy.deepcopy(self.TEST_ACTION_INFO)
    print "test start"

  def tearDown(self):
    print "test stop"

  def testGetEncodedUrl(self):
    self.assertEqual("http://url?param2=1&param1=test1",
                     self.sap.getEncodedUrl(self._actionInfo))

  def testFillFallbackDataForAction(self):
    self.assertEqual("keyword1 text1 text2", self._inputInfo["KEYWORD1"])
    self.assertEqual("keyword2 text1 text2", self._inputInfo["KEYWORD2"])

    self.sap.fillFallbackDataForAction(self._inputInfo, self._actionInfo)
    self.assertEqual("keyword1 text1", self._inputInfo["KEYWORD1"])
    self.assertEqual("all2", self._inputInfo["KEYWORD2"])

    self.sap.fillFallbackDataForAction(self._inputInfo, self._actionInfo)
    self.assertEqual("keyword1", self._inputInfo["KEYWORD1"])
    self.assertEqual("all2", self._inputInfo["KEYWORD2"])

    self.sap.fillFallbackDataForAction(self._inputInfo, self._actionInfo)
    self.assertEqual("all1", self._inputInfo["KEYWORD1"])
    self.assertEqual("all2", self._inputInfo["KEYWORD2"])


  # Test that the "case_sensitive" field is used correctly
  def testMatchCaseSensitive(self):
    self.assertEquals("result1",
                      self.sap.matchActionResult(self._actionInfo["result"][0], None,
                                        "contains result1 here", False))
    self.assertEquals(None,
                      self.sap.matchActionResult(self._actionInfo["result"][0], None,
                                        "will not match RESULT1 here", False))
    
    self.assertEquals("result2",
                      self.sap.matchActionResult(self._actionInfo["result"][1], None,
                                        "contains result2 here", False))
    self.assertEquals("RESULT2",
                      self.sap.matchActionResult(self._actionInfo["result"][1], None,
                                        "match RESULT2 here", False))

if __name__ == "__main__":
  unittest.main()
