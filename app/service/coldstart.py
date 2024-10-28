import pandas as pd
from typing import Dict, List
from app.utils.digestmeal import combine_meal
from app.utils.metabolize import Texts
from app.utils.stomach import save_model_weights, get_model_weights

def get_data() -> pd.DataFrame:
    data = combine_meal()
    txt_obj = Texts(data)
    wordbag = txt_obj.filter_ascii().wordsbag("course")
    return wordbag

def update_model_weights() -> None:
    txt_obj = Texts()
    wordbag = get_data()
    save_model_weights(model= txt_obj.generate_vector_embeddings(wordbag))

def predict(entries: Dict[str, str] = {}, top_n: int = 10) -> pd.DataFrame:
    embeddings = get_model_weights()
    wordbag = get_data().reset_index()
    index_course = wordbag[wordbag['course'].str.contains(entries['course'], case=False)].index[0]
    similarity: List[float] = list(embeddings[index_course].T)
    simdf = pd.DataFrame({"similarity": similarity})
    combined = pd.concat([wordbag, simdf], axis=1)
    combined['final_score'] = combined["similarity"] * 0.5
    sorted_df = combined.sort_values(by='final_score', ascending=False).head(top_n)
    return sorted_df
