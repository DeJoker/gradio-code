import logging
import gradio as gr # gradio==4.42.0
from gradio_modal import Modal

import user_db


def set_xxx_cookie(xxx: str, request: gr.Request):
    logging.info(f"{request.request.cookies}")
    ak = request.request.cookies.get("xxx", None)
    if not ak:
        return ""
    return f'<h2 style="color: limegreen;">xxx={xxx}</h2>'

js = '''function js() {
    window.set_cookie = function(key, value) { document.cookie = key+'='+value+'; Path=/; SameSite=Strict'; return [value]; };
    window.unset_cookie = function(key) { document.cookie = key + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Strict'; };
}
'''
with gr.Blocks(js=js) as demo:
    login_html = gr.HTML()
    user_status, ak_status = gr.Textbox("", visible=False), gr.Textbox("", visible=False)

    demo.load(user_db.check_cookie, inputs=[], outputs=[login_html, user_status, ak_status])


    with Modal(visible=False, allow_user_close=False) as login_box:
        gr.HTML(f"<h1>平台登录</h1>")
        user_tb = gr.Textbox(label="用户名", )
        passwd_tb = gr.Textbox(label="密码", type="password")
        confirm_btn = gr.Button("确定", variant="primary", elem_classes=["tool"])
        cancel_btn = gr.Button("取消", variant="secondary", elem_classes=["tool"])
        
        confirm_btn.click(user_db.check_login,
                        inputs=[user_tb, passwd_tb], outputs=[login_html, user_status, ak_status],
                    ).then(
                        lambda _:Modal(visible=False), inputs=[ak_status], outputs=[login_box],
                        js="(value) => set_cookie('ak', value)"
                    ) # input不能是state才会调用js
        cancel_btn.click(lambda:Modal(visible=False), inputs=[], outputs=[login_box])
    login_btn = gr.Button(value="登录", variant="primary", elem_classes=["tool"])
    login_btn.click(lambda: Modal(visible=True), inputs=[], outputs=[login_box])

    reset_btn = gr.Button("logout")
    def reset_cookie():
        return '<h2>未登录</h2>'
    reset_btn.click(fn=reset_cookie, inputs=[], outputs=[login_html], js="(value) => unset_cookie('ak')")



demo.launch(server_name="0.0.0.0", server_port=1234, inbrowser=True)
