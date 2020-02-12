# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 12:34:01 2019

@author: Brock
"""

"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def read_csv_as_nested_dict(filename, gdpinfo):
    
    table = {}
    with open(filename, "rt", newline='') as csvfile:
        csvreader = csv.DictReader(csvfile,
                                    skipinitialspace=True,
                                    delimiter=gdpinfo['separator'],
                                    quotechar = gdpinfo['quote'])
        
        for row in csvreader:
            rowid = row[gdpinfo['country_name']]
            table[rowid] = dict(row)
    return table
     

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  
      
      -The dictionary maps country codes from plot_countries to country names 
       from gdp_countries 
           -exp: {'pr': 'Puerto Rico', 'no': 'Norway', 'us': 'United States'}
      -The set contains the country codes from plot_countries that were not 
       found in gdp_countries.
           -exp:{'United States': {'Country Name': 'United States', 
           'Country Code': 'USA'}, 
            'Norway': {'Country Name': 'Norway', 'Country Code': 'NOR'}
    """
    result_dict = {}
    result_set = set()
                
    for ccode, cname in plot_countries.items():
        if cname in gdp_countries:
            result_dict[ccode] = gdp_countries[cname]['Country Name']  
        elif cname not in gdp_countries.values():
            result_set.add(ccode)

    return (result_dict, result_set)
             


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  
      -The dictionary maps country codes from plot_countries to the 
       log (base 10) of the GDP value for that country in the specified year.  
      -The first set contains the country codes from plot_countries that 
      were not found in the GDP data file.  
      -The second set contains the country codes from plot_countries that were 
       found in the GDP data file, but have no GDP data for the specified year.
    """
    gdp_nested_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo)
    
    gdp_values = {}
    missing_set = set()
    empty_set = set()
    
    for ccode, cname in plot_countries.items():
        if cname in gdp_nested_dict.keys():
            if len(gdp_nested_dict[cname][year]) > 0:
                gdp_value = float(gdp_nested_dict[cname][year])
                gdp_log = math.log10(gdp_value)
                gdp_values[ccode] = gdp_log
            elif len(gdp_nested_dict[cname][year]) <= 0:
                empty_set.add(ccode)
        elif cname not in gdp_nested_dict.keys():
            missing_set.add(ccode)
            
    return (gdp_values, missing_set, empty_set)



def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    
    map_dict = build_map_dict_by_name(gdpinfo, plot_countries, year) # ({country code: log10(gdp)}, missing ccs, empty ccs)
    
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
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()