import csv
import sqlite3
import os
from unicodedata import category
import utils
from data_categories_entries.data_categories import Categories
import numpy as np

from utils import PROBABILITY_THRESHOLD


def create_database_if_it_does_not_exist(category: Categories):
    file_name = category.database_name_for_category()
    if not os.path.exists(file_name):
        conn = sqlite3.connect(category.database_name_for_category())
        c = conn.cursor()
        c.execute(f"CREATE TABLE {category.name} {category.string_to_create_database()}")
        c.close()

def convert_prices_to_float(prices: list):
    listToReturn = []
    for price in prices:
        try:
            listToReturn.append(utils.parse_number_from_string(price))
        except:
            pass
    return listToReturn


def create_filter_database_parser(category: Categories) -> list:
    """
    The role of this method is to create the filter for the csv. The filter is a double dimensional matrix which
    has in each column one type of filter for example CPU, GPU etc... depending on category
    :return: the filter we will want to have to match computers with our database
    """
    with open("../database/specs_database.csv", "r") as file:
        r = list(csv.reader(file))
        matrix_to_return = []
        #fill the matrix with lists
        for i in range(len(category.header)):
            matrix_to_return.append([])
        #fill the matrix
        for i, row in enumerate(r):
            for j, title in enumerate(category.header):
                if j < len(row):
                    if row[j] not in matrix_to_return[j]:
                        matrix_to_return[j].append(row[j])
        #convert it to primitive python matrix
        return matrix_to_return



class sql_database_interface:
    def __init__(self, category: Categories):
        """
        Init the database interface with the category you want
        :param category: the category we want to open for the database
        """
        self.category = category
        create_database_if_it_does_not_exist(category)
        self.connection = sqlite3.connect(category.database_name_for_category())
        self.c = self.connection.cursor()

    def parse_line(self, tuple_values: tuple):
        """
        Parse the tuple line. The tuple has to have length equal to the number of elements one each row of the category
        :param tuple_values: the tuple values associated with the category of this database
        """
        try:
            length_tuple = len(tuple_values)
            entry_to_add = "("
            for i in range(length_tuple - 1):
                entry_to_add += f"'{tuple_values[i].lower()}',"
            # add the last one
            entry_to_add += f"'{tuple_values[length_tuple - 1].lower()}')"

            try:
                self.c.execute(f"INSERT INTO {self.category.name} VALUES {entry_to_add}")
                self.connection.commit()
            except:
                pass
        except:
            pass

    def filter_database(self) -> list:
        """
        Filter the rows of the database according to filter lists
        :param filter_lists: each list contains a number of filters for
        :return: a list of items that satisfy the filtering
        """
        filter_lists = create_filter_database_parser(Categories.LAPTOPS)
        length_filter_list = len(filter_lists)
        listToReturn = []
        self.c.execute(f"SELECT * FROM {self.category.name}")
        #after that the cursor contains rows and we keep only the ones that respect the filters
        print(filter_lists)
        price_list = convert_prices_to_float(filter_lists[10])
        min_price = min(price_list)
        max_price = max(price_list)

        for row in self.c:
            assert len(row) == len(filter_lists)
            length_row = len(row)
            matched_filters = 0
            for i in range(length_row):
                found_matching_filter = False
                 #skip first two filters
                #its the price list
                if i == 10:
                    try:
                        parsing = utils.parse_number_from_string(row[i])
                        if min_price <= parsing and parsing <= max_price:
                            matched_filters += self.category.filter_weights[10]
                    except:
                        continue
                else:
                    for string in filter_lists[i]:

                        comparaison = utils.compare_strings(string, row[i]) >= utils.PROBABILITY_THRESHOLD
                        if comparaison >= PROBABILITY_THRESHOLD and not found_matching_filter:
                            matched_filters += self.category.filter_weights[i]
                            found_matching_filter = True
            if matched_filters >= utils.FILTER_THRESHOLD:
                listToReturn.append(row)


        return listToReturn


    def close_connection(self):
        """
        Close the connection with the database
        """
        self.c.close()


laptops = sql_database_interface(Categories.LAPTOPS).filter_database()
print(laptops)
print(len(laptops))


"""
database_interface = sql_database_interface(Categories.LAPTOPS)
with open("../laptops_to_clean.csv", "r", encoding="utf-8") as file:
    r = list(csv.reader(file))
    for row in r[1:]:
        database_interface.parse_line(tuple(row))

"""
"""
database = sql_database_interface(Categories.LAPTOPS)



data = database.filter_database([[],[],[],[],[],[],[],[],[],[],[],[]])
print(data)

"""

"""
ram_list = set()
for element in data:
    ram = element[5]
    ram_list.add(ram)
with open("../scraped_lists/LAPTOPS/RAM.csv", "w") as file:
    writer = csv.writer(file)
    for ram in list(ram_list):
        try:
            writer.writerow([int(utils.parse_number_from_string(ram.lower()))])
        except:
            continue
"""