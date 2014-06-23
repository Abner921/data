#!/usr/bin/env python

# ERROR CODES:

class ErrorCode:

  ACTION_SUCCEED = 1
  ACTION_NO_RESULT = 2
  ACTION_TIMEOUT = 3
  ACTION_ERROR_404 = 4
  ACTION_ERROR_500 = 5
  ACTION_SOCKET_ERROR = 5
  ACTION_RETRY_HTTP_ERROR=6
  ACTION_RETRY_URL_ERROR=7
  ACTION_UNKNOWN_ERROR = 8

  ACTION_RETRY_NO_RESULT = 50
  ACTION_RETRY_TIMEOUT = 51

  ACTION_LOGIN_ERROR = 100
  ACTION_NO_PRODUCT_CATEGORY = 101
  # reach the limitation for this account
  ACTION_MAX_PRODUCT = 102
  # Company license is not ready, not allow to add product, etc.
  ACTION_PERMISSION_ERROR = 103
  # Product info doesn't meet the constraint (min-length, format, etc)
  ACTION_PRODUCT_INFO_ERROR = 104
