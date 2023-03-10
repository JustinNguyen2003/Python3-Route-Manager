#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@author: rivera
@author: justinnguyen
"""

import sys
import pandas as pd
import yaml
import matplotlib.pyplot as plt
import numpy as np


def sample_function(input: str) -> str:
    """Sample function (removable) that illustrations good use of documentation.
            Parameters
            ----------
                input : str, required
                    The input message.

            Returns
            -------
                str
                    The text returned.
    """
    return input.upper()


def getargs() -> str:
    """getargs gets the arguments from the command line.
        Returns
        -------
            str
                One string for each argument in the command line.
    """

    arg1:str = (sys.argv[1]).split('=')[1]
    arg2:str = (sys.argv[2]).split('=')[1]
    arg3:str = (sys.argv[3]).split('=')[1]
    arg4:str = (sys.argv[4]).split('=')[1]
    arg5:str = (sys.argv[5]).split('=')[1]

    return arg1, arg2, arg3, arg4, arg5 




def create_data_frames(airlines: str, airports: str, routes: str) -> pd.DataFrame:
    """this function creates a dataframe for each of the 3 .yaml files
        Parameters
        ----------
            airlines: str, required
                The name of the airlines.yaml file.

            airports: str, required
                The name of the airports.yaml file.

            routes: str, required
                The name of the routes.yaml file.
        
        Returns
        -------
            pd.Dataframe
                Returns a pd.Dataframe for each of the 3 .yaml files
    """
    
    files:list[str] = [airlines, airports, routes]
    names:list[str] = ['airlines', 'airports', 'routes']
    i:int = 0
    dataframes:list = []

    for filename in files:
        file = open(filename, 'r')
        data = yaml.load(file, Loader=yaml.Loader)
        data_array:str = data.get(names[i])
        dataframe:pd.Dataframe = pd.DataFrame.from_dict(data_array)
        file.close()
        i=i+1

        dataframes.append(dataframe)

    return dataframes[0], dataframes[1], dataframes[2]




def merge_data(question:str, airlines_df:pd.DataFrame, airports_df:pd.DataFrame, routes_df:pd.DataFrame) -> pd.DataFrame:
    """this function merges the dataframes depending on which question was given in the command line.
        Parameters
        ----------
            question: str, required
                Shows which question is being asked in the command line.

            airlines_df: pd.Dataframe, required
                The airlines dataframe to be merged.

            airports_df: pd.Dataframe, required
                The airports dataframe to be merged.

            routes_df: pd.Dataframe, required
                The routes dataframe to be merged.

        Returns
        -------
            pd.Dataframe
                Returns a dataframe merged from the 3 input dataframes, based on the question being asked.
    """

    if (question == 'q1' or question == 'q2' or question == 'q3' or question == 'q4'):
        merged:pd.Dataframe = routes_df.merge(airports_df, left_on='route_to_airport_id', right_on='airport_id', how='left')
        merged_all:pd.DataFrame = merged.merge(airlines_df, left_on='route_airline_id', right_on='airline_id', how='left')
        return merged_all

    else:
        merged:pd.Dataframe = routes_df.merge(airports_df, left_on='route_to_airport_id', right_on='airport_id')
        merged_all:pd.DataFrame = merged.merge(airports_df, left_on='route_from_aiport_id', right_on='airport_id')
        return merged_all





def get_data(question:str, merged_df: pd.DataFrame) -> pd.DataFrame:
    """This function takes a dataframe and filters it and returns a new dataframe that just contains the data needed to answer the specified question.
        Parameters
        ----------
            question: str, required
                Shows which question is being asked in the command line.
            
            merged_df: pd.Dataframe, required
                This contains the data that the function will filter

        Returns
        -------
            pd.Dataframe
                Returns a dataframe with just the data needed to answer the question.
    """

    if (question == 'q1'):
        result_df:pd.DataFrame = merged_df[merged_df["airport_country"] == 'Canada']
        grouped_df:pd.DataFrame = result_df.groupby(['airline_name','airline_icao_unique_code'], as_index=False).size()
        sorted_df:pd.DataFrame = grouped_df.sort_values(by=['size', 'airline_name'], ascending=[False,True]).head(20)

        return sorted_df

    elif (question == 'q2'):
        grouped_df:pd.DataFrame = merged_df.groupby('airport_country', as_index=False).size()
        grouped_df['airport_country'] = grouped_df['airport_country'].str.strip()
        sorted_df:pd.DataFrame = grouped_df.sort_values(by=['size', 'airport_country'], ascending=True).head(30)

        return sorted_df

    elif (question == 'q3'):
        grouped_df:pd.DataFrame = merged_df.groupby(['airport_name','airport_icao_unique_code','airport_city','airport_country'], as_index=False).size()
        sorted_df:pd.DataFrame = grouped_df.sort_values(by=['size','airport_name'], ascending=[False,True]).head(10)

        return sorted_df


    elif (question == 'q4'):
        grouped_df:pd.DataFrame = merged_df.groupby(['airport_city', 'airport_country'], as_index=False).size()
        sorted_df:pd.DataFrame = grouped_df.sort_values(by=['size'], ascending=False).head(15)

        return sorted_df


    elif (question == 'q5'):
        differences:list = []
        for i,row in merged_df.iterrows():
            difference:float = abs(float(row['airport_altitude_x']) - float(row['airport_altitude_y']))
            differences.append(difference)

        merged_df['difference'] = differences
        grouped_df:pd.DataFrame = merged_df[merged_df['airport_country_x'] == 'Canada']
        grouped_df = grouped_df[grouped_df['airport_country_y'] == 'Canada']
        grouped_df2:pd.DataFrame = grouped_df.groupby(['airport_icao_unique_code_y', 'airport_icao_unique_code_x', 'difference'], as_index=False).size()
        grouped_df2['difference'] = grouped_df2['difference']
        sorted_df:pd.DataFrame = grouped_df2.sort_values(by='difference', ascending=False).head(10)

        sorted_df:pd.DataFrame = sorted_df.drop(columns='size')
        return sorted_df





def merge_columns(dataframe: pd.DataFrame, question: str) -> pd.DataFrame:
    """This function takes a dataframe and merges certain columns based on the question being asked.
        Parameters
        ----------
            dataframe: pd.Dataframe, required
                This is the dataframe that needs to be merged.

            question: str, required
                Shows which question is being asked in the command line.
        Returns
        -------
            pd.Dataframe
                Returns a dataframe with certain columns merged based on the question.
    """

    if (question == 'q1'):
        dataframe['airline_name'] = dataframe['airline_name']+' ('+dataframe['airline_icao_unique_code']+')'
        dataframe = dataframe.drop(columns='airline_icao_unique_code')
        
        return dataframe

    elif (question == 'q2'):
        return dataframe

    elif (question == 'q3'):
        dataframe['airport_name'] = dataframe['airport_name']+' ('+dataframe['airport_icao_unique_code']+'), '+dataframe['airport_city']+', '+dataframe['airport_country']
        dataframe = dataframe.drop(columns=['airport_icao_unique_code','airport_city','airport_country'])

        return dataframe

    elif (question == 'q4'):
        dataframe['airport_city'] = dataframe['airport_city']+', '+dataframe['airport_country']
        dataframe = dataframe.drop(columns='airport_country')

        return dataframe

    elif (question == 'q5'):
        dataframe['airport_icao_unique_code_y'] = dataframe['airport_icao_unique_code_y']+'-'+dataframe['airport_icao_unique_code_x']
        dataframe = dataframe.drop(columns='airport_icao_unique_code_x')

        return dataframe




def make_chart(dataframe: pd.DataFrame, question: str):
    """This function takes a dataframe and inputs the data into a .csv file.
        Parameters
        ----------
            dataframe: pd.Dataframe, required
                This is the dataframe and will be inputted to the .csv file.

            question: str, required
                Shows which question is being asked in the command line.
        Returns
        -------
            None
    """

    if (question=='q1'):
        dataframe.to_csv('q1.csv', index=False)

    elif (question=='q2'):
        dataframe.to_csv('q2.csv', index=False)

    elif (question=='q3'):
        dataframe.to_csv('q3.csv', index=False)

    elif (question=='q4'):
        dataframe.to_csv('q4.csv', index=False)

    elif (question=='q5'):
        dataframe.to_csv('q5.csv', index=False)
        



def change_headings(dataframe: pd.DataFrame, question: str) -> pd.DataFrame:
    """This function changes the headings of the given dataframe to the correct headings.
        Parameters
        ----------
            dataframe: pd.Dataframe, required
                This is the dataframe that the headings will be changed.
            
            question: str, required
                Shows which question is being asked in the command line.

        Returns
        -------
            Returns a dataframe with the correct headings.
    """

    if (question =='q1'):
        dataframe = dataframe.rename({'airline_name':'subject', 'size':'statistic'}, axis=1)
        return dataframe

    elif (question == 'q2'):
        dataframe = dataframe.rename({'airport_country':'subject', 'size':'statistic'}, axis=1)
        return dataframe

    elif (question == 'q3'):
        dataframe = dataframe.rename({'airport_name':'subject', 'size':'statistic'}, axis=1)
        return dataframe

    elif (question == 'q4'):
        dataframe = dataframe.rename({'airport_city':'subject', 'size':'statistic'}, axis=1)
        return dataframe

    elif (question == 'q5'):
        dataframe = dataframe.rename({'airport_icao_unique_code_y':'subject', 'difference':'statistic'}, axis=1)
        return dataframe


    
def make_bar_graph(question:str):
    """This function makes a bar graph using the .csv file created in make_chart.
        Parameters
        ----------
            question: str, required
                Shows which question is being asked in the command line.
        
        Returns
        -------
            None
    """

    if (question == 'q1'):
        data:dict = {}

        with open('q1.csv', 'r') as f:
    
            for line in f.readlines()[1:]:
                airline, routes = line.split(',')
                data[airline] = routes

        reverse:dict = dict(reversed(list(data.items())))
            
        for i, l in enumerate(reverse.keys()):
            plt.bar(reverse.keys(), reverse.values(), color='r')
            plt.xlabel('Airlines')
            plt.xticks(rotation=65)
            plt.xticks(fontsize=5)
            plt.yticks(fontsize=5)
            plt.ylabel('Number of Routes')
            plt.title('Top 20 Airlines with most Routes to Canada')

        plt.ylim(-0.1,11)
        plt.gca().invert_xaxis()
        plt.tight_layout()
        plt.savefig('q1.pdf', format='pdf')


    elif (question == 'q2'):
        data:dict = {}

        with open('q2.csv', 'r') as f:
    
            for line in f.readlines()[1:]:
                country, appearances = line.split(',')
                data[country] = float(appearances)
            
        for i, l in enumerate(data.keys()):
            plt.bar(data.keys(), data.values(), color='b')
            plt.xlabel('Countries')
            plt.xticks(rotation=65)
            plt.xticks(fontsize=5)
            plt.yticks(fontsize=5)
            plt.ylabel('Number of Appearances')
            plt.title('Top 30 Countries with least Routes to')

        plt.tight_layout()
        plt.savefig('q2.pdf', format='pdf')

    

    elif (question == 'q3'):
        data:dict = {}

        with open('q3.csv', 'r') as f:
    
            for line in f.readlines()[1:]:
                airports, city, country, routes = line.split(',')
                airports:str = airports+', '+city+', '+country
                data[airports] = routes

        reverse:dict = dict(reversed(list(data.items())))
            
        for i, l in enumerate(reverse.keys()):
            plt.bar(reverse.keys(), reverse.values(), color='g')
            plt.xlabel('Airports')
            plt.xticks(rotation=65)
            plt.xticks(fontsize=5)
            plt.yticks(fontsize=5)
            plt.ylabel('Number of Routes')
            plt.title('Top 10 Destination Airports')

        plt.gca().invert_xaxis()
        plt.tight_layout()
        plt.savefig('q3.pdf', format='pdf')


    
    elif (question == 'q4'):
        data:dict = {}

        with open('q4.csv', 'r') as f:
    
            for line in f.readlines()[1:]:
                city, country, routes = line.split(',')
                city:str = city+', '+country
                data[city] = routes

        reverse:dict = dict(reversed(list(data.items())))
            
        for i, l in enumerate(reverse.keys()):
            plt.bar(reverse.keys(), reverse.values(), color='r')
            plt.xlabel('Destination Cities')
            plt.xticks(rotation=65)
            plt.xticks(fontsize=5)
            plt.yticks(fontsize=5)
            plt.ylabel('Number of Routes')
            plt.title('Top 15 Destination Cities')

        plt.ylim(0,136)
        plt.gca().invert_xaxis()
        plt.tight_layout()
        plt.savefig('q4.pdf', format='pdf')


    elif (question == 'q5'):
        data:dict = {}

        with open('q5.csv', 'r') as f:

            for line in f.readlines()[1:]:
                route, difference = line.split(',')
                data[route] = difference

        reverse:dict = dict(reversed(list(data.items())))
            
        for i, l in enumerate(reverse.keys()):
            plt.bar(reverse.keys(), reverse.values(), color='k')
            plt.xlabel('Routes')
            plt.xticks(rotation=65)
            plt.xticks(fontsize=5)
            plt.yticks(fontsize=5)
            plt.ylabel('Difference in Elevation')
            plt.title('Top 10 Canadian Routes with the most difference in altitude')

        plt.gca().invert_xaxis()
        plt.tight_layout()
        plt.savefig('q5.pdf', format='pdf')

    
        


def make_pie_graph(question:str):
    """This function makes a pie graph from the .csv file made in the made_chart function.
        Parameters
        ----------
            question: str, required
                Shows which question is being asked in the command line.
        Returns
        -------
            None
    """

    if (question == 'q1'):
        data:dict = {}

        with open('q1.csv', 'r') as f:
    
            for line in f.readlines()[1:]:
                airline, routes = line.split(',')
                data[airline] = int(routes)

        for i, l in enumerate(data.keys()):
            plt.pie(data.values() , labels = data.keys(), autopct='%1.1f%%', textprops={'fontsize': 4.5})
            plt.title('Top 20 Airlines with most Routes to Canada')

        plt.tight_layout()
        plt.savefig('q1.pdf', format='pdf')


    elif (question == 'q2'):
        data:dict = {}

        with open('q2.csv', 'r') as f:
    
            for line in f.readlines()[1:]:
                country, appearances = line.split(',')
                data[country] = int(appearances)
        
        for i, l in enumerate(data.keys()):
            plt.pie(data.values() , labels = data.keys(), autopct='%1.1f%%', textprops={'fontsize': 4.5})
            plt.title('Top 30 Countries with least Routes to')

        plt.tight_layout()
        plt.savefig('q2.pdf', format='pdf')

    
    elif (question == 'q3'):
        data:dict = {}

        with open('q3.csv', 'r') as f:
    
            for line in f.readlines()[1:]:
                airports, city, country, routes = line.split(',')
                airports = airports+', '+city+', '+country
                data[airports] = routes

        for i, l in enumerate(data.keys()):
            plt.pie(data.values() , labels = data.keys(), autopct='%1.1f%%', textprops={'fontsize': 5.5})
            plt.title('Top 10 Destination Airports')

        plt.tight_layout()
        plt.savefig('q3.pdf', format='pdf', bbox_inches='tight')

    
    elif (question == 'q4'):
        data:dict = {}

        with open('q4.csv', 'r') as f:
    
            for line in f.readlines()[1:]:
                city, country, routes = line.split(',')
                city:str = city+', '+country
                data[city] = routes

        for i, l in enumerate(data.keys()):
            plt.pie(data.values() , labels = data.keys(), autopct='%1.1f%%', textprops={'fontsize': 5})
            plt.title('Top 15 Destination Cities')

        plt.tight_layout()
        plt.savefig('q4.pdf', format='pdf', bbox_inches='tight')


    elif (question == 'q5'):
        data:dict = {}

        with open('q5.csv', 'r') as f:

            for line in f.readlines()[1:]:
                route, difference = line.split(',')
                data[route] = difference

        for i, l in enumerate(data.keys()):
            plt.pie(data.values() , labels = data.keys(), autopct='%1.1f%%', textprops={'fontsize': 5.5})
            plt.title('Top 10 Canadian Routes with the most difference in altitude') 

        plt.tight_layout()
        plt.savefig('q5.pdf', format='pdf', bbox_inches='tight')






def main():
    """Main entry point of the program."""
    airlines, airports, routes, question, graph = getargs()

    airlines_df, airports_df, routes_df = create_data_frames(airlines, airports, routes)

    merged_df:pd.DataFrame = merge_data(question, airlines_df, airports_df, routes_df)

    result_df:pd.DataFrame = get_data(question, merged_df)

    sorted_data:pd.DataFrame = merge_columns(result_df, question)

    final_df:pd.DataFrame = change_headings(sorted_data, question)

    make_chart(final_df, question)

    if (graph == 'bar'):
        make_bar_graph(question)
        

    elif (graph == 'pie'):
        make_pie_graph(question)

    

    




if __name__ == '__main__':
    main()
