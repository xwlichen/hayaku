# -*- coding: utf-8 -*-
import os
import sublime

def import_dir(name, fromlist=()):
    PACKAGE_EXT = '.sublime-package'
    dirname = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    if dirname.endswith(PACKAGE_EXT):
        dirname = dirname[:-len(PACKAGE_EXT)]
    return __import__('{0}.{1}'.format(dirname, name), fromlist=fromlist)

try:
    imp = import_dir('hayaku_dict_driver', ('parse_dict_json',))
    get_css_dict, merge_dict, merge_aliases = imp.get_css_dict, imp.merge_dict, imp.merge_aliases
except ImportError:
    from hayaku_dict_driver import get_css_dict, merge_dict, merge_aliases

hayaku_extra_dicts_cache = {}
hayaku_extra_aliases_cache = {}
hayaku_dict_cache = {}
hayaku_aliases_cache = {}

def get_merged_dict(self, extra_scopes):
    global hayaku_extra_dicts_cache
    global hayaku_extra_aliases_cache
    global hayaku_dict_cache
    global hayaku_aliases_cache
    result_dict, result_aliases = get_css_dict()
    if hayaku_dict_cache == {}:
        hayaku_dict_cache = result_dict
    if hayaku_aliases_cache == {}:
        hayaku_aliases_cache = result_aliases
    new_dict = {}
    new_aliases = {}

    def apply_extra_dict(scope):
        dict_name = 'hayaku_' + scope + '_dict'
        alias_name = 'hayaku_' + scope + '_aliases'

        got_dict = self.view.settings().get(dict_name)
        got_alias = self.view.settings().get(alias_name)
        if got_dict:
            new_dict[dict_name] = got_dict

        if got_alias:
            new_aliases[alias_name] = got_alias

    for scope in extra_scopes:
        apply_extra_dict(scope)

    if new_dict != hayaku_extra_dicts_cache:
        hayaku_extra_dicts_cache = new_dict

        for dict_scope in dict(hayaku_extra_dicts_cache):
            result_dict = merge_dict(result_dict, hayaku_extra_dicts_cache.get(dict_scope))

        hayaku_dict_cache = result_dict

    if new_aliases != hayaku_extra_aliases_cache:
        hayaku_extra_aliases_cache = new_aliases

        for aliases_scope in dict(hayaku_extra_aliases_cache):
            result_aliases = merge_aliases(result_aliases, hayaku_extra_aliases_cache.get(aliases_scope))

        hayaku_aliases_cache = result_aliases

    return hayaku_dict_cache, hayaku_aliases_cache