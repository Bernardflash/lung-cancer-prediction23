
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class AnalyticsDashboard:
    def __init__(self, data_path):
        self.data_path = data_path
        
    def load_data(self):
        try:
            return pd.read_csv(self.data_path)
        except Exception:
            return pd.DataFrame()

    def get_risk_distribution(self, df):
        if df.empty or 'Risk' not in df.columns:
            return None
        
        # Count risk levels
        risk_counts = df['Risk'].value_counts().reset_index()
        risk_counts.columns = ['Risk Level', 'Count']
        
        fig = px.pie(
            risk_counts, 
            values='Count', 
            names='Risk Level',
            title='Patient Risk Distribution',
            color='Risk Level',
            color_discrete_map={'High': '#ef4444', 'Low': '#22c55e'},
            hole=0.4
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#f1f5f9')
        return fig

    def get_age_distribution(self, df):
        if df.empty or 'AGE' not in df.columns:
            return None
            
        fig = px.histogram(
            df, 
            x='AGE', 
            nbins=20,
            title='Patient Age Demographics',
            color_discrete_sequence=['#3b82f6']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#f1f5f9',
            xaxis_title="Age",
            yaxis_title="Count"
        )
        return fig
        
    def get_gender_risk_comparison(self, df):
        if df.empty or 'GENDER' not in df.columns or 'Risk' not in df.columns:
            return None
            
        # 1 = Male, 0 = Female
        df_plot = df.copy()
        df_plot['Gender Label'] = df_plot['GENDER'].map({1: 'Male', 0: 'Female'})
        
        fig = px.histogram(
            df_plot,
            x='Gender Label',
            color='Risk',
            barmode='group',
            title='Risk Assessment by Gender',
            color_discrete_map={'High': '#ef4444', 'Low': '#22c55e'}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color='#f1f5f9'
        )
        return fig

    def get_key_stats(self, df):
        if df.empty:
            return 0, 0, 0.0
            
        total_patients = len(df)
        high_risk = len(df[df['Risk'] == 'High']) if 'Risk' in df.columns else 0
        
        avg_prob = 0.0
        if 'Probability' in df.columns:
            # Ensure it's numeric, coerce errors to NaN
            probs = pd.to_numeric(df['Probability'], errors='coerce')
            avg_prob = probs.mean()
        
        return total_patients, high_risk, avg_prob

    def get_risk_cluster_nebula(self, df):
        if df.empty or 'Risk' not in df.columns or 'Probability' not in df.columns:
            return None
            
        # Simulate a 3rd dimension: Symptom Intensity
        # Sum of clinical binary features (assuming they are mapped to 0/1)
        clinical_cols = [
            'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 
            'CHRONIC DISEASE', 'FATIGUE ', 'ALLERGY ', 'WHEEZING', 
            'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH', 
            'SWALLOWING DIFFICULTY', 'CHEST PAIN'
        ]
        
        # Ensure only columns that exist are used
        available_cols = [c for c in clinical_cols if c in df.columns]
        df_plot = df.copy()
        
        # Map labels to numbers for calculation if they are strings
        for col in available_cols:
            if df_plot[col].dtype == object:
                df_plot[col] = df_plot[col].map({'Yes': 1, 'No': 0, 'Male': 1, 'Female': 0}).fillna(0)
        
        df_plot['Symptom Index'] = df_plot[available_cols].sum(axis=1)
        
        # Create 3D Scatter with Nebula theme
        fig = px.scatter_3d(
            df_plot,
            x='AGE',
            y='Probability',
            z='Symptom Index',
            color='Risk',
            hover_name='Patient Name',
            title='Risk Cluster Nebula: Patient Data Universe',
            color_discrete_map={'High': '#ef4444', 'Low': '#22c55e'},
            opacity=0.7,
            template='plotly_dark'
        )
        
        fig.update_traces(
            marker={
                'size': 8, 
                'color': df_plot['Probability'], 
                'colorscale': 'Viridis', 
                'opacity': 0.8
            }, 
            selector={'mode': 'markers'}
        )
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Age',
                yaxis_title='Risk Probability',
                zaxis_title='Symptom Intensity',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(13, 25, 48, 0.8)', # Dark nebula-like blue
            font_color='#f1f5f9',
            margin=dict(l=0, r=0, b=0, t=40)
        )
        return fig
