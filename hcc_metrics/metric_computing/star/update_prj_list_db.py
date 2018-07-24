# coding:utf-8
# 临时性文件 @2018-07-23
# 更新数据库prj_list中项目的gh_url 
import dbop 

def main():

	# 先清空之前的ghurl
	dbop.execute("update prj_list set github_url=Null")

	# 更新ghurl字段
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = [item.strip() for item in prj_line.split("\t")]

			dbop.execute("update prj_list set github_url=%s where prj_id=%s",
							(prjls[1],prjls[0]))
	# 加个字段
	dbop.execute("alter table prj_list add prj_type varchar(50);")
	dbop.execute("update prj_list set prj_type='blockchain';")


if __name__ == '__main__':
	main()