#!/usr/bin/python
__author__ = "Rosh PR"

from time import sleep

__MAPPINGS = frozenset(['aws', 'azure', 'googlecloud'])

def recur_zk(zk,child):
    print 'ZK child path : {}'.format(child)
    try:
       children = zk.get_children(child)
       if len(children) > 0:
           #print 'No of children for: {} = {}'.format(child, len(children))
           for childnode in children:
               recur_zk(zk, child+'/'+childnode)
       else:
           print 'Child: {} = {}'.format(child, zk.get(child))
    except Exception as ex:
       print 'Data fetch failed'

def read_zookeeper(ip, zk_user, zk_pass):
    zk = None
    max_retry = 5
    retry = 1

    try:
        from kazoo.client import KazooClient
        zk = KazooClient(hosts='{}:2181'.format(ip), auth_data=[("digest", "{}:{}".format(zk_user,zk_pass))])
    except Exception as exp:
        print 'Zookeeper kazoo client not available'
        exit(1)

    while retry <= max_retry:
        try:
            retry += 1
            zk.start()
            print 'ZK started for nodes : {}'.format(__MAPPINGS)
            for child in __MAPPINGS:
                recur_zk(zk, "/"+child)
            zk.stop()
            print 'ZK stopped'
            break
        except:
            print 'Zookeeper cleanup failed: retry {}'.format(retry)
            sleep(1)
            if retry > max_retry:
                print 'Zookeeper read failed, exiting operation'
                sys.exit(1)
    print 'Zookeeper read completed'
    return True

if __name__ == "__main__":
    zk_ip = raw_input("Enter Zookeeper server IP")    
    zk_user = raw_input("Enter Zookeeper Admin user")    
    zk_pass = raw_input("Enter Zookeeper Admin password")    
    read_zookeeper(zk_ip, zk_user, zk_pass)
