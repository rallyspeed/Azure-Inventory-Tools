#!/usr/bin/python3
# @Author Mathieu Durand
# Version 1.1

import subprocess
import sys
import datetime
import os
import time
import json
from include import subscription
from os import path



############################################
# MAIN ROUTINE
def main():

    print("Azure Public IP Finder")
    if len(sys.argv) != 2:
        print("[~] Usage : ./checkip.py ip")
        exit()

    if path.exists("restore.txt"):
        print("Retore file found, do you to resume ?")
        answer = None
        while answer not in ("y", "n"):
            answer = input("Enter y or n: ")
            if answer == "y":
                break
            elif answer == "n":
                f=open("restore.txt","w+")
                f.close
            else:
                print("Please enter y or n.")
    else:
        print("No restore file found, starting new search")
        f=open("restore.txt","w+")
        f.close
    ip=sys.argv[1]
    try:
        subs=subscription.sub()
        for j in range(0,len(subs[0])):
            if (check(subs[0][j])):
                print("Skipping sub %s" % subs[0][j])
            else:
                print("Check for ip %s in %s" % (ip,subs[0][j]))
                os.popen('az account set --subscription "%s"' % subs[0][j])
                time.sleep(2)
                #Too Slow
                #result=os.popen('az vm list -d --query [][publicIps,name,resourceGroup] -o tsv | grep "%s"' % ip).read()
                query1=('az group list --query [][name]')
                json_cis=query_az(query1)
                if (len(json_cis)>0):
                    for i in range(len(json_cis)):
                        rg_name=str(json_cis[i][0])
                        print("Checking for the public ip within rg: %s" % rg_name)
                        #Too Slow
                        #query2 = ('az vm show -d -g %s -n %s --query publicIps -o tsv | grep %s' % (rg_name,vm_name,ip))
                        #print(query2)
                        query3 = ('az network public-ip list -g %s --query [] | grep %s' % (rg_name,ip))
                        result=os.popen(query3).read()
                        if result != "":
                            print("IP was found in subscription %s %s %s" % (subs[0][j],subs[1][j],subs[2][j]))
                            print("Public IP is used by a VM in Resource Group %s" % rg_name)
                            result_final=os.popen('az vm list -d -g %s --query [][publicIps,name] -o tsv | grep "%s"' % (rg_name,ip)).read()
                            print(result_final)
                            exit()
                print("IP was not found in subscription %s" % subs[0][j])
                f=open("restore.txt", "a")
                f.write(subs[0][j])
                f.write("\n")
                f.close
    except Exception as e:
        print("Exception in main: %s %s" % (type(e), str(e.args)))
        print("Error with subscription %s " % subs[0][j])
        print("Resume the check and this subscription will be ignored")
        f=open("restore.txt", "a")
        f.write(subs[0][j])
        f.write(" : Error\n")
        f.close
        sys.exit(0)

############################################
# QUERY AZ JSON
def query_az(query):
    json_cis=os.popen(query).read()
    return json.loads(json_cis)

############################################
# Check restore point
def check(subid):
    with open('restore.txt') as f:
        datafile = f.readlines()
    for line in datafile:
        if subid in line:
            return True
    return False

############################################
# SCRIPT EXECUTION
if __name__ == "__main__":
    # Calling main()
    main()
