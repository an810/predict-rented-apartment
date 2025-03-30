try:
    from pymongo import MongoClient, MongoReplicaSetClient
    from pymongo.errors import ConfigurationError
    from pymongo import version_tuple as mongo_version
    from gridfs import GridFS, errors
    from gridfs.errors import NoFile
except ImportError:
    MongoClient = None

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['real_estate']

# Create a GridFS object
fs = GridFS(db)

# Example: Store a file in GridFS
with open('example.txt', 'rb') as file:
    fs.put(file, filename='example.txt')

# Example: Retrieve a file from GridFS
file_data = fs.get_last_version(filename='example.txt')
print(file_data.read())