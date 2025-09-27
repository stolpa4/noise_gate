cmake_minimum_required(VERSION 3.31)
project(noise_gate C)

set(CMAKE_C_STANDARD 17)

add_library(noise_gate SHARED library.c)
