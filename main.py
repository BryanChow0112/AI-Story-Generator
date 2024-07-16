# import statements
import streamlit as st
from openai import OpenAI

# Statics
api_key = st.secrets['OPENAI_API_KEY'] 

client = OpenAI(api_key=api_key)

# Methods
def generate_story(prompt, client):
  story_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": """You are a bestseller story writer. You will take prompt from user and generate a 100 words short story for adults aged 20-30. Include funny elements and interesting storyline"""},  # system prompt
      {"role": "user", "content": f"{prompt}"}  # user prompt
    ],
    max_tokens = 400,
    temperature = 0.8
  )

  story = story_response.choices[0].message.content
  return story


def refine_story(story): 
  design_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Based on the story given, you will design a detailed image prompt for the cover of this story. The image prompt should include the theme of the story with relevant colour, suitable for adults. The output should be within 100 characters."},  # system prompt
      {"role": "user", "content": f"{story}"}  # user prompt
    ],
    max_tokens = 400,
    temperature = 0.8
  )

  refined_story = design_response.choices[0].message.content
  return refined_story


def generate_image_url(refined_story): 
  cover_response = client.images.generate(
    model="dall-e-2",
    prompt=f"{refined_story}",
    size="256x256",
    quality="standard",
    n=1,
  )

  image_url = cover_response.data[0].url
  return image_url

# prompt = 'Write an inspiring story about a computer science student studying in Monash who eventually became the richest guy in the world. Include funny elements and interesting storyline like anime style.'


# Streamlit interface
st.title("📖 AI Story Generator")
st.write("""
Welcome to the AI Story Generator! This tool uses OpenAI's powerful models to help you create short stories with interesting and funny elements. Just enter some keywords, and we'll generate a story and a cover image for you.
""")

st.markdown("## Step 1: Enter Keywords")
st.write("Provide some keywords to help us generate a story for you. The keywords should reflect the main themes or elements you want in the story.")

with st.form('story_form'):
    msg = st.text_input(label='Keywords', placeholder='e.g., computer science student, adventure, funny')
    submitted = st.form_submit_button('Submit')

    if submitted:
        with st.spinner('Generating your story...'):
            # Generate story from prompt
            story = generate_story(msg, client)

        st.markdown("## Step 2: Generated Story")
        st.write("Here is the story we generated based on your keywords:")
        st.write(story)

        with st.spinner('Refining story for cover design...'):
            # Refine story for cover design
            refined_story = refine_story(story)

        st.markdown("## Step 3: Cover Image")
        st.write("We have also created a cover image for your story:")

        with st.spinner('Generating cover image...'):
            # Generate image URL based on refined story
            image_url = generate_image_url(refined_story)

        st.image(image_url)
        st.write(refined_story)

        st.markdown("## Step 4: Rate the Story")
        rating = st.slider('Rate the story:', 1, 5)
        st.write('Your rating:', rating)

st.markdown("---")
st.write("Thank you for using the AI Story Generator! We hope you enjoyed creating your story.")