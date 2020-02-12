# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:10:42 2019

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
#    
    result_dict = {}
    result_set = set()
#    temp_dict = {}
#    temp_set = set()
    
    converter = build_country_code_converter(codeinfo)
#
#
#
    temp_converter = {}
    for key, values in converter.items():
        temp_converter[key.upper()] = values.upper()
    
    temp_plot = {}
    for keys, values in plot_countries.items():
        temp_plot[keys.upper()] = keys
    
    temp_gdp = {}
    for keys, values in gdp_countries.items():
        temp_gdp[keys.upper()] = keys

    for plot_key, real_key in temp_plot.items():
        if plot_key in temp_converter.keys():
            if temp_converter[plot_key] in temp_gdp.keys():
                result_dict[real_key] = temp_gdp[temp_converter[plot_key]]
            elif temp_converter[plot_key] not in temp_gdp.keys():
                result_set.add(real_key)
        elif plot_key not in temp_converter.keys():
            result_set.add(real_key)
                
        
        
#    for key in temp_plot.keys():
#        if key in temp_converter.keys():
#            if temp_converter[key] in temp_gdp.keys():
#                if key.lower() in plot_countries:
#                    result_dict[key.lower()] =  temp_gdp[temp_converter[key]]
#                elif key.upper() in plot_countries:
#                    result_dict[key.upper()] =  temp_gdp[temp_converter[key]]
#            elif temp_converter[key] not in temp_gdp.keys():
#                if key.lower() in plot_countries:
#                    result_set.add(key.lower())
#                elif key.upper() in plot_countries:
#                    result_set.add(key.upper())
#        if key not in temp_converter.keys():
#            if key.lower() in plot_countries:
#                result_set.add(key.lower())
#            elif key.upper() in plot_countries:
#                result_set.add(key.upper())
                
#    for key, value in gdp_countries.items():
#        if key in result_dict:
                
#    for pc_key in plot_countries.keys():
#        pc_upper = pc_key.upper()
#        if pc_upper in converter.keys():
#            test_key = converter[pc_upper]
#            if test_key.lower() in gdp_countries.keys():
#                result_dict[pc_key] = test_key
#            elif test_key.upper() in gdp_countries.keys():
#                result_dict[pc_key] = test_key
#            elif test_key not in gdp_countries.keys():
#                result_set.add(pc_key)
#        elif pc_key in converter.keys():
#            test_key = converter[pc_key]
#            if test_key.lower() in gdp_countries.keys():
#                result_dict[pc_key] = test_key
#            elif test_key.upper() in gdp_countries.keys():
#                result_dict[pc_key] = test_key
#            elif test_key not in gdp_countries.keys():
#                result_set.add(pc_key)
#        elif pc_key or pc_upper not in converter.keys():
#            result_set.add(pc_key)
       

    
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
    print('gdp_data:',gdp_data)
    converter = build_country_code_converter(codeinfo)
    print("")
    print('converter:', converter)
    print("")
    reconciled = reconcile_countries_by_code(codeinfo, plot_countries, gdp_data)
    recon = reconciled[0]
    print('recon:', recon)
    print("")
    print('plot_countries:', plot_countries)
    print("")

    result_dict = {}
    missing_set = set()
    empty_set = set()
    
    for ccode, cname in plot_countries.items():
        if ccode in recon.keys():
            if len(gdp_data[recon[ccode]][year]) > 0:
                gdp_value = float(gdp_data[recon[ccode]][year])
                gdp_log = math.log10(gdp_value)
                result_dict[ccode] = gdp_log
            elif len(gdp_data[recon[ccode]][year]) <= 0:
                empty_set.add(ccode)
        elif ccode not in recon.keys():
            missing_set.add(ccode)
            
            
    
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
    map_dict = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
    gdpMap = pygal.maps.world.World()
    gdpMap.title = 'GDP Data by Country'
    gdp = 'GDP for ' + year
    
    empty = 'No Data'
    gdpMap.add(gdp, map_dict[0])
    gdpMap.add('Missing from Wolrd Bank data', map_dict[1])
    gdpMap.add(empty, map_dict[2])
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

test_render_world_map()