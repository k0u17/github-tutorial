import re
import base64
import os
import sys

def compile_markdown(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
        
    dir_path = os.path.dirname(os.path.abspath(input_file))
    
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    def replace_img(match):
        alt_text = match.group(1)
        img_name = match.group(2)
        
        # If it's already a Data URI, skip it
        if img_name.startswith("data:"):
            return match.group(0)
            
        img_path = os.path.join(dir_path, img_name)
        if os.path.exists(img_path):
            ext = os.path.splitext(img_name)[1].lower().replace(".", "")
            mime_type = f"image/{ext}"
            if ext == "jpg" or ext == "jpeg":
                mime_type = "image/jpeg"
            elif ext == "svg":
                mime_type = "image/svg+xml"
                
            with open(img_path, "rb") as img_file:
                b64_data = base64.b64encode(img_file.read()).decode("utf-8")
            return f"![{alt_text}](data:{mime_type};base64,{b64_data})"
        else:
            print(f"Warning: Image file '{img_name}' not found at '{img_path}'. Skipping.")
            return match.group(0)
            
    # Pattern to match ![alt](path/to/image.png) but NOT http:// or https:// URLs
    pattern = r"!\[(.*?)\]\(((?!http://|https://)([^)]+))\)"
    new_content = re.sub(pattern, replace_img, content)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"Successfully compiled '{input_file}' -> '{output_file}' with embedded Base64 images.")

if __name__ == "__main__":
    # Default input/output paths
    input_file = "github_tutorial.md"
    output_file = "github_tutorial_compiled.md"
    
    # Use arguments if provided
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        
    # Get absolute paths relative to current script directory if relative paths are provided
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not os.path.isabs(input_file):
        input_file = os.path.join(script_dir, input_file)
    if not os.path.isabs(output_file):
        output_file = os.path.join(script_dir, output_file)
        
    compile_markdown(input_file, output_file)
