#!/usr/bin/env python

# Operation: (KEEP IMMUTABLE in code)
#    A standalone task which can be completed with no dependency on other data,
#    such as add a post on a website, or, delete a list.
#    Cookies will be reused within an operation.
#
# Action: (KEEP IMMUTABLE in code)
#    One and only one post / get request, with request and return values.
#
# For each operation, there could be a couple actions, to be performed sequencially.
# For example, add a product onto site A, could have following actions:
# - Login request, check and login state.
# - Upload product images, return image ids.
# - Add product with the product ids.
#
# For each action, it need to meet preconditions, which is required, in order to proceed.
# For each action, there could be return values, which will be stored in the result field.

from SiteDataMeihua import *

"""
one_action = {
  'action_name' : 'name of the action, for use in status logging and debugging',
  'type' : 'TYPE ENUM, not in use yet',
  'url' : 'http://membercenter.made-in-china.com/logon.do',
  'headers' : {
    'Referer' : "...",
  },
  'url_params' : {
    # for get, same as url
  },
  'data' : {
    # for post only
  },

  # Note: if has result_regex / response_regex, it will be used as a whitelist to
  # mark that the result succeed. Skip it to trigger the error_handling, which
  # works as kind of black list checking whether anything bad happen.

  'result' : [{
    # Note, If result present, there must be a response_regex or result_regex.
    # Note, If response_regex presents, result_regex will not be used.

    # Response regex is for checking against response header, including redirect url, cookie.
    # for example: "Set-Cookie: ab_welcome=.*"
    'response_regex' : 'http://....(.*).html',

    # Result regex is for checking against response content (body, html src)
    'result_regex' : '.*tempPhotoId":".*'

    # By default will be case sensitive.
    'case_sensitive' : True,
    # By default will not match multiline
    'match_multiline' : False
    'output_key' : "PROD_CATEGORY"  # for filling using %==>PROD_CATEGORY<==%
  }],

  # error cases will be matched sequencially, and be handled by the first matching one.
  'error_strategy' : "ALLOW_ERROR",
  'error_handling' : [
    {
      'error_regex' : '',
      'error_message' : '',
      'error_code' : ACTION_TIMEOUT,
      # By default will be case sensitive.
      'case_sensitive' : True,
      # By default will not match multiline
      'match_multiline' : False
    },
    {
      # Note: if NO error message, then the matched error will be printed:
      'error_regex' : 'abc(.*)efg',
      'error_code' : ErrorCode.ACTION_RETRY_NO_RESULT
    }, ...
  ]

  # values for use when retry: change the input_data[%data_key%] to data value
  # Retry will only be done when error code is ACTION_RETRY_NO_RESULT.
  # Note: don't allow multiple entries for the same data_key
  'retry_fallback' : [{
    'data_key' : 'KEYWORD1',
    'fallback_type' : FallbackType.REPLACE_WITH_FIXED_VALUE,
    'data_value' : 'fixed_value'
  },
  {
    'data_key' : 'KEYWORD2',
    'fallback_type' : FallbackType.REPLACE_WITH_SUBSTRING,
    'data_value' : 'subsring_empty_fallback' # otherwise empty
  }]
}
"""

"""
Common retry for category search:

  'error_handling' : [{
    'error_regex' : "No Matched Results",
    'error_message' : "Can't find corresponding category based on the keyword.",
    'error_code' : ErrorCode.ACTION_RETRY_NO_RESULT
    }
  ],
  'retry_fallback' : [{
    'data_key' : 'KEYWORD1',
    'fallback_type' : FallbackType.REPLACE_WITH_SUBSTRING,
    'data_value' : 'all'
  }]
"""


# drafts
productListSiteInfo = {
  'url' : "http://membercenter.made-in-china.com/product.do?xcase=list",
  'pattern' : '/product.do?xcase=view&amp;prodId='
}
productListSiteInfoEcvv = {
  'url' : "http://www.ecvv.com/myecvv/product/manage_product.html"
}
checkProductName = {
  'url' : "http://membercenter.made-in-china.com/product.do",
  'xcase' : 'checkUniqueProdName',
  'prodName' : "",
  'prodId' : ''
}

ADD_PRODUCT_OPERATIONS = {
  'MADE_IN_CHINA' : MADE_IN_CHINA_ACTIONS,
  'ECVV' : ECVV_ACTIONS,
  'EC21' : EC21_ACTIONS,
  'GLOBAL_SOURCES' : GLOBAL_SOURCES_ACTIONS,
  'MANUFACTURER' : MANUFACTURER_ACTIONS,
  'WORLD_OF_TRADE': WORLD_OF_TRADE_ACTIONS,
  'FIBRE2FASHION' : FIBRE2FASHION_ACTIONS,
  'DIYTRADE' : DIYTRADE_ACTIONS,
  'WDTRADE' : WDTRADE_ACTIONS,
  # pending on login
  # 'TTNET' : TTNET_ACTIONS,
  'ALL_PRODUCTS' : ALL_PRODUCTS_ACTIONS,
  'ALL_BIZ' : ALLBIZ_ACTIONS
}
