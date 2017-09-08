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
        
        self.__log()
        self.__create()

    def __def_args(self):
        parser = argparse.ArgumentParser(
            description='GitHub Repository Creator.',
        )
        parser.add_argument('path_dir_pj')
#        parser.add_argument('-u', '--username', required=True)
        parser.add_argument('-u', '--username')
        parser.add_argument('-d', '--description')
        parser.add_argument('-l', '--homepage') # -hはヘルプと被る -lはlicenseと被る
#        parser.add_argument('-t', '--topics', action='append') # 将来に備えて予約
#        parser.add_argument('-L', '--license') # 将来に備えて予約
        self.__args = parser.parse_args()

    def __log(self):
        web.log.Log.Log().Logger.info('ユーザ名: {0}'.format(self.__account['Username']))
        web.log.Log.Log().Logger.info('メアド: {0}'.format(self.__account['MailAddress']))
        web.log.Log.Log().Logger.info('SSH HOST: {0}'.format(self.__ssh_configures['HostName']))
#        web.log.Log.Log().Logger.info('リポジトリ名: {0}'.format(self.__repos['Name']))
#        web.log.Log.Log().Logger.info('説明: {0}'.format(self.__repos['Description']))
#        web.log.Log.Log().Logger.info('URL: {0}'.format(self.__repos['Homepage']))
        web.log.Log.Log().Logger.info('リポジトリ名: {0}'.format(self.__repo_name))
        web.log.Log.Log().Logger.info('説明: {0}'.format(self.__args.description))
        web.log.Log.Log().Logger.info('URL: {0}'.format(self.__args.homepage))

    def __create(self):
        auth_creator = web.service.github.api.v3.AuthenticationsCreator.AuthenticationsCreator(self.__db, self.__args.username)
        authentications = auth_creator.Create()
        client = web.service.github.api.v3.Client.Client(self.__db, authentications, self.__args)
#        main = cui.uploader.Main.Main(self.__db, client, args)
#        main.Run()
        creator = cui.uploader.command.repository.Creator.Creator(self.__db, client, self.__args)
        creator.Create()


if __name__ == '__main__':
    main = Main()
    main.Run()
