cmake_minimum_required(VERSION 3.10)
project(automatic-timetable-system)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        main.cpp
        Algorithm/Configuration.cpp
        Algorithm/Course.cpp
        Algorithm/CourseClass.cpp
        Algorithm/Professor.cpp
        Algorithm/Room.cpp
        Algorithm/Schedule.cpp
        Algorithm/StudentsGroup.cpp)

set(JSON_BuildTests OFF CACHE INTERNAL "")

add_executable(automatic-timetable-system ${SOURCE_FILES})
add_subdirectory(json)
target_link_libraries(automatic-timetable-system PRIVATE nlohmann_json::nlohmann_json)