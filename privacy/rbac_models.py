#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   :2025/7/31 11:48
@Author :lancelot.sheng
@File   :rbac_models.py
"""
from pydantic import BaseModel
from typing import List, Dict

# 角色-权限映射 (参考文档16.1节)
ROLE_PERMISSIONS = {
    "admin": ["data:read", "data:write", "user:manage"],
    "developer": ["data:read", "data:write"],
    "user": ["data:read"]
}


# 用户数据模型 (文档16.1节角色定义)
class User(BaseModel):
    user_id: str
    roles: List[str]  # 用户可拥有多个角色


# 权限装饰器响应模型
class PermissionDeniedResponse(BaseModel):
    error: str = "权限不足"
