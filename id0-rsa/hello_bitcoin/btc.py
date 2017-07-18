#!/usr/bin/env python3
import hashlib
import base58
import base64
from ecdsa import SigningKey, SECP256k1 

'''
  # http://www.criptored.upm.es/crypt4you/temas/sistemaspago/leccion3/leccion03.html
  # https://en.bitcoin.it/wiki/Elliptic_Curve_Digital_Signature_Algorithm
  # https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
   
  El resultado tiene que ser de 34 Bytes:

    1 -> 1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm
    2 -> 1LagHJk2FyCV2VzrNHVqg3gYG4TSYwDV4m
    3 -> 1NZUP3JAc9JkmbvmoTv7nVgZGtyJjirKV1
    4 -> 1MnyqgrXCmcWJHBYEsAWf7oMyqJAS81eC
    5 -> 1E1NUNmYw1G5c3FKNPd435QmDvuNG3auYk
  
  Cuando funcione, intentarlo con la clave privada 94176137926187438630526725483965175646602324181311814940191841477114099191175
'''

def generateHash(i):
  sk = SigningKey.from_secret_exponent(i,curve=SECP256k1)
  public = sk.privkey.public_key
  
  
  pk=bytearray.fromhex("04%x%x"%(public.point.x(), public.point.y()))
  #print(pk)
  #print(hashlib.sha256(pk).hexdigest())
  #print(hashlib.new('ripemd160', hashlib.sha256(pk).digest()).hexdigest())
  hash_key = "00" + hashlib.new('ripemd160', hashlib.sha256(pk).digest()).hexdigest()
  
  return bytearray.fromhex(hash_key)

def generateBitcoinAddress(privateKey):
    hash_key=generateHash(privateKey)  
    checksum = hashlib.sha256(hashlib.sha256(hash_key).digest()).digest()
    address=base58.b58encode(b''.join([hash_key, checksum[:4]]))
    return address

for i in range(6)[1:]:
  print("%d -> %s" % (i, generateBitcoinAddress(i)))

print(generateBitcoinAddress(94176137926187438630526725483965175646602324181311814940191841477114099191175))


