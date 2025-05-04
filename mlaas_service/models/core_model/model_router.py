"""
model_router.py - Provides regression model selection logic per group.
"""

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

def get_model_for_group(group):
    if group == 0:
        return LinearRegression()
    elif group == 1:
        return DecisionTreeRegressor(max_depth=5)
    else:
        return DecisionTreeRegressor(max_depth=3)
