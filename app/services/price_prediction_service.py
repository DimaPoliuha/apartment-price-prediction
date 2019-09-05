import joblib
import torch
import pandas as pd
import lightgbm as lgb
from pathlib import Path
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor
from database_pg.queries import get_apartments_list
from services.dataset_utils import detect_outliers
from ml_models.price_prediction_nn import train_nn, load_nn_model


class PricePredictionService:
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    random_state = 41
    models_path = Path("./app/_saved_price_prediction_models")
    decision_tree_model_file = Path("decision_tree.pkl")
    lightgbm_model_file = Path("lightgbm.pkl")
    nn_model_file = Path("nn.npy")
    nn_params = {
        "input_dim": 365,
        "hidden_dim": 300,
        "hidden_num": 2,
        "learning_rate": 1,
        "epochs": 1000,
    }

    def __init__(self):
        self.dataset = None
        if not self.models_path.exists():
            self.models_path.mkdir(mode=0o777, exist_ok=True)

        if not (self.models_path / self.decision_tree_model_file).exists():
            self._train_decision_tree()
        self.decision_tree_model = self._load_model(self.decision_tree_model_file)

        if not (self.models_path / self.lightgbm_model_file).exists():
            self._train_lightgbm()
        self.lightgbm_model = self._load_model(self.lightgbm_model_file)

        if not (self.models_path / self.nn_model_file).exists():
            self._train_nn()
        self._make_preprocess_nn_input()
        self.nn_model = load_nn_model(self.models_path / self.nn_model_file, self.device, self.nn_params)

    def predict(self, model, X):
        X = pd.DataFrame([X])
        if model == "decision_tree":
            pred = self.decision_tree_model.predict(X)[0]
        elif model == "lightgbm":
            pred = self.lightgbm_model.predict(X)[0]
        elif model == "nn":
            X = self.preprocess_nn_inpt.transform(X)
            X = torch.Tensor(X.toarray()).to(self.device)
            pred = self.nn_model(X).item()
        else:
            raise Exception("Specify correct model name")
        return pred

    def _train_decision_tree(self):
        self._load_dataset()
        preprocess, dataset = self._preprocess_dataset()
        X, y = dataset.drop(columns=["price_usd"]), dataset["price_usd"]
        model = make_pipeline(
            preprocess,
            DecisionTreeRegressor(
                random_state=self.random_state,
                max_depth=12,
                min_impurity_decrease=0,
                min_samples_leaf=20,
                min_samples_split=50,
                max_leaf_nodes=None
            )
        )
        model.fit(X, y)
        self._save_model(model, self.decision_tree_model_file)

    def _train_lightgbm(self):
        self._load_dataset()
        preprocess, dataset = self._preprocess_dataset()
        X, y = dataset.drop(columns=["price_usd"]), dataset["price_usd"]

        model = make_pipeline(
            preprocess,
            lgb.LGBMRegressor(
                random_state=self.random_state,
                num_leaves=26,
                n_estimators=70,
                max_depth=8,
                learning_rate=0.1,
            )
        )
        model.fit(X, y)
        self._save_model(model, self.lightgbm_model_file)

    def _make_preprocess_nn_input(self):
        self._load_dataset()
        self.preprocess_nn_inpt, dataset = self._preprocess_dataset()
        X = dataset.drop(columns=["price_usd"])
        y = dataset["price_usd"].values
        self.preprocess_nn_inpt.fit(X)
        return X, y

    def _train_nn(self):
        X, y = self._make_preprocess_nn_input()
        X = self.preprocess_nn_inpt.transform(X)
        model = train_nn(X.toarray(), y, self.device, self.nn_params)
        torch.save(model.state_dict(), self.models_path / self.nn_model_file)

    def _preprocess_dataset(self):
        dataset = pd.DataFrame(self.dataset)
        dataset = dataset.drop(
            columns=["apartment_condition", "building_number", "centre_distance", "centre_distance_type",
                     "construction_year", "creation_date", "description", "id", "images", "latitude",
                     "longitude", "price_uah", "selling_type", "title", "url", "verified_apartment",
                     "region", "street"])
        dataset.fillna(value={'heating': 'централизованное'}, inplace=True)
        dataset.drop_duplicates(inplace=True)
        to_drop_idx = dataset.query(
            "walls_material == 'кирпич' and verified_price == False and heating == 'централизованное' and "
            "city == 'Одесса' and apartment_type == 'Вторичное жилье'"
        ).index
        dataset.drop(index=to_drop_idx[:4000], inplace=True)
        categorical_features = ["apartment_type", "city", "district", "heating", "walls_material"]
        numerical_features = ["total_square", "living_square", "kitchen_square", "room_count", "floor", "floor_count"]
        outliers_idx = detect_outliers(dataset, 2, numerical_features)
        dataset.drop(index=outliers_idx, inplace=True)
        preprocess = make_column_transformer(
            (OneHotEncoder(handle_unknown='ignore'), categorical_features),
            (StandardScaler(), numerical_features),
        )
        return preprocess, dataset

    def _save_model(self, model, model_file):
        joblib.dump(model, self.models_path / model_file)

    def _load_model(self, model_file):
        return joblib.load(self.models_path / model_file)

    def _load_dataset(self):
        if self.dataset is None:
            self.dataset = get_apartments_list()
