import frida
import sys

#http://www.520monkey.com/archives/1256

rdev = frida.get_remote_device()
session = rdev.attach("cg.zz.frida.hook")

scr = """
Java.perform(function(){
	//第一、hook未导出函数功能
	//hook unexport function
	//ps | grep frida
	//cat /proc/pid/maps | grep libnet_crypto.so
	//实际地址就是0x7816A000+5070=0x7816F070，不过这个地址不是最后的地址，因为thumb和arm指令的区分，地址最后一位的奇偶性来进行标志，
	//所以这里还需加1也就是最终的0x7816F071，这一点很重要不管使用Cydia还是Frida都要注意最后计算的绝对地址要+1，不然会报错的

	var nativePointer = new NativePointer(0x76671071);
	send("net native pointers:"+nativePointer);
	var result_pointer;

	Interceptor.attach(nativePointer , {//开始hook操作
		onEnter : function(args){
			result_pointer = args[2].toInt32();
			//这里是函数执行前的可以获取函数参数信息，注意这里有一个密切相关的类Momory，他是直接操作地址内存数据的，
			//因为C中地址就是指针，指针就是地址，字符串也是用指针存的，所以如果想打印字符串信息需要把那段地址内存数据打印出来
			send("netcrypt so args:" + Memory.readCString(args[0])+", "+args[1]+", "+args[2]);
		},
		onLeave:function(retval){
			//memory alloc string
			var resultPointer = new NativePointer(result_pointer);
			//通过分析sub_5070这个函数的返回值不是通过return操作的，而是通过参数指针传值操作的，这个在C语言中很常用，因为返回值只有一个值，如果要返回多个值就可以用参数地址来进行传递
			//所以这里我们为了打印最后的结果值，需要把参数指针的那段值打印出来，这里直接读取字节，因为我们通过之前分析知道返回值是16个字节长度了
			var arybuffer = Memory.readByteArray(resultPointer , 16);
			var intary = new Uint32Array(arybuffer);
			var resultstr = "";
			for(var i=0;i<intary.length;i++){
				send("hex:"+intary[i].toString(16));
				resultstr = resultstr + revertHexString(intary[i].toString(16));
			}
			send("netcrypt result pointer:"+resultPointer+",result:"+resultstr);

			//change result 1111
			for(var i=0;i<intary.length;i++){
				intary[i] = 1;
			}
			Memory.writeByteArray(resultPointer , arybuffer);
		}
	});

	function revertHexString(hex) {
		var reverthex = "";
		for (var i = 0; i < hex.length - 1; i += 2)
			reverthex = "" + hex.substr(i, 2) + reverthex;
		return reverthex;
	}
});
"""

def on_message(message, data):
    print(message)

script = session.create_script(scr)
script.on("message", on_message)
script.load()
sys.stdin.read()