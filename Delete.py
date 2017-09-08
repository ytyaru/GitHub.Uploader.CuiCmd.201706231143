#!/usr/bin/python3
#!python3
#encoding:utf-8
import sys
import os.path
import subprocess
import configparser
import argparse
import web.service.github.api.v3.AuthenticationsCreator
import web.service.github.api.v3.Client
import database.src.Database
import cui.uploader.Main
import web.log.Log
import database.src.contributions.Main
import setting.Setting

class Main:
    def __init__(self):
        pass

    def Run(self):
        self.__def_args()
        
        self.__setting = setting.Setting.Setting(os.path.abspath(os.path.dirname(__file__)))
        # os.path.basename()で空文字を返されないための対策
        # https://docs.python.jp/3/library/os.path.html#os.path.basename
        if self.__args.path_dir_pj.endswith('/'): self.__args.path_dir_pj = self.__args.path_dir_pj[:-1]
        if None is self.__args.username: self.__args.username = self.__setting.GithubUsername
        
        self.__db = database.src.Database.Database(os.path.abspath(os.path.dirname(__file__)))
        self.__db.Initialize()
        if None is self.__db.Accounts['Accounts'].find_one(Username=self.__args.username):
            web.log.Log.Log().Logger.warning('指定したユーザ {0} はDBに存在しません。UserRegister.pyで登録してください。'.format(self.__args.username))
            return

        self.__account = self.__db.Accounts['Accounts'].find_one(Username=self.__args.username)
        self.__ssh_configures = self.__db.Accounts['SshConfigures'].find_one(AccountId=self.__account['Id'])
        self.__repo_name = os.path.basename(self.__args.path_dir_pj)
        self.__repos = self.__db.Repositories[self.__args.username]['Repositories'].find_one(Name=self.__repo_name)

        if None is self.__repos:
            web.log.Log.Log().Logger.warning('指定したユーザ {0} は {1} リポジトリを持っていません。'.format(self.__args.username, self.__repo_name))
            return

        self.__log()        
        self.__delete()
        
    def __def_args(self):
        parser = argparse.ArgumentParser(
            description='GitHub Repository Deleter.',
        )
        parser.add_argument('path_dir_pj')
        parser.add_argument('-u', '--username')
#        parser.add_argument('-u', '--username', required=True)
        self.__args = parser.parse_args()

    def __log(self):
        web.log.Log.Log().Logger.info('.gitディレクトリ、対象リモートリポジトリ、対象DBレコードを削除します。')
        web.log.Log.Log().Logger.info('リポジトリ名： {0}/{1}'.format(self.__account['Username'], self.__repos['Name']))

    def __delete(self):
        auth_creator = web.service.github.api.v3.AuthenticationsCreator.AuthenticationsCreator(self.__db, self.__args.username)
        authentications = auth_creator.Create()
        client = web.service.github.api.v3.Client.Client(self.__db, authentications, self.__args)
        deleter = cui.uploader.command.repository.Deleter.Deleter(self.__db, client, self.__args)
        deleter.ShowDeleteRecords()
        deleter.Delete()


if __name__ == '__main__':
    main = Main()
    main.Run()
