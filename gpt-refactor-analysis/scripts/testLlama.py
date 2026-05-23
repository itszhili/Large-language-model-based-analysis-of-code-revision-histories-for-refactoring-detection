from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(model_name="./llama2-7b"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return model, tokenizer

def ask_question(question, model, tokenizer):
    input_ids = tokenizer.encode(question, return_tensors="pt")
    
    # Generate a response to the question
    output = model.generate(input_ids, max_length=100, num_return_sequences=1)
    
    reply = tokenizer.decode(output[0], skip_special_tokens=True)
    return reply

# Load the model
model, tokenizer = load_model()

# Ask a question
question = "What is the capital of France?"
reply = ask_question(question, model, tokenizer)

print(f"Question: {question}\nAnswer: {reply}")


