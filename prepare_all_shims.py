import xml.etree.ElementTree as ET
import os
import shutil

# This should be the absolute path to your 'master' shim or relative to where you run the script
ROOT_SHIM_SOURCE = os.path.abspath("AICCShim.html")

def get_start_file(manifest_path):
    """Parses the manifest to find the href of the first item."""
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        ns_url = root.tag.split('}')[0].strip('{') if '}' in root.tag else ""
        ns = {'imscp': ns_url}
        
        item = root.find(".//imscp:item[@identifierref]", ns)
        if item is not None:
            res_id = item.get("identifierref")
            resource = root.find(f".//imscp:resource[@identifier='{res_id}']", ns)
            if resource is not None:
                return resource.get("href")
    except Exception as e:
        print(f"      [!] Error parsing {manifest_path}: {e}")
    return None

def process_all_folders(root_dir="."):
    if not os.path.exists(ROOT_SHIM_SOURCE):
        print(f"Critical Error: Master shim not found at {ROOT_SHIM_SOURCE}")
        return

    print(f"Scanning directories starting from: {os.path.abspath(root_dir)}")
    
    # os.walk travels through every subfolder
    for subdir, dirs, files in os.walk(root_dir):
        # If we find a manifest, we assume it's a SCORM course folder
        if "imsmanifest.xml" in files:
            manifest_path = os.path.join(subdir, "imsmanifest.xml")
            target_shim_path = os.path.join(subdir, "AICCShim.html")
            
            print(f"--- Found SCORM Course: {subdir}")
            
            # 1. Copy the AICCShim.html from root to this subfolder
            try:
                shutil.copy2(ROOT_SHIM_SOURCE, target_shim_path)
                print(f"      [+] Copied AICCShim.html to folder.")
            except Exception as e:
                print(f"      [!] Failed to copy shim to {subdir}: {e}")
                continue

            # 2. Identify the launch file
            start_file = get_start_file(manifest_path)
            if not start_file:
                print(f"      [?] Skipping Replacement: No launch file found in manifest.")
                continue

            # 3. Perform the placeholder replacement in the COPIED file
            try:
                with open(target_shim_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if "STARTING_RESOURCE" in content:
                    updated_content = content.replace("STARTING_RESOURCE", start_file)
                    with open(target_shim_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"      [✓] Updated shim to launch: {start_file}")
                else:
                    print(f"      [!] Warning: Placeholder 'STARTING_RESOURCE' missing in {target_shim_path}")
            except Exception as e:
                print(f"      [!] Error modifying {target_shim_path}: {e}")

if __name__ == "__main__":
    process_all_folders(".")
