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
    with open(fname, 'w') as f:
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
           return False
        else:
            if check_age(fname) == False:
                data = write_to_stats(sys.argv[1], sys.argv[2:], str(fname))
            else:
                db = mongo_connect(sys.argv[1])
                data = json.dumps(get_server_status(db, sys.argv[2]), default=json_util.default)
            return data
    except:
        write_to_stats(sys.argv[1], sys.argv[2:], str(fname))
        return False

def parse_cmd(command):
    try:
        return command.split('.')
    except:
        return('<Incorrect input>')

def parse_arg(data, command):
    cmd = parse_cmd(command)
    temp_data = data
    try:
        for param in cmd:
            temp_data = temp_data[param]
        return temp_data
    except:
        print('<Not successful command>')

def check_age(fname):
    with open(str(fname)) as f:
        file_time = int(f.read().split('.')[0])
    curr_time = int(time.mktime(datetime.now().timetuple()))
    if curr_time - file_time < 90:
        return True
    else:
        return False

def read_status(fname):
    with open(str(fname)) as f:
        return json.loads(f.read().split('delimeterrr')[1])


def main():
    try:
        new_data = json.loads(check_stats(sys.argv[2]))
        if type(new_data) is dict:
            old_data = read_status(sys.argv[2])
            if sys.argv[2] == 'serverStatus' and sys.argv[3].split('.')[0] == 'opcounters':
                result = int(parse_arg(new_data,sys.argv[3])) - int(parse_arg(old_data,sys.argv[3]))
            else:
                result = parse_arg(old_data, sys.argv[3])
            print(result)
    except:
        print('<Internal error>')


if __name__ == "__main__":
    main()


