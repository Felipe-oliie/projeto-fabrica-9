import streamlit as st
import pandas as pd

if "items" not in st.session_state:
    st.session_state.items = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

def add_item(nome, quantidade, categoria, prioridade, comprado):
    item = {
        "id": st.session_state.next_id,
        "nome": nome,
        "quantidade": quantidade,
        "categoria": categoria,
        "prioridade": prioridade,
        "comprado": comprado
    }
    st.session_state.items.append(item)
    st.session_state.next_id += 1

def update_item(item_id, nome=None, quantidade=None, categoria=None, prioridade=None, comprado=None):
    for item in st.session_state.items:
        if item["id"] == item_id:
            if nome: item["nome"] = nome
            if quantidade: item["quantidade"] = quantidade
            if categoria is not None: item["categoria"] = categoria
            if prioridade is not None: item["prioridade"] = prioridade
            if comprado is not None: item["comprado"] = comprado
            return True
    return False

def delete_item(item_id):
    st.session_state.items = [i for i in st.session_state.items if i["id"] != item_id]

st.title("Lista de Compras")

st.header("Adicionar novo item")
with st.form("add_form"):
    nome = st.text_input("Nome do item")
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    categoria = st.text_input("Categoria (opcional)")
    prioridade = st.selectbox("Prioridade", ["baixa", "media", "alta"], index=1)
    comprado = st.checkbox("Comprado", value=False)
    submitted = st.form_submit_button("Adicionar")
    if submitted:
        if not nome or quantidade < 1:
            st.error("Nome e quantidade >= 1 são obrigatórios")
        else:
            add_item(nome, quantidade, categoria, prioridade, comprado)
            st.success(f"Item '{nome}' adicionado!")

st.header("Itens na lista")
if st.session_state.items:
    df = pd.DataFrame(st.session_state.items)
    st.dataframe(df)

    st.header("Editar / Deletar item")
    selected_id = st.selectbox("Selecione o ID do item", df["id"])
    selected_item = next((i for i in st.session_state.items if i["id"] == selected_id), None)

    if selected_item:
        with st.form("edit_form"):
            new_nome = st.text_input("Nome", value=selected_item["nome"])
            new_quantidade = st.number_input("Quantidade", min_value=1, step=1, value=selected_item["quantidade"])
            new_categoria = st.text_input("Categoria", value=selected_item["categoria"])
            new_prioridade = st.selectbox("Prioridade", ["baixa", "media", "alta"], index=["baixa","media","alta"].index(selected_item["prioridade"]))
            new_comprado = st.checkbox("Comprado", value=selected_item["comprado"])
            update_submitted = st.form_submit_button("Atualizar")
            delete_submitted = st.form_submit_button("Deletar")

            if update_submitted:
                update_item(selected_id, new_nome, new_quantidade, new_categoria, new_prioridade, new_comprado)
                st.success("Item atualizado!")
            if delete_submitted:
                delete_item(selected_id)
                st.warning("Item deletado!")
else:
    st.info("Nenhum item cadastrado ainda.")
