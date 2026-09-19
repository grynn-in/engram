# `import importlib.util` does not give you `importlib.machinery`

**Symptom**: `engram compound` raised
`AttributeError: module 'importlib' has no attribute 'machinery'` on line 31 —
on every invocation, on every platform, since the commit that introduced it.
Nobody had ever run it successfully. It was advertised in `engram --help`.

**Cause**: the file did `import importlib.util` at line 30, used
`importlib.machinery.SourceFileLoader` at line 31, and imported
`importlib.machinery` at line 36 — five lines too late. Importing a submodule
binds the *parent package name*, so `importlib` exists and the attribute access
looks perfectly ordinary. Only the specific submodule you imported is attached.

**Cost**: ~1 hour to find, but the command had been 100% broken for months.

**Avoid**:
- Import every submodule you touch, at the top, explicitly.
- **pyflakes does not catch this.** It sees `importlib` bound and an attribute
  access on it; there is no undefined name. I ran pyflakes over the whole tree
  and it reported zero undefined names while this bug was live. The only thing
  that finds it is executing the code path.

**Discovered**: 2026-09-19, first untested command poked at. Fixed in a418d2a.

Related: [exit-zero defects](commands-that-exit-zero-and-do-nothing.md), [the importlib trap](compound-crashed-on-importlib-machinery.md)
