# CodeTool


## envinit

envinit is a tool for  manage the environments of project. usually, the dev enviroment is not equal to the prod environment, so we can use this tool to manage the environment.

**step1:**

git glone and install the tool

```bash 
git clone git@github.com:buptlsp/codetool.git
cd codetool
./install
```

**step2:**

initial the environment. if you have already initial the environment, you can skip this step.

```bash
cd your_project
envinit init
# you can edit ./environments/config.json to edit your environments
````

**step3:**

sync the environment

```bash
cd your_project
envinit run 
# you can just run envinit to see the params
envinit
envinit --help
```
the script will copy `./environment/prod/a/b/config.xx` to `./a/b/config.txt`，thus, we can save our environments in `./environments`.

**Tips:** the `./environments` should add to git, and the destfile should add to gitignore.



