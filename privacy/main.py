#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   :2025/7/31 11:50
@Author :lancelot.sheng
@File   :main.py
"""
from fastapi import FastAPI, Depends, HTTPException
from .rbac_models import User
from .rbac_middleware import permission_required, get_current_user

app = FastAPI()

# 公开端点：获取当前用户角色
@app.get("/whoami")
async def whoami(user: User = Depends(get_current_user)):
    return {"user_id": user.user_id, "roles": user.roles}

# 需data:read权限 (文档中的knowledge_base:query)
@app.get("/data", dependencies=[Depends(permission_required("data:read"))])
async def read_data():
    return {"data": "敏感数据，需data:read权限可见"}

# 需data:write权限 (文档中的knowledge_base:upload)
@app.post("/data", dependencies=[Depends(permission_required("data:write"))])
async def write_data():
    return {"status": "数据写入成功"}

# 需user:manage权限 (文档中的管理员专属操作)
@app.delete("/users/{user_id}", dependencies=[Depends(permission_required("user:manage"))])
async def delete_user(user_id: str):
    return {"status": f"用户{user_id}已删除"}