import streamlit as st
import pandas as pd
import os
import json


def read_json(input_json_path):
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File not found: {input_json_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {input_json_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# 设置固定的CSV文件和图片路径
csv_path = r"result_hpto1.1_hpto1.3_cogvlm2.csv"
rating_path = r"result_hpto1.1_hpto1.2_cogvlm2.csv"
images_path = "images"

# 初始化页面配置
st.set_page_config(page_title='HPT Evaluation System', layout='wide')
st.title("HPT Evaluation System")

# 读取CSV文件
data = pd.read_csv(csv_path, encoding='utf-8')
rating = pd.read_csv(rating_path, encoding='utf-8')

# 初始化状态
if "index" not in st.session_state:
    st.session_state.index = 0

# 获取当前记录的索引
index = st.session_state.index

# 设置布局：左侧放图片和问题，右侧放响应，底部放评分
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Current Record")
    st.write(f"### Record {index + 1}/{len(data)}")

    st.subheader("Image")
    image_name = data.loc[index, data.columns[0]]
    image_path = os.path.join(images_path, image_name)
    if os.path.exists(image_path):
        st.image(image_path)
    else:
        st.write(f"Image not found: {image_path}")

    st.subheader("Question")
    st.write(data.loc[index, 'question'])

with col2:
    st.subheader("Responses")

    with st.expander("hpto1.1"):
        st.write(data.loc[index, 'hpto1.1'])

    with st.expander("hpto1.3"):
        st.write(data.loc[index, 'hpto1.3'])

    with st.expander("cogvlm2"):
        st.write(data.loc[index, 'cogvlm2'])

    # with st.expander("glm4v"):
    #     st.write(data.loc[index, 'glm4v'])

# 添加题型选择
# st.subheader("Select Question Type")
# question_type = st.radio("Question Type:", ["subjective", "objective"], key="question_type")

#初始化值为上一次评分的值
hpto1_1_default = int(rating.loc[index, 'hpto1.1_rating'])
cogvlm2_default = int(rating.loc[index, 'cogvlm2_rating'])

# 根据问题类型显示相应的输入控件
if True:
# if question_type == 'subjective':
    hpto1_1_rating = st.radio("hpto1.1 Rating:", [1, 2, 3, 4, 5], index=hpto1_1_default-1, key="hpto1.1_rating",
                              horizontal=True)
    hpto1_3_rating = st.radio("hpto1.3 Rating:", [1, 2, 3, 4, 5], key="hpto1.3_rating", horizontal=True)
    cogvlm2_rating = st.radio("cogvlm2 Rating:", [1, 2, 3, 4, 5], index=cogvlm2_default-1, key="cogvlm2_rating",
                              horizontal=True)
    # glm4v_rating = st.radio("glm4v Rating:", [1, 2, 3, 4, 5], key="glm4v_rating", horizontal=True)
        # glm4v_rating = st.radio("glm4v Rating:", [1, 2, 3, 4, 5], key="glm4v_rating", horizontal=True)

else:
    st.subheader("Please evaluate the responses (True/False)")
    hpto1_1_rating = st.radio("hpto1.1 Correct:", ["True", "False"], key="hpto1_1_rating", horizontal=True)
    cogvlm2_rating = st.radio("cogvlm2 Correct:", ["True", "False"], key="cogvlm2_rating", horizontal=True)
    glm4v_rating = st.radio("glm4v Correct:", ["True", "False"], key="glm4v_rating", horizontal=True)


# 添加备注部分
st.subheader("Add a note")
note = st.text_area("Note", key="note")

if st.button("Save Rating and Note"):
    # data.loc[index, "question_type"] = question_type
    data.loc[index, "hpto1.1_rating"] = hpto1_1_rating
    data.loc[index, "hpto1.3_rating"] = hpto1_3_rating
    data.loc[index, "cogvlm2_rating"] = cogvlm2_rating
    # data.loc[index, "glm4v_rating"] = glm4v_rating

    data.loc[index, "note"] = note
    data.to_csv(csv_path, index=False)
    st.session_state.index += 1
    if st.session_state.index >= len(data):
        st.write("### Evaluation completed!")
    else:
        #st.experimental_rerun()

# 添加导航按钮和输入框
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 2])
with nav_col1:
    if st.button("Previous Data"):
        if st.session_state.index > 0:
            st.session_state.index -= 1
            #st.experimental_rerun()

with nav_col2:
    if st.button("Next Data"):
        if st.session_state.index < len(data) - 1:
            st.session_state.index += 1
            #st.experimental_rerun()

with nav_col3:
    jump_to_index = st.number_input("Go to record number", min_value=1, max_value=len(data), value=index + 1)
    if st.button("Go"):
        st.session_state.index = jump_to_index - 1
        #st.experimental_rerun()
