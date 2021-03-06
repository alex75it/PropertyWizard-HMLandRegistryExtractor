# HM Land Registry Extractor
Part of the Property Wizard project   
Last update: 16 August 2017
  
This program is an extractor of the HM Land Registry public data.  
The extracted data are stored for a successive use by the [Property Wizard API](https://github.com/alex75it/PropertyWizard-API).  
It is a Python script that run on scheduled times.


# How it works

The program can elaborate Price Paid Data CSV file obtained from HM Land Property.   
Thew process start with a call to main.py passing the CSV file to read.  
The CSV file is parsed and raw data is stored in the database (MongoDB).  
In a second step custom data is generated from the raw data and saved in a new position in the database.
The new data contains only relevant data from the source and processed information. The Address is composed using raw data fields.   
Partial post code is extracted (district) to be used a search key.  
Data are stored in a MongoDB database.

"Transaction ID" is (should be) the unique identifier for records. 

The process can be execute against a file that contains the same data multiple times (it is idempotent).
How to recognize that a file is already elaborated and eventually force a new elaboration?
The process can retrieve the file itself?


## Developer configuration

The program read configuration from the config.py file.
On the local dev machine you can use a config_dev.py file that override the default values.

# HM Land Registry

The source of data is the "Price Paid data" taken from here: https://www.gov.uk/government/collections/price-paid-data

Single file: https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#single-file
CSV: http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-complete.csv

Current month CSV: http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv

## Address data

The following fields comprise the address data included in Price Paid Data:

- Postcode
- PAON Primary Addressable Object Name. Typically the house number or name.
- SAON Secondary Addressable Object Name. If there is a sub-building, for example the building is divided into flats, there will be a SAON.
- Street
- Locality
- Town/City
- District
- County

## Transaction ID

It can be duplicated (ex.: {49B7852A-2AAF-7921-E050-A8C063056E8D}). 


### Example data

First record in 2017/05 CSV data file:

<pre>
Id:                     {4E95D757-1CA7-EDA1-E050-A8C0630539E2}
Price:                  970000	
Date:                   2002-05-31 00:00	
Post code:              SW3 2BZ	
Type:                   F	
New build:              N	
Holding type:           L	
PAON:                   46	
SAON:                   FLAT 4	
Street:                 EGERTON GARDENS
Locality:        
City:                   LONDON	
District:               KENSINGTON AND CHELSEA	
County:                 GREATER LONDON	
Transaction category    A	
Action:                 A
</pre>

# Description of the fields:

Reference: http://landregistry.data.gov.uk/app/ppd/search

<pre>
- Id:                   It is a UUID wrapped in curly brackets. It is duplicated in 2 or 3 cases in the last years, I tend to consider that an error.
- Price:                Sell price in GBP
- Date:                 The date of the sale
   - Year
   - Month
- Post code:            can be empty. 
   - Partial post code. Obtained form the 4 initial characters and removing the space return the partial post code.
- Type:                 D/F/O/S/T  (Detached, Semi-detached, Terraced, Flat, Other)
- new build:            Y/N, Is a new building?  
- Holding type:         L/F (Leasehold/Freehold)
- PAON:                 Primary addressable object name. Typically the house number or name
- SAON:                 Secondary Addressable Object Name. If there is a sub-building, for example the building is divided into flats, there will be a SAON.
- Street:
- Locality:
- City:                 Town or City
- District:
- County:
- Transaction category: A/B (A=Standard, B=Additional)
- action:               A/C/D (record status notation Add/Change/Delete)
</pre>
 
## Note

Some prices seems wrong. For example 1£ or 125 millions of pounds.  
The second case could be an error inserting the value with a wrong decimal character resulting 100 times more. It could be 1 million, and this is resasonable compared to the other apartments in the same building.
  
3 thousands of records for year are duplicated for post code, address and date. How is it possible?      
Some addresses actually does not exist.  
"6 Mountford Gardens" is not found by Google Map but you can find it in many web sites, also on Zoopla.
There are 2 different sells on the same date, on this address, with different prices! One is market "new building" the other not ?!   

# Heroku

[Virtualenv and requirements.txt](https://devcenter.heroku.com/articles/getting-started-with-python#declare-app-dependencies)
