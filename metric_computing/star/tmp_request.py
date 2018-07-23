#coding:utf-8
from collections import OrderedDict
dateTime = "2018-07-20 20:43:33"
REPO_IDS,REPO_GITS,REPO_NAMES = [],[],[]
import random
import dbop
import json

def readPrjLists():
	with open("prjs.txt","r") as fp:
		for prj_line in fp.readlines():
			prjls = [item.strip() for item in prj_line.split("\t")]
			REPO_IDS.append(int(prjls[0]))
			REPO_GITS.append("https://github.com/%s"%(prjls[1]))
			REPO_NAMES.append(prjls[2])
			

readPrjLists()
result = []
ranking = []

for i in range(0,len(REPO_IDS)):
	prj_result = OrderedDict()
	prj_result["id"] = REPO_IDS[i]
	prj_result["repo_url"] = REPO_GITS[i]
	prj_result["coin_name"] = REPO_NAMES[i]

	# m1 = sum(dbop.select_one("select inf_dev,inf_social from inf where repo_id=%s and computed_at<=%s order by id limit 1",
	# 				(prj,dateTime),(0,0)))
	# m2 = sum(dbop.select_one("select issue_done, commit_total, age_dev, fans_dev, fans_social from maturity where repo_id=%s and computed_at<=%s order by id limit 1",
	# 				(prj,dateTime),(0,0)))
	# m3 = sum(dbop.select_one("select repair_ratio,repair_time from quality_sub where repo_id=%s and computed_at<=%s order by id limit 1",
	# 				(prj,dateTime),(0,0)))
	# m4 = sum(dbop.select_one("selecg  ccr,ngr,tbr from team_health where repo_id=%s and computed_at<=%s order by id limit 1",
	# 				(prj,dateTime),(0,0)))
	# m5 = sum(dbop.select_one("select  ,dev,rel from dev_actv where repo_id=%s and computed_at<=%s order by id limit 1",
	# 				(prj,dateTime),(0,0)))
	# m6 = sum(dbop.select_one("select  dit,tit,dcpt,ucpt from trend where repo_id=%s and computed_at<=%s order by id limit 1",
	# 				(prj,dateTime),(0,0)))

	prj_result["m1_inf"] = float("%3.2f"%random.random())
	prj_result["m2_maturity"] = float("%3.2f"%random.random())
	prj_result["m3_quality"] =float("%3.2f"%random.random())
	prj_result["m4_team_healty"] = float("%3.2f"%random.random())
	prj_result["m5_activatin"] = float("%3.2f"%random.random())
	prj_result["m6_trend"] = float("%3.2f"%random.random())
	prj_result["score"] =float("%3.2f"%(prj_result["m1_inf"] + prj_result["m2_maturity"] +prj_result["m3_quality"] + prj_result["m4_team_healty"]+prj_result["m5_activatin"]+prj_result["m6_trend"]))
	prj_result["rank_date"] = "2018-07-21"
	result.append(prj_result)
	ranking.append((REPO_IDS[i],prj_result["score"]))


sr = sorted(ranking,key=lambda x: x[1],reverse=True)
for i in range(0,len(sr)):
	for prj in result:
		if prj["id"] ==sr[i][0]:
			prj["rank"] = i+1

# ranked_result = sorted(ranking,key=lambda x: x["score"],reverse=True)

with open('rank_template.txt', 'w') as f:
        json.dump(result, f, indent=2)  # 会在目录下


class JsonFormatter:
    def __init__(self, intend=4, name="", encoding="utf-8"):
        '''
        intend: 缩进空格数
        name: 文件名
        encoding: 文件编码
        '''
        self.name = name
        self.intend = intend
        self.encoding = encoding
        self.stack = []
        self.obj = None
        self.source = self.get_source(name)
        self.prepare()

    @staticmethod
    def json_str(s):
        '''
        给字符串套上双引号
        '''
        return '"' + s + '"'

    @staticmethod
    def get_source(name):
        with open(name, 'r',) as f:
            # 当不给split函数传递任何参数时，分隔符sep会采用任意形式的空白字符：空格、tab、换行、回车以及换页符
            return ''.join(f.read().split())

    def prepare(self):
        try:
            # python对象和json格式还是略有不同
            self.source = self.source.replace("null", "None").replace("true", "True").replace("false", "False")
            self.obj = eval(self.source)
        except:
            # json string 一定满足python dict和list的组合
            raise Exception('Invalid json string!')

    def line_intend(self, level=0):
        return '\n' + ' ' * self.intend * level

    def parse_dict(self,obj=None,intend_level=0):
        if intend_level == 0:
            # 这个判断是为了防止文件开头出现空行
            self.stack.append('{')
        else:
            self.stack.append(self.line_intend(intend_level)+'{')
        intend_level += 1
        i = 0
        for key, value in obj.items():
            key = self.json_str(str(key))
            self.stack.append(self.line_intend(intend_level)+key+':')
            self.parse(value, intend_level)
            if i != len(obj.items())-1:
                # 这个处理是为了防止最后一对kv后面还有个逗号，这样会造成json.load()函数无法读取
                self.stack.append(',')
            i += 1
        self.stack.append(self.line_intend(intend_level-1)+'}')

    def parse_list(self, obj=None, intend_level=0):
        if intend_level == 0:
            self.stack.append('[')
        else:
            self.stack.append(self.line_intend(intend_level)+'[')
        intend_level += 1
        for i, item in zip(range(0, len(obj)), obj):
            self.parse(item, intend_level)
            if i != len(obj)-1:
                self.stack.append(',')
        self.stack.append(self.line_intend(intend_level-1)+']')

    def parse(self, obj, intend_level=0):
        if obj is None:
            self.stack.append('null')
        elif obj is True:
            self.stack.append('true')
        elif obj is False:
            self.stack.append('false')
        elif isinstance(obj, (int, float)):
            self.stack.append(str(obj))
        elif isinstance(obj, str):
            self.stack.append(self.json_str(obj))
        elif isinstance(obj, (list, tuple)):
            self.parse_list(obj, intend_level)
        elif isinstance(obj, dict):
            self.parse_dict(obj, intend_level)
        else:
            raise Exception('Invalid json type %s!' % obj)

    def render(self):
        self.parse(self.obj, 0)
        res_file = self.name
        res = ''.join(self.stack)
        with open(res_file, 'w') as f:
            f.write(res)

# if __name__ == "__main__":
#     jf = JsonFormatter(name="1.json")
#     jf.render()

