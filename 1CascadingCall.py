
import gradio as gr # gradio==4.42.0
import consts

with gr.Blocks(title="字符串拼接", css=consts.css) as demo:
    step1_tb = gr.Textbox(label="step1")
    step2_tb = gr.Textbox(label="step2")
    step_out_tb = gr.Textbox(label="output_demo")

    add_btn = gr.Button("直接拼接", variant="primary", elem_classes=["tool"])
    add_btn.click(fn=lambda x:x,
                      inputs=[step1_tb], outputs=[step1_tb],
                ).success(
                    fn=lambda x:x,
                    inputs=[step2_tb], outputs=[step2_tb],
                ).then(
                    fn=lambda x,y:x+"  "+y,
                    inputs=[step1_tb, step2_tb], outputs=[step_out_tb],
                )
    add_and_check_btn = gr.Button("全部存在才相加", variant="secondary", elem_classes=["tool"])

    def empty(x):
        if not x:
            raise gr.Error("input is empty")
        return x
    
    def happen_bad(x, y):
        if not x or not y:
            raise gr.Error("step1 or step1 is empty")
        return x+y
    add_and_check_btn.click(fn=empty,
                      inputs=[step1_tb], outputs=[step1_tb],
                ).success(
                    fn=empty,
                    inputs=[step2_tb], outputs=[step2_tb],
                ).success(
                    fn=happen_bad,
                    inputs=[step1_tb, step2_tb], outputs=[step_out_tb],
                )


demo.launch(server_name="0.0.0.0", server_port=1234, inbrowser=True)
