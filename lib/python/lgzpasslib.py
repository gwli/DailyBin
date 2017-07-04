#!/usr/bin/env python
# -*- coding=utf-8 -*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import hashlib
import argparse
import sqlite3

class AESCrypto():
    def __init__(self,key):
        self.key = key
        self.mode = AES.MODE_CBC
	#print AES.block_size

    def encrypt(self,text):
        if len(text)%16!=0:
            text=text+str((16-len(text)%16)*'0')
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self,text):
        cryptor = AES.new(self.key,self.mode,b'0000000000000000')
        plain_text  = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

def gen_SHA(data):
     e = hashlib.sha1(data)
     return e.hexdigest()

def gen_key(data,salt):
  
     raw_data="{}{}".format(data,salt)
     print "{},{},{}".format(data,salt,raw_data)
     e = hashlib.sha512(raw_data)
     e= hashlib.md5(e.hexdigest())
     return e.hexdigest()

def encrypt(key,msg):
    pc = AESCrypto(key[0:32]) #初始化密钥
    e = pc.encrypt(msg)
    return e

def decrypt(key,msg):
    new_key=key[0:32]
    pc = AESCrypto(new_key) #初始化密钥
    d = pc.decrypt(msg) #解密
    return d

def listdb(db_file='lgzpwdb'):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd ="select * from lgzpwd"
    cur.execute(cmd)
    raw_msg= cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return raw_msg 

def decryptfromdb(key,msg,db_file="lgzpwdb"):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd ="select * from lgzpwd where account = '{}'".format(msg)
    cur.execute(cmd)
    raw_msg= cur.fetchone()[2]
    conn.commit()
    cur.close()
    conn.close()
    new_key=key[0:32]
    pc = AESCrypto(new_key) #初始化密钥
    d = pc.decrypt(raw_msg) #解密
    return d
def addtodb(key,value,db_file="lgzpwdb"):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cmd ='insert into lgzpwd(account,password) values ("{}","{}")'.format(key,value)
    cur.execute(cmd)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="crypt msg")
    parser.add_argument("-k",help = "the key",type=str,default="")    
    parser.add_argument("-msg",help = "msg",type=str,default="")    
    parser.add_argument("-t",help = "the type;d,g,c ",type=str,default="g")    
    parser.add_argument("-s",help = "salt",type=str,default="")    
    parser.add_argument("-db",help = "db file",type=str,default="lgzpwdb")    
    args = parser.parse_args()
    if args.t == 's':
       gen_SHA(args.msg)
    elif args.t == 'd':
       decryptfromdb(args.k,args.msg,args.db)
    elif args.t == 'c':
       encrypt(args.k,args.msg)
    elif args.t == 'k':
       gen_key(args.msg,args.s)
    elif args.t == 'a':
       addtodb(args.k,args.msg,db_file=args.db)
    else: 
       gen_SHA(args.msg)
