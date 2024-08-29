import gradio as gr

js = "(x) => confirm('Are you sure?')"

with gr.Blocks() as demo:
    btn = gr.Button()
    hidden_checkbox = gr.Checkbox(visible=False)
    textbox = gr.Textbox()
    num = gr.Number(visible=False)
    
    def hidden_checkbox_fn(checkbox_state, number):
        if checkbox_state:
            number += 1
        display = f'confirmed {number} times'
        return False, display, number
        
    btn.click(None, None, hidden_checkbox, js=js)
    hidden_checkbox.change(hidden_checkbox_fn, [hidden_checkbox, num], [hidden_checkbox, textbox, num])
    
demo.launch(server_name="0.0.0.0", server_port=1234, inbrowser=True)
