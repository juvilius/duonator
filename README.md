# duonator - duolingo story bot

This little script was written out of spite.
Arriving at the Diamond League I realised in the matter of a day that the person at the top must be using some sort of automation to chow through around a 100 stories for 28XP each. First hint: their score was divisible by 28. Well, maybe they use multiple devices and people to get there... but I doubt it.

So I started writing a script the next day to increase my chances (being already 4000XP behind).
A plethora of little hurdles had to be overcome, but in a matter of a week I arrived at almost complete automation.
I came in only second the first week, but dominated in the following week.  
**Legendary**

## Disclaimer
Use it once to get the trophy and never again. There is absolutely no gain in solving all these stories automatically aside from annoying another bot.
If you further use it, it will only destroy all hopes for anyone that's playing duolingo for it's original purpose.
It might also go against duo's terms and conditions, i haven't made the effort to check (since they clearly don't ban anyone else that is using a bot...).

## Target group
Tinkerers that really want the trophy but are obstructed by stupid bots.  
This is by no means a finished product or even just an elegant script. It's very ugly in fact because I was in the end just reacting to bugs and explicitly ruling them out, which in most cases let's it guess the right solution.

## Instructions
mkdir new-stories retired-stories  
create a translations file for your language called 'translations'  
create cookies by logging in.  
paste the base of the story url in a 'todo-stories' file.  
figure out the script and change it to your needs.

## Requirements
Python
selenium + webdriver
