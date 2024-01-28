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
            'Какую модель вы хотите использовать?',
            ('Not selected', models_2x[0], models_2x[1], models_2x[2], models_2x[3],
             models_2x[4]))
    elif scale == '3x':
        model = st.selectbox(
            'Какую модель вы хотите использовать?',
            ('Not selected', models_3x[0], models_3x[1], models_3x[2], models_3x[3]))
    elif scale == '4x':
        model = st.selectbox(
            'Какую модель вы хотите использовать?',
            ('Not selected', models_4x[0], models_4x[1], models_4x[2], models_4x[3], models_4x[4]))
    elif scale == '8x':
        model = st.selectbox(
            'Какую модель вы хотите использовать?',
            ('Not selected', models_8x[0]))
    else:
        return False, False

    model_name = get_modelname(model)
    return model, model_name

st.title('Upscaler изображений с использованием технологий глубокого обучения❌☠')
st.markdown(
    'By [ZIRAKAMI](https://github.com/zirakami)', unsafe_allow_html=True)

about = """
Эта демонстрация предоставляет простой интерфейс для увеличения масштаба ваших изображений с помощью глубокого обучения (AI). 


**Note:** Если вы видите ошибку типа "Если вы видите ошибку типа "О, приложение запущено без ошибок", это связано с нехваткой процессора в streamlit.", это связано с нехваткой процессора в streamlit.
"""
st.markdown(about, unsafe_allow_html=True)

scale = st.selectbox(
    'Какой масштаб вы хотите применить к своему изображению?',
    ('Not selected', '2x', '3x', '4x', '8x'))


uploaded_file = None
model, model_name = model_selector(scale)
if model and model != 'Not selected':
    model_path = BASE_PATH + scale + '/' + model
    uploaded_file = st.file_uploader("Загрузите изображение в формате jpg", type=["jpg", "png"])


image = None
if uploaded_file is not None:
    # file_details = {"Filename":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    st.image(image, channels="BGR", caption='Ваше загруженное изображение')

    if scale == '8x' and image.shape[0] <= 128 and STREAMLIT==True:
        st.error("Ваше изображение для 8-кратного масштаба слишком велико, потому что его не хватает \
             что касается процессора, то для решения этой проблемы используйте код GitHub на вашем собственном устройстве или \
            **пожалуйста, дважды выберите другое изображение или используйте другой масштаб.**")
    elif scale == '4x' and image.shape[0] <= 200 and STREAMLIT==True:
        st.error("Ваше изображение для 4-кратного масштаба слишком велико, потому что его не хватает \
             что касается процессора, то для решения этой проблемы используйте код GitHub на вашем собственном устройстве или \
            **пожалуйста, дважды выберите другое изображение или используйте другой масштаб.**")
    elif scale == '3x' and image.shape[0] <= 540 and STREAMLIT==True:
        st.error("Ваше изображение для 3-кратного масштаба слишком велико, потому что его не хватает \
             что касается процессора, то для решения этой проблемы используйте код GitHub на вашем собственном устройстве или \
            **пожалуйста, дважды выберите другое изображение или используйте другой масштаб.**")   
    elif scale == '2x' and image.shape[0] <= 550 and STREAMLIT==True:
        st.error("Ваше изображение для 2-кратного масштаба слишком велико, потому что его не хватает \
             что касается процессора, то для решения этой проблемы используйте код GitHub на вашем собственном устройстве или \
            **пожалуйста, дважды выберите другое изображение или используйте другой масштаб.**")                              
    else:
        left_column, right_column = st.columns(2)
        pressed = left_column.button('Upscale!')

        if pressed:
            pressed = False
            st.info('Обработка ...')
            result, save_path = upscale(
                model_path, model_name, scale, image, uploaded_file.type)
            st.success('Изображение готово, вы можете скачать его прямо сейчас!')
            st.balloons()
            st.image(result, channels="RGB", caption='Ваше увеличенное изображение')
            with open(save_path, 'rb') as f:
                st.download_button('Скачать изображение', f, file_name=scale +
                                   '_' + str(datetime.now()) + '_' + save_path)
