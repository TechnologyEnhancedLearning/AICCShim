import xml.etree.ElementTree as ET
import os

def prepare_scorm_shim(manifest_path="imsmanifest.xml", shim_path="AICCShim.html"):
    # Ensure both files are present in the current folder
    if not os.path.exists(manifest_path):
        print(f"Error: {manifest_path} not found.")
        return
    if not os.path.exists(shim_path):
        print(f"Error: {shim_path} not found.")
        return

    try:
        # 1. Extract the starting resource from imsmanifest.xml
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        
        # SCORM uses namespaces. Extract the default one to search correctly.
        ns_url = root.tag.split('}')[0].strip('{') if '}' in root.tag else ""
        ns = {'imscp': ns_url}
        
        # Find the first <item> with a resource reference
        item = root.find(".//imscp:item[@identifierref]", ns)
        if item is None:
            print("Error: No starting <item> found in the manifest.")
            return
            
        res_id = item.get("identifierref")
        
        # Find the <resource> that matches that ID to get the file path (href)
        resource = root.find(f".//imscp:resource[@identifier='{res_id}']", ns)
        if resource is None or not resource.get("href"):
            print(f"Error: Could not find launch file (href) for resource '{res_id}'.")
            return
            
        start_file = resource.get("href")
        print(f"Detected starting resource: {start_file}")

        # 2. Update the AICCShim.html file
        with open(shim_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        if "STARTING_RESOURCE" not in html_content:
            print("Warning: Placeholder 'STARTING_RESOURCE' not found in AICCShim.html.")
            print("It may have already been replaced or is missing from the file.")
            return
            
        # Replace the placeholder with the actual file path
        updated_html = html_content.replace("STARTING_RESOURCE", start_file)
        
        with open(shim_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)
            
        print(f"Successfully updated {shim_path} to launch: {start_file}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    prepare_scorm_shim()
