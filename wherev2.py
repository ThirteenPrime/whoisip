
import os
import argparse

'''
#!/usr/bin/env bash
python3 /home/pi/bin/where.py /home/pi/interfacedb $1
exit
'''

# cwd = os.getcwd()+'/'


def main():
    parser = argparse.ArgumentParser(description="IP Database build")
    parser.add_argument("ip_address", help="ip_address")
    parser.add_argument("-d", "--dbfile", help="dbfilepath", default="intdb")
    args = parser.parse_args()
    findaddr = args.ip_address
    dbfilepath = args.dbfile
    for line in findipadlist(findaddr, dbfilepath):
        print(line)


def iptonumber(ipaddress='192.168.1.1'):
    ipnumber = 0
    for x in ipaddress.split('.', 4):
        ipnumber <<= 8
        ipnumber += int(x)
    return (ipnumber)


def isipsubnet(ipnumber1, ipnumber2, mask):
    '''
    checks if ipnumber1 is a subnet of ipnumber2 and mask(integer)
    '''
    # subnetmask Hex
    subnetmaskList = [0x0, 0x80000000, 0xc0000000, 0xe0000000, 0xf0000000, 0xf8000000, 0xfc000000, 0xfe000000, 0xff000000, 0xff800000, 0xffc00000, 0xffe00000, 0xfff00000, 0xfff80000, 0xfffc0000, 0xfffe0000,
                      0xffff0000, 0xffff8000, 0xffffc000, 0xffffe000, 0xfffff000, 0xfffff800, 0xfffffc00, 0xfffffe00, 0xffffff00, 0xffffff80, 0xffffffc0, 0xffffffe0, 0xfffffff0, 0xfffffff8, 0xfffffffc, 0xfffffffe, 0xffffffff]

    if ((subnetmaskList[mask] & ipnumber1) == (subnetmaskList[mask] & ipnumber2)):
        return (True)
    else:
        return (False)


# findaddr = args.ip_address
# dbfilepath = args.dbfile
# test manual
# findaddr = '10.123.173.130'
# dbfilepath = 'interfacedb'


def findipadlist(findaddr='1.1.1.1', dbfilepath='intdb'):
    findaddrNum = iptonumber(findaddr)
    index1 = findaddr.find('.')
    # read first 2 octets faster read? lols
    f2b = findaddr[:findaddr.find('.', index1+1)+1]
    matchedlist = []
    with open(dbfilepath, 'r') as file:
        intdbfile = file.readlines()

    for line in intdbfile:
        line = line.strip().strip('\n')
        if line:
            hostname, ipadd, interface = line.strip().split(',', 3)
            ipadd, mask = ipadd.split('/')
            if f2b in ipadd:
                # print(f'TEST ipadd:{ipadd},mask:{mask}')
                if (isipsubnet(findaddrNum, iptonumber(ipadd), int('32'))):
                    matchedlist = []
                    matchedlist.append(f'{line}')
                    return matchedlist
                elif (isipsubnet(findaddrNum, iptonumber(ipadd), int(mask))):
                    matchedlist.append(line)
    return matchedlist


if __name__ == "__main__":
    main()
# for line in findipadlist(findaddr, dbfilepath):
#    print(line)
'''
findaddrNum = iptonumber(findaddr)
index1 = findaddr.find('.')
# read first 2 octets faster read? lols
f2b = findaddr[:findaddr.find('.', index1+1)+1]

with open(dbfilepath, 'r') as file:
    intdbfile = file.readlines()

for line in intdbfile:
    line = line.strip().strip('\n')
    if line:
        hostname, ipadd, interface = line.strip().split(',', 3)
        ipadd, mask = ipadd.split('/')
        if f2b in ipadd:
            # print(f'TEST ipadd:{ipadd},mask:{mask}')
            if (isipsubnet(findaddrNum, iptonumber(ipadd), int('32'))):
                print(line)
#'''


'''
result = iptonumber("192.169.1.1")  # 192.168.1.1
result2 = iptonumber("192.168.31.1")  # 192.168.128.1
mask = 16
# if ((subnetmaskList[mask] & result) == (subnetmaskList[mask] & result2)):
#    print('hit')
if (isipsubnet(result, result2, mask)):
    print('hit')
'''
