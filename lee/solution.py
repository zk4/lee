class Solution:
    def __init__(self):
        self._raw_edge =None
        self._language = None
        self._votes =None
        self._author_name=None
        self._qid = None
        self._sid = None
        self._content=None
        self._discuss_url=None
        self._eng_name=None
        self._title =None
        

    def load_from_edge(self,qid,eng_name,raw_edge):
        self._raw_edge = raw_edge
        self._qid = qid
        self._eng_name = eng_name

        solution = raw_edge["node"]
        self._sid = solution["id"]
        self._title = solution["title"]
        self._votes = solution["post"]["voteCount"]
        self._discuss_url=f"discuss: https://leetcode.com/problems/{self._eng_name}/discuss/{ self._qid }"
        self._author_name=solution["post"]["author"]["username"]
        self._content =(solution["post"]["content"]) \
        .replace("\\n"," \n") \
        .replace("\\t"," \t") \
        .replace("```","``` ")


    @property
    def content(self):
        return self._content

    @property
    def title(self):
        return self._title

    @property
    def language(self):
        return self._language

    @property
    def votes(self):
        return self._votes

    @property
    def author_name(self):
        return self._author_name

    @property
    def qid(self):
        return self._qid

    @property
    def discuss_url(self):
        return self._discuss_url

