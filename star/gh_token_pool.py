#coding:utf-8

tokens =[
"7da4689533777fcb9424a67d4dc3b13309e4b525",
"16c32f5f65f9799beb489b910b6de5d8e9725c7b"
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

