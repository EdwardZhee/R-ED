#!/usr/bin/env python3.7

import urllib.request
import argparse


def url_correction(site_url):
    if site_url[:4] != "www." and (site_url[:7] != "http://" or site_url[:8] == "https://"):
        res = 'http://' + site_url
    elif site_url[:4] == "www.":
        tmp = str.split(site_url, ".")
        res = "http://"
        for _ in range(len(tmp)):
            if _ > 0 :
                if _ < len(tmp)-1:
                    res += tmp[_] + '.'
                else:
                    res += tmp[_]
    else:
        res = site_url
    return res


def get_return_code(site):
    try:
        site = url_correction(site)
        return urllib.request.urlopen(site).getcode()
    except urllib.error.URLError:
        return "null"


def output_write(var, filename):

    ok = {}
    other = {}
    output_filename = str.split(filename, ".")[0] + '_checked.txt'
    output_file = open(str(output_filename), 'w+')

    for key,value in var.items():
        if value == 200:
            ok.update({key:value})
        else:
            other.update({key:value})

    output_file.write('200 OK :\n')
    for key,value in ok.items():
        output_file.writelines('{} : {}'.format(str(value).rstrip('\n'),str(key)))

    output_file.write('\nOther responses :\n')
    for key,value in other.items():
        output_file.writelines('{} : {}'.format(str(value).rstrip('\n'),str(key)))

    output_file.close()
    print("[*] File written to {}".format(output_filename))


if __name__ == '__main__':

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("filename", help="File containing sites to check.")
        args = parser.parse_args()

        print("[*] Starting...")
        site_list = open(args.filename, 'r')
        site_result = {}
        ok = {}
        others = {}
        for _ in  site_list.readlines():
            crrctd_url = url_correction(_)
            print("[*] Checking : {}".format(crrctd_url))
            site_result.update({_:get_return_code(str(_)) })

        print("[*] Writing output to file.")
        output_write(site_result, args.filename)
        site_list.close()

    except KeyboardInterrupt:
        print("\n[!!] ^C initiated, stopping...")
        print("[!!] Have a nice day!")
        exit(0)

    except Exception as e:
        print("[!!] {}".format(e))
        exit(1)