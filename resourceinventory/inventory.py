#!/usr/bin/python3
# @Author Mathieu Durand
# Version 1.1



import subprocess
import sys
import datetime
import os
import time
from include import subscription



############################################
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
        reportname=("Inventory.csv")

        menu_item=True
        while menu_item:
            print("--------------------")
            for i in range(0,len(subs[0])):
                print("%d. %s" % (i,subs[2][i]))
            print("A. All Subscriptions")
            print("Q. Quit")
            menu_item = input("Select a subscription from the menu: ")
            if menu_item=="Q":
                print("Q")
                break
            elif menu_item=="A":
                print("A")
                f=open(reportname,"w+")
                f.write('Subscription Name,Number of VNET,Number of VM,Number of Windows VM,Nomber of Linux VM,Number of NSG, Number of Application Gateway, Number of LB, Number of SQL Servers\n')
                f.close()
                for j in range(0,len(subs[0])):
                    print("Starting V NET Count for: %s" % subs[2][j])
                    os.popen('az account set --subscription "%s"' % subs[0][j])
                    time.sleep(2)
                    #id print(subs[0][j])
                    #environementName print(subs[1][j])
                    #name print(subs[2][j])
                    vnet=os.popen('az network vnet list --query [][id] --output tsv | wc -l')
                    vm=os.popen('az vm list --query [][id] --output tsv | wc -l')
                    vm_win=os.popen('az vm list | grep \'"osType": "Windows"\' | wc -l')
                    vm_lin=os.popen('az vm list | grep \'"osType": "Linux"\' | wc -l')
                    nsg=os.popen('az network nsg  list --query [][id] --output tsv | wc -l')
                    alg=os.popen('az network application-gateway list --query [][id] --output tsv | wc -l')
                    lb=os.popen('az network lb list --query [][id] --output tsv | wc -l')
                    sql=os.popen('az sql server list --query [][id] --output tsv | wc -l')

                    vnet_number=int(vnet.read())
                    vm_number=int(vm.read())
                    vm_win_number=int(vm_win.read())
                    vm_lin_number=int(vm_lin.read())
                    nsg_number=int(nsg.read())
                    alg_number=int(alg.read())
                    lb_number=int(lb.read())
                    sql_number=int(sql.read())

                    totalvnetnumber = totalvnetnumber + vnet_number
                    totalvmnumber = totalvmnumber + vm_number

                    print('Number of VNET: %i' % vnet_number)
                    print('Number of VM: %i' % vm_number)
                    f=open(reportname,"a")
                    f.write('%s,%i,%i,%i,%i,%i,%i,%i,%i\n' % (subs[2][j],vnet_number,vm_number,vm_win_number,vm_lin_number,nsg_number,alg_number,lb_number,sql_number))
                    f.close() 
                print('Total Number of VNET: %i' % totalvnetnumber)
                print('Total Number of VM: %i' % totalvmnumber)
                break
            elif (menu_item.isdigit() and int(menu_item) in range(0,len(subs[0]))):
                print("Starting V NET Count for: %s" % subs[2][int(menu_item)])

                os.popen('az account set --subscription "%s"' % subs[0][int(menu_item)])
                vnet=os.popen('az network vnet list --query [][id] --output tsv | wc -l')
                vm=os.popen('az vm list --query [][id] --output tsv | wc -l')
                vm_win=os.popen('az vm list | grep \'"osType": "Windows"\' | wc -l')
                vm_lin=os.popen('az vm list | grep \'"osType": "Linux"\' | wc -l')
                nsg=os.popen('az network nsg  list --query [][id] --output tsv | wc -l')
                alg=os.popen('az network application-gateway list --query [][id] --output tsv | wc -l')
                lb=os.popen('az network lb list --query [][id] --output tsv | wc -l')
                sql=os.popen('az sql server list --query [][id] --output tsv | wc -l')

                vnet_number=int(vnet.read())
                vm_number=int(vm.read())
                vm_win_number=int(vm_win.read())
                vm_lin_number=int(vm_lin.read())
                nsg_number=int(nsg.read())
                alg_number=int(alg.read())
                lb_number=int(lb.read())
                sql_number=int(sql.read())

                print('Total Number of VNET: %i' % vnet_number)
                print('Number of VM: %i' % vm_number)
                print('Number of NSG: %i' % nsg_number)
                print('Number of ALG: %i' % alg_number)
                print('Number of LB: %i' % lb_number)
                print('Number of SQL Servers: %i' % sql_number)
                break
            else:
                print("\n Not Valid Choice Try again")

        print("Report %s was Created" % reportname)
        print("\nDone\n")

    except Exception as e:

        print("Exception in main: %s %s" % (type(e), str(e.args)))
        sys.exit(0)


############################################
# SCRIPT EXECUTION
if __name__ == "__main__":
    # Calling main()
    main()
