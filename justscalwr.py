import cv2
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from datetime import datetime

############################# start - variables ################################
sr = cv2.dnn_superres.DnnSuperResImpl_create()

models_2x = ['EDSR_x2.pb', 'ESPCN_x2.pb',
             'FSRCNN-small_x2.pb', 'FSRCNN_x2.pb', 'LapSRN_x2.pb']
models_3x = ['EDSR_x3.pb', 'ESPCN_x3.pb', 'FSRCNN-small_x3.pb', 'FSRCNN_x3.pb']
models_4x = ['EDSR_x4.pb', 'ESPCN_x4.pb',
             'FSRCNN-small_x4.pb', 'FSRCNN_x4.pb', 'LapSRN_x4.pb']
models_8x = ['LapSRN_x8.pb']

BASE_PATH = 'models/'
STREAMLIT = True # измените на False, если вы работаете на своем компьютере.

def upscale(model_path: str, model_name: str, scale: str, img, img_type: str):
    scale = int(scale.split('x')[0])
    sr.readModel(model_path)
    sr.setModel(model_name, scale)
    result = sr.upsample(img)
    img_type = img_type.split('/')[1]
    save_path = f'result.{img_type}'
    plt.imsave(save_path, result[:, :, ::-1])
    return result[:, :, ::-1], save_path


def get_modelname(selected_model: str) -> str:
    if 'EDSR' in selected_model:
        return 'edsr'
    elif 'LapSRN' in selected_model:
        return 'lapsrn'
    elif 'ESPCN' in selected_model:
        return 'espcn'
    elif 'FSRCNN' in selected_model:
        return 'fsrcnn'
    elif 'LapSRN' in selected_model:
        return 'lapsrn'


def model_selector(scale: str) -> str:
    model = ''
    if scale == '2x':
        model = st.selectbox(
            'Which model do you want to use?',
            ('Not selected', models_2x[0], models_2x[1], models_2x[2], models_2x[3],
             models_2x[4]))
    elif scale == '3x':
        model = st.selectbox(
            'Which model do you want to use?',
            ('Not selected', models_3x[0], models_3x[1], models_3x[2], models_3x[3]))
    elif scale == '4x':
        model = st.selectbox(
            'Which model do you want to use?',
            ('Not selected', models_4x[0], models_4x[1], models_4x[2], models_4x[3], models_4x[4]))
    elif scale == '8x':
        model = st.selectbox(
            'Which model do you want to use?',
            ('Not selected', models_8x[0]))
    else:
        return False, False

    model_name = get_modelname(model)
    return model, model_name


############################# start - Streamlit ################################

st.title('Free Image Upscaler Using Deep Learning 📸')
st.markdown(
    'By [Mehrdad Mohammadian](https://mehrdad-dev.github.io)', unsafe_allow_html=True)

about = """
This demo provides a simple interface to upscale your images using deep learning (AI). 
In streamlit, there is a shortage in terms of CPU, to solve this issue use codes in 
GitHub on your own device or use another scale twice.


**Note:** If you see a error like "Oh, no - Error running app", it is because CPU shortage in streamlit.
"""
st.markdown(about, unsafe_allow_html=True)

scale = st.selectbox(
    'Which scale do you want to apply to your image?',
    ('Not selected', '2x', '3x', '4x', '8x'))


uploaded_file = None
model, model_name = model_selector(scale)
if model and model != 'Not selected':
    model_path = BASE_PATH + scale + '/' + model
    uploaded_file = st.file_uploader("Upload a jpg image", type=["jpg", "png"])


image = None
if uploaded_file is not None:
    # file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    st.image(image, channels="BGR", caption='Your uploaded image')

    if scale == '8x' and image.shape[0] <= 128 and STREAMLIT==True:
        st.error("Your image for the 8x scale is too big, because there is a shortage \
             in terms of CPU, to solve this issue use GitHub codes on your own device or \
            **plseae select another image or use another scale twice.**")
    elif scale == '4x' and image.shape[0] <= 200 and STREAMLIT==True:
        st.error("Your image for the 4x scale is too big, because there is a shortage \
             in terms of CPU, to solve this issue use GitHub codes on your own device or \
            **plseae select another image or use another scale twice.**")  
    elif scale == '3x' and image.shape[0] <= 540 and STREAMLIT==True:
        st.error("Your image for the 3x scale is too big, because there is a shortage \
             in terms of CPU, to solve this issue use GitHub codes on your own device or \
            **plseae select another image or use another scale twice.**")    
    elif scale == '2x' and image.shape[0] <= 550 and STREAMLIT==True:
        st.error("Your image for the 3x scale is too big, because there is a shortage \
             in terms of CPU, to solve this issue use GitHub codes on your own device or \
            **plseae select another image or use another scale twice.**")                                       
    else:
        left_column, right_column = st.columns(2)
        pressed = left_column.button('Upscale!')

        if pressed:
            pressed = False
            st.info('Processing ...')
            result, save_path = upscale(
                model_path, model_name, scale, image, uploaded_file.type)
            st.success('Image is ready, you can download it now!')
            st.balloons()
            st.image(result, channels="RGB", caption='Your upscaled image')
            with open(save_path, 'rb') as f:
                st.download_button('Download the image', f, file_name=scale +
                                   '_' + str(datetime.now()) + '_' + save_path)
