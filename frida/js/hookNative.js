
function getLoadedModules() {
    send("enumerating all loaded modules ...");
    Process.enumerateModules({
        onMatch: function(module) {
            send(module.name + " : " +  module.base + "\t" + module.size + "\t" + module.path);
        },
        onComplete: function() {
            send("enumerating completed !!!");
        }
    });
}

function getExportSymbols(moduleName) {
    var symbols = Module.enumerateExportsSync(moduleName);
    symbols.forEach(function(symbol){
        send(symbol.name + " address = " + symbol.address);
    });
    return symbols;
}

function getModuleAddr(moduleName) {
    var address = Module.findBaseAddress(moduleName);
    if (address != null) {
        send("get module '" + moduleName + "' address = " + address);
    }
    return address;
}

function getExportSymbolAddr(moduleName, symbol_sig) {
    var address = Module.findExportByName(moduleName, symbol_sig);
    if (address != null) {
        send("get symbol '" + symbol_sig + "' address = " + address);
    }
    return address;
}

function getSymbolAddr(moduleName, symbol_sig) {
    var symbols = Module.enumerateSymbolsSync(moduleName);
    var address = null;
    for(var i = 0; i < symbols.length; i++) {
        var symbol = symbols[i];
        if(symbol.name == symbol_sig){
            address = symbol.address;
        }
    }
    if (address != null) {
        send("get symbol '" + symbol_sig + "' address = " + address);
    }
    return address;
}

function getRegisterInfo() {
    var RegisterNativesAddr = getSymbolAddr("libart.so", "_ZN3art3JNI15RegisterNativesEP7_JNIEnvP7_jclassPK15JNINativeMethodi");
    if(RegisterNativesAddr != null){
        send("find symbol 'RegisterNatives' in libart.so, address = " + RegisterNativesAddr);
        Interceptor.attach(RegisterNativesAddr, {
            onEnter: function(args) {
                var class_name = Java.vm.getEnv().getClassName(args[1]);
                var methods_ptr = ptr(args[2]);
                var module = Process.findModuleByAddress(Memory.readPointer(methods_ptr));
				send("methods_ptr "+Memory.readPointer(methods_ptr)+",module " + module);
                //send("RegisterNativeMethod class = " + class_name + ", module = " + module.name + ", base = " + module.base);
				send("RegisterNativeMethod class = " + class_name);
                var method_count = parseInt(args[3]);
                send("registered methods count = " + method_count);
                // get registered native method info
                var offset = Process.pointerSize;
                for (var i = 0; i < method_count; i++) {
                    var name = Memory.readCString(Memory.readPointer(methods_ptr.add(offset*3*i)));
                    var sig = Memory.readCString(Memory.readPointer(methods_ptr.add(offset*3*i+offset)));
                    var address = Memory.readPointer(methods_ptr.add(offset*(3*i+2)));
                    //send("methods name = " + name + ", sig = " + sig + ", address = " + ptr(address) + ", offset = " + ptr(address).sub(module.base));
					send("methods name = " + name + ", sig = " + sig + ", address = " + ptr(address));
                }
            },
            onLeave: function() {}
        });
    }
}

send("start frida hook ~~~ ");
getRegisterInfo();