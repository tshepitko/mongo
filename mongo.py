from bson import json_util
import json
import sys
import os
from pymongo import MongoClient
from datetime import datetime
import time

mongo_stats = {'serverStatus': 'serverstatus',
               'dbStats': 'dbstats',
               'replSetGetStatus': 'repsetgetstatus'
}

def mongo_connect(HOST):
    client, db = 0, 0
    try:
        client = MongoClient(host='mongodb://' + str(HOST))
        if get_server_db() == 'replSetGetStatus':
            db = client.admin
        else:
            db = client.data
        client.close()
    except:
        test = 0

    return (db)

def get_server_db():
    try:
        return str(mongo_stats[str(sys.argv[2])])
    except:
        return('<Not successful command>')

def get_server_status(db, command):
    if db != 0:
        try:
            data = db.command({str(command): 1})
            db.logout()
            return (data)
        except:
            return ('<Not successful command>')
    else:
        return ('<Not successful connect to Database>')

def write_to_stats(host, command, fname):
    db = mongo_connect(host)
    data = json.dumps(get_server_status(db, command[0]), default=json_util.default)
    with open(fname, 'a') as f:
        f.write(str(time.mktime(datetime.now().timetuple())) + " delimeterrr " + str(data))
    return (data)

def file_len(fname):
    with open(fname) as f:
        for i,l in enumerate(f):
            pass
    return (i + 1)

def cut(fname):
    with open(fname) as f:
        lines = f.readlines()
    with open(fname,'w') as f:
        for ind in range(1,len(lines)):
            f.write(lines[ind])
    return()

def check_stats(fname):
    try:
        lines = file_len(str(fname))
        if lines == 0:
           write_to_stats(sys.argv[1], sys.argv[2:], str(fname))
           return 0
        else:
            cut(str(fname))
            write_to_stats(sys.argv[1], sys.argv[2:], str(fname))
            return 1
    except:
        write_to_stats(sys.argv[1], sys.argv[2:], str(fname))
        return 0

def parse_cmd(data,command):
    try:
        for param in command:
            data = data[param]

    except:
        print('<Not successful command>')

def parse_arg(old_data, new_data, command):
    command = command.split()
    temp_data = new_data
    if command[0] == 'opcounters':
        try:
            for param in command:
                temp_data = temp_data[param]
            return temp_data
        except:
            print('<Not successful command>')

def check_age(fname):
    with open(str(fname)) as f:
        file_time = int(f.read().split('.')[0])
    curr_time = int(time.mktime(datetime.now().timetuple()))
    if curr_time - file_time < 90:
        return 0
    else:
        write_to_stats(sys.argv[1], sys.argv[2:], str(fname))
        return 1

def read_status(fname):
    with open(str(fname)) as f:
        return json.loads(f.read().split('delimeterrr')[1])


def main():
    check_stats(sys.argv[2])


if __name__ == "__main__":
    main()


