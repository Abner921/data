************************************************中文*****************************************************
发布介绍:

使用示例请参考*.py。本客户端库旨在提供WebService调用封装以及代理类生成，并不提供客户端
业务逻辑。

使用过程中如果遇到任何问题，请联系apihelp@baidu.com并在标题注明《Baidu API Client V2使用过程问题求助》

注意事项:

1. 如何设置SOAP Header ?
	参见baidu-api.properties。您需要填写username、password和token。请您填写这些信息后再尝试使用此客户端库。

2. 如何处理SOAP Response Header 数据 ?
	请通过BaiduNmsApiClientHelper.py. 来获取。该代码中有格式化输出返回信息的函数

3. 如何访问沙盒环境
	请参见Sandbox.txt。

5. 本客户端库的运行环境
	python 2.6+
	
6. 服务器证书
	如果想通过程序下载报告，可以导入证书到开发环境

***********************************************English***********************************************************
Release Notes:

Please see *.py for sample usage.

Please contact apihelp@baidu.com with email title: "Baidu API Client V2 Help" if any questions.

KeyPoints:

1. How to set the SOAP Header?
	See baidu-api.properties. You will need to fill in your username, password & token before using this client lib.

2. How to deal with SOAP Response Header data?
	Please use BaiduNmsApiClientHelper.py. It has function to print reponses.

3. How to access SandBox?
	See Sandbox.txt
	We prepared both online environment address & sandbox environment address for you.

4. Running environment
	python 2.6+

5. Server CA cert
	If you want to download report files through https, please use the certification attached.
------------------------------------------------------------------------------------------------------------------
Copyright 2012 Baidu.com Inc.
Baidu API Team