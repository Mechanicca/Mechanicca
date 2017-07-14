#!/usr/bin/python

import sys, getopt, sqlite3

class ParameterTagCollectionGenerator:

	# Constructor
	def __init__( self, argv ):
		self.HeaderFileHeader = \
'''/*
 * <COMPNAME>ParameterTagCollection.h
 *
 *  [GENERATED FILE - Do not edit manually]

 *  Author: Martin Kopecky <martin.monster696@gmail.com>
 */

#ifndef GENERATED_<COMPNAME_UPPERCASE>_PARAMETERTAGCOLLECTION_H_
#define GENERATED_<COMPNAME_UPPERCASE>_PARAMETERTAGCOLLECTION_H_

/* Standard library inclusions */
#include <type_traits>

/* Project specific inclusions */
#include "Parameter/IParameterTagCollection.h"
#include "Parameter/Parameter.h"

/* Shared library support */
#include "<COMPNAME>/<COMPNAME>Export.h"
/* As Gear_Export.h header is generated during build, the required <COMPNAME_UPPERCASE>_EXPORT
 * definition might not exist due to missing header file. In order to prevent
 * syntax errors cause by undefined <COMPNAME_UPPERCASE>_EXPORT, define temporary blank one */
/* [GENERATED] */
#ifndef <COMPNAME_UPPERCASE>_EXPORT
	#define <COMPNAME_UPPERCASE>_EXPORT
	#define <COMPNAME_UPPERCASE>_NO_EXPORT
#endif

struct <COMPNAME_UPPERCASE>_EXPORT <COMPNAME>ParameterTagCollection
	:	public Core::IParameterTagCollection
{'''
		self.ElementDeclaration = \
'''
	struct <COMPNAME_UPPERCASE>_EXPORT <ELEMENT_NAME> 
		:	public IParameterTag
	{
		/* <ELEMENT_NAME> parameter's unit type definition */
		using TUnit = boost::units::<ELEMENT_UNIT_TYPE>;
		/* <ELEMENT_NAME> parameter's data type definition */
		using TData = <ELEMENT_DATA_TYPE>;
		/* <ELEMENT_NAME> parameter's data type definition */
		using TParameter = Core::Parameter<TUnit, TData>;
		/* <ELEMENT_NAME> parameter's DesignRules DB ID */
		using ID = std::integral_constant<IParameterTag::TIdentifier, <ELEMENT_VALUE>>;
	};
'''


		self.HeaderFileFooter = \
'''
#endif /* GENERATED_<COMPNAME_UPPERCASE>_CONSTRAINEDPARAMETERIDENTIFICATION_H_ */

'''
		# Parse script input arguments and store the filenames to class
		# member variables
		self.ParseArguments( argv )

		# Connect SQLite3 DesignRules database
		[self.DBConnection, self.DBCursor] = self.ConnectDesignRulesDB( self.DatabaseFileName )

		# Create / open generated header file
		self.GeneratedHeaderFile = open( self.OutputFileName, "w" )

		self.GenerateHeader()

	# Destructor
	def __del__( self ):
		# Close DesignRules DB connection
		self.DBConnection.close()
		# Close generated file
		self.GeneratedHeaderFile.close()

	# Main method - generate output header file
	def GenerateHeader( self ):
		# Write HEADER
		self.HeaderFileHeader = self.HeaderFileHeader.replace( "<COMPNAME>", self.Component )
		self.HeaderFileHeader = self.HeaderFileHeader.replace( "<COMPNAME_UPPERCASE>", self.Component.upper() )
		self.GeneratedHeaderFile.write( self.HeaderFileHeader )

		# Process and write Identification group declaration
		#self.IdentificationGroupDeclaration = self.IdentificationGroupDeclaration.replace( "<COMPNAME>", self.Component );
		#self.IdentificationGroupDeclaration = self.IdentificationGroupDeclaration.replace( "<COMPNAME_UPPERCASE>", self.Component.upper() );
		#self.GeneratedHeaderFile.write( self.IdentificationGroupDeclaration );
		#self.GeneratedHeaderFile.write( "\t{" )

		# Process and write element base declaration
		#self.GeneratedHeaderFile.write( self.ElementBaseDeclaration );

		# Process all the elements
		# Select all parameter identifications related to processed component...
		self.DBCursor = self.DBConnection.execute( "SELECT Identification,ID,UnitType,DataType FROM Parameters WHERE Component=?", [self.Component] )
		# ... and iterate through all of them
		for row in self.DBCursor:
			currentElementDeclaration = self.ElementDeclaration;
			currentElementDeclaration = currentElementDeclaration.replace( "<COMPNAME_UPPERCASE>", self.Component.upper() );
			currentElementDeclaration = currentElementDeclaration.replace( "<ELEMENT_NAME>", str( row[0] ) );
			currentElementDeclaration = currentElementDeclaration.replace( "<ELEMENT_UNIT_TYPE>", str( row[2] ) );
			currentElementDeclaration = currentElementDeclaration.replace( "<ELEMENT_DATA_TYPE>", str( row[3] ) );
			currentElementDeclaration = currentElementDeclaration.replace( "<ELEMENT_VALUE>", str( row[1] ) );
			self.GeneratedHeaderFile.write( currentElementDeclaration );

		# Finalize Identification group declaration
		self.GeneratedHeaderFile.write( "};\n" )

		# Write FOOTER
		self.HeaderFileFooter = self.HeaderFileFooter.replace( "<COMPNAME_UPPERCASE>", self.Component.upper() )
		self.GeneratedHeaderFile.write( self.HeaderFileFooter )

	# Connect to DesignRulesDB and return the connection object as well as sqlite3 cursor
	def ConnectDesignRulesDB( self, DBFileName ):
		try:
			# Connect to SQLite3 database
			DB = sqlite3.connect( DBFileName )
			# Create cursor to access the database
			Cursor = DB.cursor()
		except sqlite3.Error:
			# Something went wrong while connecting the database. Exit...
			print "DesignRules database not connected."
			sys.exit(2)
		return [DB, Cursor]

	# Process all script input parameters
	def ParseArguments( self, argv ):
		# Declare filenames
		self.OutputFileName = ''
		self.DatabaseFileName = ''
		self.Component = ''
		try:
			# Parse script input argument
			opts, args = getopt.getopt(argv,"ho:d:c:p:",["output=", "database=", "component=", "pluginpath="])
		except getopt.GetoptError:
			# Display help when unsupported argument is set up...
			print '-o <OutputFileName> -d <DatabaseFileName> -c <Component> -p <Plugin path>'
			# ...and exit the script
			sys.exit(2)
		# Iterate through the options
		for opt, arg in opts:
			# Help...
			if opt == '-h':
				print '-o <OutputFileName> -d <DatabaseFileName> -c <Component> -p <Plugin path>'
				sys.exit()
			# Output file settings
			elif opt in ("-o", "--output"):
				self.OutputFileName = arg
			# Database file settings
			elif opt in ("-d", "--database"):
				self.DatabaseFileName = arg			
			# Component settings
			elif opt in ("-c", "--component"):
				self.Component = arg
	
# Script main()
def main( argv ):
	# Instantiate generator
	Generator = ParameterTagCollectionGenerator( argv )

# Script entry point	
if __name__ == "__main__":
	main( sys.argv[1:] )
