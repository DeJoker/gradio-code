from functools import partial
import logging
import time
import gradio as gr # gradio==4.42.0
from gradio_modal import Modal



push_ok_button = None
def confirm_value(x: bool):
    global push_ok_button
    push_ok_button = x
    return Modal(visible=False), x

def wait_confirm():
    global push_ok_button
    while push_ok_button is None:
        time.sleep(0.1)
    return push_ok_button

def clear_confirm():
    global push_ok_button
    push_ok_button = None
    return None

def confirm_wrapper(func, confirm: bool, *args, **kwargs):
    if not confirm:
        logging.info(f"cancel {func} args={repr(args)} kwargs={repr(kwargs)}")
        return
    logging.info(f"confirm {func} args={repr(args)} kwargs={repr(kwargs)}")
    res = func(*args, **kwargs)
    return res

countries = [
    "Algeria", "Argentina", "Australia", "Brazil", "Canada", "China", "Democratic Republic of the Congo", "Greenland (Denmark)", "India", "Kazakhstan", "Mexico", "Mongolia", "Peru", "Russia", "Saudi Arabia", "Sudan", "United States"
]
def remove_country(country: str):
    global countries
    countries.remove(country)
    return " ".join(countries)

with gr.Blocks() as demo:
    user_status, ak_status = gr.Textbox("", visible=False), gr.Textbox("", visible=False)
    confirm_info, confirm_status = gr.State(""), gr.State(None)

    with Modal(visible=False, allow_user_close=False) as confirm_box:
        confirm_html = gr.HTML(f"<h1>{confirm_info.value}</h1>")
        confirm_btn = gr.Button("confirm", variant="primary", elem_classes=["tool"])
        cancel_btn = gr.Button("cancel", variant="secondary", elem_classes=["tool"])
        confirm_btn.click(partial(confirm_value, True), inputs=[], outputs=[confirm_box, confirm_status])
        cancel_btn.click(partial(confirm_value, False), inputs=[], outputs=[confirm_box, confirm_status])

    instance_dr = gr.Dropdown(label="instance", choices=countries, value=countries[0], interactive=True,)
    exsit_tb = gr.Textbox(label="instance", value=" ".join(countries), interactive=True,)
    remove_btn = gr.Button(value="remove this instance", variant="stop", elem_classes=["tool"])

    def show_remove_confirm_box(instance=""):
        return Modal(visible=True), f'<h1 style="color: red;">are you sure to remove {instance} </h1>'
    
    remove_btn.click(fn=partial(show_remove_confirm_box),
        inputs=[instance_dr], outputs=[confirm_box, confirm_html]
    ).success(
        fn=wait_confirm, inputs=[], outputs=[confirm_status]
    ).then(
        partial(confirm_wrapper, remove_country), inputs=[confirm_status, instance_dr], outputs=[exsit_tb]
    ).then(
        fn=clear_confirm, inputs=[], outputs=[]
    )

demo.launch(server_name="0.0.0.0", server_port=1234, inbrowser=True)

