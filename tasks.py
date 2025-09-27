import os
import sys

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


# @task
# def cbuild(
#     c,
#     debug=True,
#     tests=True,
#     sanitize_address=False,
#     sanitize_ub=False,
#     sanitize_leak=False,
#     quiet=False,
#     other_flags="",
#     install=False,
#     install_prefix="./installed",
# ):
#     flags = "-DCMAKE_BUILD_TYPE=" + ("Debug" if debug else "Release")
#     flags += " -DBUILD_TESTS=" + ("ON" if tests else "OFF")
#     flags += " -DSANITIZE_ADDRESS=" + ("ON" if sanitize_address else "OFF")
#     flags += " -DSANITIZE_UB=" + ("ON" if sanitize_ub else "OFF")
#     flags += " -DSANITIZE_LEAK=" + ("ON" if sanitize_leak else "OFF")
#     flags += " " + other_flags
#     command_postfix = "> /dev/null 2>&1" if quiet else ""
#     c.run(f"{sys.executable} -m cmake -S . -B build {flags} {command_postfix}", pty=True)
#     c.run(f"{sys.executable} -m cmake --build build {command_postfix}", pty=True)
#
#     if install:
#         c.run(
#             f"{sys.executable} -m cmake --install build --prefix {install_prefix}",
#             pty=True,
#         )
#
#
# @task(pre=[clear])
# def ctest(c, once=False):
#     # NOTE: this is needed to make the asan workable in our case
#     os.environ["ASAN_OPTIONS"] = "verify_asan_link_order=0"
#     if once:
#         cbuild(
#             c,
#             debug=True,
#             tests=True,
#             sanitize_address=False,
#             sanitize_ub=True,
#             sanitize_leak=True,
#             quiet=False,
#         )
#         _test_one(c)
#         return
#
#     for debug in [True, False]:
#         for additional_flags in [
#             {"sanitize_address": True},
#             {"sanitize_ub": True, "sanitize_leak": True},
#         ]:
#             print(f"Testing with debug={debug}, additional flags: {additional_flags}")
#             cbuild(c, debug=debug, tests=True, **additional_flags, quiet=True)
#             _test_one(c)
#             clear(c)
#
#
# def _test_one(c):
#     c.run(f"./build/tests/{PACKAGE_NAME}_test", pty=True)
