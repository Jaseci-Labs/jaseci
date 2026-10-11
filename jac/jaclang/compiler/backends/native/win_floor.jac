"""The Windows floor: what a PE image needs beneath the native runtime.

A Linux executable links musl and a Mach-O one libSystem, and both give the
runtime the C library it was written against. A Windows image imports the
Universal C Runtime (ucrtbase.dll, part of every supported Windows), which is
a C library but not a POSIX one, and not quite the hosted C library either: its
printf family is a set of inline wrappers in the SDK headers, its standard
streams are a function call, and it has no pthread keys.

The floor is the LLVM IR that closes that gap. It is linked into every PE
artifact with the rest of the link glue, defines the names the runtime calls
with their C library meaning, and implements them over ucrtbase and kernel32.
A name the floor does not define is imported from ucrtbase by the PE linker,
under the spelling `WIN_CRT_ALIAS` gives it when the UCRT spells it otherwise.
`WIN_FLOOR_IMPORTS` names the DLL of each system import the floor itself
makes that the UCRT does not provide.
"""

glob WIN_CRT_DLL: str = "ucrtbase.dll";

"""C library names the UCRT exports under another spelling, with the same
arguments in the registers the Win64 convention passes them in."""
glob WIN_CRT_ALIAS: dict[str, str] = {
    "malloc_usable_size": "_msize",
    "strdup": "_strdup",
    "getpid": "_getpid",
    "getcwd": "_getcwd",
    "chdir": "_chdir",
    "rmdir": "_rmdir",
    "unlink": "_unlink",
    "access": "_access",
    "fileno": "_fileno",
    "isatty": "_isatty",
    "close": "_close",
    "read": "_read",
    "write": "_write",
    "dup": "_dup",
    "dup2": "_dup2",
    "strcasecmp": "_stricmp",
    "strncasecmp": "_strnicmp",
    "fseek": "_fseeki64",
    "ftell": "_ftelli64",
    "fseeko": "_fseeki64",
    "ftello": "_ftelli64",
    "lseek": "_lseeki64",
    "putenv": "_putenv",
    "tzset": "_tzset",
    "timegm": "_mkgmtime64",
    "mktime": "_mktime64",
    "time": "_time64",
    "strtok_r": "strtok_s",
    "_exit": "_Exit",
    "j0": "_j0",
    "j1": "_j1",
    "y0": "_y0",
    "y1": "_y1"
};

"""The DLL behind each system call the floor makes outside the UCRT."""
glob WIN_FLOOR_IMPORTS: dict[str, str] = {
    "__chkstk": "kernel32.dll",
    "FlsAlloc": "kernel32.dll",
    "FlsGetValue": "kernel32.dll",
    "FlsSetValue": "kernel32.dll",
    "SetConsoleOutputCP": "kernel32.dll",
    "SetConsoleCP": "kernel32.dll"
};

"""Logical C library names whose functions the UCRT holds on Windows: an
`import from c` or `import from m` binds the CRT, not a DLL of that name."""
glob WIN_CRT_LIBRARIES: list[str] = [
    "c.dll", "m.dll", "pthread.dll", "dl.dll", "rt.dll", "msvcrt.dll"
];

def win_import_dll(name: str, declared: (str | None)) -> str {
    """The DLL a PE image imports `name` from. `declared` is the library the
    program named for it, if it named one.""";
    import os;
    if declared {
        base = os.path.basename(declared.replace("\\", "/"));
        if base.lower().endswith(".dll") and base.lower() not in WIN_CRT_LIBRARIES {
            return base;
        }
    }
    return WIN_FLOOR_IMPORTS.get(name, WIN_CRT_DLL);
}

def win_import_name(name: str) -> str {
    """The spelling `name` is imported under.""";
    return WIN_CRT_ALIAS.get(name, name);
}

def _win_jmp_ir -> str {
    """`__jac_setjmp` and `__jac_longjmp`: the pair native exception frames arm
    and raise through. The UCRT's `longjmp` unwinds through the image's
    exception tables, which a Jac image does not carry, so the floor keeps its
    own pair: the Win64 callee-saved state (rbx, rbp, rsi, rdi, r12-r15, rsp,
    the return address and xmm6-xmm15) in 240 bytes, with no unwind.""";
    lines = [
        ".text",
        ".globl __jac_setjmp",
        ".p2align 4",
        "__jac_setjmp:",
        "movq %rbx, 0(%rcx)",
        "movq %rbp, 8(%rcx)",
        "movq %rsi, 16(%rcx)",
        "movq %rdi, 24(%rcx)",
        "movq %r12, 32(%rcx)",
        "movq %r13, 40(%rcx)",
        "movq %r14, 48(%rcx)",
        "movq %r15, 56(%rcx)",
        "leaq 8(%rsp), %rax",
        "movq %rax, 64(%rcx)",
        "movq (%rsp), %rax",
        "movq %rax, 72(%rcx)",
        "movups %xmm6, 80(%rcx)",
        "movups %xmm7, 96(%rcx)",
        "movups %xmm8, 112(%rcx)",
        "movups %xmm9, 128(%rcx)",
        "movups %xmm10, 144(%rcx)",
        "movups %xmm11, 160(%rcx)",
        "movups %xmm12, 176(%rcx)",
        "movups %xmm13, 192(%rcx)",
        "movups %xmm14, 208(%rcx)",
        "movups %xmm15, 224(%rcx)",
        "xorl %eax, %eax",
        "retq",
        ".globl __jac_longjmp",
        ".p2align 4",
        "__jac_longjmp:",
        "movl %edx, %eax",
        "testl %eax, %eax",
        "jne 1f",
        "movl $1, %eax",
        "1:",
        "movq 0(%rcx), %rbx",
        "movq 8(%rcx), %rbp",
        "movq 16(%rcx), %rsi",
        "movq 24(%rcx), %rdi",
        "movq 32(%rcx), %r12",
        "movq 40(%rcx), %r13",
        "movq 48(%rcx), %r14",
        "movq 56(%rcx), %r15",
        "movups 80(%rcx), %xmm6",
        "movups 96(%rcx), %xmm7",
        "movups 112(%rcx), %xmm8",
        "movups 128(%rcx), %xmm9",
        "movups 144(%rcx), %xmm10",
        "movups 160(%rcx), %xmm11",
        "movups 176(%rcx), %xmm12",
        "movups 192(%rcx), %xmm13",
        "movups 208(%rcx), %xmm14",
        "movups 224(%rcx), %xmm15",
        "movq 64(%rcx), %rsp",
        "jmpq *72(%rcx)"
    ];
    return "".join([f'module asm "{line}"\n' for line in lines]) + "\n";
}

def _win_stdio_ir -> str {
    """The standard streams and the printf family. The UCRT hands out its
    streams through `__acrt_iob_func` and formats through the
    `__stdio_common_*` entry points its headers wrap; option 2 asks those for
    C99 `snprintf` truncation, which returns the length the text needed.""";
    return (
        "@stdin = global ptr null\n"
        "@stdout = global ptr null\n"
        "@stderr = global ptr null\n\n"
        "declare ptr @__acrt_iob_func(i32)\n"
        "declare i32 @__stdio_common_vfprintf(i64, ptr, ptr, ptr, ptr)\n"
        "declare i32 @__stdio_common_vsprintf(i64, ptr, i64, ptr, ptr, ptr)\n"
        "declare i32 @__stdio_common_vsscanf(i64, ptr, i64, ptr, ptr, ptr)\n"
        "declare void @llvm.va_start(ptr)\n"
        "declare void @llvm.va_end(ptr)\n\n"
        "define i32 @printf(ptr %fmt, ...) {\n"
        "entry:\n"
        "  %ap = alloca ptr\n"
        "  call void @llvm.va_start(ptr %ap)\n"
        "  %args = load ptr, ptr %ap\n"
        "  %out = load ptr, ptr @stdout\n"
        "  %r = call i32 @__stdio_common_vfprintf(i64 0, ptr %out, ptr %fmt, ptr null, ptr %args)\n"
        "  call void @llvm.va_end(ptr %ap)\n"
        "  ret i32 %r\n"
        "}\n\n"
        "define i32 @fprintf(ptr %stream, ptr %fmt, ...) {\n"
        "entry:\n"
        "  %ap = alloca ptr\n"
        "  call void @llvm.va_start(ptr %ap)\n"
        "  %args = load ptr, ptr %ap\n"
        "  %r = call i32 @__stdio_common_vfprintf(i64 0, ptr %stream, ptr %fmt, ptr null, ptr %args)\n"
        "  call void @llvm.va_end(ptr %ap)\n"
        "  ret i32 %r\n"
        "}\n\n"
        "define i32 @snprintf(ptr %buf, i64 %size, ptr %fmt, ...) {\n"
        "entry:\n"
        "  %ap = alloca ptr\n"
        "  call void @llvm.va_start(ptr %ap)\n"
        "  %args = load ptr, ptr %ap\n"
        "  %r = call i32 @__stdio_common_vsprintf(i64 2, ptr %buf, i64 %size, ptr %fmt, ptr null, ptr %args)\n"
        "  call void @llvm.va_end(ptr %ap)\n"
        "  %failed = icmp slt i32 %r, 0\n"
        "  %out = select i1 %failed, i32 -1, i32 %r\n"
        "  ret i32 %out\n"
        "}\n\n"
        "define i32 @sprintf(ptr %buf, ptr %fmt, ...) {\n"
        "entry:\n"
        "  %ap = alloca ptr\n"
        "  call void @llvm.va_start(ptr %ap)\n"
        "  %args = load ptr, ptr %ap\n"
        "  %r = call i32 @__stdio_common_vsprintf(i64 2, ptr %buf, i64 -1, ptr %fmt, ptr null, ptr %args)\n"
        "  call void @llvm.va_end(ptr %ap)\n"
        "  %failed = icmp slt i32 %r, 0\n"
        "  %out = select i1 %failed, i32 -1, i32 %r\n"
        "  ret i32 %out\n"
        "}\n\n"
        "declare i64 @strlen(ptr)\n\n"
        "define i32 @sscanf(ptr %text, ptr %fmt, ...) {\n"
        "entry:\n"
        "  %ap = alloca ptr\n"
        "  call void @llvm.va_start(ptr %ap)\n"
        "  %args = load ptr, ptr %ap\n"
        "  %n = call i64 @strlen(ptr %text)\n"
        "  %r = call i32 @__stdio_common_vsscanf(i64 0, ptr %text, i64 %n, ptr %fmt, ptr null, ptr %args)\n"
        "  call void @llvm.va_end(ptr %ap)\n"
        "  ret i32 %r\n"
        "}\n\n"
    );
}

def _win_tls_ir -> str {
    """pthread keys over fiber-local storage, which runs a slot's destructor
    when its thread exits as a pthread key does. The runtime keeps a key in 64
    bits; an FLS index is 32.""";
    return (
        "declare i32 @FlsAlloc(ptr)\n"
        "declare ptr @FlsGetValue(i32)\n"
        "declare i32 @FlsSetValue(i32, ptr)\n\n"
        "define i32 @pthread_key_create(ptr %key, ptr %destructor) {\n"
        "entry:\n"
        "  %index = call i32 @FlsAlloc(ptr %destructor)\n"
        "  %wide = zext i32 %index to i64\n"
        "  store i64 %wide, ptr %key\n"
        "  %failed = icmp eq i32 %index, -1\n"
        "  %r = select i1 %failed, i32 11, i32 0\n"
        "  ret i32 %r\n"
        "}\n\n"
        "define ptr @pthread_getspecific(i64 %key) {\n"
        "entry:\n"
        "  %index = trunc i64 %key to i32\n"
        "  %v = call ptr @FlsGetValue(i32 %index)\n"
        "  ret ptr %v\n"
        "}\n\n"
        "define i32 @pthread_setspecific(i64 %key, ptr %value) {\n"
        "entry:\n"
        "  %index = trunc i64 %key to i32\n"
        "  %ok = call i32 @FlsSetValue(i32 %index, ptr %value)\n"
        "  %failed = icmp eq i32 %ok, 0\n"
        "  %r = select i1 %failed, i32 22, i32 0\n"
        "  ret i32 %r\n"
        "}\n\n"
    );
}

def _win_init_ir -> str {
    """`__jac_win_floor_init`, run before any Jac code: it binds the standard
    streams and makes UTF-8 the encoding of the console and of the narrow
    strings the UCRT takes for paths (LC_CTYPE only, so number formatting
    keeps the C locale).""";
    return (
        '@.jac.win.utf8 = private unnamed_addr constant [7 x i8] c".UTF-8\\00"\n'
        "declare ptr @setlocale(i32, ptr)\n"
        "declare i32 @SetConsoleOutputCP(i32)\n"
        "declare i32 @SetConsoleCP(i32)\n\n"
        "define void @__jac_win_floor_init() {\n"
        "entry:\n"
        "  %in = call ptr @__acrt_iob_func(i32 0)\n"
        "  store ptr %in, ptr @stdin\n"
        "  %out = call ptr @__acrt_iob_func(i32 1)\n"
        "  store ptr %out, ptr @stdout\n"
        "  %err = call ptr @__acrt_iob_func(i32 2)\n"
        "  store ptr %err, ptr @stderr\n"
        "  %loc = call ptr @setlocale(i32 2, ptr @.jac.win.utf8)\n"
        "  %cp.out = call i32 @SetConsoleOutputCP(i32 65001)\n"
        "  %cp.in = call i32 @SetConsoleCP(i32 65001)\n"
        "  ret void\n"
        "}\n\n"
    );
}

def win_floor_ir -> str {
    """The floor's IR, for the link glue of a PE artifact.""";
    return "; --- Windows floor ---\n"
        + _win_jmp_ir()
        + _win_stdio_ir()
        + _win_tls_ir()
        + _win_init_ir();
}
