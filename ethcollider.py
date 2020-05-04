#!/usr/bin/env python
# coding=utf8

# Ethereum Collider
# Copyright (C) 2017  Trent Pierce
#
# Pure Python address generator with Collision detection
#
# Random source for key generation :
# CryptGenRandom in Windows
# /dev/urandom   in Unix-like
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# Uses python-sha3 from moshekaplan
#
# Enter optional argument : a hex string shorter than 11 chars
#
# Updated 2020 
#
from lib.ECDSA_BTC import *
import lib.python_sha3
import requests
import json
import os
import sys

def hexa(cha):
	hexas=hex(cha)[2:-1]
	while len(hexas)<64:
		hexas="0"+hexas
	return hexas

def hashrand(num):
	#return sha256 of num times 256bits random data
	rng_data=''
	for idat in xrange(num):
		rng_data = rng_data + os.urandom(32)
	assert len(rng_data) == num*32
	return hashlib.sha256(rng_data).hexdigest()

def randomforkey():
	candint = 0
	r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L
	while candint<1 or candint>=r:
		cand=hashrand(1024)
		candint=int(cand,16)
	return candint

def compute_adr(priv_num):
	try:
		pubkey = Public_key( generator_256, mulG(priv_num) )
		pubkeyhex = (hexa(pubkey.point.x())+hexa(pubkey.point.y())).decode("hex")
		return lib.python_sha3.sha3_256(pubkeyhex).hexdigest()[-40:]
	except KeyboardInterrupt:
		return "x"

def found():
       	load_gtable('lib/G_Table')
        wallets = 0
	balance = 0
        while True:
        	try:
               		privkeynum = randomforkey()
               		address = compute_adr(privkeynum)
                	foundprivkeynum = privkeynum
                	wallets = wallets + 1
                	pvhex = hexa(foundprivkeynum)
                	# address = '56Ed8A68c1B5074522Bc681b629f27139019F63B'
                	url = 'https://api.etherscan.io/api?module=account&action=balance&address=0x' + address + '&tag=latest&apikey=V7GSGSMWZ2CZH1B6MBXM84SZ1XG4DXDCW9';
                	# print url
                	r = requests.get(url)
                	# r.text
                	# print r.text
                	data = json.loads(r.text)
                	balance = data['result']
                	print '\r'+'Searched ',wallets,' addresses 0x' + address + ' ' + pvhex

                	if balance != '0':
                        	print 'Wallet Found!'

                        	print "\nAddress :  %s \n" % address

                        	print "PrivKey :  %s\n" % pvhex

                        	with open('money.prv', 'a+') as f:
                                	f.write(address+ '    ' + pvhex +'    ' + balance + '\n')
                	else:
                        	with open('record.txt', 'a+') as f:
                                	f.write(address+ '    ' + pvhex +'    ' + balance + '\n')
        	except Exception as e:
                	print str(e)
        
if __name__ == '__main__':
	import hashlib
        import re
        import sys
        import time
        import os.path
        from lib.humtime import humanize_time
	found()
