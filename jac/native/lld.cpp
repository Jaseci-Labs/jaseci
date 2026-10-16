#include "core.h"

#include "lld/Common/Driver.h"
#include "llvm/ADT/ArrayRef.h"
#include "llvm/ADT/StringRef.h"
#include "llvm/BinaryFormat/COFF.h"
#include "llvm/Object/COFFImportFile.h"
#include "llvm/Support/Error.h"
#include "llvm/Support/raw_ostream.h"

#include <string>
#include <vector>

LLD_HAS_DRIVER(elf)
LLD_HAS_DRIVER(macho)
LLD_HAS_DRIVER(coff)
LLD_HAS_DRIVER(wasm)

extern "C" {

// Run one LLD link in-process. argv[0] names the flavor the way the LLD
// binaries do ("ld.lld", "ld64.lld", "lld-link", "wasm-ld"); the rest are the
// linker's own command-line arguments. Returns the linker's exit code and
// hands back everything it printed. A link that crashed leaves LLD unable to
// run again in this process; *CanRunAgain reports that.
API_EXPORT(int)
LLVMPY_LldLink(const char **Argv, size_t Argc, const char **Out,
               int *CanRunAgain) {
    std::string text;
    llvm::raw_string_ostream os(text);
    std::vector<const char *> args(Argv, Argv + Argc);
    lld::Result result = lld::lldMain(
        args, os, os,
        {{lld::Gnu, &lld::elf::link},
         {lld::Darwin, &lld::macho::link},
         {lld::WinLink, &lld::coff::link},
         {lld::Wasm, &lld::wasm::link}});
    os.flush();
    *Out = LLVMPY_CreateString(text.c_str());
    *CanRunAgain = result.canRunAgain ? 1 : 0;
    return result.retCode;
}

// Write a COFF import library that binds Names to DllName, so lld-link can
// name a DLL the link never sees. Machine is an IMAGE_FILE_MACHINE_* value.
// Returns 0 on success, otherwise 1 with the reason in *Err.
API_EXPORT(int)
LLVMPY_WriteImportLibrary(const char *DllName, const char *Path,
                          unsigned Machine, const char **Names,
                          const int *IsData, size_t Count, const char **Err) {
    std::vector<llvm::object::COFFShortExport> exports;
    exports.reserve(Count);
    for (size_t i = 0; i < Count; ++i) {
        llvm::object::COFFShortExport e;
        e.Name = Names[i];
        e.Data = IsData[i] != 0;
        exports.push_back(e);
    }
    llvm::Error failed = llvm::object::writeImportLibrary(
        DllName, Path, exports,
        static_cast<llvm::COFF::MachineTypes>(Machine), false);
    if (failed) {
        *Err = LLVMPY_CreateString(llvm::toString(std::move(failed)).c_str());
        return 1;
    }
    return 0;
}

} // end extern "C"
