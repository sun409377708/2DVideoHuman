import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

if __name__ == "__main__":
    print("Starting test server...")
    demo.launch(server_name="127.0.0.1", server_port=7861)
