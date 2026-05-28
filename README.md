# anaxagoras

![](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Les_parisiens_pendant_l%27%C3%A9clipse_du_28_Juillet.jpg/330px-Les_parisiens_pendant_l%27%C3%A9clipse_du_28_Juillet.jpg)

- Parisians watching the solar eclipse of July 28, 1851.


NightmareEclipse/Deadeclipse666 has been creating a lot of fuzz with their public disclosures of bugs. Recently, they've made a blog post stating they've moved off to GitLab, and more are coming:

`Mark this date July 14th, I will make sure your bones are shattered that day. Nothing will be released this June (or maybe I will release smtg, depending on circumstances).`

This repository is a scraper to try and monitor the situation.

At this moment, it is tracking deadeclipse666 blogspot account, and trying to find any of the known alias' and their variants from git instances. Once an account is activated on a git instance, it will conveyor-belt straight into following its activity, as the repo used to do with gitlab. 

For the old, tracker, check legacy/git_actions_legacy.py


## Currently bit in progress again!

Running:
```sh
pip install -r requirements.txt
```

add "DISCORD" variable into .env, as follows:
```sh
DISCORD = "https://discord.com/api/...
```


This will run all the scrapers.
```sh
python3 main.py
```


