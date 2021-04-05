# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:47:07 2021

@author: Carla
"""
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_score
import numpy as np
from load_data import read_numerical_data_from_local
import re
import shap

def f1_score(clusters):
    data = read_numerical_data_from_local()
    data = data.drop(columns = ['Diagnóstico'])
    data = data.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))
    clf_kp = LGBMClassifier(colsample_by_tree=0.8)
    cv_scores_kp = cross_val_score(clf_kp, data, clusters, scoring='f1_weighted')
    print(f'CV F1 score clustering is {np.mean(cv_scores_kp)}')
    
    clf_kp.fit(data, clusters)
    explainer_kp = shap.TreeExplainer(clf_kp)
    shap_values_kp = explainer_kp.shap_values(data)
    shap.summary_plot(shap_values_kp, data, plot_type="bar", plot_size=(15, 10))