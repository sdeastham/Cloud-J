# Cloud-J/src/CMakeLists.txt

add_library(CloudJ_Py STATIC EXCLUDE_FROM_ALL
	CJ77.f90
)
target_link_libraries(CloudJ_Py
	PUBLIC CloudJ_Core
)
target_include_directories(CloudJ_Py
        INTERFACE ${CLOUDJ_BINARY_DIR}/mod
)
target_compile_options(CloudJ_Py
        PRIVATE
                ""
                $<$<STREQUAL:"${CMAKE_Fortran_COMPILER_ID}","GNU">:-ffree-line-length-none>
)

#install(TARGETS cloudj_py
#        RUNTIME DESTINATION ${RUNDIR}
#)
##if("cloudj_py" IN_LIST CLOUDJ_EXE_TARGETS)
#        add_executable(cloudj_py
#                CJ77.f90
#        )
#        target_link_libraries(cloudj_py
#                PUBLIC CloudJ_Py
#        )
#        set_target_properties(cloudj_py PROPERTIES
#                RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
#        install(TARGETS cloudj_py
#                RUNTIME DESTINATION ${RUNDIR}
#        )
##endif()
