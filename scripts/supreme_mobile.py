#!/bin/env python3.4

# 99% credit to @Jayzer1217 https://twitter.com/jayzer1217 FOLLOW HIM
# Run around 1059 as early as 1055.
# Polling times vary pick something nice.
# Ghost checkout timer can be changed by 
# adjusting for loop range near bottom.
# Fill out personal data in checkout payload dict.

import sys, json, time, requests, codecs
import urllib.request as urllib_request
import urllib.parse as urllib_parse
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

def UTCtoEST():
    current=datetime.now()
    return str(current) + ' EST'
    
def find(item_to_find):
    global found_items
    
    keywords = item_to_find['model']
    color = item_to_find['color'].title()
    sz = item_to_find['size'].title()
        
    req = urllib_request.Request('http://www.supremenewyork.com/mobile_stock.json')
    req.add_header('User-Agent', "User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25")
    resp = urllib_request.urlopen(req)
    data = json.load(reader(resp))
    
    ID=0
    variant=''
    cw=''
    for i in range(len(data['products_and_categories'].values())):
        for j in range(len(list(data['products_and_categories'].values())[i])):
            item=list(data['products_and_categories'].values())[i][j]
            name=str(item['name'].encode('ascii','ignore')).lower()
            # SEARCH WORDS HERE
            # if string1 in name or string2 in name:
            in_name = True
            for keyword in keywords:
                if not keyword.lower() in name:
                    in_name = False
            if in_name:
                # match/(es) detected!
                # can return multiple matches but you're 
                # probably buying for resell so it doesn't matter
                myproduct=name                
                ID=str(item['id'])
                print (UTCtoEST(),'::',name, ID, 'found ( MATCHING ITEM DETECTED )')
    if (ID == 0):
        # variant flag unchanged - nothing found - rerun
        time.sleep(poll)
        print (UTCtoEST(),':: Reloading and reparsing page...') # incorrect keywords will cause this to loop forever
        find(item_to_find)
    else:
        print (UTCtoEST(),':: Selecting',str(myproduct),'(',str(ID),')')
        jsonurl = 'http://www.supremenewyork.com/shop/'+str(ID)+'.json'
        req = urllib_request.Request(jsonurl)
        req.add_header('User-Agent', "User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B350 Safari/8536.25")
        resp = urllib_request.urlopen(req)
        data = json.load(reader(resp))
        found=0
        for numCW in data['styles']:
            # COLORWAY TERMS HERE
            # if string1 in numCW['name'] or string2 in numCW['name']:
            if color in numCW['name'].title():
                for sizes in numCW['sizes']:
                    # SIZE TERMS HERE
                    if str(sizes['name'].title()) == sz: # Medium
                        found=1;
                        variant=str(sizes['id'])
                        cw=numCW['name']
                        print (UTCtoEST(),':: Selecting size:', sizes['name'],'(',numCW['name'],')','(',str(sizes['id']),')')
                        
        if found ==0:
            # DEFAULT CASE NEEDED HERE - EITHER COLORWAY NOT FOUND OR SIZE NOT IN RUN OF PRODUCT
            # PICKING FIRST COLORWAY AND LAST SIZE OPTION
            print (UTCtoEST(),':: Selecting default colorway:',data['styles'][0]['name'])
            sizeName=str(data['styles'][0]['sizes'][len(data['styles'][0]['sizes'])-1]['name'])
            variant=str(data['styles'][0]['sizes'][len(data['styles'][0]['sizes'])-1]['id'])
            cw=data['styles'][0]['name']
            print (UTCtoEST(),':: Selecting default size:',sizeName,'(',variant,')')
            
    found_items.append({
        'ID': ID,
        'variant': variant,
        'cw': cw,
    })
    
def add(item):
    addUrl='http://www.supremenewyork.com/shop/'+str(item['ID'])+'/add.json'
    addHeaders={
        'Host':              'www.supremenewyork.com',                                                                                                                     
        'Accept':            'application/json',                                                                                                                             
        'Proxy-Connection':  'keep-alive',                                                                                                                                   
        'X-Requested-With':  'XMLHttpRequest',                                                                                                                               
        'Accept-Encoding':   'gzip, deflate',                                                                                                                                
        'Accept-Language':   'en-us',                                                                                                                                        
        'Content-Type':      'application/x-www-form-urlencoded',                                                                                                            
        'Origin':            'http://www.supremenewyork.com',                                                                                                                
        'Connection':        'keep-alive',                                                                                                                                   
        'User-Agent':        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257',                               
        'Referer':           'http://www.supremenewyork.com/mobile'   
    }
    addPayload={
        'size': str(item['variant']),
        'qty':  '1'
    }
    print (UTCtoEST() +' :: Adding product to cart...')
    addResp=session.post(addUrl,data=addPayload,headers=addHeaders)

    print (UTCtoEST() +' :: Checking status code of response...')

    if addResp.status_code!=200:
        print (UTCtoEST() +' ::',addResp.status_code,'Error \nExiting...')
        print
        return
    else:
        if addResp.json()==[]:
            print (UTCtoEST() +' :: Response Empty! - Problem Adding to Cart\nExiting...')
            print
            return
        print (UTCtoEST() +' :: '+str(item['cw'])+' - '+addResp.json()[0]['name']+' - '+ addResp.json()[0]['size_name']+' added to cart!')
        
def checkout():
    cookie_sub = {}
    for item in found_items:
        cookie_sub[item['ID']] = 1
       
    cookie_sub = urllib_parse.quote(str(cookie_sub))
    print(found_items)
    
    checkoutUrl='https://www.supremenewyork.com/checkout.json'
    checkoutHeaders={
        'host':              'www.supremenewyork.com',
        'If-None-Match':    '"*"',
        'Accept':            'application/json',                                                                                                                             
        'Proxy-Connection':  'keep-alive',                                                                                                                                   
        'Accept-Encoding':   'gzip, deflate',                                                                                                                                
        'Accept-Language':   'en-us',                                                                                                                                        
        'Content-Type':      'application/x-www-form-urlencoded',                                                                                                            
        'Origin':            'http://www.supremenewyork.com',                                                                                                                
        'Connection':        'keep-alive',                                                                                                                                   
        'User-Agent':        'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257',                               
        'Referer':           'http://www.supremenewyork.com/mobile'   
    }

    #################################
    # FILL OUT THESE FIELDS AS NEEDED
    #################################
    checkoutPayload={
        'store_credit_id':    '',      
        'from_mobile':              '1',
        'cookie-sub':               cookie_sub,                               # cookie-sub: eg. {"VARIANT":1} urlencoded
        'same_as_billing_address':  '1',                                    
        'order[billing_name]':      'anon mous',                              # FirstName LastName
        'order[email]':             'anon@mailinator.com',                    # email@domain.com
        'order[tel]':               '999-999-9999',                           # phone-number-here
        'order[billing_address]':   '123 Seurat lane',                        # your address
        'order[billing_address_2]': '',
        'order[billing_zip]':       '90210',                                  # zip code
        'order[billing_city]':      'Beverly Hills',                          # city
        'order[billing_state]':     'CA',                                     # state
        'order[billing_country]':   'USA',                                    # country
        'store_address':            '1',                                
        'credit_card[type]':        'visa',                                   # master or visa
        'credit_card[cnb]':         '9999 9999 9999 9999',                    # credit card number
        'credit_card[month]':       '01',                                     # expiration month
        'credit_card[year]':        '2026',                                   # expiration year
        'credit_card[vval]':        '123',                                    # cvc/cvv
        'order[terms]':             '0',
        'order[terms]':             '1'                
    }

    # GHOST CHECKOUT PREVENTION WITH ROLLING PRINT
    for i in range(delay):
            sys.stdout.write("\r" +UTCtoEST()+ ' :: Sleeping for '+str(delay-i)+' seconds to avoid ghost checkout...')
            sys.stdout.flush()
            time.sleep(1)
    print 
    print (UTCtoEST()+ ' :: Firing checkout request!')
    checkoutResp=session.post(checkoutUrl,data=checkoutPayload,headers=checkoutHeaders)
    try:
        print (UTCtoEST()+ ' :: Checkout',checkoutResp.json()['status'].title()+'!')
    except:
        print (UTCtoEST()+':: Error reading status key of response!')
        print (checkoutResp.json())
    print 
    print (checkoutResp.json())
    if checkoutResp.json()['status']=='failed':
        print
        try:
            print ('!!!ERROR!!! ::',checkoutResp.json()['errors'])
        except KeyError:
            print ('!!!ERROR!!! :: Card was declined')
    print

def main(options):
    global poll
    global delay
    poll = options['settings']['interval']
    delay = options['settings']['delay']
    pool = ThreadPool(len(options['items']))
    pool.map(find, options['items'])
    for item in found_items:
        add(item)
    checkout()
    
options = {
    'settings': {
        'interval': 1,
        'delay': 5
    },
    'items': [
        {
            'model': ['twill', 'parka'],
            'color': 'black',
            'size': 'small'
        },
        {
            'model': ['hanes', 'socks'],
            'color': 'white',
            'size': 'n/a'
        },
    ]
}

qty = '1'
reader = codecs.getreader("utf-8")
found_items = []
session = requests.Session()

print (UTCtoEST(),':: Parsing page...')
main(options)
