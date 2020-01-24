#coding: utf-8
import json
import logging
logger = logging.getLogger(__name__)


class Question:
    def __init__(self):
        self._raw_question=None
        self._raw_detail=None


        self._eng_name = None 
#         self._eng_slug_name = None
        self._chs_name = None 
        self._qid      = None
        self._content  = None
        self._stats    = None
        self._codeDefinition= {}
        self._sampleTestCase= None
        self._enableRunCode = None
        self._metaData = None
        self._translatedContent = None
        self._paid_only = None
        self._difficilty_level = None
        self._status = None
        

    def load_from_raw_question(self,raw_question):
        self._raw_question=raw_question
        self._qid = str(raw_question["stat"]["question_id"])
        self._eng_name=raw_question["stat"]["question__title_slug"]
        self._paid_only=raw_question["paid_only"]
        self._difficilty_level = raw_question["difficulty"]["level"]
        self._status = raw_question["status"]
        # print("raw_question",raw_question)

    def load_from_raw_detail(self,raw_detail):
        self._raw_detail=raw_detail
        question = raw_detail["data"]["question"]
#         self._eng_name = raw_detail["eng_name"]
        self._content =question["content"]
        self._stats = question["stats"]
        self._sampleTestCase= question["sampleTestCase"]
        self._enableRunCode = question["enableRunCode"]
        self._metaData =question["metaData"]
        self._translatedContent = question["translatedContent"]
        code_definations= question["codeSnippets"]
        for  code in code_definations:
                self._codeDefinition[code["langSlug"].lower()]=code["code"]
        print("_sampleTestCase",self._sampleTestCase)
        
    
    def get_code_defination(self,lang):
        assert lang
        return self._codeDefinition.get(lang.lower())

    
    def load_from_translation(self,translation):
        self._chs_name=translation["title"]

    def get_template(self,lang):
        return self._codeDefinition.get(lang)

    @property
    def difficulty_level(self):
        return self._difficilty_level

    @property
    def status(self):
        return self._status
    @property
    def sampleTestCase(self):
        return self._sampleTestCase

    @property
    def translatedContent(self):
        return self._translatedContent

    @property
    def enableRunCode(self):
        return self._enableRunCode

    @property
    def metaData(self):
        return self._metaData
    @property
    def qid(self):
        return self._qid

    @property
    def content(self):
        return self._content

    @property
    def paid_only(self):
        return self._paid_only
    @property
    def eng_name(self):
        return self._eng_name

    @property
    def chs_name(self):
        return self._chs_name

    @property
    def raw_detail(self):
        return self._raw_detail
  
if __name__ == "__main__":
    q = Question()
    print(q.eng_name)
