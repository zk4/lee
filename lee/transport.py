import requests,pickle
from diskcache import FanoutCache,Cache
import re
import json
import time

import logging
logger = logging.getLogger(__name__)
# proxy_on={"verify":False}
proxy_on={}
class Transport:
    def __init__(self):
        self.cache_session= Cache("~/.config/lee/cache_session")
        self.session = requests.session()

        # with open('session', 'rb') as f:
        self.grabCSRF()
        if self.cache_session.get("session"):
            self.session.cookies.update(self.cache_session["session"])
        else:
            self.loginPrompt()


    
    def grabCSRF(self):
        url = "https://leetcode-cn.com"
        headers = {
            'X-Requested-With': "XMLHttpRequest",
            'host': "leetcode-cn.com",
            'cache-control': "no-cache"
            }
        response = self.session.request("GET", url, headers=headers,**proxy_on)
        html=  response.text
        
        match = re.findall('csrfmiddlewaretoken" value="(.*)"',html)
        if match and len(match[0])>0:
            # self.XCSRFToken=match[0]
            self.session.headers['X-CSRFToken']=match[0]
            return match[0]
        raise Exception("can`t find csrf token")

    def loginPrompt(self):
        email = input("email: ")
        pwd = input("pwd: ")
        return self.login(email,pwd)

    def login(self,email,pwd):
        url = "https://leetcode-cn.com/accounts/login/"

        payload = f"csrfmiddlewaretoken={self.session.headers['X-CSRFToken']}&login={email}&password={pwd}"
        headers = {
            'Origin': "https://leetcode-cn.com",
            'Referer': "https://leetcode-cn.com/accounts/login/",
            'Cookie': "csrftoken=null;",
            'host': "leetcode-cn.com",
            'content-type': "application/x-www-form-urlencoded",
            'content-length': "65",
            'cache-control': "no-cache"
            }

        response = self.session.request("POST", url, data=payload, headers=headers,**proxy_on)
        # with open('session', 'wb') as f:
        #     pickle.dump(self.session.cookies, f)
        self.cache_session.set("session",self.session.cookies,expire=24*7*3600)
        print(response, response.text)
        return response


    def questions(self):
        payload = "{\"operationName\":\"getQuestionTranslation\",\"variables\":{},\"query\":\"query getQuestionTranslation($lang: String) {\\n  translations: allAppliedQuestionTranslations(lang: $lang) {\\n    title\\n    questionId\\n    __typename\\n  }\\n}\\n\"}"        
        response = self._graphql(payload)
        if not response.ok:
            raise Exception(response)
        return response.json()

    def question_detail(self,eng_question_name):
        logger.info("question name: "+eng_question_name)
        payload = "{\"operationName\":\"questionData\",\"variables\":{\"titleSlug\":\""+eng_question_name+"\"},\"query\":\"query questionData($titleSlug: String!) {\\n  question(titleSlug: $titleSlug) {\\n    questionId\\n    questionFrontendId\\n    boundTopicId\\n    title\\n    titleSlug\\n    content\\n    translatedTitle\\n    translatedContent\\n    isPaidOnly\\n    difficulty\\n    likes\\n    dislikes\\n    isLiked\\n    similarQuestions\\n    contributors {\\n      username\\n      profileUrl\\n      avatarUrl\\n      __typename\\n    }\\n    langToValidPlayground\\n    topicTags {\\n      name\\n      slug\\n      translatedName\\n      __typename\\n    }\\n    companyTagStats\\n    codeSnippets {\\n      lang\\n      langSlug\\n      code\\n      __typename\\n    }\\n    stats\\n    hints\\n    solution {\\n      id\\n      canSeeDetail\\n      __typename\\n    }\\n    status\\n    sampleTestCase\\n    metaData\\n    judgerAvailable\\n    judgeType\\n    mysqlSchemas\\n    enableRunCode\\n    envInfo\\n    book {\\n      id\\n      bookName\\n      pressName\\n      description\\n      bookImgUrl\\n      pressImgUrl\\n      productUrl\\n      __typename\\n    }\\n    isSubscribed\\n    __typename\\n  }\\n}\\n\"}" 
        response = self._graphql(payload)
        if not response.ok:
            raise Exception(response)      
        return response.json()

    def _graphql(self,payload):

        url = "https://leetcode-cn.com/graphql" 
        headers = {
            'X-Requested-With': "XMLHttpRequest",
            'Origin': "https://leetcode-cn.com",
            'host': "leetcode-cn.com",
            'accept': "application/json",
            'content-type': "application/json",
            'cache-control': "no-cache"
            }
        response = self.session.request("POST", url, data=payload, headers=headers,**proxy_on)
        if not response.ok:
            logger.error(response)
        return response  
    
    def _basic(self,name):
        url = f"https://leetcode-cn.com/api/problems/{name}/"
        headers = {
            'X-Requested-With': "XMLHttpRequest",
            'host': "leetcode-cn.com",
            'cache-control': "no-cache"
            }
        response = self.session.request("GET", url, headers=headers,**proxy_on)
        return response.json()

    def shell(self):
        return self._basic("shell")
    def all(self):
        return self._basic("all")

    def algorithms(self):
        return self._basic("algorithms")

    def database(self):
        return self._basic("database")
    
    def submit(self,qid,code,language='python',retry=3):
        if retry==0:
            print(f"submit fails after 3 retires, try later")
            return 
        url = "https://leetcode-cn.com/problems/two-sum/submit/"
        payload  ={
        "judge_type": "large",
        "lang": language,
        "question_id": int(qid),
        "test_mode": False,
        "typed_code": code
        }
        payload= json.dumps(payload)
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'Origin': "https://leetcode-cn.com"
            }
        response = self.session.request("POST", url, data=payload, headers=headers,**proxy_on)
        if response.ok:
            submission_id = response.json()["submission_id"]

            ret = self.check(submission_id)
            while "state" in ret and ret["state"]!='SUCCESS':
                time.sleep(1)
                ret = self.check(submission_id)       
            print(ret)
            return  ret
        else:
            try:
                j = response.json()
            except Exception as e:
                pass
            print(response.text)
            print(f"retry...{retry} sleep {(5-retry)**2}")
            time.sleep((5-retry)**2)
            
            return self.submit(qid,code,language,retry-1)
    def check(self,submission_id):
        url = "https://leetcode-cn.com/submissions/detail/"+str(submission_id)+"/check/"
        response = self.session.request("GET", url,  **proxy_on)
        return response.json()

    def test(self,qid,code,sampleTestCase,language):
        url = "https://leetcode-cn.com/problems/two-sum/interpret_solution/"
        payload  ={
        # input 
        # TODO real data_iput 
        # "data_input": "[2,7,11,15]\n9",
        "data_input": sampleTestCase,
        "lang": language,
        "question_id": 1,
        "test_mode": True,
        "typed_code": code
        }
        payload= json.dumps(payload)
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'Origin': "https://leetcode-cn.com"
            }
        response = self.session.request("POST", url, data=payload, headers=headers,**proxy_on)
        interpret_id = response.json()["interpret_id"]

        ret = self.check(interpret_id)
        while "state" in ret and ret["state"]!='SUCCESS':
            time.sleep(1)
            ret = self.check(interpret_id)       
        return ret
    def solution(self,qid,topK,language="python"):
        qid =str(qid)
        topK=str(topK)
#         payload = {
#                 "query": "query questionTopicsList($questionId: String!, $orderBy: TopicSortingOption, $skip: Int, $query: String, $first: Int!, $tags: [String!]) {\n  questionTopicsList(questionId: $questionId, orderBy: $orderBy, skip: $skip, query: $query, first: $first, tags: $tags) {\n    ...TopicsList\n  }\n}\nfragment TopicsList on TopicConnection {\n  totalNum\n  edges {\n    node {\n      id\n      title\n      post {\n        content\n        voteCount\n        author {\n          username\n        }\n      }\n    }\n  }\n}",
#                 "operationName": "questionTopicsList",
#                 "variables": "{\"query\":\"\",\"first\":"+topK+",\"skip\":0,\"orderBy\":\"most_votes\",\"questionId\":\""+qid+"\",\"tags\":[\"python\"]}"
#                 }

        url = "https://leetcode.com/graphql"

        payload = "{\"query\":\"query questionTopicsList($questionId: String!, $orderBy: TopicSortingOption, $skip: Int, $query: String, $first: Int!, $tags: [String!]) {\\n  questionTopicsList(questionId: $questionId, orderBy: $orderBy, skip: $skip, query: $query, first: $first, tags: $tags) {\\n    ...TopicsList\\n  }\\n}\\nfragment TopicsList on TopicConnection {\\n  totalNum\\n  edges {\\n    node {\\n      id\\n      title\\n      post {\\n        content\\n        voteCount\\n        author {\\n          username\\n        }\\n      }\\n    }\\n  }\\n}\",\"operationName\":\"questionTopicsList\",\"variables\":\"{\\\"query\\\":\\\"\\\",\\\"first\\\":"+topK+",\\\"skip\\\":0,\\\"orderBy\\\":\\\"most_votes\\\",\\\"questionId\\\":\\\""+qid+"\\\",\\\"tags\\\":[\\\""+language+"\\\"]}\"}"
        headers = {
            'host': "leetcode.com",
            'accept': "application/json",
            'content-type': "application/json",
            'cache-control': "no-cache"
            }

        response = requests.request("POST", url, data=payload, headers=headers,**proxy_on)

        return response.json()
