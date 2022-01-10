import pandas

# csv file with stork data should be saved in "stork-data" directory
# and named "LifeTrackWhiteStorkRheinland-Pfalz.csv"
filename = "stork-data/LifeTrackWhiteStorkRheinland-Pfalz.csv"

# number of records in file (excludes header)
n = sum(1 for line in open(filename)) - 1 # n = 7887758

# desired sample size
sampleSize = 1000

# column names that we want to load from the csv file
colNames = ['event-id',
            'timestamp',
            'location-long',
            'location-lat',
            'height-above-ellipsoid',
            'individual-taxon-canonical-name',
            'tag-local-identifier']

# reading csv file
df = pandas.read_csv(filename, nrows=sampleSize, usecols=colNames)

# Print first row as example
print(df.iloc[0])

