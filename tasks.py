import os
import sys
import shlex

from invoke.tasks import task

PACKAGE_NAME: str = "noise_gate"

@task
def cfmt(c):
    print("Formatting the code ...")
    c.run(f"clang-format -i ./{PACKAGE_NAME}/*.*pp", pty=True)
    print("OK")


@task(aliases=["clean"])
def clear(c):
    c.run("rm -rf build installed dist", pty=True,)
    os.environ["ASAN_OPTIONS"] = ""


@task
def cbuild(
    c,
    debug=True,
    app=True,
    tests=True,
    sanitize_address=False,
    sanitize_ub=False,
    sanitize_leak=False,
    quiet=False,
    other_flags="",
    install=False,
    install_prefix="./installed",
):
    cmake_flags = [
        f"-DCMAKE_BUILD_TYPE={'Debug' if debug else 'Release'}",
        f"-DBUILD_APP={'ON' if app else 'OFF'}",
        f"-DBUILD_TESTS={'ON' if tests else 'OFF'}",
        f"-DSANITIZE_ADDRESS={'ON' if sanitize_address else 'OFF'}",
        f"-DSANITIZE_UB={'ON' if sanitize_ub else 'OFF'}",
        f"-DSANITIZE_LEAK={'ON' if sanitize_leak else 'OFF'}",
    ]
    if other_flags:
        cmake_flags.append(other_flags)

    flags_str = " ".join(cmake_flags)

    run_kwargs = {"pty": not quiet, "hide": quiet}

    c.run(f"{sys.executable} -m cmake -S . -B build {flags_str}", **run_kwargs)
    c.run(f"{sys.executable} -m cmake --build build", **run_kwargs)

    if install:
        c.run(
            f"{sys.executable} -m cmake --install build --prefix {shlex.quote(install_prefix)}",
            **run_kwargs,
        )


@task(pre=[clear])
def ctest(c, once=False):
    # NOTE: this is needed to make the asan workable in our case
    os.environ["ASAN_OPTIONS"] = "verify_asan_link_order=0"
    if once:
        cbuild(
            c,
            debug=True,
            tests=True,
            sanitize_address=False,
            sanitize_ub=True,
            sanitize_leak=True,
            quiet=False,
        )
        _test_one(c)
        return

    for debug in [True, False]:
        for additional_flags in [
            {"sanitize_address": True},
            {"sanitize_ub": True, "sanitize_leak": True},
        ]:
            print(f"Testing with debug={debug}, additional flags: {additional_flags}")
            cbuild(c, debug=debug, tests=True, **additional_flags, quiet=True)
            _test_one(c)
            clear(c)


def _test_one(c):
    c.run(f"./build/tests/{PACKAGE_NAME}_test", pty=True)


@task(post=[clear])
def pysync(c, dev=True, update_lock=False, verbose=False):
    cmd_postfix = ""
    if dev:
        cmd_postfix += " --extra dev"
    else:
        cmd_postfix += " --no-dev --no-editable"
    if verbose:
        cmd_postfix += " --verbose"
    if not update_lock:
        cmd_postfix += " --frozen"

    c.run(f"uv sync --active --inexact {cmd_postfix}", pty=True)
    _sync_requirements(c)


@task(post=[pysync], aliases=["pyupdate"])
def pyupgrade(c, verbose=False):
    cmd_postfix = ""
    if verbose:
        cmd_postfix += " --verbose"

    c.run(f"uv lock --upgrade {cmd_postfix}", pty=True)


@task(post=[clear], iterable=["p"])
def pyadd_dep(c, p, dev=False, update_lock=True, verbose=False):
    cmd_postfix = ""
    if dev:
        cmd_postfix += " --optional dev"
    if verbose:
        cmd_postfix += " --verbose"
    if not update_lock:
        cmd_postfix += " --frozen"

    packages = " ".join(p)

    c.run(f"uv add --active {cmd_postfix} {packages}", pty=True)
    _sync_requirements(c)


def _sync_requirements(c) -> None:
    common_cmd_postfix = (
        " --format requirements-txt --no-editable --no-emit-project --frozen --no-hashes -q"
    )
    c.run(f"uv export -o requirements.txt --no-dev {common_cmd_postfix} ", pty=True)
    c.run(f"uv export -o requirements-dev.txt --extra dev {common_cmd_postfix} ", pty=True)
