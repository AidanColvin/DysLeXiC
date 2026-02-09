import json
from datasets import load_dataset
from transformers import BartTokenizer, BartForConditionalGeneration, Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq

# 1. Load your standardized data
dataset = load_dataset("json", data_files="standardized_training_data.jsonl", split="train")
dataset = dataset.train_test_split(test_size=0.1)  # Use 10% for validation

model_name = "facebook/bart-base"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def preprocess_function(examples):
    inputs = [ex for ex in examples["original_text"]]
    targets = [ex for ex in examples["corrected_text"]]
    model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
    
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# 2. Tokenize data
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# 3. Training Arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./bart-neuro-read",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=3,
    predict_with_generate=True,
    logging_steps=10,
    push_to_hub=False,
    report_to="none"
)

# 4. Initialize Trainer
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
)

# 5. Start Training
print("Starting training...")
trainer.train()

# 6. Save the model
model.save_pretrained("./neuro-read-model")
tokenizer.save_pretrained("./neuro-read-model")
print("Model saved to ./neuro-read-model")
