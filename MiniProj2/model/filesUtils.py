import pickle

#save in file a object receive
def saveInFile(object, filename):
    filehandler = open(filename, 'wb')
    pickle.dump(object, filehandler)


#load from file an object
def loadFromFile(filename):
    try:
        file = open(filename, 'rb')
        return pickle.load(file)
    except EOFError:
        return []