# Data

## Data source
Movebank, a free online animal tracking database maintained by Max-Planck-Institut für VerhaltensbiologieSelected surveys (stork locations)

LifeTrack White Stork Rheinland-Pfalz:

https://www.movebank.org/cms/webapp?gwt_fragment=page=studies,path=study76367850


## How to prepare data?
1. Download GPS data in CSV format by:
   - selecting on the page: Download > Download Data,
   - approving the terms of the download,
   - selecting "GPS" in the "Available Sensor Types" field,
   - making sure the box that specifies that the file will be downloaded in CSV format is checked,
   - confirming by pressing the "Download" button.

**PROTIP**: Select only data from GPS sensors. Data from other sensors, such as magnetometer or accelerometer,
will not be useful for the task.

2. Change name of the file to:
```
LifeTrackWhiteStorkRheinland-Pfalz.csv
```

3. Copy file to stork-relationships/stork-data directory
