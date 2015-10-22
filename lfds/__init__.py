# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import ctypes

import _lfds

lib = ctypes.CDLL(_lfds.__file__)

malloc_fn = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_size_t)
free_fn = ctypes.CFUNCTYPE(None, ctypes.c_void_p)

lib.lfds611_abstraction_malloc_impl = ctypes.cast(
    lib.lfds611_abstraction_malloc_impl, ctypes.POINTER(ctypes.c_uint64))
lib.lfds611_abstraction_free_impl = ctypes.cast(
    lib.lfds611_abstraction_free_impl, ctypes.POINTER(ctypes.c_uint64))

# FIXME: Make context struct
malloc_impl = None
free_impl = None

def set_mem_fns(malloc, free):
    global malloc_impl
    global free_impl

    if malloc_impl is not None:
        raise TypeError()

    malloc_impl = malloc_fn(malloc)
    free_impl = free_fn(free)

    lib.lfds611_abstraction_malloc_impl.contents.value = ctypes.cast(malloc_impl, ctypes.c_void_p).value
    lib.lfds611_abstraction_free_impl.contents.value = ctypes.cast(free_impl, ctypes.c_void_p).value


abstraction_malloc = lib.lfds611_abstraction_malloc.restype
lib.lfds611_abstraction_malloc.restype = ctypes.c_void_p
lib.lfds611_abstraction_malloc.argtypes = [ctypes.c_size_t]

abstraction_free = lib.lfds611_abstraction_free.restype
lib.lfds611_abstraction_free.restype = None
lib.lfds611_abstraction_free.argtypes = [ctypes.c_void_p]


atom_t = ctypes.c_uint64


freelist_query_type = ctypes.c_int
FREELIST_QUERY_ELEMENT_COUNT = 0
FREELIST_QUERY_VALIDATE = 1

class freelist_state(ctypes.Structure):
    pass
class freelist_element(ctypes.Structure):
    pass

freelist_new__user_data_init_function = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_void_p), # user_data
    ctypes.c_void_p, # user_state
)

freelist_new = lib.lfds611_freelist_new
freelist_new.restype = ctypes.c_int
freelist_new.argtypes = [
    ctypes.POINTER(ctypes.POINTER(freelist_state)), # ss
    atom_t, # number_elements
    freelist_new__user_data_init_function, # user_data_init_function
    ctypes.c_void_p, # user_state
]

freelist_use = lib.lfds611_freelist_use
freelist_use.restype = None
freelist_use.argtypes = [
    ctypes.POINTER(freelist_state), # fs
]

freelist_delete__user_data_delete_function = ctypes.CFUNCTYPE(
    None,
    ctypes.c_void_p, # user_data
    ctypes.c_void_p, # user_state
)

freelist_delete = lib.lfds611_freelist_delete
freelist_delete.restype = None
freelist_delete.argtypes = [
    ctypes.POINTER(freelist_state), # fs
    freelist_delete__user_data_delete_function, # user_data_delete_function
    ctypes.c_void_p, # user_data
]

freelist_new_elements = lib.lfds611_freelist_new_elements
freelist_new_elements.restype = atom_t
freelist_new_elements.argtypes = [
    ctypes.POINTER(freelist_state), # fs
    atom_t, #  number_elements
]

freelist_pop = lib.lfds611_freelist_pop
freelist_pop.restype = ctypes.POINTER(freelist_element)
freelist_pop.argtypes = [
    ctypes.POINTER(freelist_state), # fs
    ctypes.POINTER(ctypes.POINTER(freelist_element)), # fe
]

freelist_guaranteed_pop = lib.lfds611_freelist_guaranteed_pop
freelist_guaranteed_pop.restype = ctypes.POINTER(freelist_element)
freelist_guaranteed_pop.argtypes = [
    ctypes.POINTER(freelist_state), # fs
    ctypes.POINTER(ctypes.POINTER(freelist_element)), # fe
]

freelist_push = lib.lfds611_freelist_push
freelist_push.restype = None
freelist_push.argtypes = [
    ctypes.POINTER(freelist_state), # fs
    ctypes.POINTER(freelist_element), # fe
]

freelist_get_user_data_from_element = lib.lfds611_freelist_get_user_data_from_element
freelist_get_user_data_from_element.restype = ctypes.c_void_p
freelist_get_user_data_from_element.argtypes = [
    ctypes.POINTER(freelist_element), # fe
    ctypes.POINTER(ctypes.c_void_p), # user_data
]

freelist_set_user_data_in_element = lib.lfds611_freelist_set_user_data_in_element
freelist_set_user_data_in_element.restype = None
freelist_set_user_data_in_element.argtypes = [
    ctypes.POINTER(freelist_element), # fe
    ctypes.c_void_p, # user_data
]

freelist_query = lib.lfds611_freelist_query
freelist_query.restype = None
freelist_query.argtypes = [
    ctypes.POINTER(freelist_state), # fs
    freelist_query_type, # query_type
    ctypes.c_void_p, # query_input,
    ctypes.c_void_p, # query_output
]


queue_query_type = ctypes.c_int
QUEUE_QUERY_ELEMENT_COUNT = 0
QUEUE_QUERY_VALIDATE = 1

class queue_state(ctypes.Structure):
    pass

queue_new = lib.lfds611_queue_new
queue_new.restype = ctypes.c_int
queue_new.argtypes = [
    ctypes.POINTER(ctypes.POINTER(queue_state)), # sq
    atom_t, # number_elements
]

queue_use = lib.lfds611_queue_use
queue_use.restype = None
queue_use.argtypes = [
    ctypes.POINTER(queue_state), # qs
]

queue_delete__user_data_delete_function = ctypes.CFUNCTYPE(
    None,
    ctypes.c_void_p, # user_data
    ctypes.c_void_p, # user_state
)

queue_delete = lib.lfds611_queue_delete
queue_delete.restype = None
queue_delete.argtypes = [
    ctypes.POINTER(queue_state), # qs
    queue_delete__user_data_delete_function, # user_data_delete_function
    ctypes.c_void_p, # user_state
]

queue_delete_ = lib.lfds611_queue_delete
queue_delete_.restype = None
queue_delete_.argtypes = [
    ctypes.POINTER(queue_state), # qs
    ctypes.c_void_p, # user_data_delete_function
    ctypes.c_void_p, # user_state
]

queue_enqueue = lib.lfds611_queue_enqueue
queue_enqueue.restype = ctypes.c_int
queue_enqueue.argtypes = [
    ctypes.POINTER(queue_state), # qs
    ctypes.c_void_p, # user_data
]

queue_guaranteed_enqueue = lib.lfds611_queue_guaranteed_enqueue
queue_guaranteed_enqueue.restype = ctypes.c_int
queue_guaranteed_enqueue.argtypes = [
    ctypes.POINTER(queue_state), # qs
    ctypes.c_void_p, # user_data
]

queue_dequeue = lib.lfds611_queue_dequeue
queue_dequeue.restype = ctypes.c_int
queue_dequeue.argtypes = [
    ctypes.POINTER(queue_state), # qs
    ctypes.POINTER(ctypes.c_void_p), # user_data
]

queue_query = lib.lfds611_queue_query
queue_query.restype = None
queue_query.argtypes = [
    ctypes.POINTER(queue_state), # qs
    queue_query_type, # query_type
    ctypes.c_void_p, # query_input
    ctypes.c_void_p, # query_output
]

if hasattr(lib, 'lfds611_queue_freelist_new'):
    queue_freelist_new = lib.lfds611_queue_freelist_new
    queue_freelist_new.restype = ctypes.POINTER(freelist_state)
    queue_freelist_new.argtypes = [
        atom_t, # number_elements
        atom_t, # number_queues
    ]

if hasattr(lib, 'lfds611_queue_new_with_freelist'):
    queue_new_with_freelist = lib.lfds611_queue_new_with_freelist
    queue_new_with_freelist.restype = ctypes.c_int
    queue_new_with_freelist.argtypes = [
        ctypes.POINTER(ctypes.POINTER(queue_state)), # qs
        atom_t, # number_elements
        ctypes.POINTER(freelist_state), # fs
    ]

if hasattr(lib, 'lfds611_queue_delete_with_freelist'):
    queue_delete_with_freelist = lib.lfds611_queue_delete_with_freelist
    queue_delete_with_freelist.restype = None
    queue_delete_with_freelist.argtypes = [
        ctypes.POINTER(queue_state), # qs
        queue_delete__user_data_delete_function, # user_data_delete_function
        ctypes.c_void_p, # user_state
        atom_t, # delete_freelist
    ]

    queue_delete_with_freelist_ = lib.lfds611_queue_delete_with_freelist
    queue_delete_with_freelist_.restype = None
    queue_delete_with_freelist_.argtypes = [
        ctypes.POINTER(queue_state), # qs
        ctypes.c_void_p, # user_data_delete_function
        ctypes.c_void_p, # user_state
        atom_t, # delete_freelist
    ]
