cmake_minimum_required(VERSION 3.12)
project(handler LANGUAGES CXX VERSION 0.0.1)
set(CMAKE_CXX_STANDARD 17)

option(ENABLE_TESTING "build tests" OFF)
if(ENABLE_TESTING)
  enable_testing()
endif()

include_directories(hdr/)
add_subdirectory(src)
