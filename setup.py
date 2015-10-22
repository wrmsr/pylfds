#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys

import setuptools


if sys.version_info[0] > 2:
    try:
        exec_ = __builtins__['exec']
    except TypeError:
        exec_ = getattr(__builtins__, 'exec')
else:
    def exec_(_code_, _globs_=None, _locs_=None):
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
            exec("""exec _code_ in _globs_, _locs_""")


BASE_DIR = os.path.dirname(__file__)
ABOUT = {}
with open(os.path.join(BASE_DIR, 'lfds', '__about__.py')) as f:
    exec_(f.read(), ABOUT)


_lfdsExtension = setuptools.Extension(
    '_lfds', [
        '_lfds.c',
        'liblfds6.1.1/liblfds611/src/lfds611_abstraction/lfds611_abstraction_malloc.c',
        'liblfds6.1.1/liblfds611/src/lfds611_abstraction/lfds611_abstraction_free.c',
        'liblfds6.1.1/liblfds611/src/lfds611_freelist/lfds611_freelist_delete.c',
        'liblfds6.1.1/liblfds611/src/lfds611_freelist/lfds611_freelist_get_and_set.c',
        'liblfds6.1.1/liblfds611/src/lfds611_freelist/lfds611_freelist_new.c',
        'liblfds6.1.1/liblfds611/src/lfds611_freelist/lfds611_freelist_pop_push.c',
        'liblfds6.1.1/liblfds611/src/lfds611_freelist/lfds611_freelist_query.c',
        'liblfds6.1.1/liblfds611/src/lfds611_liblfds/lfds611_liblfds_abstraction_test_helpers.c',
        'liblfds6.1.1/liblfds611/src/lfds611_liblfds/lfds611_liblfds_aligned_free.c',
        'liblfds6.1.1/liblfds611/src/lfds611_liblfds/lfds611_liblfds_aligned_malloc.c',
        'liblfds6.1.1/liblfds611/src/lfds611_queue/lfds611_queue_delete.c',
        'liblfds6.1.1/liblfds611/src/lfds611_queue/lfds611_queue_new.c',
        'liblfds6.1.1/liblfds611/src/lfds611_queue/lfds611_queue_query.c',
        'liblfds6.1.1/liblfds611/src/lfds611_queue/lfds611_queue_queue.c',
        'liblfds6.1.1/liblfds611/src/lfds611_ringbuffer/lfds611_ringbuffer_delete.c',
        'liblfds6.1.1/liblfds611/src/lfds611_ringbuffer/lfds611_ringbuffer_get_and_put.c',
        'liblfds6.1.1/liblfds611/src/lfds611_ringbuffer/lfds611_ringbuffer_new.c',
        'liblfds6.1.1/liblfds611/src/lfds611_ringbuffer/lfds611_ringbuffer_query.c',
        'liblfds6.1.1/liblfds611/src/lfds611_slist/lfds611_slist_delete.c',
        'liblfds6.1.1/liblfds611/src/lfds611_slist/lfds611_slist_get_and_set.c',
        'liblfds6.1.1/liblfds611/src/lfds611_slist/lfds611_slist_link.c',
        'liblfds6.1.1/liblfds611/src/lfds611_slist/lfds611_slist_new.c',
        'liblfds6.1.1/liblfds611/src/lfds611_stack/lfds611_stack_delete.c',
        'liblfds6.1.1/liblfds611/src/lfds611_stack/lfds611_stack_new.c',
        'liblfds6.1.1/liblfds611/src/lfds611_stack/lfds611_stack_push_pop.c',
        'liblfds6.1.1/liblfds611/src/lfds611_stack/lfds611_stack_query.c',
    ],
    include_dirs=[
        'liblfds6.1.1/liblfds611/inc',
        'liblfds6.1.1/liblfds611/src',
    ],
    extra_compile_args=[
        '-Wall',
        '-Wno-unknown-pragmas',
        '-std=c99',
        '-pthread',
        '-O2',
        '-finline-functions',
        '-Wno-strict-aliasing',
        '-march=core2'
    ]
)


setuptools.setup(
    name=ABOUT['__title__'],
    version=ABOUT['__version__'],
    description=ABOUT['__description__'],
    author=ABOUT['__author__'],
    author_email=ABOUT['__email__'],
    url=ABOUT['__url__'],
    license=ABOUT['__license__'],

    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],

    packages=setuptools.find_packages(exclude=['tests']),
    setup_requires=['setuptools'],
    include_package_data=True,
    entry_points={},
    ext_modules=[_lfdsExtension],
)
