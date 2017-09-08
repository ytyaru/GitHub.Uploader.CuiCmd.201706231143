# このソフトウェアについて

GitHubアップローダからCUIコマンドを書いてみた。

とりあえず版。CUIによる表示確認や入力を取り去った。コマンドで叩けるようにした。

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [Python 3.4.3](https://www.python.org/downloads/release/python-343/)
* [SQLite](https://www.sqlite.org/) 3.8.2

## WebService

* [GitHub](https://github.com/)
    * [アカウント](https://github.com/join?source=header-home)
    * [AccessToken](https://github.com/settings/tokens)
    * [Two-Factor認証](https://github.com/settings/two_factor_authentication/intro)
    * [API v3](https://developer.github.com/v3/)

# 以前のコマンド

コマンド|説明
--------|----
GitHubUserRegister.py|対象とするGitHubアカウントを本ツールに登録する。
GitHubUploader.py|指定ディレクトリをリポジトリとして作成、アップロードする。
GitHubOtpCreator.py|指定ユーザのOTP(ワンタイムパスワード)をクリップボードにコピーする。
./database/src/contributions/SvgCreator.py|草SVGファイルを出力する

# 刷新したコマンド

コマンド|説明
--------|----
UserRegister.py|このツール群で使うGitHubアカウントを登録する。改名前: `GitHubUserRegister.py`
OtpCopy.py|TwoFactor認証アカウントのOTPをクリップボードにコピーする。改名前: `GitHubOtpCreator.py`
Create.py|指定したディレクトリに`.git`が無いならリポジトリとして作成する。（ローカル、リモート両方）
Upload.py|既存で`-m`引数があるならadd,commit,pushする
Delete.py|リポジトリを削除する。（ローカル、リモート両方）
Edit.py|リポジトリを編集する。（リモートのみ。説明文とURL）
ContributionGet.py|GitHubサイトからコントリビューション情報を取得する。
ContributionOutput.py|コントリビューションDBからSVGファイルを作成する。
IssueCreate.py|Issueを作成する。（※未完）

IssueCreate.pyはまだできていない。

## 以前のコマンドとの違い

* 多くは`GitHubUploader.py`をバラして各コマンドに置き換えた感じ
    * CUI入力確認をなくしたのがキモ
        * エラーが出ないかぎり処理が止まることはないはず
* ついでに改名もした

# 問題

* GitHubユーザIDをDBで保存していないことに気づいた
    * これによりIssueのAsiggneeなどでユーザ参照するときに困る
        * IDでなくユーザ名で参照する案もあるが、ユーザ名はGitHubサイトで変更できてしまう
            * 一意に特定できる保証がない

# 方針

* IssueCreate.py実装の前にAccountsデータベースを改修する
    * ついでにDBまわりも改修できたらいいかも？

# 準備

`GitHubUserRegister.py`でユーザ登録済みであること。

# 各コマンドの引数

## Create.py

```sh
$ python3 Create.py `pwd` -u username -d "説明文" -h "http://..." 
```

略名|名前|型|制約|説明
----|----|--|----|----
(1)|`path_dir_pj`|str|必須|リポジトリにしたいディレクトリパス
-u|`username`|str|必須|作成先のGitHubユーザ名
-d|`description`|str|-|リポジトリの説明文。
-l|`homepage`|str|-|リポジトリのURL。lはlinkの略。
-t|`topics`|list(str)|-|将来実装に備え名前を予約。リポジトリのタグ。`-t`を複数付与可能。
-L|`license`|str|-|将来実装に備え名前を予約。リポジトリのライセンス指定。LICENSE.txt自動作成。

### homepageの略名に悩んだ

* `-h`だとデフォルトの`--help`と被る。`-h`は頭文字なので良かったのだが`--help`より優先度が低いコマンドなので潰せない
* `-u`(URL)だと`--username`と被る
* `-p`(page)や`-s`(site)でもいいと思ったが、すでに`-l`(link)にしていたので`-l`にした
    * `License`と被るのでLicenseを大文字にした

## Upload.py

```sh
$ python3 Upload.py `pwd` -u username -m "コミットメッセージタイトル" -m "本文1行目" -m "本文2行目" ... -i "Issueタイトル" -i "# 本文1行目" ... -l "Issueラベル名1" -l "Issueラベル名2" ... -c
```

略名|名前|型|制約|説明
----|----|--|----|----
(1)|`path_dir_pj`|str|必須|リポジトリにしたいディレクトリパス
-u|`username`|str|必須|作成先のGitHubユーザ名
-m|`messages`|list(str)|必須|コミットメッセージ。1件目はタイトル(必須)。2件目以降は本文(任意)。
-i|`issues`|list(str)|-|Issueのタイトルと本文。
-l|`labels`|list(str)|-|将来実装に備え名前を予約。Issueのラベル。
-c|`is_close`|boolean|-|Issueを作成した直後に閉じるか否か。真ならコミットメッセージの先頭に`fix #Issue番号`が付与される。`-i`が1つもないと無視される

## Delete.py

```sh
$ python3 Delete.py `pwd` -u username
```

略名|名前|型|制約|説明
----|----|--|----|----
(1)|`path_dir_pj`|str|必須|リポジトリにしたいディレクトリパス
-u|`username`|str|必須|作成先のGitHubユーザ名

## Edit.py

```sh
$ python3 Edit.py `pwd` -u username
```

略名|名前|型|制約|説明
----|----|--|----|----
(1)|`path_dir_pj`|str|必須|リポジトリにしたいディレクトリパス
-u|`username`|str|必須|作成先のGitHubユーザ名
-r|`reponame`|str|-|リポジトリ名。path_dir_pjのディレクトリ名も変更される。
-d|`description`|str|-|リポジトリの説明文。
-l|`homepage`|str|-|リポジトリのURL。lはlinkの略。
-t|`topics`|list(str)|-|将来実装に備え名前を予約。リポジトリのタグ。`-t`を複数付与可能。

ライセンスは変更すべきでない。1度公開した時点で固定すべき。と勝手に考えているので更新はしない。

## ContributionGet.py

```sh
$ python3 ContributionGet.py -u username1 -u username2 ...
```

略名|名前|型|制約|説明
----|----|--|----|----
-u|`usernames`|list(str)|-|指定されたユーザのみ取得する。指定がないなら登録された全ユーザを取得する。

## ContributionOutput.py

```sh
$ python3 ContributionGet.py -o `pwd` -u username1 -u username2 ...
```

略名|名前|型|制約|説明
----|----|--|----|----
-u|`usernames`|list(str)|-|指定されたユーザのみ取得する。指定がないなら登録された全ユーザを取得する。
-o|`output_dir`|str|-|SVGファイルの出力先ディレクトリパス。指定がないならツール所定のパスとする。

## IssueCreate.py

```sh
$ python3 IssueCreate.py -u username -r "対象リポジトリ名" -i "Issueタイトル" -i "# 本文1行目" ... -l "Issueラベル名1" -l "Issueラベル名2" ... -c
```

略名|名前|型|制約|説明
----|----|--|----|----
-u|`username`|str|必須|作成先のGitHubユーザ名
-r|`reponame`|str|必須|作成先のリポジトリ名
-i|`issues`|list(str)|必須|Issueのタイトルと本文。1件目はタイトル(必須)。2件目以降は本文(任意)。
-l|`labels`|list(str)|-|将来実装に備え名前を予約。Issueのラベル。
-c|`is_close`|boolean|-|Issueを作成した直後に閉じるか否か。真ならコミットメッセージの先頭に`fix #Issue番号`が付与される。

上記のようにしたかった。しかし現状、GitHubAPIのラッパ実装コードをみると以下のようにする必要がある。`IssueCreate.py`は未実装なので今後の課題。

略名|名前|型|制約|説明
----|----|--|----|----
(1)|`path_dir_pj`|str|必須|リポジトリにしたいディレクトリパス
-u|`username`|str|必須|作成先のGitHubユーザ名
-i|`issues`|list(str)|必須|Issueのタイトルと本文。1件目はタイトル(必須)。2件目以降は本文(任意)。
-l|`labels`|list(str)|-|将来実装に備え名前を予約。Issueのラベル。
-c|`is_close`|boolean|-|Issueを作成した直後に閉じるか否か。真ならコミットメッセージの先頭に`fix #Issue番号`が付与される。

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

Library|License|Copyright
-------|-------|---------
[requests](http://requests-docs-ja.readthedocs.io/en/latest/)|[Apache-2.0](https://opensource.org/licenses/Apache-2.0)|[Copyright 2012 Kenneth Reitz](http://requests-docs-ja.readthedocs.io/en/latest/user/intro/#requests)
[dataset](https://dataset.readthedocs.io/en/latest/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2013, Open Knowledge Foundation, Friedrich Lindenberg, Gregor Aisch](https://github.com/pudo/dataset/blob/master/LICENSE.txt)
[bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright © 1996-2011 Leonard Richardson](https://pypi.python.org/pypi/beautifulsoup4),[参考](http://tdoc.info/beautifulsoup/)
[pytz](https://github.com/newvem/pytz)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2003-2005 Stuart Bishop <stuart@stuartbishop.net>](https://github.com/newvem/pytz/blob/master/LICENSE.txt)
[furl](https://github.com/gruns/furl)|[Unlicense](http://unlicense.org/)|[gruns/furl](https://github.com/gruns/furl/blob/master/LICENSE.md)
[PyYAML](https://github.com/yaml/pyyaml)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2006 Kirill Simonov](https://github.com/yaml/pyyaml/blob/master/LICENSE)

