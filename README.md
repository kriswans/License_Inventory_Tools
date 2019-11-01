# License_Inventory_Tools
 
##3K_license_finder.py: 

Takes a CCW-R export in a csv format as input, then searches and parses out all of the CAT3K SKUs that indicate license entitlement. It then generates an output report in CSV format. This is meant to assist with licensing cases where large quantities of data must be pulled based on SO, contract, etc. from CCW-R then submitted for entitlement into the customer Smart Account. The use case for this is SLR where the on-box license must exist prior to the customer performing license registration (and device led conversion woin't work.

##Example syntax:

python 3K_license_finder.py inputfile.csv report.csv sa.domain.mil
