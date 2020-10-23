import time
import os,sys
import subprocess as sp
import pickle
from pathlib import Path
import random
from selenium import webdriver

def logg(m):
    with open('log', 'at') as f:
        f.write(str(m)+'\n')

def add_to_translations(w1,w2):
    with open('translations', 'a') as f:
        f.write('{}:{}\n'.format(w1,w2)) 
    logg('{}:{}\n'.format(w1,w2))

def sl(t):
    t = t*1000*0.7
    r = random.randint(int(t), int(t+0.25*t))
    time.sleep(r/1000)

def notify(txt):
    os.system('notify-send {}'.format(txt))

def beep():
    os.system('ffmpeg -loglevel quiet -f lavfi -i "sine=frequency=525:duration=0.55" -f ogg - | mpv -')

def xp(tag,code):
    return driver.find_elements_by_xpath('//{}[@class="{}"]'.format(tag,code))

def fixit():
    beep()
    with open('fixit','w') as f:
        f.write('stopped, delete file to continue')
    notify('and... you have to fix it...')
    while Path('fixit').is_file():
        time.sleep(3)
    return


# headlessness
# fireFoxOptions = webdriver.FirefoxOptions()
# fireFoxOptions.set_headless()
# driver = webdriver.Firefox(firefox_options=fireFoxOptions)
driver = webdriver.Firefox()

url='https://www.duolingo.com/stories'

'''
driver.get(url)
time.sleep(30)
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
driver.close()
sys.exit()
# '''

cookies = pickle.load(open("cookies_julius.pkl", "rb"))
driver.get(url)
for cookie in cookies:
    driver.add_cookie(cookie)

driver.get(url)
time.sleep(8)
logg(driver.page_source)

# choose story
def choose_story(n):
    pics = xp('a','X4jDx')
    while len(pics) == 0:
        sl(3)
        fixit()
        sl(2)
        pics = xp('a','X4jDx')
    [pic for pic in pics if n in pic.get_attribute("outerHTML")][0].click()
    sl(6)

def det_end():
    pics = xp('a','X4jDx')
    if len(pics) > 0:
        return True
    else:
        return False

def det_conti():
    sl(1)
    continue_link = xp('button','Ejd2j _2C9ly _1Ylz- whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j')
    continue_link.extend(xp('button','_3KO6Y nWm9- whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j'))
    continue_link.extend(xp('button','_33XG4 _1vUZG whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j'))
    if len(continue_link) > 0:
        if 'autofocus' in continue_link[-1].get_attribute('outerHTML'):
            return True
        else:
            return False
    else:
        return False

current = 'fr-en-trois-souhaits'
def add_to_instruction(line):
    with open('new-stories/'+current, 'a') as f:
        f.write(str(line)+'\n') 

def modeguesser():
    t1 = time.time()
    for jj in range(8):
        sl(1)
        if det_conti():
            t2 = round(time.time() - t1)
            conti(0.5)
            # add_to_instruction(t2)
            break
        # checkbox and yes/no
        alle = xp('li','_1eDrh _2Qk72')
        alle.extend(xp('li','_1eDrh _1ZeuM')) # with translation
        alle.extend(xp('li','_1eDrh'))
        alle.extend(xp('li','_1eDrh _1ZeuM _2Qk72'))
        if len(alle) == 3:
            det_ch()
            break 
        elif len(alle) == 2:
            det_ch2()
            break 
        # textarea    
        alle = xp('textarea','_2PAEX')
        if len(alle) > 0:
            det_t()
            break 
        # b1, wide phrase button
        alle = xp('button','_1nCoa _27o_2')
        if len(alle) > 0:
            det_b1()
            break 
        # b2, single correct block
        alle = xp('div','_3GBp7 _1t6SZ')
        if len(alle) > 0:
            det_b2()
            break 
        # a, sentence blocks
        alle = xp('span','_37HGt')
        if len(alle) > 0:
            det_a()
            break 
        # p, pairs
        alle = xp('button','_1hk_1 _27o_2')
        alle.extend(xp('button','_1hk_1 _27o_2 _33juy')) # already tried
        if len(alle) > 0:
            # add_to_instruction('p')
            find_pairs()
            break
        if det_end():
            return 1
        if jj == 7:
            logg('oh...')
            contiend(3)


def det_ch():
    lis = xp('li','_1eDrh _2Qk72')
    lis.extend(xp('li','_1eDrh _1ZeuM'))
    lis.extend(xp('li','_1eDrh'))
    lis.extend(xp('li','_1eDrh _1ZeuM _2Qk72'))
    # read each option's text
    texts = [tuple([i.split('</span')[0].split('>')[1] for i in a.get_attribute('outerHTML').split('<span')][1:]) for a in lis]
    allbuttons = xp('button','_21Icd')
    allbuttons[0].click()
    time.sleep(0.7)
    li = xp('li','_1eDrh _2ob7j _2mWtz')
    li.extend(xp('li','_1eDrh _2ob7j _2mWtz _1ZeuM'))
    if len(li) == 1: # first choice was wrong
        allbuttons[1].click()
        time.sleep(0.7)
        li = xp('li','_1eDrh _2ob7j _2mWtz')
        li.extend(xp('li','_1eDrh _2ob7j _2mWtz _1ZeuM'))
        if len(li) == 2: # second choice was wrong
            allbuttons[2].click()
            time.sleep(0.7)
            corr = 2
        else:
            corr = 1
    else: # first choice was correct
        corr = 0
    add_to_instruction('c[{}'.format('['.join(texts[corr])))

def det_ch2():
    lis = xp('li','_1eDrh _2Qk72')
    lis.extend(xp('li','_1eDrh _1ZeuM'))
    lis.extend(xp('li','_1eDrh'))
    lis.extend(xp('li','_1eDrh _1ZeuM _2Qk72'))
    # read each option's text
    texts = [tuple([i.split('</span')[0].split('>')[1] for i in a.get_attribute('outerHTML').split('<span')][1:]) for a in lis]
    allbuttons = xp('button','_21Icd')
    allbuttons[0].click()
    time.sleep(0.7)
    li = xp('li','_1eDrh _2ob7j _2mWtz')
    li.extend(xp('li','_1eDrh _2ob7j _2mWtz _1ZeuM'))
    if len(li) == 1: # first choice was wrong
        allbuttons[1].click()
        time.sleep(0.7)
        corr = 1
    else: # first choice was correct
        corr = 0
    add_to_instruction('c[{}'.format('['.join(texts[corr])))

def det_yn():
    lis = xp('li','_1eDrh _2Qk72')
    allbuttons = xp('button','_21Icd')
    allbuttons[0].click()
    li = xp('li','_1eDrh _2ob7j _2mWtz')
    if len(li) == 1: # first choice was wrong
        corr = 1 # choice 2 is correct
    else: # first choice was correct
        corr = 0
    if 'Yes' == lis[corr].get_attribute('outerHTML').split('<span')[1].split('</span')[0].split('>')[1]:
        add_to_instruction('y')
    else:
        add_to_instruction('n')
    if corr: # click remaining
        allbuttons[1].click()

def det_a():
    lis = xp('span','_37HGt')
    lis.extend(xp('span','_37HGt Pjf_O'))
    numberof = len(lis)
    sentence = []
    solved = 0
    while solved < numberof:
        for b in lis:
            b.click()
            sl(0.7)
            if solved < len(xp('span','_37HGt G1JDk')):
                sentence.append(b.get_attribute('outerHTML').split('</span')[0].split('>')[1])
                break
        lis = xp('span','_37HGt')
        lis.extend(xp('span','_37HGt Pjf_O'))
        solved = len(xp('span','_37HGt G1JDk'))
    add_to_instruction('a,'+','.join(sentence))


def det_b2():
    lis = xp('div','_3GBp7 _1t6SZ')
    for i,b in enumerate(lis):
        b.click()
        time.sleep(0.9)
        if len(xp('div','_3GBp7 _2GUPW _1t6SZ')) > 0:
            add_to_instruction('b2,{}'.format(str(i)))
            break

def det_b1():
    lis = xp('button','_1nCoa _27o_2')
    numberof = len(lis)
    # read each option's text
    texts = [a.get_attribute('outerHTML').split('</button')[0].split('>')[1] for a in lis]
    lis[0].click()
    time.sleep(0.9)
    li = xp('button','_1nCoa _27o_2 _16lcC kAVeU')
    if len(li) == 1: # first choice was wrong
        lis[1].click()
        time.sleep(0.9)
        li = xp('button','_1nCoa _27o_2 _16lcC kAVeU')
        if (len(li) == 2 and numberof > 2): # second choice was wrong
            lis[2].click()
            time.sleep(0.9)
            corr = 2
        else:
            corr = 1
    else: # first choice was correct
        corr = 0
    add_to_instruction('b1,{}'.format(texts[corr]))

def det_t():
    textarea('je ne sais pas')
    conti(1)
    solution = xp('div','_1fyi8')[0].get_attribute('outerHTML').split('</span')[0].split('>')[-1]
    add_to_instruction('t,'+solution)


def contiend(tts):#                                                    Ejd2j _2C9ly _1Ylz- whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j
    sl(tts)
    continue_link = xp('button','Ejd2j _2C9ly _1Ylz- whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j')
    continue_link.extend(xp('button','_33XG4 _1vUZG whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j'))
    continue_link.extend(xp('button','_3KO6Y nWm9- whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j'))
    continue_link.extend(xp('button','_33XG4 _1vUZG whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j'))
    if len(continue_link) == 0:
        return
    else:
        continue_link[-1].click()

def conti(tts):#                                                    Ejd2j _2C9ly _1Ylz- whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j
    sl(tts)
    continue_link = xp('button','Ejd2j _2C9ly _1Ylz- whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j')
    continue_link.extend(xp('button','_33XG4 _1vUZG whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j'))
    continue_link.extend(xp('button','_3KO6Y nWm9- whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j'))
    continue_link.extend(xp('button','_33XG4 _1vUZG whuSQ _2gwtT _1nlVc _2fOC9 t5wFJ _3dtSu _25Cnc _3yAjN UCrz7 yTpGk _1KV6j'))
    if len(continue_link) == 0:
        fixit()
        return
    else:
        continue_link[-1].click()

def checker(txttuple):
    sl(1)
    lis = xp('li','_1eDrh _2Qk72')
    lis.extend(xp('li','_1eDrh _1ZeuM'))
    lis.extend(xp('li','_1eDrh'))
    # read each option's text
    texts = [tuple([i.split('</span')[0].split('>')[1] for i in a.get_attribute('outerHTML').split('<span')][1:]) for a in lis]
    correct_choice = [i for i,t in enumerate(texts) if t == txttuple]
    allbuttons = xp('button','_21Icd')
    numberof = len(lis)
    print('checkbox', numberof)
    if len(correct_choice) == 0:
        allbuttons[0].click(); sl(0.9)
        li = xp('li','_1eDrh _2ob7j _2mWtz')
        li.extend(xp('li','_1eDrh _2ob7j _2mWtz _1ZeuM'))
        if len(li) == 1:
            allbuttons[1].click(); sl(0.9)
            li = xp('li','_1eDrh _2ob7j _2mWtz')
            li.extend(xp('li','_1eDrh _2ob7j _2mWtz _1ZeuM'))
            if (len(li) == 2 and numberof > 2):
                allbuttons[2].click(); sl(0.9)
    else:
        allbuttons[correct_choice[0]].click(); sl(0.9)
        li = xp('li','_1eDrh _2ob7j _2mWtz')
        li.extend(xp('li','_1eDrh _2ob7j _2mWtz _1ZeuM'))
        if len(li) == 1:
            allbuttons[(correct_choice[0]+1)%numberof].click(); sl(0.9)
            li = xp('li','_1eDrh _2ob7j _2mWtz')
            li.extend(xp('li','_1eDrh _2ob7j _2mWtz _1ZeuM'))
            if (len(li) == 2 and numberof > 2):
                allbuttons[(correct_choice[0]+2)%numberof].click(); sl(0.9)


def buttontxt(txt):
    sl(1)
    alle = xp('button','_1nCoa _27o_2')
    words = [a.get_attribute("outerHTML") for a in alle]
    if len(words)<1:
        fixit()
        return
    if type(txt) != str:
        det_b1()
    else:
        right = [i for i,line in enumerate(words) if txt in line]
        if len(right) < 1:
            det_b1()
        else:
            alle[right[0]].click()
            sl(2)

def buttontxt2(nr):
    sl(1)
    if type(nr) != int:
        lis = xp('div','_3GBp7 _1t6SZ')
        for i,b in enumerate(lis):
            b.click()
            time.sleep(0.9)
            if len(xp('div','_3GBp7 _2GUPW _1t6SZ')) > 0:
                break
    else:
        alle = xp('div','_3GBp7 _1t6SZ')
        if len(alle) == 0:
            det_b2()
        elif len(alle) < nr+1:
            det_b2()
        else:
            alle[int(nr)].click()
    sl(2)

def buttontxt3(tx):
    sl(1)
    alle = xp('span','_37HGt')
    words = [a.get_attribute("outerHTML") for a in alle]
    for txt in tx:
        if len(words)<1:
            fixit()
            return
        right = [i for i,line in enumerate(words) if '>{}</'.format(txt) in line]
        if len(right) == 0:
            lis = xp('span','_37HGt')
            lis.extend(xp('span','_37HGt Pjf_O'))
            numberof = len(lis)
            sentence = []
            solved = 0
            while solved < numberof:
                for b in lis:
                    b.click()
                    sl(0.7)
                    if solved < len(xp('span','_37HGt G1JDk')):
                        sentence.append(b.get_attribute('outerHTML').split('</span')[0].split('>')[1])
                        break
                lis = xp('span','_37HGt')
                lis.extend(xp('span','_37HGt Pjf_O'))
                solved = len(xp('span','_37HGt G1JDk'))
            break
        else:
            alle[right[0]].click()
    sl(1)

def textarea(txt):
    driver.find_element_by_xpath('//textarea[@class="_2PAEX"]').send_keys(txt)
    sl(2)


# initialise pairs
def ini_pairs():
    pairs = []
    for line in open('translations', 'r'):
        if not line.startswith('\n'):
            line = line.rstrip().split(':')
            line = tuple(l.lower() for l in line)
            pairs.append(line)
    return pairs

def find_pairs():
    # dealing with duplicates
    alle = xp('button','_1hk_1 _27o_2')
    alle.extend(xp('button','_1hk_1 _27o_2 _33juy'))
    different = dict()
    for a in alle:
        w = a.get_attribute("outerHTML").split('</')[0].split('>')[-1].lower()
        if w in different:
            a.click(); sl(0.5)
            different[w].click(); sl(0.5)
        different[w] = a
    searching = 1
    while searching:
        go = set()
        unknown = set()
        known = set()
        alle = xp('button','_1hk_1 _27o_2')
        alle.extend(xp('button','_1hk_1 _27o_2 _33juy'))
        words = {a.get_attribute("outerHTML").split('</')[0].split('>')[-1].lower():a for a in alle}
        for p in ini_pairs():
            if (p[0] in words and p[1] in words):
                go.add(p)
                known = known | {p[0], p[1]}
        unknown = (words.keys() | set()) ^ known
        if len(unknown) == 2:
            go.add(tuple(unknown))
            new_confirmed = tuple(unknown)
            add_to_translations(*new_confirmed)
            continue
        elif len(unknown) > 2:
            justtry(unknown)
            continue
        elif len(words) <= 2*len(go):
            for p in go:
                if p[0] != p[1]:
                    words[p[0]].click()
                    sl(0.5)
                    words[p[1]].click()
                    sl(1)
                else:
                    remaining = xp('button','_1hk_1 _27o_2')
                    doubles = [a for a in remaining if p[0] == a.get_attribute("outerHTML").split('</')[0].split('>')[-1].lower()]
                    for but in doubles:
                        but.click()
                        sl(0.5)
        elif not len(alle)%2:
#_1hk_1 _27o_2 _3rU1U clicked
            alle[0].click()
        else:
            beep()
            with open('unknowns', 'w') as f:
                [f.write('\n{}'.format(p)) for p in list(unknown)]
            cached_stamp = os.stat('translations').st_mtime
            stamp = os.stat('translations').st_mtime
            while stamp == cached_stamp:
                stamp = os.stat('translations').st_mtime
                time.sleep(3)

        for_counting = xp('button','_1hk_1 _27o_2 _3alTu')
        if len(for_counting) == 10:
            searching = 0
        sl(1)


def justtry(unkn):
    alle = xp('button','_1hk_1 _27o_2')
    alle.extend(xp('button','_1hk_1 _27o_2 _33juy'))
    correct_status = len(xp('button','_1hk_1 _27o_2 _3alTu'))
    wor = {a.get_attribute("outerHTML").split('</')[0].split('>')[-1].lower():a for a in alle}
    u = list(unkn)
    for i in range(1,len(u)):
        wor[u[0]].click(); sl(0.5)
        wor[u[i]].click(); sl(0.5)
        sl(1)
        counting = len(xp('button','_1hk_1 _27o_2 _3alTu')) - correct_status
        if counting == 2:
            add_to_translations(u[0],u[i]) 
            break

def oneup(n):
    scores = dict()
    for line in open('count', 'r'):
        line = line.split(':')
        scores[line[0]] = int(line[1])
    scores[n] = scores.get(n, 0) + 1
    with open('count', 'w') as f:
        for k,i in scores.items():
            f.write('{}:{}\n'.format(k,i))
    for s,i in scores.items():
        if i > 8:
            if Path('new-stories/'+s).is_file():
                os.rename('new-stories/'+s, 'retired-stories/'+s)
                logg(s+' retired.')


def exe(inst):
    t1 = time.time()
    for jj in range(8):
        sl(0.5)
        if det_conti():
            conti(0.5)
            break
        # checkbox and yes/no
        alle = xp('li','_1eDrh _2Qk72')
        alle.extend(xp('li','_1eDrh _1ZeuM')) # with translation
        alle.extend(xp('li','_1eDrh'))
        alle.extend(xp('li','_1eDrh _1ZeuM _2Qk72'))
        if len(alle) == 3:
            checker(inst[0])
            return 2
            break 
        elif len(alle) == 2:
            checker(inst[0])
            return 2
            break 
        # textarea    
        alle = xp('textarea','_2PAEX')
        if len(alle) > 0:
            textarea(inst[0])
            return 2
            break 
        # b1, wide phrase button
        alle = xp('button','_1nCoa _27o_2')
        if len(alle) > 0:
            buttontxt(inst[0])
            return 2
            break 
        # b2, single correct block
        alle = xp('div','_3GBp7 _1t6SZ')
        if len(alle) > 0:
            buttontxt2(inst[0])
            return 2
            break 
        # a, sentence blocks
        alle = xp('span','_37HGt')
        if len(alle) > 0:
            if type(inst[0]) == int:
                det_a()
            else:
                buttontxt3(inst[0])
            return 2
            break 
        # p, pairs
        alle = xp('button','_1hk_1 _27o_2')
        alle.extend(xp('button','_1hk_1 _27o_2 _33juy')) # already tried
        if len(alle) > 0:
            find_pairs()
            break
        if det_end():
            return 1
        if jj == 7:
            contiend(0.5)

def read_instructions(file):
    choose_story(os.path.basename(file))
    current = os.path.basename(file)
    inst = []
    for line in open(file, 'r'):
        line = line.rstrip()
        if line.startswith('c'):
            inst.append(tuple(line.split('[')[1:]))
        elif line.startswith('b1'):
            inst.append(line.split(',')[1])
        elif line.startswith('b2'):
            inst.append(int(line.split(',')[1]))
        elif line.startswith('t'):
            inst.append(line.split(',')[1])
        elif line.startswith('a'):
            inst.append(line.split(',')[1:])
    return inst,current

# for line in open('todo-stories', 'r'):
#     current = line.rstrip()
#     choose_story(current)
#     while modeguesser() != 1:
#         pass
#     notify(current+' finished.')
#     logg(current+', finished')
#     contiend(1)
#     contiend(5)
#     contiend(5)
#     sl(10)

for _ in range(200):
    inst,current = read_instructions('new-stories/'+random.choice(os.listdir('new-stories/')))
    ongoing = 1 
    while ongoing == 1:
        if len(inst) == 0:
            inst = [tuple(['dhfalkdj','damn'])]
        res = exe(inst)
        if res == 2:
            print(inst.pop(0))
            continue
        elif res == 1:
            ongoing = 0
        else:
            continue
    notify(current+' finished.')
    logg(current+', finished')
    oneup(current)
    contiend(1)
    contiend(5)
    contiend(5)
    sl(10)
    with open('todo-stories', 'r') as f:
        todos = f.readlines()
    for line in todos:
        current = line.rstrip()
        choose_story(current)
        while modeguesser() != 1:
            pass
        notify(current+' finished.')
        logg(current+', finished')
        with open('todo-stories', 'w') as f:
            [f.write(lin) for lin in todos if not current in lin]
        contiend(1)
        contiend(5)
        contiend(5)
        sl(10)
