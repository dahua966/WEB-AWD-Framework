#!/usr/bin/env python
# encoding: utf-8

import color
import sys

class Log():
    @staticmethod
    def _print(word):
        sys.stdout.write(word)
        sys.stdout.flush()

    @staticmethod
    def info(word):
        Log._print(color.white("[*] %s\n" %word))

    @staticmethod
    def warning(word):
        Log._print(color.yellow("[!] %s\n" % word))

    @staticmethod
    def error(word):
        Log._print(color.red("[-] %s\n" % word))

    @staticmethod
    def success(word):
        Log._print(color.green("[+] %s\n" % word))

    @staticmethod
    def query(word):
        Log._print(color.underline("[?] %s\n" % word))

    @staticmethod
    def wait(word):
        Log._print(color.cyan("[.] %s\n" % word))

    @staticmethod
    def banner(context):
        Log._print(color.purple("%s" % context))

    @staticmethod
    def console(header):
        Log._print(color.red(header))
