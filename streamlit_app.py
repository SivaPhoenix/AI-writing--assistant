import streamlit as st
from happytransformer import HappyTextToText, TTSettings
from annotated_text import annotated_text
import difflib
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events


st.set_page_config(
    page_title="AI writing Assisant",
)

st.title(" ")
#st.sidebar.success("Select a page")
checkpoint = "team-writing-assistant/t5-base-c4jfleg"

def diff_strings(a, b):
    result = []
    diff = difflib.Differ().compare(a.split(), b.split())
    replacement = ""
    
    for line in diff:
        if line.startswith("  "):
            if len(replacement) == 0:
                result.append(" ")
                result.append(line[2:])
            else:
                result.append(" ")
                result.append(("", replacement, "#eb0f0f"))
                replacement = ""
                result.append(line[2:])
        elif line.startswith("- "):
            if len(replacement) == 0:
                replacement = line[2:]
            else:
                result.append(" ")
                result.append(("", replacement, "#eb0f0f"))
                replacement = ""
        elif line.startswith("+ "):
            if len(replacement) == 0:
                result.append((line[2:], "", "#eb0f0f"))
            else:
                result.append(" ")
                result.append((line[2:], replacement, "#eb0f0f"))
                replacement = ""
                
    return result
  
#@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_happy_text(model_name):
    st.write(f" ")
    return HappyTextToText("T5", model_name)
  
happy_tt = get_happy_text(checkpoint)
args = TTSettings(num_beams=5, min_length=1)
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
st.title("AI - WRITING ASSISTANT")
st.title("Check & Improve English Grammar")
st.markdown("This writing assistant detects error🔍 and corrects ✍️ grammatical mistakes for you!")
#st.subheader("Example text: ")
st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://p1.pxfuel.com/preview/879/495/832/writing-pen-books-book.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
st.markdown(
        """<style>
        .element-container:nth-of-type(3) button {
            height: 3em;
            width:3rem;
            background:red;
        }
        </style>""",
        unsafe_allow_html=True,
        )

#col1, col2 = st.columns([1, 1])

#with col1:
    #example_1 = st.button("Speed of light is fastest then speed of sound")
#with col2:
    #example_2 = st.button("Who are the president?")
    
input_text = st.text_area('Enter your text here')
button = st.button('Submit')

def output(text):
    with st.spinner('Detecting error 🔍..'):
        text = "grammar: " + text
        result = happy_tt.generate_text(text, args=args)
        
        diff = diff_strings(text[9:], result.text)
        annotated_text(*diff)
        
        copy_button = Button(label="Copy the Result")
        copy_button.js_on_event("button_click", CustomJS(args=dict(result=result.text), code="""
            navigator.clipboard.writeText(result);
            """))
        
        streamlit_bokeh_events(
            copy_button,
            events="GET_TEXT",
            key="get_text",
            refresh_on_update=True,
            override_height=75,
            debounce_time=0)
        

if input_text:
    output(input_text)
