# -*- coding: utf-8 -*-

import time
import random
import requests
import ConfigParser 
import oss2
from qcloud_cos import CosClient, UploadFileRequest, StatFileRequest, DelFileRequest

COS_BUCKET = u'your-cos-bucket'

def get_oss_client():
    config = ConfigParser.ConfigParser()
    config.read('./test.cfg')
    access_key = config.get('OSS', 'access_key')
    access_secret = config.get('OSS', 'access_secret')
    auth = oss2.Auth(access_key, access_secret)
    endpoint = config.get('OSS', 'endpoint')
    bucket = config.get('OSS', 'bucket')
    oss_client = oss2.Bucket(auth, endpoint, bucket)
    return oss_client

def get_cos_client():  
    config = ConfigParser.ConfigParser()
    config.read('./test.cfg')
    appid = int(config.get('COS', 'appid'))
    secret_id = unicode(config.get('COS', 'secret_id'))
    secret_key = unicode(config.get('COS', 'secret_key'))
    global COS_BUCKET
    COS_BUCKET = unicode(config.get('COS', 'bucket'))
    cos_client = CosClient(appid, secret_id, secret_key)
    return cos_client

def random_str(randomlength = 8):
    str = ''
    char_set = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    list = []
    for i in xrange(0, randomlength):
        list.append(random.choice(char_set))
    return "".join(list)

def gen_random_file(file_name, size):
    f = file(file_name, 'w+')
    content = random_str(size)
    f.write(content)
    f.close()

def get_timelocal():
    return time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))

def upload_oss(count, size, save = 'upload-result-oss', wait = 0):
    oss_client = get_oss_client()
    result = open(save, 'w+')
    while count > 0:
        try:
            count = count - 1
            file = 'tmp-file-oss'
            gen_random_file(file, size)
            with open(file, 'rb') as fileobj:
                file_oss = '%d-%d'%(size, count)
                start = time.time()
                resp = oss_client.put_object(file_oss, fileobj)
                end = time.time()
                if resp.status != 200:
                    continue
                latency = (end - start) * 1000.0
                result.write("%s OSS UPLOAD %d %.03f\n" % (get_timelocal(), size, latency))
                result.flush()
                print u'upload %s to oss time spend %0.3f ms in size %dB' % (file_oss, latency, size)
            if wait != 0:
                time.sleep(wait)
        except:
            print 'Error Occur'
        else:
            pass
    result.close()

def upload_cos(count, size, save = 'upload-result-cos', wait = 0):
    cos_client = get_cos_client()
    bucket = COS_BUCKET
    result = open(save, 'w+')
    while count > 0:
        try:
            count = count - 1
            file = 'tmp-file-cos'
            gen_random_file(file, size)
            file_cos = u'/' + '%d-%d'%(size, count)
            request = UploadFileRequest(bucket, file_cos, unicode(file))
            request.set_insert_only(0)
            start = time.time()
            resp = cos_client.upload_file(request)
            end = time.time()
            if resp['code'] != 0:
                continue
            latency = (end - start) * 1000.0
            result.write("%s COS UPLOAD %d %.03f\n" % (get_timelocal(), size, latency))
            result.flush()
            print u'upload %s to cos time spend %0.3f ms in size %dB' % (file_cos, latency, size)
            if wait != 0:
                time.sleep(wait)
        except:
            print 'Error Occur'
        else:
            pass
    result.close()


def download_oss(count , size, save = 'download-result-oss', wait = 0):
    oss_client = get_oss_client()
    result = open(save, 'w+')
    while count > 0:
        try:
            count = count - 1
            file_oss = '%d-%d'%(size, count)
            presign_url = oss_client.sign_url('GET', file_oss, 120)
            start = time.time()
            ask = requests.get(presign_url, timeout = 30)
            end = time.time()
            if ask.status_code != 200:
                continue
            latency = (end - start) * 1000.0
            result.write("%s OSS DOWNLOAD %d %.03f\n" % (get_timelocal, size, latency))
            result.flush()
            print u'download %s from oss time spend %0.3f ms in size %dB' % (file_oss, latency, size) 
            if wait != 0:
                time.sleep(wait)
        except:
            print 'Error Occur'
        else:
            pass
    result.close()
        

def download_cos(count, size, save = 'download-result-cos', wait = 0):
    cos_client = get_cos_client()
    bucket = COS_BUCKET
    result = open(save, 'w+')
    while count > 0: 
        try:
            count = count - 1
            file_cos = u'/' + '%d-%d'%(size, count)
            request = StatFileRequest(bucket, file_cos)
            status = cos_client.stat_file(request)
            if status['code'] != 0:
                continue
            cos_url = status['data']['source_url']
            start = time.time()
            ask = requests.get(cos_url, timeout=60)
            end = time.time()
            if ask.status_code != 200:
                continue
            latency = (end - start) * 1000.0
            result.write("%s COS DOWNLOAD %d %.03f\n" % (get_timelocal(), size, latency))
            result.flush()
            print u'download %s from cos time spend %0.3f ms in size %dB' % (file_cos, latency, size) 
            if wait != 0:
                time.sleep(wait)
        except:
            print 'Error Occur'
        else:
            pass
    result.close()


def delete_oss(count, size, save = 'delete-result-oss', wait = 0):
    oss_client = get_oss_client()
    result = open(save, 'w+')
    while count > 0:
        try:
            count = count - 1
            file_oss = '%d-%d'%(size, count)
            start = time.time()
            resp = oss_client.delete_object(file_oss)
            end = time.time()
            if resp.status != 204:
                continue
            latency = (end - start) * 1000.0
            result.write("%s OSS DELETE %d %.03f\n" % (get_timelocal(), size, latency))
            result.flush()
            print u'delete %s from oss time spend %0.3f ms in size %dB' % (file_oss, latency, size) 
            if wait != 0:
                time.sleep(wait)
        except:
            print 'Error Occur'
        else:
            pass
    result.close()

def delete_cos(count, size, save = 'delete-result-cos', wait = 0):
    cos_client = get_cos_client()
    bucket = COS_BUCKET
    result = open(save, 'w+')
    while count > 0:
        try:
            count = count - 1
            file_cos = u'/' + '%d-%d'%(size, count)
            request = DelFileRequest(bucket, file_cos)
            start = time.time()
            resp = cos_client.del_file(request)
            end = time.time()
            if resp['code'] != 0:
                continue
            latency = (end - start) * 1000.0
            result.write("%s COS DELETE %d %.03f\n" % (get_timelocal(), size, latency))
            result.flush()
            print u'delete %s from cos time spend %0.3f ms in size %dB' % (file_cos, latency, size)
            if wait != 0:
                time.sleep(wait)
        except:
            print "Error Occur"
        else:
            pass
    result.close()

if __name__ == '__main__':
    pass

