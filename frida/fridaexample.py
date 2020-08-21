import frida
import sys

#device = frida.get_usb_device()
#pid = device.spawn(["cg.zz.frida.hook"])
#session = device.attach(pid)

rdev = frida.get_remote_device()
session = rdev.attach("cg.zz.frida.hook")

scr = """
Java.perform(function(){
	var utils = Java.use("cg.zz.frida.hook.util.Utils");
	var coinClass = Java.use("cg.zz.frida.hook.dto.CoinMoney");
	var clazz = Java.use("java.lang.Class");
	var Exception = Java.use("java.lang.Exception");

	//hook constructor method 然后构造方法是固定写法：$init
	/*coinClass.$init.overload("int" , "java.lang.String").implementation = function(money , value) {
		send("Money : " + money + ",value="+value);
		arguments[0] = 13;
		arguments[1] = "13.0";

		return this.$init(12 , "12.0");
	};*/

	//hook normal method
	/*utils.getPwd.overload().implementation = function() {
		var s = this.getPwd();

		send("pwd return : " + s);

		return "SmallOrange attack ssd";
	};*/

	//hook overload method 这里的普通方法包括了静态方法，私有方法和公开方法等，这个操作和上面的构造方法其实很类似
	/*utils.getPwd.overload("java.lang.String").implementation = function() {
		var arg = arguments[0];
		send("pwd arg : " + arg);
		//change args and result value

		//这一步修改了方法的参数和返回值
		return this.getPwd("666") + ",Hello World!";
	};*/

	//构造和修改自定义类型对象和属性
	//这里我们拦截getCoin方法，然后构造一个新的CoinMoney对象返回，这里构造一个实例方法是固定写法$new即可。当然也可以调用call方法形式也是可以的。
	utils.getCoin.implementation = function() {
		var coinObj = coinClass.$new(2 , "2.0");
		coinObj.setExtMoney(22);

		return coinObj;
	};

	//如何修改一个对象的属性值呢？
	utils.getCoinMoney.overload("cg.zz.frida.hook.dto.CoinMoney").implementation = function() {
		var coin = arguments[0];
		send("coin obj:" + coin);

		//call public method 直接调用方法没问题
		var money = coin.getMoney();
		send("getCoinMoney money : "+money);

		//get public field 直接调用字段就有问题了，不管这个字段是private还是public都会失败
		var extMoney = coin.extMoney;
		send("extMoney field:"+extMoney);

		//reflect field to get value 正确的做法是用反射进行操作，先用Java.cast获取对应类的class类型，然后就和Java中类似了，基本类型修改值都是setXXX方法，对象类型都是set方法即可
		var money_field_name = Java.cast(coin.getClass() , clazz).getDeclaredField("money");
		money_field_name.setAccessible(true);
		send("reflect money field:"+money_field_name.get(coin));
		//reflect field to set value
		money_field_name.setInt(coin , 101);

		return coin.getMoney();
	};

	//打印方法的堆栈信息
	utils.getPwd.overload("java.lang.String").implementation = function() {
		//get args after change result value
		var arg = arguments[0];
		send("pwd arg:"+arg);

		//get StackInfo after use cmd : "adb locat -s AndroidRuntime"
		throw Exception.$new("CoinMoney Constructor Exception...");

		//change args and ressult value
		return this.getPwd("SmallOrange") + "yyyy";
	};

	//第一、Hook类的构造方法和普通方法，注意构造方法是固定写法$init即可，获取参数可以通过自定义参数名也可以直接用系统隐含的arguments变量获取即可。
	//第二、修改方法的参数和返回值，直接调用原始方法传入需要修改的参数值和直接修改返回值即可。
	//第三、构造对象使用固定写法$new即可。
	//第四、如果需要修改对象的字段值需要用反射去进行操作。
	//第五、堆栈信息打印直接调用Java的Exception类即可，通过adb logcat -s AndroidRuntime来过滤日志信息查看崩溃堆栈信息。
	//总结：记得用Java.use方法获取类的类型，如果遇到重载的方法用overload实现即可。
});
"""

def on_message(message, data):
    print(message)

script = session.create_script(scr)
#设置message 回调函数为 on_message。js 调用send 就会发到 on_message
script.on("message", on_message)
script.load()
#device.resume(pid)
sys.stdin.read()