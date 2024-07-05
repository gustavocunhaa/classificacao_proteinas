import os
import json
import pickle
from datetime import datetime
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score

SEED = 1337

class TrainTestModel():

    def __init__(self, model_name, 
                 x, y, test_size, 
                 otimization_metric, model_params, n_splits,
                 model, path_save
                 ):
        
        self.model_name = model_name
        self.x = x
        self.y = y
        self.test_size = test_size
        self.otimization_metric = otimization_metric
        self.model_params = model_params
        self.n_splits = n_splits
        self.path_save = path_save
        self.model = model

    def split_data(self):
        x = self.x
        y = self.y
        test_size = self.test_size
        print(f">>> Spliting data on {test_size*100}% for test")

        try:
            X_train, X_test, y_train, y_test = train_test_split(x, y, 
                                                                random_state=SEED, 
                                                                test_size=test_size)
            print(f"SUCESS: Slipt Data")
        except ValueError as e:
            print(f"ERROR: Slipt Data - {e}")
        
        return X_train, X_test, y_train, y_test 
    
    def search_model_params(self, X_train, y_train):        
        model = self.model
        params = self.model_params
        n_splits = self.n_splits
        scoring = self.otimization_metric
        print(f">>> Grid Search for optimize {scoring} | params: {params}")

        try:
            grid = GridSearchCV(
                        estimator=model,
                        param_grid=params,
                        cv=KFold(n_splits=n_splits, shuffle=True),
                        scoring=scoring,
                        n_jobs=-1,
                        verbose=3
                        ).fit(X_train, y_train)
            print(f"SUCESS: Find best model")
        except ValueError as e:
            print(f"ERROR: Find best model - {e}")

        return grid.best_estimator_ 

    def train_evalute_model(self, model, X_train, X_test, y_train, y_test):
        print(f">>> Traning model: {model}")

        try:
            model_fit = model.fit(X_train, y_train)
            predictions = model_fit.predict(X_test)
            acc_value = accuracy_score(y_test, predictions)
            precision_value = precision_score(y_test, predictions, average='weighted')
            recall_value = recall_score(y_test, predictions, average='weighted')
            f1_value = f1_score(y_test, predictions, average='weighted')
            results = {
                'accuracy':  round(acc_value, 4),
                'precision': round(precision_value, 4),
                'recall':    round(recall_value, 4),
                'f1':        round(f1_value, 4)       
            }
            print(classification_report(y_test, predictions))
            print(f"SUCESS: Train and test model")
        except ValueError as e:
            print(f"ERROR: Train and test model - {e}")

        return model_fit, results
    
    def save_model(self, model_fit, results):
        path = self.path_save
        model_name = self.model_name
        timestamp = int(datetime.now().timestamp())
        hash = f"{model_name}_{timestamp}"
        save_path = os.path.join(path, f"{hash}.pkl")
        results_path = os.path.join(path, f"{hash}_results.json")
        print(f">>> Saving model in {save_path}")
        
        try:
            sav_model = open(save_path, 'wb')
            pickle.dump(model_fit, sav_model)
            sav_model.close()
            with open(results_path, 'w') as result:
                json.dump(results, result)
            print(f"SUCESS: Model save")
        except ValueError as e:
            print(f"ERROR: Model save - {e}")

    def run(self):
        X_train, X_test, y_train, y_test = self.split_data()
        best_model = self.search_model_params(X_train,y_train)
        model_fit, results = self.train_evalute_model(best_model, X_train, X_test, y_train, y_test)
        self.save_model(model_fit, results)