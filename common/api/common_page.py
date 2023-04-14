#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2020/11/26 10:53
@note     
"""


class CommonPage:

    @staticmethod
    def restPage(pagination):
        return {
            # 当前页码
            "page_num": pagination.page,
            # 总页数
            "total_page": pagination.pages,
            # 页大小
            "page_size": pagination.per_page,
            # 结果总数
            "total": pagination.total,
            # 结果列表
            "list": [item.to_dict() for item in pagination.items]
        }

    @staticmethod
    def page(current_page, total_page, page_size, total_count, items):
        return {
            # 当前页码
            "page_num": current_page,
            # 总页数
            "total_page": total_page,
            # 页大小
            "page_size": page_size,
            # 结果总数
            "total": total_count,
            # 结果列表
            "list": items
        }
