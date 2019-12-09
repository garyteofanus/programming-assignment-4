"""
The Model component of BudayaKB app.
Contains two classes:
- class BudayaItem : the representation of a data in BudayaKB app
- class BudayaCollection: the representation of the collection of BudataItem objects
"""

import csv

"""
class BudayaItem
This class represents a data in BudayaKB app.
The data contains 4 field:
- name (unique)
- type (the type of the data)
- prov (the province)
- URL
"""


class BudayaItem(object):
    def __init__(self, name="", type="", prov="", url=""):
        """The constructor of BudayaItem"""
        self.name = name
        self.type = type
        self.prov = prov
        self.url = url

    def __str__(self):
        """Return a string that deescribes an instance of BudayaItem"""
        return self.name + ", " + self.type + ", " + self.prov + ", " + self.url

    def __lt__(self, anotherBudayaItem):
        """Override "less than" operation, so that this object can be sorted by "name" field"""
        return self.name < anotherBudayaItem.nama

    def __eq__(self, anotherBudayaItem):
        """Override "equal" operation, so that this object can be sorted by "name" field"""
        return self.name == anotherBudayaItem.nama


"""
class BudayaCollection
This class represents the data structure that stores the BudayaKB data
List of operations:
- import and export from a CSV file
- search by "name", "type", and "prov"
- add, update and delete 
- statistics (data size, data size by type and by prov)

"""


class BudayaCollection(object):

    def __init__(self, collection={}):
        """
        The constructor of BudayaCollection object
        """
        self.collection = collection

    def __str__(self):
        """
        Return a string that describe the BudayaCollection object
        """
        return str(self.collection)

    def importFromCSV(self, fileName):
        """
        To import data from a CSV file, and create the BudayaCollection object
        return the number of data imported
        """
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line in csv_reader:
                if len(line) == 4 and line[0] != "":
                    budItem = BudayaItem(line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip())
                    if line[0] not in self.collection:
                        self.collection[line[0]] = budItem

    def exportToCSV(self, fileName):
        """
        To export the data from a BudayaCollection object to a CSV file
        return None
        """
        fileName = fileName + ".csv"
        fh = open(fileName, "w")
        resultStr = ""

        for value in self.collection.values():
            resultStr += str(value) + "\n"

        print(resultStr, file=fh)
        fh.close()

    def searchByName(self, aName):
        """Return a list contains BudayaItem object of a certain name"""
        result = []

        for item in self.collection:
            if aName.strip().lower() in item.lower():
                result.append(self.collection[item])

        return result

    def searchByType(self, aType):
        """Return a list contains BudayaItem object of a certain type"""
        result = []

        for item in self.collection.values():
            if aType.strip().lower() in item.type.lower():
                result.append(item)

        return result

    def searchByProv(self, aProv):
        """Return a list contains BudayaItem object of a certain prov"""
        result = []

        for item in self.collection.values():
            if aProv.strip().lower() in item.prov.lower():
                result.append(item)

        return result

    def add(self, aName, aType, aProv, anURL):
        """To add a new data to a collection of BudayaItem
        return 1 if the new data has a new unique name and the addition has been done
        return 0 otherwise, new data is not processed
        """

        if aName not in self.collection:
            new_budaya_item = BudayaItem(aName.strip(), aType.strip(), aProv.strip(), anURL.strip())
            self.collection[aName] = new_budaya_item
            return 1
        else:
            return 0

    def delete(self, aName):
        """
        To remove a data to the collection of BudayaItem
        return 1 if the removal has been done
        return 0 if the data does not exist
        """
        if aName in self.collection:
            self.collection.pop(aName.strip())
            return 1
        else:
            return 0

    def ubah(self, aName, aTipe, aProv, anURL):
        """
        To update a data in the collection of BudayaItem
        return 1 if the data to be updated is in the collection and the update has been done
        return 0 if the old data with the same key (name) does not exist
        """
        if aName in self.collection:
            new_budaya_item = BudayaItem(aName.strip(), aTipe.strip(), aProv.strip(), anURL.strip())
            self.collection[aName] = new_budaya_item
            return 1
        else:
            return 0

    def stat(self):
        """Return the number of item in the collection"""
        return len(self.collection)

    def statByType(self):
        """Return a dictionary contains the number of occurences of each type"""
        result = {}
        for v in self.collection.values():
            if v.type not in result:
                result[v.type] = 1
            else:
                result[v.type] += 1

        return result

    def statByProv(self):
        """Return a dictionary contains the number of occurences of each prov"""
        result = {}
        for v in self.collection.values():
            if v.prov not in result:
                result[v.prov] = 1
            else:
                result[v.prov] += 1

        return result

    def __str__(self):
        """Return a string that describe the object"""
        result_str = ""

        for value in self.collection.values():
            result_str += str(value) + "\n"

        return result_str


#####################################################################################
# for testing 
#####################################################################################
def main():
    mydb = BudayaCollection()

    #### Test import
    print("=================================================")
    print("Test Import Data")
    mydb.importFromCSV("dataSmall.csv")
    print("ImporCSV: Sukses menambahkan {} data baru\n".format(len(mydb.collection)))
    print(mydb)

    #### Test cari
    print("=================================================")
    print("Test Cari Data")

    keyCari = "a"
    result = mydb.searchByName(keyCari)
    result.sort()
    if len(result) > 0:
        print("CariByNama: Ditemukan {} data dengan name {}".format(len(result), keyCari))
        for item in result:
            print(item)
        print()
    else:
        print("CariByNama: Tidak ada data dengan name {}\n".format(keyCari))


if __name__ == "__main__":
    main()
