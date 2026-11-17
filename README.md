# pairwise-character-controller

QA 反馈角色在斜坡上往下滑，走到台阶前直接卡死，贴着墙走会被吸进去，从高处落地还会反弹一下，快速移动时直接穿墙。查下来是 game/controller.py 的角色控制器有严重问题：integrate_velocity() 完全不积分加速度，输入只改朝向不改速度，摩擦力也没生效；is_walkable() 永远返回可走，90 度墙也能走上去；project_velocity() 不把速度投影到地面，撞墙后速度还朝着墙里；step_up_allowed() 永远允许上台阶，一米高的台子也能直接迈；resolve_penetration() 不做法线推出，角色卡在碰撞体里；substep_count() 恒为 1，高速移动一步跨过整面墙；apply_gravity() 不积分重力也不限制下落速度；can_coyote_jump() 永远允许起跳，离开地面很久还能二段跳；land() 不做落地处理，下落速度原样保留。你要修的是：速度积分包含加速度、摩擦和限速；坡度按法线夹角判定；速度投影到地面平面；台阶高度限制；按法线推出穿透；按最大步长细分；重力积分并限制最大下落速度；土狼时间有上限；落地按恢复系数处理竖直速度。game/controller.py 是核心，tests/test_controller.py 15个红。

## 运行

```
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。
