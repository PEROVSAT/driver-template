cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(__MODULE_NAME___unit_test)

file(GLOB app_sources src/*.c)
target_sources(app PRIVATE ${app_sources})

target_sources(app PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../../lib/__DRIVER_SLUG__/__DRIVER_SLUG___lib.c)
target_include_directories(app PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../../lib/__DRIVER_SLUG__)
