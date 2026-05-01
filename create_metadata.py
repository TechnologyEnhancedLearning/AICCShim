import xml.etree.ElementTree as ET
import os

def generate_aicc_from_scorm(manifest_path, output_dir="aicc_output"):
    # 1. Parse the manifest and handle namespaces
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    ns = {'imscp': 'http://imsglobal.org',
          'adlcp': 'http://adlnet.org'} # Common namespaces

    # 2. Extract basic information
    course_id = root.get('identifier', 'COURSE_001')
    title_elem = root.find('.//imscp:title', ns)
    title = title_elem.text if title_elem is not None else "Untitled Course"
    
    # Extract the main launch file from the first resource
    resource = root.find('.//imscp:resource', ns)
    launch_file = resource.get('href', 'index.html') if resource is not None else 'index.html'

    # 3. Create the output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 4. Generate the 4 AICC Files
    base_name = os.path.join(output_dir, course_id)

    # .CRS (Course Description)
    with open(f"{base_name}.crs", "w") as f:
        f.write("[Course]\n")
        f.write(f"Course_ID={course_id}\n")
        f.write(f"Course_Title={title}\n")
        f.write("Level=1\nCourse_Creator=PythonScript\n")
        f.write("[Course_Description]\nGenerated from SCORM manifest.\n")

    # .DES (Descriptor)
    with open(f"{base_name}.des", "w") as f:
        f.write('"System_ID","Type","Developer_ID","Title","Description"\n')
        f.write(f'"A1","AU","{course_id}","{title}","Main Course Unit"\n')

    # .AU (Assignable Unit)
    with open(f"{base_name}.au", "w") as f:
        f.write('"System_ID","Type","Command_Line","File_Name","Max_Score","Mastery_Score"\n')
        f.write(f'"A1","","","{launch_file}","100","80"\n')

    # .CST (Course Structure)
    with open(f"{base_name}.cst", "w") as f:
        f.write('"Block","Member"\n')
        f.write(f'"{course_id}","A1"\n')

    print(f"✅ AICC files generated in '{output_dir}'")

if __name__ == "__main__":
    # Ensure 'imsmanifest.xml' is in the same folder as this script
    generate_aicc_from_scorm("imsmanifest.xml")

