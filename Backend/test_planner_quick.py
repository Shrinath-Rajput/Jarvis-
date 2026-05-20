#!/usr/bin/env python3
"""Quick planner test"""

from planner_ai import DynamicPlanner

print("\n" + "="*60)
print("PLANNER TEST")
print("="*60)

p = DynamicPlanner()

tasks = [
    "open youtube",
    "search for kubernetes tutorial on youtube",
    "create folder MyProject on desktop"
]

for task in tasks:
    print(f"\n>>> Task: {task}")
    plan = p.plan_task(task)
    
    if plan:
        print(f"    Plan generated! {len(plan)} actions:")
        for i, action in enumerate(plan[:3], 1):
            tool = action.get("tool", "unknown")
            params = action.get("params", {})
            print(f"      {i}. {tool} - {params}")
        if len(plan) > 3:
            print(f"      ... and {len(plan) - 3} more actions")
    else:
        print(f"    NO PLAN GENERATED")

print("\n" + "="*60)
