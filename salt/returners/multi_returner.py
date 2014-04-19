# -*- coding: utf-8 -*-
'''
Read/Write multiple returners

'''

# Import python libs
import logging

# Import salt libs
import salt.minion

log = logging.getLogger(__name__)

CONFIG_KEY = 'multi_returner'

# cache of the master mininon for this returner
MMINION = None


def _mminion():
    '''
    Create a single mminion for this module to use, instead of reloading all the time
    '''
    global MMINION

    if MMINION is None:
        MMINION = salt.minion.MasterMinion(__opts__)

    return MMINION


def returner(load):
    '''
    Write return to all returners in multi_returner
    '''

    for returner in __opts__[CONFIG_KEY]:
        _mminion().returners['{0}.returner'.format(returner)](load)


def save_load(jid, clear_load):
    '''
    Write load to all returners in multi_returner
    '''
    for returner in __opts__[CONFIG_KEY]:
        _mminion().returners['{0}.save_load'.format(returner)](jid, clear_load)


def get_load(jid):
    '''
    Merge the load data from all returners
    '''
    ret = {}
    for returner in __opts__[CONFIG_KEY]:
        ret.update(_mminion().returners['{0}.get_load'.format(returner)](jid))

    return ret


def get_jid(jid):
    '''
    Merge the return data from all returners
    '''
    ret = {}
    for returner in __opts__[CONFIG_KEY]:
        ret.update(_mminion().returners['{0}.get_jid'.format(returner)](jid))

    return ret


def get_jids():
    '''
    Return all job data from all returners
    '''
    ret = {}
    for returner in __opts__[CONFIG_KEY]:
        ret.update(_mminion().returners['{0}.get_jids'.format(returner)]())

    return ret


def clean_old_jobs():
    '''
    Clean out the old jobs from all returners (if you have it)
    '''
    for returner in __opts__[CONFIG_KEY]:
        fstr = '{0}.clean_old_jobs'.format(returner)
        if fstr in _mminion().returners:
            _mminion().returners[fstr]()
