import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("com.ss.android.ugc.aweme")

scr = """
Java.perform(function () {
	var userInfo = Java.use("com.ss.android.common.applog.UserInfo");
	var cms = Java.use("com.ss.sys.ces.a");
	var req = Java.use("com.ss.android.ugc.aweme.app.astispam.c");
	var signature = Java.use("android.content.pm.Signature");
	
	//Hook UserInfo getUserInfo
	userInfo.getUserInfo.overload("int" , "java.lang.String", "[Ljava.lang.String;","java.lang.String").implementation = function(serverTime, params, strArr, c) {
		send("getUserInfo serverTime : " + serverTime);
		send("getUserInfo params : " + params);
		send("getUserInfo strArr : " + strArr);
		send("getUserInfo c : " + c);

		var retvalue = this.getUserInfo(serverTime, params, strArr, c);
		send("getUserInfo retvalue : " + retvalue);

		return retvalue;
	};

	userInfo.initUser.overload("java.lang.String").implementation = function(str) {
		send("initUser str : " + str);

		var retvalue = this.initUser(str);

		send("initUser retvalue : " + retvalue);

		return retvalue;
	};

	userInfo.setAppId.overload("int").implementation = function(appid) {
		send("setAppId appid : " + appid);

		this.setAppId(appid);
	};

	//Hook Signature
	signature.toCharsString.overload().implementation = function() {
		var retvalue = this.toCharsString();

		send("toCharsString retvalue : " + retvalue);

		return retvalue;
	};

	//Hook CMS
	cms.e.overload("[B").implementation = function(bArr) {
		var buffer = Java.array('byte', bArr);
		var result = "";
		for(var i = 0; i < buffer.length; ++i){
			result+= (String.fromCharCode(buffer[i]));
		}
		send("e bArr : " + result);
		
		var retvalue = this.e(bArr);
		buffer = Java.array('byte', retvalue);
		result = "";
		for(var i = 0; i < buffer.length; ++i){
			result+= buffer[i]+",";
		}
		send("e retvalue : " + result);

		return retvalue;
	};

	//Hook Request URL
	req.a.overload("java.lang.String","java.util.List","int").implementation = function(str, list, i) {
		send("a str : " + str);
		send("a list : " + list);
		send("a i : " + i);

		var retvalue = this.a(str, list, i);
		send("a retvalue : " + retvalue);

		return retvalue;
	};
});
"""

script = session.create_script(scr)
def on_message(message ,data):
    print(message)
script.on("message" , on_message)
script.load()
sys.stdin.read()