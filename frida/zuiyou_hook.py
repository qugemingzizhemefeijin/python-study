import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("cg.zz.zuiyou")

scr = """
Java.perform(function () {
//********************************hook native*********************************//

//hook unexport function

//sub_4BCC ==> input:data+data.size; output:decrypt_data
var pointer = Module.findExportByName("libnet_crypto.so" , "JNI_OnLoad");
var hookpointer = '0x'+ parseInt(parseInt(pointer) - parseInt('0x488C') + parseInt('0x5070')).toString(16);
var nativePointer = new NativePointer(hookpointer);
console.log("net native pointers:"+nativePointer);
var arg0, arg1, arg2;
Interceptor.attach(nativePointer, {
    onEnter: function(args) {
    	arg0 = args[0];
    	arg1 = args[1];
    	arg2 = args[2];
    	console.log("sub_5070 args: " + Memory.readCString(args[0])+","+ args[1]+","+Memory.readCString(args[2]));
    },
    onLeave:function(retval){
    	var arybuffer = Memory.readByteArray(arg2, 16);
    	var intary = new Uint32Array(arybuffer);
    	var resultstr = "";
    	for(var i=0;i<intary.length;i++){
    		resultstr = resultstr + revertHex(intary[i].toString(16));
    	}
        console.log("sub_5070 result:"+resultstr);
    }
});


hookpointer = '0x'+ parseInt(parseInt(pointer) - parseInt('0x488C') + parseInt('0x4B04')).toString(16);
nativePointer = new NativePointer(hookpointer);
console.log("net native pointers:"+nativePointer);
Interceptor.attach(nativePointer, {
    onEnter: function(args) {
        arg0 = args[0];
        arg1 = args[1];
        //console.log("sub_4B04 args: " + Memory.readCString(args[0])+","+ args[1]);
    },
    onLeave:function(retval){
        var arybuffer = Memory.readByteArray(arg0, 16);
        //console.log("sub_4B04 result:" + Memory.readCString(arg0)+","+ arg1);
    }
});
//****************************************************************************//

function revertHex(hexStr){
	var str = "";
	str = str + hexStr[6];
	str = str + hexStr[7];
	str = str + hexStr[4];
	str = str + hexStr[5];
	str = str + hexStr[2];
	str = str + hexStr[3];
	str = str + hexStr[0];
	str = str + hexStr[1];
	return str;
}

});
"""

script = session.create_script(scr)
def on_message(message ,data):
    print(message)
script.on("message" , on_message)
script.load()
sys.stdin.read()