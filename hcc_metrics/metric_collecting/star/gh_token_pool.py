#coding:utf-8

tokens =[
"0e5d6ee655bed62cb438bbd32943f2d9713040b5",
"1d25dd98d765f0cc954c20ef707f073eb4ed641c",
"8473449bccdefa3dec9ac06f80fc042b67d7a4e3",
"f026d39092d3807e48019a52c49618a24fc168df",
"1d9a0dfdc0cd255bbc951019837983de46f26138",
"126de57727c7925354aacb270b8ae8b65801b0dd",
"46a708f7c745587ad9b6abd71e62622ec0e882ee",
"19b22fd65f2c4f05756c5189e0a1c035bbe941b8",
"fcdd16ebde8359b49969664b41b51c0c610d7562",
"668df5618567c22481756377bdf298eaa64aeb94",
"453f40d1ae7edc594669ea949dbb920767f16f08",
"dde41c87025db2e4a2e19a3fd1ec26c138a5897e",
"16c32f5f65f9799beb489b910b6de5d8e9725c7b",
"7da4689533777fcb9424a67d4dc3b13309e4b525"
]

import Queue
TOKEN_POOL = Queue.Queue()
for token in tokens:
	TOKEN_POOL.put(token)

def get_token():
	if TOKEN_POOL.empty():
		return None
	token = TOKEN_POOL.get()
	# !!!!应该判断该token是否还有访问机会，否则再放回池子里
	return token

def push_token(token):
	TOKEN_POOL.put(token)

