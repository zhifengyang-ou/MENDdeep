import os
import shutil
import sys
from datetime import datetime

now_string = str(datetime.now())
comment = sys.argv[1]

filename = 'MEND_namelist.nml'
filename2 = 'FBEM_namelist.nml'
folder = ''

with open(filename, 'r') as file:
    for line in file:
        line = line.strip()
        if 'Dir_Output  = ' in line:
            folder = line.split('=')[1].strip().replace("'", '').replace('/', '\\')

if folder:
    os.makedirs(folder, exist_ok=True)

logfile = 'log.txt'
with open(logfile, 'r') as log_file, open(os.path.join(folder, logfile), 'w') as output_file:
    for line in log_file:
        output_file.write(line)

with open(os.path.join(folder, logfile), 'a') as output_file:
    output_file.write(folder + '\n')
    output_file.write(now_string + '\n')

shutil.copy(os.path.join(folder, logfile), 'log.txt')
with open(os.path.join(folder, 'comment.txt'), 'w') as comment_file:
    comment_file.write(comment)

shutil.copy(filename, os.path.join(folder, 'MEND_namelist.nml'))
shutil.copy(filename2, os.path.join(folder, 'FBEM_namelist.nml'))

# --- NEW CODE ADDED HERE ---
# This will copy all files from 'src' into 'folder/src'
if os.path.exists('src'):
    shutil.copytree('src', os.path.join(folder, 'src'), dirs_exist_ok=True)

# if os.path.exists('userio/inp'):
#     shutil.copytree('userio/inp', os.path.join(folder, 'inp'), dirs_exist_ok=True)
# ---------------------------

# File paths with backslashes for Windows
FSRCS = [
    "src\\MOD_Photosynthesis.F90",
    "src\\MOD_MEND_TYPE.F90",
    "src\\MOD_OPT_TYPE.F90",
    "src\\MOD_USRFS.F90",
    "src\\MOD_STRING.F90",
    "src\\MOD_MEND.F90",
    "src\\MOD_MCMC.F90",
    "src\\MOD_OPT.F90",
    "src\\MEND_IN.F90",
    "src\\MEND_main.F90"
]

# Aggressive optimization flags
OPTFLAGS = "-O3 -march=native -funroll-loops"
MATH_TUNE = "-ffast-math -fassociative-math -freciprocal-math -fno-signed-zeros"
F90_FLAGS = "-fallow-argument-mismatch -fimplicit-none"
CPPFLAGS = "-cpp"

if comment == "fast":
    print("Use previous program, no compilation")
else:
    # Build process
    os.makedirs("build", exist_ok=True)
    os.makedirs("include", exist_ok=True)  # Create include directory to prevent warnings

    # Change working directory to ensure proper file paths
    original_dir = os.getcwd()
    os.chdir("src")

    # Compile each source file separately
    object_files = []
    print("🚀 Starting maximum-optimization build...")
    for src_file in FSRCS:
        base_name = os.path.basename(src_file)
        obj_file = f"../build/{base_name.replace('.F90', '.o')}"
        compile_cmd = (
            f"gfortran -c {base_name} "
            f"{OPTFLAGS} {MATH_TUNE} {F90_FLAGS} {CPPFLAGS} "
            f"-J../build -I../include -o {obj_file}"
        )
        print(f"🔧 Compiling: {base_name}")
        if os.system(compile_cmd) != 0:
            print(f"❌ Compilation failed for {base_name}!")
            sys.exit(1)
        object_files.append(obj_file)

    # Link all object files
    link_cmd = (
        f"gfortran {' '.join(object_files)} {OPTFLAGS} -o ../nws.exe "
        f"-static-libgcc -static-libgfortran"
    )
    print(f"🔗 Link command: {link_cmd}")
    if os.system(link_cmd) != 0:
        print("❌ Linking failed!")
        sys.exit(1)
    os.chdir(original_dir)

os.system("nws.exe")

# Cleanup
print("🧹 Cleaning build artifacts...")
for f in os.listdir():
    if f.endswith((".o", ".mod")):
        os.remove(f)