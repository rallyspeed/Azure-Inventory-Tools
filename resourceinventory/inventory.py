#!/usr/bin/python3
# @Author Mathieu Durand
# Version 1.1


import subprocess
from subprocess import call  
import sys
import datetime
import os
import time
import json
import tempfile
from include import subscription
#from azure.cli.core import get_default_cli as azcli
from os import path
from colorama import Fore,init
import shutil

############################################
#AZ-CLI
def az_cli (args_str):
    args = args_str.split()
    proc = subprocess.Popen(args,stdout=subprocess.PIPE)
    out = proc.stdout.readlines()
    count = len(out)
    return count

############################################
# Check restore point
def check(subid):
    with open('restore.csv') as f:
        datafile = f.readlines()
    for line in datafile:
        if subid in line:
            return True
    return False

############################################
# Menu
def Menu(subs):
    menu_item=True
    while menu_item:
        print("--------------------")
        for i in range(0,len(subs[0])):
            print("%d. %s" % (i,subs[2][i]))
        print("A. All Subscriptions")
        print("Q. Quit")
        menu_item = input("Select a subscription from the menu: ")
        if menu_item=="Q":
            break
        elif menu_item=="A":
            Multiple_sub(subs)
            break
        elif (menu_item.isdigit() and int(menu_item) in range(0,len(subs[0]))):
            #print("Starting V NET Count for: %s" % subs[2][int(menu_item)])
            #cli_cmd = 'az account set --subscription %s' % subs[0][int(menu_item)]
            try:
                print("Accessing Subscription to: %s" % subs[2][int(menu_item)])
                # Switch subscription id
                cli_cmd = 'az account set --subscription %s' % subs[0][int(menu_item)]
                az_cli(cli_cmd)
            except:
                print("Logging to Azure")
                az_cli('az login --use-device-code')
                print("Accessing Subscription to: %s" % subs[2][int(menu_item)])
                cli_cmd_2 = 'az account set --subscription %s' % subs[0][int(menu_item)]
                az_cli(cli_cmd_2)
            Single_sub()
            break
        else:
            print("\n Not Valid Choice Try again")

############################################
# Single Sub
def Single_sub():
     
    vm_number = 0
    vm_lin_number = 0
    vm_win_number = 0
    vnet_number = 0
    nsg_number = 0
    alg_number = 0
    lb_number = 0
    sql_number = 0
    aks_number=0
    aksnodes_number=0
    azfw_number=0
    vnet_number = az_cli('az network vnet list --query [][id] --output tsv')
    print('Total Number of VNET: %i' % vnet_number)
    vm_number=az_cli('az vm list --query [][id] --output tsv')
    print('Number of VM: %i' % vm_number)
    vm_win_number=az_cli('az vm list --query [][][storageProfile.osDisk.osType] --output tsv ')
    vm_lin_number=az_cli('az vm list --query [][][storageProfile.osDisk.osType] --output tsv ')
    nsg_number=az_cli('az network nsg  list --query [][id] --output tsv')
    print('Number of NSG: %i' % nsg_number)
    alg_number=az_cli('az network application-gateway list --query [][id] --output tsv')
    print('Number of ALG: %i' % alg_number)
    lb_number=az_cli('az network lb list --query [][id] --output tsv')
    print('Number of LB: %i' % lb_number)
    sql_number=az_cli('az sql server list --query [][id] --output tsv')
    print('Number of SQL Servers: %i' % sql_number)
    aks_number=az_cli('az aks list --query [][id] --output tsv')
    print('Number of AKS Cluster: %i' % aks_number)
    if aks_number!=0:
        aksnodes=os.popen('az aks list --query [][agentPoolProfiles][][][count] --output tsv | paste -sd+ | bc')
        aksnodes_number=int(aksnodes.read())
    else:
        aksnodes_number=0
    print('Number of AKS Nodes: %i' % aksnodes_number)
    #Required azure-firewall extension
    azfw_number=az_cli('az network firewall list --query [][id] --output tsv')
    print('Number of Azure Firewalls Nodes: %i' % azfw_number)

############################################
# Multiple Sub
def Multiple_sub(subs):

    init(autoreset=True)

    #Checking for any previous restore points
    if path.exists("restore.csv"):
        print("Retore file found, do you to resume ?")
        answer = None
        while answer not in ("y", "n"):
            answer = input("Enter y or n: ")
            if answer == "y":
                break
            elif answer == "n":
                f=open("restore.csv","w+")
                f.write('Subscription Name,Number of VNET,Number of VM,Number of Windows VM,Nomber of Linux VM,Number of NSG, Number of Azure Firewall,Number of Application Gateway, Number of LB, Number of SQL Servers,Number of AKS Cluster,Number of AKS nodes\n')
                f.close
            else:
                print("Please enter y or n.")
    else:
        print("No restore file found, starting new search")
        f=open("restore.csv","w+")
        f.write('Subscription Name,Number of VNET,Number of VM,Number of Windows VM,Nomber of Linux VM,Number of NSG, Number of Azure Firewall,Number of Application Gateway, Number of LB, Number of SQL Servers,Number of AKS Cluster,Number of AKS nodes\n')
        f.close

    for j in range(0,len(subs[0])):
        #reset counters
        vm_number = 0
        vm_lin_number = 0
        vm_win_number = 0
        vnet_number = 0
        nsg_number = 0
        alg_number = 0
        lb_number = 0
        sql_number = 0
        aks_number=0
        aksnodes_number=0
        azfw_number=0

        if (check(subs[2][j])):
            print(Fore.MAGENTA + ("Skipping subscription %s" % subs[2][j]))
        else:
            try:
                print("Accessing Subscription to: %s" % subs[2][j])
                # Switch subscription id
                cli_cmd = 'az account set --subscription %s' % subs[0][j]
                az_cli(cli_cmd)

            except:
                print("Logging to Azure")
                #os.popen('az login')
                #cli_cmd_1 = "login --use-device-code"
                az_cli('az login --use-device-code')
                print("Accessing Subscription to: %s" % subs[2][j])
                cli_cmd_2 = 'az account set --subscription %s' % subs[0][j]
                az_cli(cli_cmd_2)  
            print("Collection Data for %s ..." % subs[2][j])
            vnet_number = az_cli('az network vnet list --query [][id] --output tsv')
            vm_number=az_cli('az vm list --query [][id] --output tsv')
            
            win_vm_query_1 = ("[?storageProfile.osDisk.osType=='Windows'].{Name:name}")
            win_vm_query_2='az vm list --query "%s" --output tsv' % win_vm_query_1
            vmpopen=os.popen("%s | wc -l" % win_vm_query_2)
            vm_win_number=int(vmpopen.read())

            lin_vm_query_1 = ("[?storageProfile.osDisk.osType=='Linux'].{Name:name}")
            lin_vm_query_2='az vm list --query "%s" --output tsv' % lin_vm_query_1
            vmpopen=os.popen("%s | wc -l" % lin_vm_query_2)
            vm_lin_number=int(vmpopen.read())

            nsg_number=az_cli('az network nsg list --query [][id] --output tsv')
            alg_number=az_cli('az network application-gateway list --query [][id] --output tsv')
            lb_number=az_cli('az network lb list --query [][id] --output tsv')
            sql_number=az_cli('az sql server list --query [][id] --output tsv')
            aks_number=az_cli('az aks list --query [][id] --output tsv')

            #vm_win = "%s | wc -l | grep \'Windows\'" % vm_win_cmd
            #vm_lin = "%s | wc -l | grep \'Linux\'" % vm_lin_cmd

            #Required azure-firewall extension
            azfw_number=az_cli('az network firewall list --query [][id] --output tsv')   

            if aks_number!=0:
                try:
                    aksnodes_cmd=az_cli('az aks list --query [][agentPoolProfiles][][][count] --output tsv')
                    aksnodes = "%s | paste -sd+ | bc" % aksnodes_cmd
                    aksnodes_number=int(aksnodes.read())
                except:
                    aksnodes_number=0
            else:
                aksnodes_number=0

            #totalvnetnumber = totalvnetnumber + vnet_number
            #totalvmnumber = totalvmnumber + vm_number
            f=open("restore.csv","a")
            f.write('%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i,%i\n' % (subs[2][j],vnet_number,vm_number,vm_win_number,vm_lin_number,nsg_number,azfw_number,alg_number,lb_number,sql_number,aks_number,aksnodes_number))
            f.close()
            print(Fore.GREEN + ("Collection completed for subscription %s" % subs[2][j]))
            #print('Number of VNET: %i' % vnet_number)
            #print('Number of VM: %i' % vm_number)
            
    #print('Total Number of VNET: %i' % totalvnetnumber)
    #print('Total Number of VM: %i' % totalvmnumber)
    

    timestr = time.strftime("%Y%m%d-%H%M%S")
    reportname=("Inventory"+timestr+".csv")
    shutil.copy("restore.csv",reportname)
    print("Report %s was Created" % reportname)
    print("\nDone\n")

# MAIN ROUTINE
def main():

    print("Azure Inventory")

    try:
        subs=subscription.sub()
        menu_item = 0
        totalvnetnumber = 0
        totalvmnumber = 0
        vm_number = 0
        vnet_number = 0
        nsg_number = 0
        alg_number = 0
        lb_number = 0
        sql_number = 0
        aks_number=0
        aksnodes_number=0
        azfw_number=0
        Menu(subs)

    except Exception as e:

        print("Exception in main: %s %s" % (type(e), str(e.args)))
        sys.exit(0)


############################################
# SCRIPT EXECUTION
if __name__ == "__main__":
    # Calling main()
    main()
