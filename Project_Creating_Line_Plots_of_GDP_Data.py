# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 11:15:16 2019

@author: Brock
"""

"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.
                    exp: {'2000': '1', '2001': '2', '2002': '3', '2003': '4', '2004': '5', '2005': '6'}
    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """

    gdpYear = []
    for keys, value in gdpdata.items():
        for years in range(gdpinfo['min_year'], gdpinfo['max_year']+1):
            if str(years) == keys and len(value) != 0:
                gdpYear.append((int(years), float(value)))
                gdpYear = sorted(gdpYear, key = lambda tup: tup[0])

    return gdpYear
  

def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.
          {country_name : (x_value, y_value)}

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
      
      {'Country1': [(2000, 1.0), (2001, 2.0), (2002, 3.0), (2003, 4.0), (2004, 5.0), (2005, 6.0)]}
    """
    gdpdata = read_csv_as_nested_dict(gdpinfo['gdpfile'], 
                                       gdpinfo['country_name'],     #keyfield
                                       gdpinfo['separator'], 
                                       gdpinfo['quote'])
    plot_dict = {}
    for country in country_list:
        plot_dict.setdefault(country, [])
        for key, value in gdpdata.items():
            if country in key:
                bpv = build_plot_values(gdpinfo,value)
                plot_dict[key] = bpv
                print(type(plot_dict))
                
            
    return plot_dict


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    plot_dict = build_plot_dict(gdpinfo, country_list)
    
    xy_chart= pygal.XY(title = "GDP Data", y_title = 'GDP in $US', x_title = 'Year')
    
    for country, data in plot_dict.items():
        if country in country_list:
            xy_chart.add(country, data)
        
    xy_chart.render_to_file(plot_file)
#    xy_chart.render_in_browser()
    return None


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
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

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

test_render_xy_plot()