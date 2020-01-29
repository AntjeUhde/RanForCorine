# -*- coding: utf-8 -*-
"""
tuning.py: implements hyperparameter tuning for random forest model

@author: Theresa Möller
"""


from sklearn import ensemble as ensemble 
from sklearn.model_selection import RandomizedSearchCV

def tuneModel(grid, x_train, y_train, n_iter=3, cv=3, random_state=42, n_jobs = -1):
    """
    Implements randomized parameter search for Random Forest models.

    Parameters
    ----------
    grid: dictionary with list of possible values for each parameter 
        that should be tuned
    x_train: training dataset values
    y_train: traing dataset labels
    n_iter: int number of iterations
    cv: int number of folds of cross validation
    random_state: random integer to ensure reproducability
    n_jobs: parallel computing turned on (1) or off (-1) (default: -1)

    Examples
    --------
    >>> base_grid = {
    >>>        'n_estimators': [int(x) for x in np.linspace(start = 50, stop = 200, num = 5)],
    >>>        'max_features': ['auto', 'sqrt'],
    >>>        'max_depth': max_depth_base}
    >>> best_base_model = tuneModel(base_grid, x_train, y_train, n_jobs=1)

    Returns
    -------
    fitted best Random Forest model
    """
    tune_model = ensemble.RandomForestClassifier()
    tune_model_random = RandomizedSearchCV(
            estimator = tune_model, 
            param_distributions = grid, 
            n_iter = n_iter, 
            cv = cv, 
            verbose = 2, 
            random_state = random_state, 
            n_jobs = n_jobs)
    # Fit the random search model
    tune_model_random.fit(x_train, y_train)
    best_random = tune_model_random.best_estimator_
    return best_random


def getParamsOfModel(model):
    """
    Returns list of parameters used in model

    Parameters
    ----------
    model: random forest model
    
    Examples
    --------
    >>> base_model = RandomForestClassifier(2, 245, 100)
    >>> params = getParamsOfModel(base_model)

    Returns
    -------
    list of parameters
    """
    params = model.get_params()
    return params