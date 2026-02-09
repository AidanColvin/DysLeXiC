from datasets import load_dataset
from transformers import BartTokenizer, BartForConditionalGeneration, Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq

dataset = load_dataset("json", data_files="standardized_training_data.jsonl", split="train").train_test_split(test_size=0.05)

tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")

def preprocess(examples):
    inputs = tokenizer(examples["original_text"], max_length=64, truncation=True, padding="max_length")
    labels = tokenizer(text_target=examples["corrected_text"], max_length=64, truncation=True, padding="max_length")
    inputs["labels"] = labels["input_ids"]
    return inputs

tokenized_data = dataset.map(preprocess, batched=True)

args = Seq2SeqTrainingArguments(
    output_dir="./bart-neuro-read",
    per_device_train_batch_size=8,
    predict_with_generate=True,
    fp16=False, # Set to True if you have a GPU
    num_train_epochs=1, # Start with 1 to verify it works
    logging_steps=100,
    save_strategy="no"
)

trainer = Seq2SeqTrainer(
    model=model,
    args=args,
    train_dataset=tokenized_data["train"],
    eval_dataset=tokenized_data["test"],
    tokenizer=tokenizer,
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model)
)

trainer.train()
model.save_pretrained("./fine_tuned_bart")
tokenizer.save_pretrained("./fine_tuned_bart")
