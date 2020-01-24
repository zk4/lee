#coding: utf-8
from .transport import Transport
from .question import Question
from .solution import Solution
from  diskcache import Cache
import logging
logger = logging.getLogger(__name__)
class Cli:
    def __init__(self):
        self.transport =Transport()
        self.cache_questions = {}

    def login(self,email,pwd):
        return self.transport.login(email,pwd)

    def loginPrompt(self):
        email = input("email: ")
        pwd = input("pwd: ")
        return self.transport.login(email,pwd)


    def submit(self,qid ,content,language):
        ret=  self.transport.submit(qid,content,language)
        self.cache_questions.pop( str(qid) )
        return ret


    def test(self,qid,content,language):
        q = self.question_detail (qid)
#         print("q-------------",q.sampleTestCase)
        ret= self.transport.test(qid,content,q.sampleTestCase,language)
        return ret

    def findAll(self,reverse=True):
        self.find(1)
        ints = [int(x) for x in self.cache_questions.keys()]
        for qid in sorted(ints,reverse=reverse):
            yield self.find(qid)

    def find(self,qid):
        qid = str(qid)
        ret = self.cache_questions.get(qid)

        if not ret:
            raw =self.transport.all()["stat_status_pairs"]
            chinese = self.transport.questions()['data']['translations']
            for r in raw:
                q = Question()
                q.load_from_raw_question(r)
                for c in chinese:
                    # logger.info(c)
                    if q.qid == str(c["questionId"]): 
                        q.load_from_translation(c)
                        self.cache_questions[q.qid]=q
                        break 

        return self.cache_questions.get(qid)
        

    def question_detail(self,qid):
        qid = str(qid)
        question = self.find(qid)
        if not question.raw_detail:
            raw_detail = self.transport.question_detail(question.eng_name)
            question.load_from_raw_detail(raw_detail)
            self.cache_questions[question.qid]=question
        return question

    def solution(self,qid,topK,language):
        ret =  self.transport.solution(qid,topK,language)
        q   =  self.find(qid)
        for edge in ret["data"]["questionTopicsList"]["edges"]:
            s = Solution()
            s.load_from_edge(qid,q.eng_name,edge)
            yield s

