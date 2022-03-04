function candyJniHook() {
	console.log("native");
	var pSize = Process.pointerSize;
	var env = Java.vm.getEnv();
	var handlePointer = Memory.readPointer(env.handle);
	var RegisterNatives = 215, FindClassIndex= 6;// search "215" @ https://docs.oracle.com/javase/8/docs/technotes/guides/jni/spec/functions.html
	var jclassAddress2NameMap = {};
	var moduleDict = {};
	function getNativeAddress(idx) {
		return Memory.readPointer(handlePointer.add(idx * pSize));
	}
	function ModuleScanning(args) {
		Process.enumerateModules({
			onMatch: function (exp) {
				if (exp.name in args) {
					console.log("[*] Module:" + exp.name+ ",Address:" + exp.base);
				}
			},
			onComplete: function () {
				
			}
		});
	}
	// intercepting FindClass to populate Map
	Interceptor.attach(getNativeAddress(FindClassIndex), {
		onEnter: function (args) {
			jclassAddress2NameMap[args[0]]= args[1].readCString();
		},
		onLeave: function (args) {
		}
	});
	// RegisterNative(jClass*, .., JNINativeMethod *methods[nMethods], uint nMethods) // https://android.googlesource.com/platform/libnativehelper/+/master/include_jni/jni.h#977
	Interceptor.attach(getNativeAddress(RegisterNatives), {
		onEnter: function (args) {
			for (var i = 0, nMethods = parseInt(args[3]); i < nMethods; i++) {
				/*
				https://android.googlesource.com/platform/libnativehelper/+/master/include_jni/jni.h#129
				typedef struct {
					const char* name;
					const char* signature;
					void* fnPtr;
				} JNINativeMethod;
				*/
				var structSize = pSize* 3;// = sizeof(JNINativeMethod)
				var methodsPtr = ptr(args[2]);
				var methodName = Memory.readPointer(methodsPtr.add(i* structSize ));
				var signature = Memory.readPointer(methodsPtr.add(i* structSize+ pSize));
				var fnPtr = Memory.readPointer(methodsPtr.add(i* structSize + pSize* 2));// void* fnPtr
				var jClass = jclassAddress2NameMap[args[0]].split('/');
				var moduleName = DebugSymbol.fromAddress(fnPtr)['moduleName'];
				var find_module = Process.findModuleByAddress(fnPtr);
				console.log(JSON.stringify({module: moduleName,// https://www.frida.re/docs/javascript-api/#debugsymbol
					package: jClass.slice(0,-1).join('.'),
					class: jClass[jClass.length- 1],
					method: methodName.readCString(),// char* name
					signature: signature.readCString(),// char* signature TODO Java bytecode signature parser { Z: 'boolean', B: 'byte', C: 'char', S: 'short', I: 'int', J: 'long', F: 'float', D: 'double', L: 'fully-qualified-class;', '[': 'array' } https://github.com/skylot/jadx/blob/master/jadx-core/src/main/java/jadx/core/dex/nodes/parser/SignatureParser.java
					address: fnPtr
				}));
				moduleDict[moduleName]= "1";
			}
		},
		onLeave: function (args) {
			ModuleScanning(moduleDict);
		}
	});
}

send("start frida candyjni hook ~~~ ");
if (Java.available) {
  Java.perform(function () {
    candyJniHook();
  });
}

// frida -l hook_candyjni.js com.sankuai.meituan.takeoutnew
// frida -U --no-pause -f com.sankuai.meituan.takeoutnew -l hook_candyjni.js

// frida -U -l hook_candyjni.js -f com.sankuai.meituan.takeoutnew --no-pause
