from datetime import datetime, timedelta
import pysftp
import os

from fabric import Connection #ssh
import pyodbc


def Yesterday(frmt='%Y-%m-%d', string=True):
    yesterday=datetime.now()-timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday
## want YYYYMMDD
yesterday=Yesterday()
def remove_hyphens(string):
    string=string.replace('-', '')
    return string
yesterday=remove_hyphens(yesterday)

#Restaurant must enable data exports https://central.toasttab.com/s/article/Enabling-Data-Exports-1492810278449
#Follow these instructions to generate SSH key pair https://central.toasttab.com/s/article/Automated-Nightly-Data-Export-1492723819691
SERVERNAME = ''
USERNAME= ''
private_key_path= r'C:path' #where the id_rsa key pairs are stored
restaurant_id=''

##TODO
# 1) Access AllItemsReport.csv
with pysftp.Connection(host=SERVERNAME, username=USERNAME, private_key=r'C:\Users\sabri\.ssh\id_rsa') as sftp:
    with sftp.cd(f'/{restaurant_id}'):           # temporarily chdir to '/{restaurant_id}' which is the bucket that
                                                #stores files in YYYYMMDD format containing sales reports
            #download yesterday's sales reports to a specified desktop folder
        sftp.get_d((f'/{restaurant_id}/{yesterday}'), (r'C:\Users\sabri\Desktop\Toast'))

sql= ("update Ingredient"
      "set"
      "QuantityAvailable = ISNULL(QuantityAvailable - (select sum(mii.Quantity * a.[  # Orders]) as QtyOfIngUsed)"
      "from MenuItem m"
      "inner join AllItemsReport1 a"
      "on m.Name = a.[Menu Item]"
      "inner join MenuItemIngredient mii"
      "on mii.MenuItemId = m.MenuItemId"
      "inner join Ingredient i"
      "on mii.IngredientId = i.IngredientId"
      "where i.IngredientId = ix.IngredientId"
      "group by m.MenuItemId, m.Name, i.Name, mii.IngredientId), ix.QuantityAvailable)"
      "from Ingredient ix")
# 2) SQL database for minimum quantity thresholds

# 3) Connect to database

# 5) Twilio send email if lower

print(yesterday)