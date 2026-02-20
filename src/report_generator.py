
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
from datetime import datetime
import os

class MedicalReportGenerator:
    def __init__(self, output_path="report.pdf"):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _create_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='Header1',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#0d47a1'),
            spaceAfter=12
        ))
        self.styles.add(ParagraphStyle(
            name='Header2',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1565c0'),
            spaceBefore=12,
            spaceAfter=6
        ))
        self.styles.add(ParagraphStyle(
            name='NormalText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            leading=14
        ))
        self.styles.add(ParagraphStyle(
            name='AlertText',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.red,
            fontName='Helvetica-Bold'
        ))

    def generate_report(self, patient_data, prediction_result):
        doc = SimpleDocTemplate(self.output_path, pagesize=letter)
        elements = []

        # 1. Hospital Header
        elements.append(Paragraph("OncoPredict Medical Center", self.styles['Header1']))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", self.styles['NormalText']))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph("CONFIDENTIAL MEDICAL REPORT", self.styles['Header2']))
        elements.append(Spacer(1, 0.1 * inch))

        # 2. Patient Information Table
        data = [
            ["Patient Name:", patient_data.get('Patient Name', 'N/A')],
            ["Patient ID:", patient_data.get('Patient ID', 'N/A')],
            ["Phone Number:", patient_data.get('Phone', 'N/A')],
            ["Location:", patient_data.get('Location', 'N/A')],
            ["Age:", str(patient_data.get('AGE', 'N/A'))],
            ["Gender:", "Male" if patient_data.get('GENDER') == 1 else "Female"]
        ]
        
        t = Table(data, colWidths=[1.5*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.3 * inch))

        # 3. Clinical Parameters
        elements.append(Paragraph("Clinical Assessment Parameters", self.styles['Header2']))
        
        # Format parameters beautifully
        params = []
        exclude_keys = ['Patient Name', 'Patient ID', 'AGE', 'GENDER']
        for key, value in patient_data.items():
            if key not in exclude_keys:
                display_key = key.replace('_', ' ').title()
                display_val = "Yes" if value == 1 else "No"
                params.append([display_key, display_val])
        
        # Split into two columns for better layout
        mid = len(params) // 2
        col1_data = params[:mid]
        col2_data = params[mid:]
        
        # If uneven, add empty placeholder
        if len(col2_data) < len(col1_data):
            col2_data.append(["", ""])

        combined_data = []
        for i in range(len(col1_data)):
            combined_data.append(col1_data[i] + col2_data[i])

        t2 = Table(combined_data, colWidths=[2*inch, 0.8*inch, 2*inch, 0.8*inch])
        t2.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTSIZE', (0, 0), (-1, -1), 9)
        ]))
        elements.append(t2)
        elements.append(Spacer(1, 0.3 * inch))

        # 4. Assessment Results
        elements.append(Paragraph("Risk Assessment Analysis", self.styles['Header2']))
        
        risk_level = "HIGH RISK" if prediction_result['prediction'] == 1 else "LOW RISK"
        risk_color = colors.red if prediction_result['prediction'] == 1 else colors.green
        prob_percent = f"{prediction_result['probability']:.1%}"
        
        res_data = [
            ["Risk Classification:", risk_level],
            ["Malignancy Probability:", prob_percent],
            ["Model Confidence:", "High" if prediction_result['probability'] > 0.8 or prediction_result['probability'] < 0.2 else "Moderate"]
        ]
        
        t3 = Table(res_data, colWidths=[2*inch, 3*inch])
        t3.setStyle(TableStyle([
            ('TEXTCOLOR', (1, 0), (1, 0), risk_color),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(t3)
        elements.append(Spacer(1, 0.2 * inch))

        # 5. Recommendations
        if prediction_result['prediction'] == 1:
            rec_text = "URGENT ACTION REQUIRED: The patient shows clinical signs consistent with high risk for lung cancer. Immediate referral to an oncologist for further diagnostic imaging (CT/PET) and biopsy is strongly recommended."
            elements.append(Paragraph(rec_text, self.styles['AlertText']))
        else:
            rec_text = "Standard screening protocol recommended. No immediate high-risk indicators found. Advise patient on smoking cessation and healthy lifestyle choices."
            elements.append(Paragraph(rec_text, self.styles['NormalText']))
            
        elements.append(Spacer(1, 0.5 * inch))
        
        # 6. Footer Disclaimer
        disclaimer = "DISCLAIMER: This report is generated by an AI decision support tool. It is not a definitive diagnosis. " \
                     "All results must be verified by a qualified medical professional."
        elements.append(Paragraph(disclaimer, ParagraphStyle('Disclaimer', fontSize=8, textColor=colors.grey)))

        # Build PDF
        doc.build(elements)
        return self.output_path
