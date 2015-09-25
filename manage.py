#!/usr/bin/env python
#coding=utf-8


from flask import Flask
from flask import current_app
from flask.ext.script import Manager

from rpress import create_app


#----------------------------------------------------------------------
def main():
    """"""
    manager = Manager(create_app)
    #app = create_app

    manager.run()

    return


if __name__ == "__main__":
    main()