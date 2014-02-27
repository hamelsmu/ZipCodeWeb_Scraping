def back_out_unicode(stringval):
    return str(stringval.encode('utf-8').decode('ascii', 'ignore'))

def zip_info(zipcode):
    """
    Takes a zip code and goes to www.uszip.com/zip/*zipcode and
    screen scrapes relevant information down.  *zipcode is the 5-digit zipcode  parameter
    
    input value zipcode must be a string value
    returns a list of tuples, which are (key, value) pairs
    
    Written by Hamel Husain
    hamel.husain@gmail.com
    """
    #Type Safety

    if type(zipcode) <> str or len(zipcode) > 5:
        raise Exception('zipcode passed to this function must be a 5-digit string')
    
    from bs4 import BeautifulSoup
    import urllib

    data = [('zipcode', str(zipcode))] #Initializes zipcode list
    
   
    webaddress = 'http://www.uszip.com/zip/'+str(zipcode) #build web address
    try:
        html_collector = urllib.urlopen(webaddress).read() #read contents of HTML into variable
    except:
        print str(zipcode) #+ ' was an invalid zipcode, please try again - must be a 5 digit string value'
        raise
        
        
    soup = BeautifulSoup(html_collector) #make a Beautiful Soup object from HTML string so that we can parse
    raw_html = soup.prettify() #this is so you can inspect html, will dump this into a file called sample_html.txt
    
    with open('sample_html.txt', 'w') as html: #so you can dump a copy of the HTML somewhere
        html.write(back_out_unicode(raw_html))
        
    ##############
    #Checks to see if zipcode returned by website is the one you input!##
    #############
    zipcode_returned = back_out_unicode(soup.find('strong').text.strip())
    if zipcode <> zipcode_returned:
        print '%s was not found as a zipcode! Will Skip This' % (zipcode)
        zip_valid = False
    else:
        zip_valid = True
        city = back_out_unicode(soup.find('title').text.strip().replace(' zip code', ''))
        
        
    ##Mark Zip Code as Retrieved Or Not##
    data.append(('Zip Found', zip_valid)) 
    
    if zip_valid:
        data.append(('City', city))
    
    #return an iterable that has all of the results for 'dt', or the fieldnames
    search_results_titles = soup.findAll('dt') #for this websites, titles are tagged 'dt', numbers are tagged 'dd'

    for label in search_results_titles:
        current_name = label.name #tag name
        current_string = back_out_unicode(label.text.strip()) #tag text
        
        next_name = label.find_next_sibling().name #next tag's name
        next_string = back_out_unicode(label.find_next_sibling().text.strip()) #next tag's text
        
        #Want a 'dt' tag to be followed by a 'dd' tag, otherwise don't need it to be part of the result
        if (current_name <> next_name) and current_name == 'dt' and next_name == 'dd' and zip_valid:
            data.append((current_string, next_string))
        
    
    return data


if __name__ == '__main__':
    print 'you have run the main file!'
    hamel = zip_info('75019')
    
