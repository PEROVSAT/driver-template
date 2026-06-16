cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(__MODULE_NAME___public_mock_test)

file(GLOB app_sources src/*.c)
target_sources(app PRIVATE ${app_sources})

zephyr_include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../../drivers/__SUBSYS__/__DRIVER_SLUG__)
