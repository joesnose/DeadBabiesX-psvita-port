# Vita v0.2 crash-fix test build

Based on upstream commit b72d61599c6f64d012847b98b9fda1c00c8b0dc3.

The v0.1 link included pthread_create but left pthread_cancel as an unresolved
weak symbol. VitaSDK libstdc++ uses the address of pthread_cancel as its thread
availability probe. Disassembly of a v0.1 rebuild confirms this probe evaluates
to zero, and std::thread creation takes the system_error/EPERM path. Host and
Join both create std::threads; the top-level exception handler then exits the
game. The same probe selects non-atomic shared_ptr reference counting. Sound
data is shared between gameplay and the SDL audio thread, so this also creates
a plausible heap-corruption path during gameplay. A physical-device crash dump
is needed to establish whether it caused the reported random gameplay crash.

The v0.2 link explicitly requires pthread_cancel from libpthread. The rebuilt
ELF defines the function and the thread probe has its nonzero address. LAN
pthread stacks are also increased from 32 KiB to 256 KiB to give the C++ worker
and newlib polling code more headroom. Poll alone reserves about 9 KiB in the
tested toolchain. No gameplay rules or network protocol were changed.

Build as described in README.md. The package is now named
DeadBabiesX-Vita-v0.2-crashfix.vpk, with application version 00.20 and the same
title ID DBXV00001. Install using VitaShell over the existing application; saves
remain in ux0:data/DeadBabiesX. Back up that directory first if desired.

Verify the ELF before packaging or distribution:

```
python3 tests/check_thread_link.py "$VITASDK/bin/arm-vita-eabi-nm" build/DeadBabiesXVita
```

This is a hardware-test build. On Vita, check solo gameplay, repeated weapon
pickups, Host/Cancel/Host, Join/Cancel/Join, an unreachable host, and a full LAN
round including pause, Play Again and disconnect. Use this build on both Vitas
for initial testing. Cross-platform play remains unverified.

If a crash remains, retain ux0:data/DeadBabiesX/native.log, any
lan-diagnostics.txt, the Vita error code and the corresponding ux0:data/*.psp2dmp
file if generated. Debug symbols matching this build are included in the
companion developer archive.
