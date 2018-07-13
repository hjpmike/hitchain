#coding:utf-8
'''
created by starlee @ 2018-07-13 15:00
for fetching raw infos from html
'''

def readPrjLists():
	prjs = []
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = prj_line.split("\t")
			prjs.append(prjls[0])
	return prjs
			
def main():
	prjs = readPrjLists()

if __name__ == '__main__':
	main()