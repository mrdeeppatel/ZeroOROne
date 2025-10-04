from flask import Flask, render_template
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# -------------------------
# Step 1: Connect to MongoDB Atlas
# -------------------------
# Replace <username>, <password>, <cluster_url>, <dbname>, <collection> with your info
client = MongoClient("mongodb+srv://100xDev:i0XUrTfJXBtKTdk4@cluster0.9uh7q.mongodb.net/")
db = client["ZeroOrOne"]
collection = db["data"]

# -------------------------
# Step 2: Fetch data and convert to DataFrame
# -------------------------
data = list(collection.find())  # Fetch all documents
df = pd.DataFrame(data)

# -------------------------
# Step 3: Generate plots
# -------------------------
# Make sure the column exists: Predicted_Risk_Label_5
if 'Predicted_Risk_Label_5' not in df.columns:
    df['Predicted_Risk_Label_5'] = df['Risk_Label_5']  # or compute if necessary

# 1️⃣ Bar chart
bar_fig = px.bar(df['Predicted_Risk_Label_5'].value_counts().reindex(
    ["Very Low","Low","Medium","High","Very High"], fill_value=0),
    labels={'index':'Risk Level','value':'Number of Students'},
    title='Number of Students per Risk Level'
)
bar_plot = pio.to_html(bar_fig, full_html=False)

# 2️⃣ Pie chart
pie_fig = px.pie(df, names='Predicted_Risk_Label_5', title='Percentage of Students per Risk Level',
                 color='Predicted_Risk_Label_5',
                 category_orders={'Predicted_Risk_Label_5': ["Very Low","Low","Medium","High","Very High"]})
pie_plot = pio.to_html(pie_fig, full_html=False)

# 3️⃣ Box plot Attendance%
box_fig = px.box(df, x='Predicted_Risk_Label_5', y='Attendance%',
                 category_orders={'Predicted_Risk_Label_5': ["Very Low","Low","Medium","High","Very High"]},
                 title='Attendance% Distribution by Risk Level')
box_plot = pio.to_html(box_fig, full_html=False)

@app.route("/")
def home():
    return render_template("index.html", bar_plot=bar_plot, pie_plot=pie_plot, box_plot=box_plot)

if __name__ == "__main__":
    app.run(debug=True)
