var ishook_libart = false;

function hook_libart() {
    if (ishook_libart === true) {
        return;
    }

	console.log(Module.findExportByName('libcms.so', 'JNI_OnLoad'));

    ishook_libart = true;
}

hook_libart();

//frida -U com.ss.android.ugc.aweme -l hook_so.js