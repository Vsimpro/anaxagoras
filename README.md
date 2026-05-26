# anaxagoras

![](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Les_parisiens_pendant_l%27%C3%A9clipse_du_28_Juillet.jpg/330px-Les_parisiens_pendant_l%27%C3%A9clipse_du_28_Juillet.jpg)

- Parisians watching the solar eclipse of July 28, 1851.


NightmareEclipse/Deadeclipse666 has been creating a lot of fuzz with their public disclosures of bugs. Recently, they've made a blog post stating they've moved off to GitLab, and more are coming:

`Mark this date July 14th, I will make sure your bones are shattered that day. Nothing will be released this June (or maybe I will release smtg, depending on circumstances).`

### This repository is a scraper to get alerted immediately if a new repository is posted.

It polls the Atom feed of a GitLab user, looks for new `<entry>` items, stores them into a SQLite database, and will clone the repositories locally for archival in case of takedowns. **With slight modifications, can be used for the moderating of other accounts as well**.


## How to run
Install the dependencies:
```shell
pip install -r requests.txt
```

Insert webhook url as argument and run:
```sh
python3 main.py -w "<DISCORD_WEBHOOK>"
```

Run with cloning/ archival enabled.
```sh
python3 main.py -w "<DISCORD_WEBHOOK>" -c
```

Entries are stored in `database.db`. For the schema, check database/quries.py