#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   :2025/7/31 11:48
@Author :lancelot.sheng
@File   :rbac_middleware.py
"""
from fastapi import Depends, HTTPException, status
from .rbac_models import ROLE_PERMISSIONS, User, PermissionDeniedResponse

# 模拟用户数据库 (文档中的角色定义)
USER_DATABASE = {
    "user1": User(user_id="user1", roles=["user"]),
    "dev1": User(user_id="dev1", roles=["developer"]),
    "admin1": User(user_id="admin1", roles=["admin"])
}


# 获取当前用户 (实际项目应替换为JWT验证)
def get_current_user(user_id: str) -> User:
    if user := USER_DATABASE.get(user_id):
        return user
    raise HTTPException(status_code=404, detail="用户不存在")


# RBAC权限验证装饰器 (文档16.1节伪代码实现)
def permission_required(permission: str):
    def decorator(user: User = Depends(get_current_user)):
        # 合并用户所有角色的权限
        user_permissions = set()
        for role in user.roles:
            user_permissions.update(ROLE_PERMISSIONS.get(role, []))

        # 权限检查 (参考文档权限分配原则)
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=PermissionDeniedResponse().error
            )
        return user

    return decorator