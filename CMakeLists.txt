cmake_minimum_required(VERSION 3.20)

project(WG21-Papers LANGUAGES NONE)

find_package(Python3 3.12 REQUIRED COMPONENTS Interpreter)

set(VENV_DIR "${CMAKE_CURRENT_BINARY_DIR}/venv")
if(WIN32)
    set(VENV_PYTHON "${VENV_DIR}/Scripts/python.exe")
else()
    set(VENV_PYTHON "${VENV_DIR}/bin/python")
endif()

if(NOT EXISTS "${VENV_PYTHON}")
    execute_process(
        COMMAND "${Python3_EXECUTABLE}" -m venv "${VENV_DIR}"
        COMMAND_ERROR_IS_FATAL ANY
    )
endif()

execute_process(
    COMMAND "${VENV_PYTHON}" -m pip install --disable-pip-version-check
            -r "${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt"
    COMMAND_ERROR_IS_FATAL ANY
)
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS requirements.txt)

set(PAPER_DIR "${CMAKE_CURRENT_SOURCE_DIR}" CACHE PATH "Directory containing .bs papers")
set(OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated" CACHE PATH "Directory for generated papers")
file(GLOB papers CONFIGURE_DEPENDS "${PAPER_DIR}/*.bs")

if(NOT papers)
    message(FATAL_ERROR "No .bs papers found in ${PAPER_DIR}")
endif()

foreach(source IN LISTS papers)
    get_filename_component(name "${source}" NAME_WE)
    set(output "${OUTPUT_DIR}/${name}.html")

    add_custom_command(
        OUTPUT "${output}"
        COMMAND "${CMAKE_COMMAND}" -E make_directory "${OUTPUT_DIR}"
        COMMAND "${VENV_PYTHON}" -m bikeshed --no-update --die-on warning
                spec "${source}" "${output}"
        DEPENDS "${source}"
        COMMENT "Building ${name}.html"
        VERBATIM
    )

    list(APPEND outputs "${output}")
    string(REPLACE " " "_" target_name "${name}")
    add_custom_target("paper-${target_name}" DEPENDS "${output}")
endforeach()

add_custom_target(papers ALL DEPENDS ${outputs})
