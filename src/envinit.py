#!/usr/bin/env python
#coding:utf-8
import json
import copy
import os
import fire
import sys
from helpers import *

message = {
    "en" : {
        "configFileNotExist" : "配置文件%s不存在，请查证后输入",
        "envNameQuestion": "please input the environment you want to init:",
        "fileNotChange": "[ ]%s notchanged",
        "fileGenerate": "[+]%s generated",
        "fileSkiped": "[ ]%s ...skiped",
        "fileOverwrite": "[!]%s overwrite",
        "fileOverwriteQuestion": "the file %s is already exist, do you want to overwrite？（Yes|No|Quit|All）",
        "fileERR" : "文件%s打不开或没有读权限",
    },
    "zh-cn" : {
        "configFileNotExist" : "配置文件%s不存在，请查证后输入",
        "envNameQuestion": "请选择你想要选择的环境名:",
        "fileNotChange": "[ ]%s 未改变",
        "fileGenerate": "[+]%s 已新建",
        "fileSkiped": "[ ]%s ...已忽略",
        "fileOverwrite": "[!]%s 已覆盖",
        "fileOverwriteQuestion": "文件%s已经存在，是否要覆盖？（Yes|No|Quit|All）",
        "fileERR" : "文件%s打不开或没有读权限",
    }
}

class CodeInit(object):
    def __init__(self, envName="dev", envPath="environments", language="zh-cn", projectRoot=".", overwrite=False):
        '''
        :param envName:str  the environment name. it may be "dev", "prod" etc.
        :param envPath:str  the environment path, default to "./environments".
        :param language:str  the language, can be "en" or "zh-cn". default to "zh-cn".
        :param projectRoot:str  the root of project. default to "./".
        :param overwrite:Boolean if file exist, should the script overwrite the exist file.default to False.
        '''
        self.__setLanguage(language)
        self.projectRoot = projectRoot
        self.envName = envName
        self.envPath = envPath
        self.overwrite = overwrite

        self.__console = Console.Console()
        self.__message = message
        self.__all = False
    def run(self):
        '''initial the environments'''
        configFile = os.path.join(self.envPath, "config.json")
        if not os.path.exists(configFile):
            self.__printDanger("configFileNotExist", configFile)
            return
        data = json.loads(FileHelper.file_get_content(configFile))
        # find the select environment
        if not self.envName:
            self.__printNormal("envNameQuestion")
            print("===========================================")
            for key in data.keys():
                name = data[key]["name"] if data[key].__contains__("name") else key
                print("[ %s ]: %s" %(key, name))
            string = input("===========================================\n")
            try:
                index = int(string)
                print(data.keys())
                if data.keys()[index]:
                    self.envName = data.keys()[index]
                else:
                    self.__printDanger("envNameNotExist", self.envName)
                    return
            except:
                self.__printDanger("envNameNotExist", str)
                return
        dataPath = os.path.join(self.envPath, self.envName)
        envData = data[self.envName]

        # get all files
        files = self.__getFileList(dataPath)
        # copy all files to the dest
        for fileName in files:
            if not self.__copyFile(self.projectRoot, os.path.join(dataPath, fileName), fileName):
                break

    def init(self):
        '''initial the config of environments'''
        obj = copy.copy(self)
        filePath = __file__
        if os.path.islink(filePath):
            filePath = os.readlink(filePath)
        curDir = os.path.dirname(filePath)
        obj.envPath = os.path.join(curDir, "environments")
        obj.projectRoot = os.path.join(".", "environments")
        if not os.path.isdir(obj.projectRoot):
            os.makedirs(obj.projectRoot)
            os.makedirs(os.path.join(obj.projectRoot, "dev"))
            os.makedirs(os.path.join(obj.projectRoot, "prod"))
        obj.envName = "dev"
        obj.run()

    def __setLanguage(self, lang):
        self.language = lang
        return self.language

    def __printDanger(self, key, *args):
        self.__print(key, "danger", *args)
    def __printNormal(self, key, *args):
        self.__print(key, "primary", *args)
    def __printSuccess(self, key, *args):
        self.__print(key, "success", *args)
    def __print(self, key, *args):
        self.__print(key, "primary", *args)
    def __print(self, key, msgtype, *args):
        msg = self.__getMessage(key, *args)
        self.__console.print(msg, msgtype)
    def __getMessage(self, key, *args):
        if self.__message[self.language].__contains__(key):
            str = self.__message[self.language][key] %args
        else:
            str = "未知错误:"+key
        return str


    def __getFileList(self, root, base=""):
        files = []
        pathDir = os.listdir(root)
        for item in pathDir:
            if item == "." or item == ".." or item == ".git" or item == ".svn":
                continue
            itemPath = os.path.join(root, item)
            relativePath = os.path.join(base, item)
            print(itemPath, relativePath)
            print(os.path.isdir(itemPath))
            if os.path.isdir(itemPath):
                files += self.__getFileList(itemPath, relativePath)
            else:
                files.append(relativePath)
            print(files)
        return files

    def __copyFile(self, root, source, dest):
        print("copy", source, dest)
        if not os.path.isfile(source):
            self.__printDanger("fileERR", source)
            return False
        destfile = os.path.join(root, dest)
        str1 = FileHelper.file_get_content(source)
        if os.path.isfile(destfile):
            # check if need overwrite
            str2 = FileHelper.file_get_content(destfile)
            print(str1)
            print(str2)
            if str1 == str2:
                self.__printSuccess("fileNotChange", destfile)
                return True
            if self.__all or self.overwrite:
                self.__printDanger("fileOverwrite", destfile)
                return True
            self.__printNormal("fileOverwriteQuestion", destfile)
            ret = input()
            if ret[0] == 'y' or ret[0] == 'Y':
                FileHelper.file_put_content(destfile, str1)
                self.__printDanger("fileOverwrite", destfile)
                return True
            if ret[0] == 'q' or ret[0] == 'Q':
                return False
            if ret[0] == 'a' or ret[0] == 'A':
                FileHelper.file_put_content(destfile, str1)
                self.__printDanger("fileOverwrite", destfile)
                self.__all = True
                return True
            self.__printNormal("fileSkiped", destfile)
            return True
        FileHelper.file_put_content(destfile, str1)
        self.__printSuccess("fileGenerate", destfile)
        return True

if __name__ == '__main__':
    fire.Fire(CodeInit);

