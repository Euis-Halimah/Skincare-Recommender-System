import gradio as gr
import pandas as pd
from joblib import load
from model_recommender import SkincareRecommender

# Load model & data
model = load("rekomendasi_model.pkl")
df = pd.read_excel("data_cleaned.xlsx")
subcat_list = sorted(df['sub-category'].dropna().unique().tolist())

# Load key active ingredients dari CSV
key_ingredients_df = pd.read_csv("key_active_ingredients.csv")
key_ingredients_list = sorted(key_ingredients_df['Ingredient_Name'].dropna().unique().tolist())

# Fungsi rekomendasi
def recommend(input_benefit, input_ingredients, input_subcat, jumlah):
    return model.recommend(input_benefit, input_ingredients, input_subcat, jumlah)

# Custom CSS
custom_css = """
/* Semua teks termasuk label dan deskripsi jadi hitam */
.gr-text, .gr-label, .block-label, label, span, p, h2, h3, h4 {
    color: #000000 !important;
}

/* Judul besar */
.center-text {
    text-align: center;
}

.title-text {
    color: #6A5ACD;
    font-weight: bold;
    font-size: 28px;
    margin-bottom: 10px;
}

.desc-text {
    color: #000000;
    font-size: 18px;
    margin-bottom: 20px;
}

/* Field input */
input, textarea, select, .gr-textbox textarea, .gr-dropdown select, input[type=range] {
    background-color: #E6E6FA !important;
    border: 1.5px solid #6A5ACD !important;
    border-radius: 8px !important;
    color: #000000 !important;
}

/* Slider thumb + angka */
input[type=range] {
    accent-color: #6A5ACD !important;
}
.range-min, .range-max {
    color: #000000 !important;
}

/* Tombol submit */
button, .gr-button {
    background-color: #7B68EE !important;
    color: white !important;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    border: none !important;
}
button:hover, .gr-button:hover {
    background-color: #6A5ACD !important;
}

/* Kotak input form */
#form-container {
    border: 2px solid #6A5ACD;
    border-radius: 12px;
    padding: 20px;
    background-color: #F5F5FF;
}

/* Label output */
.gr-dataframe-label {
    color: #000000 !important;
    font-weight: bold;
}

/* Output tabel */
.gr-dataframe, .gr-dataframe-container {
    background-color: #E6E6FA !important;
    border: 0.8px solid #6A5ACD !important;
    border-radius: 5px !important;
    color: #000000 !important;
    font-weight: normal !important;
}

/* Header tabel */
.gr-dataframe thead {
    background-color: #D8BFD8 !important;
    color: #000000 !important;
    font-weight: bold !important;
}

/* Body tabel */
.gr-dataframe tbody td {
    background-color: #F5F5FF !important;
    font-weight: normal !important;
}

/* Scroll bar */
.gr-dataframe-container::-webkit-scrollbar {
    height: 6px;
}
.gr-dataframe-container::-webkit-scrollbar-thumb {
    background: #6A5ACD;
    border-radius: 5px;
}
"""

# UI
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("<div class='center-text title-text'>🌸 Sistem Rekomendasi Skincare 🌸</div>")
    gr.Markdown("<div class='center-text desc-text'>Masukkan kriteria skincare yang kamu inginkan, lalu dapatkan rekomendasinya!</div>")

    with gr.Column(elem_classes="centered-form"):
        with gr.Group(elem_id="form-container"):
            input_benefit = gr.Textbox(label="Masukkan Benefit (contoh: Mencerahkan kulit dan Menyamarkan Noda Hitam)")
            input_ingredients = gr.Dropdown(choices=key_ingredients_list, label="Pilih Key Ingredients")  # <--- diubah jadi dropdown
            input_subcat = gr.Dropdown(choices=subcat_list, label="Pilih Sub-kategori")
            jumlah = gr.Slider(1, 10, value=5, step=1, label="Jumlah Rekomendasi")
            submit_btn = gr.Button("Submit")

    output = gr.Dataframe(label="Hasil Rekomendasi")

    submit_btn.click(fn=recommend, inputs=[input_benefit, input_ingredients, input_subcat, jumlah], outputs=output)

# Run
if __name__ == "__main__":
    demo.launch()
