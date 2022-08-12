# Copyright 2021 Reza Masoumvand <rmasoumvand@yahoo.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import xlsxwriter
import sys

def extractPptpId(line):
    #in:<pptp-462710015>
    pptpId = line.split("-")[1]

    if pptpId.endswith('>'):
        pptpId = pptpId[:-1]
        
    return pptpId

def extractUserConnectionInfo(line):
    #10.20.21.26:55156->142.250.185.42:443,
    if ',' in line:
      line = line[:-1]

    connection = line.split('->')

    source = connection[0]
    destination = connection[1]

    connection_info = {}
    
    connection_info["source_ip"], connection_info["source_port"] = source.split(':')
    connection_info["destination_ip"], connection_info["destination_port"] = destination.split(':')

    return connection_info
    

def createXLSReport(data, file_name):
    workbook = xlsxwriter.Workbook('{0}.xlsx'.format(file_name))
    logsheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    
    logsheet.set_column('C:C', 20)
    logsheet.set_column('D:D', 20)
    logsheet.set_column('E:E', 20)
    logsheet.set_column('F:F', 20)
    logsheet.set_column('G:G', 20)
    logsheet.set_column('H:H', 20)

    logsheet.write(0, 0, 'Date', bold)
    logsheet.write(0,1, 'Time', bold)
    logsheet.write(0,2, 'Host Name', bold)
    logsheet.write(0, 3, 'Username', bold)
    logsheet.write(0, 4, 'Source IP', bold)
    logsheet.write(0, 5, 'Source Port', bold)
    logsheet.write(0, 6, 'Destination IP', bold)
    logsheet.write(0, 7, 'Destination Port', bold)

    for i, j in enumerate(data):
        logsheet.write(i+1, 0, j['log_date'])
        logsheet.write(i+1,1, j['log_time'])
        logsheet.write(i+1,2, j['host_name'])
        logsheet.write(i+1, 3, j['user_id'])
        logsheet.write(i+1, 4, j['source_ip'])
        logsheet.write(i+1, 5, j['source_port'])
        logsheet.write(i+1, 6, j['destination_ip'])
        logsheet.write(i+1, 7, j['destination_port'])
    
    workbook.close()
    print("*** Proccessed total #{} records ***".format(i))

def parseLogLine(line):
    log_info = {}
    log_info['log_date'] = "{0} {1}".format(line[0],line[1])
    log_info['log_time'] = line[2]
    log_info['host_name'] = line[3]
    log_info['user_id'] = extractPptpId(line[7])
    log_info.update(extractUserConnectionInfo(line[-3]))

    
    return log_info


def genFileName(filename):
    if '.' in filename:
        filename = filename.split('.')
        return str(filename[0])
    return filename

if __name__ == '__main__':

    if (len(sys.argv) < 2):
        exit(-1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()


    data = []

    for line in lines:
        l = line.split()
        if len(l) < 15:
            continue
        else:
            data.append(parseLogLine(l))    

    createXLSReport(data, genFileName(sys.argv[1]))
