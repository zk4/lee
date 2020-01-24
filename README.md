Yet Anther LeetCode Cli

# Api is similar to git
- lee show 
- lee pull 
- lee push 
- lee log 

# install
```bash
pip install lee
```




# help
``` bash
usage: main.py [-h] [-p] [-r] [-d] [-j] {ls,pull,push,log} ...

positional arguments:
  {ls,pull,push,log}
    ls                list questions, solution
    pull              pull question related files to local disk by
    push              push file to server
    log               status of server

optional arguments:
  -h, --help          show this help message and exit
  -p, --proxy         auto proxy at 127.0.0.1:18888 for debug, and ignore SSL
                      certificate verification (default: False)
  -r, --refresh       get request will refresh cache (default: False)
  -d, --debug         debug mode. debug logger will output (default: False)
  -j, --json          pure json output (default: False)
``` 

# development
``` bash
# tox for distribute 
 make dev

```
# todo 
- [ ] work with fzf 
- [ ] supoort leetcode.com, and it should be easr
- [ ] automatically  cache your language setting. every time you specify you language with -l, it will change automatically



# thx
leetcode-cli. :)






