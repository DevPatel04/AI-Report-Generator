import streamlit as st
from groq import Groq
from datetime import datetime

# Configure Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_report(topic,report_sections, model_name):
    try:
        # Create a detailed prompt for the report
        prompt = f"""Create a detailed report on the topic: {topic}. 
        Include the following Report sections:
        {report_sections}
        Put the report in a professional style.
        Put the report sections in a professional order For example Title page , Abstract (or Executive Summary in business reports) , Introduction , Methodology , Results and Conclusion , References and use only mention report sections .
        title only include the topic name in the title.
        Follow the hierarchy format for the titles for the report.
        Follow the hierarchy format for the report sections for the report.
        heading are the report sections.
        subheading are the sub sections of a report section.
        text are the body of a report section.
        Make it informative and well-structured.
        when user specify the other requirements to you like (Abstract,Methodology,References) then don't change the format that i specified, retain original format.
        Ensure the report is written in a professional style with clear, organized content and informative text for each section.


        
        Structure the report using the following hierarchy:

        Title : Represent the report Title; use a font size heading1.
        Headings: Represent the report sections; use a font size  heading2.
        Subheadings: Represent any subdivisions within a section; use a font size heading3.
        Body Text: Include the detailed, informative content of each section; use a font size between 12-14.

        """
        completion = client.chat.completions.create(
            model=model_name,  # Groq's most capable model
            messages=[
                {"role": "system", "content": "You are a professional report writer who creates detailed, well-structured reports."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating report: {str(e)}"

def main():
    st.title("AI Report Generator")
    # st.write("Enter a topic, and I'll generate a detailed report for you!")

    model_name = st.selectbox("Select the model", ["llama-3.1-8b-instant","gemma2-9b-it","mixtral-8x7b-32768"] )

    # User input
    topic = st.text_input("What topic would you like a report on?")
    report_sections_input = st.text_input("What are other report sections you want to include in the report?")
    report_sections = ["Title of the report","Introduction","Key Points","Analysis","Conclusion"]

    if report_sections_input is not None:
        report_sections.extend(report_sections_input.split(","))
    
    if st.button("Generate Report"):
        if topic:
            with st.spinner("Generating your report..."):
                report = generate_report(topic,report_sections,model_name)
                st.markdown("### Generated Report")
                st.markdown(report)
        else:
            st.warning("Please enter a topic first!")

    # Add some helpful information
    with st.sidebar:
        st.markdown("### How to use")
        st.markdown("""
        1. Enter any topic you want to learn about
        2. Select the model you want to use
        3. select what you want to include in the report
        3. Click 'Generate Report'
        4. Wait a few seconds for your detailed report
        
        The report will include by default:
        - Title of the report
        - Introduction
        - Key Points
        - Analysis
        - Conclusion
        """)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This report generator uses the Groq's multiple models, 
        known for its fast and high-quality text generation.
        """)

if __name__ == "__main__":
    main()
