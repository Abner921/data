#!/usr/bin/env python
#encoding: utf-8

import unittest
from baidu_news_parser import BaiduNewsParser

class BaiduNewsParserTest(unittest.TestCase):
  
  # a test baidu news result with:
  # record with all fields
  # record without image
  # record without similar results
  raw_text = """
<div id="ecomAdDiv_1"></div><div id="ecomAdDiv_2"></div><script type="text/javascript">BAIDU_CLB_addOrientation('newsquery', '测试');BAIDU_CLB_fillSlotAsync('639913', 'ecomAdDiv_1');BAIDU_CLB_fillSlotAsync('639914', 'ecomAdDiv_2');</script><div></div></div><div id="content_left"><div id="bdRankTips"><div id="bdRankTipsContent"></div><a href="javascript:void(0)" id="bdRankTipsClose">x</a></div><div class="ecom_pingzhuan">
</div><ul><li class="result" id="6"><h3 class="c-title"><a href="http://testlink"
  data-click="{
    'f0':'77A717EA',
    'f1':'9F63F1E4',
    'f2':'4CA6DE6E',
    'f3':'54E5243F',
    't':'1405490946'
    }"

              target="_blank"
          
  >testtitle</a></h3><span class="c-author">&nbsp;testsource&nbsp;testtime</span><div class="c-summary"><a class="c_photo" href="http://www.itbear.com.cn/n97893c86.aspx" target="_blank" ><img src="http://testimg.JPG" alt="" /></a>testdescription&nbsp;<a href="/ns?word=%E6%B5%8B%E8%AF%95+cont:896630147&same=2&cl=1&tn=news&rn=30&fm=sd" class="c-more_link" data-click="{'fm':'sd'}" >2条相同新闻</a>&nbsp;-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763105392230e54f7387a8787463fc3933fc23904564711b2e73a7e1b01d9ce7d360bab5e5c9da377307d1765eadb9e875dadbb855f2f9f5647676a80&amp;p=882a95418e8512a05aacc8625b05&amp;newp=cb778315d9c345dd43be9b7c505292695912c10e3fd5a20e&user=baidu&fm=sc&query=%B2%E2%CA%D4&qid=cb5e7c32000044e8&p1=8" 
    data-click="{'fm':'sc'}"
      target="_blank"  class="c-cache">百度快照</a></div></li><li class="result" id="9"><h3 class="c-title"><a href="testlink2"
  data-click="{
    'f0':'77A717EA',
    'f1':'9F63F1E4',
    'f2':'4CA6DD6E',
    'f3':'54E5243F',
    't':'1405490946'
    }"

                target="_blank"
            
    >testtitle2</a></h3><span class="c-author">&nbsp;testsource2&nbsp;testtime2</span><div class="c-summary"><a class="c_photo" href="http://wow.17173.com/content/2014-07-16/20140716135105144.shtml" target="_blank" ><img src="testimage2.JPEG" alt="" /></a>testdescription2&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece76310538a230e54f76039d4d51468d4e419ce3b46101a3aa5ec7b640d04d1c67a7001d94b59fdf04071331e20b598ce8a4fdebf9129288b2533731a805612a458f58d197bd565cd1abfa00e97bae74593b9a3a0c82255&amp;p=882a95478e8512a05aacc8625b05&amp;newp=cb778315d9c343dd43be9b7c505292695912c10e3aa5cb&user=baidu&fm=sc&query=%B2%E2%CA%D4&qid=cb5e7c32000044e8&p1=9" 
      data-click="{'fm':'sc'}"
        target="_blank"  class="c-cache">百度快照</a></div></li><li class="result" id="10"><h3 class="c-title"><a href="testlink3"
    data-click="{
      'f0':'77A717EA',
      'f1':'9F63F1E4',
      'f2':'4CA6DE6E',
      'f3':'54E5243F',
      't':'1405490946'
      }"

              target="_blank"
          
  >testTitle3</a></h3><span class="c-author">&nbsp;testsource3&nbsp;testtime3</span><div class="c-summary"> testdescription3...&nbsp;<a href="/ns?word=%E6%B5%8B%E8%AF%95+cont:3722282078&same=3&cl=1&tn=news&rn=30&fm=sd" class="c-more_link" data-click="{'fm':'sd'}" >3条相同新闻</a>&nbsp;-&nbsp;<a href="http://cache.baidu.com/c?m=9f65cb4a8c8507ed4fece763104a8023584380146a848a4268d4e419cf795b434460feb922351072d0c1616403ae4a59ebf23679200357eddd97d65e98e6d27e209f5734676b865663a00ed9cd&amp;p=c2759a41d29506e50be29662550e&amp;newp=cb64c54ad2c717c30ebe9b7c1c0892695912c10e3bd5867929&user=baidu&fm=sc&query=%B2%E2%CA%D4&qid=cb5e7c32000044e8&p1=10" 
    data-click="{'fm':'sc'}"
      target="_blank"  class="c-cache">百度快照</a></div></li></ul></div>
  """
  
  parser = BaiduNewsParser()
  
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
  
  def testParse(self):
    results = self.parser.parseBaiduNewsHtml(self.raw_text, "news")
    self.assertEqual(results, [
        {'origin': 'testsource',
         'picture': 'http://testimg.JPG',
         'title': 'testtitle',
         'creation_time': 'testtime',
         'content': 'testdescription',
         'link': 'http://testlink'
        },
        {'origin': 'testsource2',
         'picture': 'testimage2.JPEG',
         'title': 'testtitle2',
         'creation_time': 'testtime2',
         'content': 'testdescription2',
         'link': 'testlink2'
        },
        {'origin': 'testsource3',
         'picture': '',
         'title': 'testTitle3',
         'creation_time': 'testtime3',
         'content': ' testdescription3...',
         'link': 'testlink3'
        }
    ])

if __name__ =='__main__':
  unittest.main()

"""  
  # @unittest.skip("skip")
  suite1 = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
  suite2 = unittest.TestLoader().loadTestsFromTestCase(TestDictValueFormatFunctions)
  suite = unittest.TestSuite([suite1, suite2])  
  unittest.TextTestRunner(verbosity=2).run(suite)
"""