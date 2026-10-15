import streamlit as st
from db import init_db, save_image, save_receipt
from extract import extract_receipt
from agent import ask

init_db()
    
st.title("Food Receipt Tracker")

uploaded = st.file_uploader(
    "Upload a food receipt",
    type=["png", "jpg", "jpeg"],
)

if uploaded is not None:
    st.image(uploaded, caption="Your receipt", width=350)
    image_bytes = uploaded.getvalue()   # raw bytes: this goes to the vision LLM in 5b
    st.success(f"Uploaded {uploaded.name} ({len(image_bytes) / 1024:.0f} KB)")

    if st.button("Extract"):
        with st.spinner("Reading receipt..."):
            receipt = extract_receipt(image_bytes, uploaded.type)   # uploaded.type = "image/png" etc.
        st.json(receipt.model_dump())    # show what Gemini extracted
        
        #handles the case where the sum of items + fees does not equal the total
        items_sum = sum(i.price for i in receipt.items)
        if abs(items_sum + receipt.fees - receipt.total) > 1:
            st.warning(f"Check this receipt: items {items_sum:,.0f} + fees {receipt.fees:,.0f} ≠ total {receipt.total:,.0f}")
            
        image_path = save_image(image_bytes, uploaded.name)
        receipt_id = save_receipt(receipt.model_dump(), image_path)
        st.success(f"Saved as receipt #{receipt_id}")
        
st.divider()
st.header("Ask about your purchases")

# Keep chat history across Streamlit re-runs
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# New question
if question := st.chat_input("ask a question about your food purchases"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask(question)
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})