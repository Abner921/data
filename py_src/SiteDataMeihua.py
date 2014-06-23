from ErrorCode import *
from FallbackType import *

# done.

MeihuaLoginAction = {
  'action_name': 'MeihuaLogin',
  'data': { 'remember': '1',
            'su_bus_task': 'Check Member Login',
            'su_user_id': '%==>USERNAME<==%',
            'su_user_pass': '%==>PASSWORD<==%'},
  'headers': { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Host': 'www.Meihua.com',
               'Origin': 'http://www.Meihua.com',
               'Referer': 'http://www.Meihua.com/member/login.htm',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11'},
  'result': [ { 'output_key': 'WORLD_OF_TRADE_USERNAME',
                'result_regex': 'Welcome (.*),'}],
  'error_handling' : [{
    'error_regex' : ".*",
    'error_message' : "Username or password error.",
    'error_code' : ErrorCode.ACTION_LOGIN_ERROR
    }
  ],
  'url': 'http://www.Meihua.com/member/login.htm'
}

# result, list of: <input type="radio" value="Auto Bearing|2263" name="cp_catories[]" id="cp_categories">
MeihuaSearchCategoryAction = {
  'action_name': 'MeihuaSearchCategory',
  'data': { 'cs_bus_task': 'Search',
            'cs_search': '%==>KEYWORD1<==%'},
  'headers': { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Host': 'www.Meihua.com',
               'Origin': 'http://www.Meihua.com',
               'Referer': 'http://www.Meihua.com/category_select.php',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11'},
  'result': [ { 'output_key': 'WORLD_OF_TRADE_CATEGORY_ID',
                'result_regex': '<input type="radio" value=".*\|(\d+)" '}],
  'error_handling' : [{
    'error_regex' : "No category found",
    'error_message' : "Can't find corresponding category based on the keyword %==>KEYWORD1<==%.",
    'error_code' : ErrorCode.ACTION_RETRY_NO_RESULT
    }
  ],
  'retry_fallback' : [{
    'data_key' : 'KEYWORD1',
    'fallback_type' : FallbackType.REPLACE_WITH_SUBSTRING,
    'data_value' : 'Auto'
  }],
  'url': 'http://www.Meihua.com/category_select.php'
}


MeihuaAddProductAction = {
  'action_name': 'MeihuaAddProduct',
  'headers': { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryw1kGRja7LfZUknFt',
               'Host': 'www.Meihua.com',
               'Origin': 'http://www.Meihua.com',
               'Referer': 'http://www.Meihua.com/member/product-sell-posting.htm',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11'},
  'error_handling' : [{
    'error_regex' : "div class=\"full_error_div\">(.*?)<",
    'error_code' : ErrorCode.ACTION_PRODUCT_INFO_ERROR
    }, {
    'error_regex' : "<div class=\"centermessage_error\">(.*?)<",
    'error_code' : ErrorCode.ACTION_PRODUCT_INFO_ERROR
    }
  ],
  'url': 'http://www.Meihua.com/member/product-sell-posting.htm'
}

WORLD_OF_TRADE_ACTIONS = (MeihuaLoginAction,
                          MeihuaSearchCategoryAction,
                          MeihuaAddProductAction)
