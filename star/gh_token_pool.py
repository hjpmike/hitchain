#coding:utf-8

tokens =[
"7da4689533777fcb9424a67d4dc3b13309e4b525",
"16c32f5f65f9799beb489b910b6de5d8e9725c7b"
]

import threading
token_lock = threading.RLock()


def get_token():
	token_lock.acquire()
	if len(tokens) == 0:
		return None
	token = tokens.pop(0)
	# !!!!应该判断该token是否还有访问机会，否则再放回池子里
	token_lock.release()
	return token

def push_token(token):
	token_lock.acquire()
	tokens.append(token)
	token_lock.release()
	return token

