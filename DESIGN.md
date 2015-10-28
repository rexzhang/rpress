
rPress
======

a mulit-site and mulit-user blog system.

多站点支持
---------

* 不同域名
* 不同子目录？？

所有 post 均使用类 uuid 的唯一编号

####所有 name

* 均只支持小写字母、数字、减号组合，同时字母开头
	* 导入是将所有 name 小写化处理
* 同时在需要时可用于组合 url

所有 site_id 为 0 标示为系统级设置与具体站点无关，或者系统级默认设置

blog 隶属于 user

page 隶属于 site

站点模式
-------

* 单域名、支持多人的单站点、（个人博客、团队博客）
    * www.rpress.com/rp-admin/rrr
    * www.rpress.com/ppp
    * www.rpress.com/bbb
    * www.rpress.com/category/term-name/bbb
    * 系统初始化的时候默认建一个 site

* 单域名、基于子目录的多站点（多人公用域名的个人博客、用户之间无关联）
    * 不同 user-name 下面是否有不同的 theme 设置？
    * www.rpress.com/rp-admin/rrr
    * www.rpress.com/ppp
    * www.rpress.com/user-name/bbb
    * www.rpress.com/user-name/category/term-name/bbb

* 多域名、基于不同域名的多站点（同一个系统支持多个有自己域名的用户，不支持单一域名下多个用户）
    * 每一个用户域名对应一个 user-name
    * 通过配置文件／数据库设置来激活多站点模式；其实激活进入超级站点管理界面
    * www.siteX.com/sites-admin/rrr

    * www.site1.com/bbb
    * www.site1.com/rp-admin/rrr
    * www.site2.com/bbb
    * www.site2.com/rp-admin/rrr

最好是基于账号是否是超级管理员来判断是否能管理整个系统，这样就可以将具体站点内容相关的权限分发下去

站点编号从 1 开始

URL 规则
-------
特色子类均用固定子目录来区分 blog/archive/category/tag/date/

* blog
		* /post/uuid0001 recommend

    * /
    * /paginate/1

* page
    * /name - recommend
		* /post/uuid0001

* category
    * /category/xxxx
    * /category/xxxx/paginate/1

* tag
    * /tag/xxxx
    * /tag/xxxx/paginate/1

* archive
    * /date/YYYY/MM
    * /date/YYYY
    * /date/YYYY/paginate/1

* author
	* /author/rex
	* /author/rex/paginate/1

* rPress admin
	* /rpadmin/xxxx


数据库表结构
----------

###用户／账号表结构 users

* id
* name

* display_name
* password
* email


###站点信息表结构 sites

* id            #需要规避 0 ，可以在初始化的时候初始化一个 id 为 0 来占位，如果要支持 subdir 模式，需要为 0 号站点设置 domain_name
* name          #同时作为子目录名 subdir_name

* domain   #域名，可选？


###设置 settings

* id ??
* site_id

* name
* value


###权限 roles

* id ??
* site_id
* user_id

* role      #admin/writer


###文章表结构 posts

* id
* site_id

* author_user_id

* published       #True/False
* publish_state   #publish / history/draft/auto-draft/trash
* publish_date

* updater_user_id
* update_date

* allow_comment #True/False

* type          #blog/page
* name

* title
* content


###分类表结构 terms

* id
* site_id
* name

* type          #tag/category 系统将 category 也视为 tag 处理，只是前台用途不同，必然某些工作博客需要一个大分类机制来归纳文章
* display_name  #显示用；


###分类与文章之间的关联 term_relation

* site_id
* past_id
* term_id

post发布状态机
-------------
~~~
@startuml
digraph pic2 {
  draft -> published[label="更新发布时间"]
  published -> unpublish
  unpublish -> published
  published -> trash
  trash -> published
  published -> history
}
@enduml
~~~
