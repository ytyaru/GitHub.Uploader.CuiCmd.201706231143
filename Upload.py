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
        self.__commit()
        
    def __def_args(self):
        parser = argparse.ArgumentParser(
            description='GitHub Repository Uploader.',
        )
        parser.add_argument('path_dir_pj')
        parser.add_argument('-u', '--username')
#        parser.add_argument('-u', '--username', required=True)
        parser.add_argument('-m', '--messages', required=True, action='append')
        parser.add_argument('-i', '--issues', action='append')
        parser.add_argument('-l', '--labels', action='append')
        parser.add_argument('-c', '--is-close', action='store_false') # is_close
        self.__args = parser.parse_args()

    def __log(self):
        web.log.Log.Log().Logger.info('リポジトリ名： {0}/{1}'.format(self.__account['Username'], self.__repos['Name']))
        web.log.Log.Log().Logger.info('説明: {0}'.format(self.__repos['Description']))
        web.log.Log.Log().Logger.info('URL: {0}'.format(self.__repos['Homepage']))
        web.log.Log.Log().Logger.info('----------------------------------------')

    def __commit(self):
        auth_creator = web.service.github.api.v3.AuthenticationsCreator.AuthenticationsCreator(self.__db, self.__args.username)
        authentications = auth_creator.Create()
        client = web.service.github.api.v3.Client.Client(self.__db, authentications, self.__args)
#        main = cui.uploader.Main.Main(self.__db, client, self.__args)
#        main.Run()
        if None is not self.__args.issues:
            issue = self.__create_issue()
            self.__args.messages[0] = "fix #{0} ".format(issue['number']) + self.__args.messages[0]
        commiter = cui.uploader.command.repository.Commiter.Commiter(self.__db, client, self.__args)
        self.__create_message_command()
        commiter.ShowCommitFiles()
        commiter.AddCommitPush(self.__args.messages)
        
    def __create_message_command(self):
        # 2行目に空データを入れる（1行目タイトル, 2行目空行, 3行目以降本文, の書式にする）
        if 2 <= len(self.__args.messages) and '' != self.__args.messages[1]: self.__args.messages.insert(1, '')
    
    def __create_issue(self):
        if None is self.__args.issues: return None
        title = self.__args.issues[0]
        body = None
        # 1行目タイトル, 2行目空行, 3行目以降本文。
        if 1 < len(self.__args.issues): body = '\n'.join(self.__args.issues[1:])
        return self.__client.Issues.create(title, body=body)


if __name__ == '__main__':
    main = Main()
    main.Run()
