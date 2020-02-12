# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 12:53:25 2019

@author: Brock
"""

"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }


def read_csv_as_nested_dict(filename, infodict, keyfield):
    
    table = {}
    with open(filename, "rt", newline='') as csvfile:
        csvreader = csv.DictReader(csvfile,
                                    skipinitialspace=True,
                                    delimiter=infodict['separator'],
                                    quotechar = infodict['quote'])
        
        for row in csvreader:
            rowid = row[infodict[keyfield]]
            table[rowid] = dict(row)
    return table


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    result = {}
    with open(codeinfo['codefile'], newline='') as codefile:
        csvreader = csv.DictReader(codefile,
                                   skipinitialspace=True,
                                   delimiter=codeinfo['separator'],
                                   quotechar=codeinfo['quote'])
        
        for line in csvreader:
             result[line[codeinfo['plot_codes']]] = line[codeinfo['data_codes']]
    
    return result
    


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    cc_converter = build_country_code_converter(codeinfo)

    result_dict = {}
    result_set = set()
    
#    for ccode, cname in plot_countries.items():
        
        
    for ccode, cname in plot_countries.items(): 
        if ccode.upper() in cc_converter.keys():
            code = ccode.upper()
            converted_key = cc_converter[code]
            if converted_key in gdp_countries.keys():
                result_dict[ccode] = converted_key
            elif converted_key not in gdp_countries.keys():
                result_set.add(ccode)
                
        elif ccode.upper() in cc_converter.keys():
            code = ccode.lower()
            converted_key = cc_converter[code]
            if converted_key in gdp_countries.keys():
                result_dict[ccode] = converted_key
            elif converted_key not in gdp_countries.keys():
                result_set.add(ccode)

        elif cname.upper() in cc_converter.keys():
            code = cname.upper()
            converted_key = cc_converter[code]
            if converted_key in gdp_countries.keys():
                result_dict[cname] = converted_key
            elif converted_key not in gdp_countries.keys():
                result_set.add(cname)

        elif cname.upper() in cc_converter.keys():
            code = cname.lower()
            converted_key = cc_converter[code]
            if converted_key in gdp_countries.keys():
                result_dict[cname] = converted_key
            elif converted_key not in gdp_countries.keys():
                result_set.add(cname)        
            
    return (result_dict, result_set)


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_data = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo, 'country_code')
#    print('gdp_data:',gdp_data)
    converter = build_country_code_converter(codeinfo)
    print("")
    print('converter:', converter)
    print("")
    reconciled = reconcile_countries_by_code(codeinfo, plot_countries, gdp_data)
    recon = reconciled[0]
    print('recon:', recon)

    result_dict = {}
    missing_set = set()
    empty_set = set()
    
#    for ccode, cname in plot_countries.items():
#        if recon[ccode] in gdp_data.keys():
#            if len(gdp_data[recon[ccode]][year]) > 0:
#                gdp_value = float(gdp_data[recon[ccode]][year])
#                gdp_log = math.log10(gdp_value)
#                result_dict[ccode] = gdp_log
#            elif len(gdp_data[recon[ccode]][year]) <= 0:
#                empty_set.add(ccode)
#        elif recon[ccode] not in gdp_data.keys():
#            missing_set.add(ccode)
#            
#            
#    
    return (result_dict, missing_set, empty_set)



def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    map_plot = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
    
    gdpMap = pygal.maps.world.World()
    gdpMap.title = 'GDP Data by Country'
    gdp = 'GDP for ' + year
    
    empty = 'No Data'
    gdpMap.add(gdp, map_plot[0])
    gdpMap.add('Missing from Wolrd Bank data', map_plot[1])
    gdpMap.add(empty, map_plot[2])
    gdpMap.render()
    gdpMap.render_in_browser()
    
    
    return


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()