import logging
import gradio as gr # gradio==4.42.0
import consts


def check_xxx_cookie(request: gr.Request):
    xxx = request.request.cookies.get("xxx", None)
    if not xxx:
        return '<h2 style="color: red;">无xxx此cookie</h2>', xxx
    return f'<h2 style="color: limegreen;">xxx={xxx}</h2>', xxx

def set_xxx_cookie(xxx: str, request: gr.Request):
    logging.info(f"{request.request.cookies}")
    ak = request.request.cookies.get("xxx", None)
    if not ak:
        return ""
    return f'<h2 style="color: limegreen;">xxx={xxx}</h2>'

js = '''function js() {
    window.set_cookie = function(key, value){document.cookie = key+'='+value+'; Path=/; SameSite=Strict';return [value]}
}
'''
with gr.Blocks(js=js) as demo:
    login_html = gr.HTML()
    xxx_status = gr.Textbox("", visible=False) # set invisible textbox for future read

    demo.load(check_xxx_cookie, inputs=[], outputs=[login_html, xxx_status])

    xxx = gr.Textbox(label="cookie xxx")
    add_btn = gr.Button("add cookie")
    add_btn.click(fn=set_xxx_cookie, inputs=[xxx], outputs=[login_html], js="(value) => set_cookie('xxx', value)")



demo.launch(server_name="0.0.0.0", server_port=1234, inbrowser=True)
