#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 16:04:52 2020

@author: danielhayler
"""
#Import libraries

import requests
import bs4
import re
import smtplib
import os
import datetime
from pandas.core.common import flatten
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#Set variables

#Automation email and app password
email = ""
password = ""

cambridge_url = "https://www.findaphd.com/phds/cambridge/biological-and-medical-sciences/?N0gccxS700&Show=M"
london_url = "https://www.findaphd.com/phds/london/biological-and-medical-sciences/?N0gcc1W700&Show=M"

old_cam_path = "/Users/haylerautoserver/Documents/Automation/old_camPhD.txt"
old_lon_path = "/Users/haylerautoserver/Documents/Automation/old_lonPhD.txt"
log_file_path = "/Users/haylerautoserver/Documents/Automation/PhD_checker_log.txt"

today = datetime.date.today()
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")

#Define fucntions

def get_titles(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    
    texted = str(soup)
    titles = []

    pattern = '<a class="courseLink phd-result__title" (.*?)>'
    title_pattern = 'title="(.*?)"'
    hyperlink = 'href="(.*?)"'
    
    substring = re.findall(pattern, texted)
    for i in substring:
        a = re.search(title_pattern, i).group(1)
        b = re.search(hyperlink, i).group(1)
        x = "https://www.findaphd.com"+b
        c = [a,x]
        titles.append(c)    
    
    return titles


def write_file(inst,lst):               #write list to file
    with open(f'/Users/haylerautoserver/Documents/Automation/old_{inst}PhD.txt', 'w') as filehandle:
        filehandle.writelines("%s\n" % phd for phd in lst)
        
        
def read_file(inst):                #read the file and return as a list
    prev_list = []
        
    with open(f'/Users/haylerautoserver/Documents/Automation/old_{inst}PhD.txt', 'r') as filehandle:
        filecontents = filehandle.readlines()
    
        for line in filecontents:
            # remove linebreak which is the last character of the string
            current_place = line[:-1]
    
            # add item to the list
            prev_list.append(current_place)
            
    return prev_list


def diff_list(list1, list2):        #make list 1 the new list and list 2 the previous
    return (list(set(list1) - set(list2)))

def splitter(word):                 #split the title of PhD to separate title from location
    w = word.rsplit(" at ", 1)
    return w

    
def find_that_phd(inst, url):
    current_phds = []
    previous_phds = read_file(inst)
    curr_phd_link = get_titles(url)
    for x in curr_phd_link:
        current_phds.append(x[0])
    new_phds = diff_list(current_phds, previous_phds)
    
    new_phds_html = []
    
    for n in new_phds:
        for c in curr_phd_link:
            if n == c[0]:
                new_phds_html.append(c)
    
    new_phds_html_flat = []      
    
    for p in new_phds_html: 
        broken = splitter(p[0])
        p[0] = broken
        x = list(flatten(p))
        new_phds_html_flat.append(x)
                
    
    if len(new_phds) == 0:
        return f"No new PhDs found in {inst}"
    else:
        write_file(inst, current_phds)
        return new_phds_html_flat #Issue here as if len == 0, one item is returned but else 2 returned
    
#Is there a need to take 2 lists forward now? Maybe take html list forward and have 2 functions;
#One that makes the plain text version of the email
#The other that makes the HTML version

            
#Initalise the email server connection + func for disconnect (easier to reference) + send results

def email_results(email, password, results, results_pt):
    smtp_object = smtplib.SMTP('smtp.gmail.com',587)
    smtp_object.starttls()
    smtp_object.login(email,password)
    
    from_address = email
    to_address = "" #sending to work email
    message = MIMEMultipart("alternative")
    message["Subject"] = "New PhDs matching your criteria found!"
    message["From"] = from_address
    message["To"] = to_address
    
    part1 = MIMEText(results_pt, "plain")
    part2 = MIMEText(results, "html")
    
    message.attach(part1)
    message.attach(part2)
    
    smtp_object.sendmail(from_address, to_address, message.as_string())
    
    smtp_object.quit()
    

def convert_list(lst):
    return '\n\n' .join(lst)

def html_style(it):
    html = """\
    <html>
      <body>
        """
    
    html2 = """
      </body>
    </html>
    """
    
    html_list= []
    for i in it:
        html_list.append(f'<p style="font-family:arial;"><a href="{i[2]}" style="text-decoration: none; font-size:22px; color:black;">{i[0]}</a><br>{i[1]}</p>')
    all_in_one = ''.join(html_list)
    output = html + all_in_one + html2
    return output

def plain_text(conv):
    new_list = []
    for c in conv:
        c[0] = c[0]+ "\n"
        c[1] = c[1]+ "\n\n"
        new_list.append((c[0]+c[1]))
    pt_message = "".join(new_list)
    return pt_message


#Check to see if a log file and existing phd lists for Cambridge and London are present

if os.path.exists(old_cam_path) == False:
    open(old_cam_path, 'w')
    
if os.path.exists(old_lon_path) == False:
    open(old_lon_path, 'w')
    
if os.path.exists(log_file_path) == False:
    with open(log_file_path, 'a') as filehandle:
        filehandle.write(f"FILE CREATED: {today} {current_time}")
    

#Running code
    
cam_ops = find_that_phd("cam", cambridge_url)
lon_ops = find_that_phd("lon", london_url)


#print(type(cam_ops))

if type(cam_ops) == list and type(lon_ops) == list:
    output = cam_ops + lon_ops
    results = html_style(output)
    results_pt = plain_text(output)
else:
    if type(cam_ops) == list:
        results = html_style(cam_ops)
        results_pt = plain_text(cam_ops)
        
    if type(lon_ops) == list:
        results = html_style(lon_ops)
        results_pt = plain_text(lon_ops)
        
    elif type(cam_ops) == str and type(lon_ops) == str:
        results = False

print(results)

if results == False:
    with open(log_file_path, 'a') as filehandle:
        filehandle.write(f"\n{today} {current_time}: No new PhDs found")
else:
    email_results(email, password, results, results_pt)
    with open(log_file_path, 'a') as filehandle:
        filehandle.write(f"\n{today} {current_time}: Email sent")
        
#log what has been done (IE no new Phds or email sent - add time and date)
    