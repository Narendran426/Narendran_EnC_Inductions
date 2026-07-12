cmake_minimum_required(VERSION 3.8)
project(kratos_naren)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -std=c++17)
endif()

# Find basic ament tools
find_package(ament_cmake REQUIRED)

# Install the Python scripts from the src/ folder
install(PROGRAMS
  src/rover_status_publisher.py
  src/rover_status_subscriber.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files so 'ros2 launch' can find them
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()