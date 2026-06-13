cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(__MODULE_NAME___unit_test)

zephyr_include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../drivers/__SUBSYS__/__DRIVER_BASE__)
