# This script is the main logic for the AI Blog Generator.

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

def generate_blog_post(topic, length, tone, language, keywords, context):
    keywords = ", ".join(keywords)
    
    template = """
    Write a {length} blog post in {language} on the following topic:
    
    "{topic}"
    
    Make it {tone}, engaging, and SEO-friendly. 
    The blog should explore and refer to {context} if available for the most relevant informtion.
    f"Research the latest about: {keywords}\n\n if avaliable"
    Instructions:
    The blog should be properly and beautifully formatted using markdown.
    The blog title should be SEO optimized.
    The blog title, should be crafted with the topic in mind and should be catchy and engaging. But not overly expressive.
    Each sub-section should have at least 3 paragraphs.
    Each section should have at least three subsections.
    Sub-section headings should be clearly marked.
    Clearly indicate the title, headings, and sub-headings using markdown.
    Each section should cover the specific aspects as outlined.
    For each section, generate detailed content that aligns with the provided subtopics. Ensure that the content is informative and covers the key points.
    Ensure that the content flows logically from one section to another, maintaining coherence and readability.
    Where applicable, include examples, case studies, or insights that can provide a deeper understanding of the topic.
    Always include discussions on ethical considerations, especially in sections dealing with data privacy, bias, and responsible use. Only add this where it is applicable.
    In the final section, provide a forward-looking perspective on the topic and a conclusion.
    Please ensure proper and standard markdown formatting always.
    Make the blog post sound as human and as engaging as possible, add real world examples and make it as informative as possible.
    You are a professional blog post writer and SEO expert.


    Blog: 
    """
    filled_template = PromptTemplate.from_template(template)
    
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.7)
    chain = filled_template | llm | StrOutputParser()
    
    return chain.invoke({
        "topic": topic,
        "length": length,
        "tone": tone,
        "language": language,
        "keywords": keywords,
        "context": context
    })

