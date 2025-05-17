from enum import Enum

class Categories(Enum):
    LAPTOPS = (["Brand", "Model", "Category", "Display", "CPU", "RAM", "Storage", "GPU", "OS", "Weight", "Price", "Link"],
               ["TEXT", "TEXT", "TEXT","TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT","TEXT", "TEXT", "TEXT"]
               ,[0,0, 0, 0.05, 0.15, 0.1, 0.1, 0.15, 0, 0.05, 0.4, 0])


    def __init__(self, header: list, type: list, filter_weights: list):
        self.header = header
        self.type = type
        self.filter_weights = filter_weights

    def database_name_for_category(self):
        return f"{self.name}.db"

    def string_to_create_database(self):
        stringToReturn = "("
        length_header = len(self.header)
        for i in range(length_header - 1):
            stringToReturn += f"{self.header[i]} {self.type[i]},"
        #append the last one
        stringToReturn += f"{self.header[length_header -1]} {self.type[length_header -1]})"

        return stringToReturn

