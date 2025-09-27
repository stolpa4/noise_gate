cmake_minimum_required(VERSION 3.23)

## Common things
################

if (NOT DEFINED CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 20)
endif()

set(CMAKE_CXX_EXTENSIONS OFF)

project(
        noise_gate
        VERSION 1.0.0
        DESCRIPTION "C++ library for audio noise reduction"
        LANGUAGES CXX C)

## Library and sources
######################

add_library(noise_gate SHARED noise_gate/noise_gate.cpp)
