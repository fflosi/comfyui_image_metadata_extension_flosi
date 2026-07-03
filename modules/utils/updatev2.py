import json
import os

def add_prompt_node_name_input(file_path, output_path=None):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    modified = False

    for node in data.get("nodes", []):
        if node.get("type") == "SaveImageWithMetaDataV2":
            # Check if input named "Prompt_node_name" exists
            input_names = [inp["name"] for inp in node.get("inputs", [])]
            if "Prompt_node_name" not in input_names:
                # Find index to insert — after "output_format" (common order)
                inputs = node["inputs"]
                insert_index = next(
                    (i for i, inp in enumerate(inputs) if inp["name"] == "quality"),
                    len(inputs)
                )

                # Insert new input definition
                new_input = {
                    "localized_name": "Prompt_node_name",
                    "name": "Prompt_node_name",
                    "type": "STRING",
                    "widget": {"name": "Prompt_node_name"},
                    "link": None
                }
                inputs.insert(insert_index, new_input)

                # Update widgets_values
                # Only count inputs with widgets for the widget insert index
                widget_insert_index = sum(1 for i, inp in enumerate(inputs[:insert_index]) if "widget" in inp)
                widgets = node.get("widgets_values", [])
                if widget_insert_index <= len(widgets):
                    widgets.insert(widget_insert_index, "auto")
                else:
                    # In case widgets_values is shorter than widget inputs
                    widgets.append("auto")

                modified = True

    if modified:
        out_path = output_path or file_path
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"File updated: {out_path}")
    else:
        print("No changes made; all nodes already have 'Prompt_node_name'.")

def process_directory(directory_path):
    """Process all JSON files in a directory that start with a letter or number."""
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return
    
    processed_count = 0
    
    for filename in os.listdir(directory_path):
        # Check if file has .json extension and starts with letter or number
        if filename.endswith('.json') and filename[0].isalnum():
            file_path = os.path.join(directory_path, filename)
            print(f"Processing: {filename}")
            
            try:
                add_prompt_node_name_input(file_path)
                processed_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    print(f"Processed {processed_count} files in directory: {directory_path}")

# Example usage:
# Process a single file:
# add_prompt_node_name_input(r'V:\StabilityMatrix\Data\Packages\ComfyUI-Zluda\user\default\workflows\tiled-diffusion-example.json')

# Process all valid JSON files in a directory:
process_directory(r'V:\StabilityMatrix\Data\Packages\ComfyUI-Zluda\user\default\workflows')
