#
# http://root.cern.ch/viewvc/trunk/cint/reflex/cmake/modules/FindCppUnit.cmake
#
# - Find CppUnit
# This module finds an installed CppUnit package.
#
# It sets the following variables:
#  CPPUNIT_FOUND       - Set to false, or undefined, if CppUnit isn't found.
#  CPPUNIT_INCLUDE_DIR - The CppUnit include directory.
#  CPPUNIT_LIBRARY     - The CppUnit library to link against.

find_path( CPPUNIT_INCLUDE_DIR cppunit/Test.h )
find_library( CPPUNIT_LIBRARY NAMES cppunit )

if( CPPUNIT_INCLUDE_DIR AND CPPUNIT_LIBRARY )
   set( CPPUNIT_FOUND TRUE )
endif()

if( CPPUNIT_FOUND )

   # show which CppUnit was found only if not quiet
   if( NOT CppUnit_FIND_QUIETLY )
      message ( STATUS "Found CppUnit: ${CPPUNIT_LIBRARY}" )
   endif()

else()

   # fatal error if CppUnit is required but not found
   if( CppUnit_FIND_REQUIRED )
      message( FATAL_ERROR "Could not find CppUnit" )
   endif()

endif()
