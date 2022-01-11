import pandas

# csv file with stork reference data should be saved in "stork-data" directory
# and named "LifeTrackWhiteStorkRheinland-Pfalz-reference-data.csv"
reference_data_filename = "stork-data/LifeTrackWhiteStorkRheinland-Pfalz-reference-data.csv"

# reading csv file with reference data
ref_df = pandas.read_csv(reference_data_filename)

# Print first row of reference data as example
print("REFERENCE DATA EXAMPLE:")
print(ref_df.iloc[0], "\n")


# csv file with stork gps data should be saved in "stork-data" directory
# and named "LifeTrackWhiteStorkRheinland-Pfalz.csv"
gps_data_filename = "stork-data/LifeTrackWhiteStorkRheinland-Pfalz.csv"

# number of records in gps data file (excludes header)
n = sum(1 for line in open(gps_data_filename)) - 1  # n = 7887758

# desired sample size of gps data
sample_size = 1000

# column names that we want to load from the csv file
col_names = ['event-id',
            'timestamp',
            'location-long',
            'location-lat',
            'tag-local-identifier']

# reading csv file with gps data
gps_df = pandas.read_csv(gps_data_filename, nrows=sample_size, usecols=col_names)

# Print first row as example
print("GPS DATA EXAMPLE:")
print(gps_df.iloc[0])
