import argparse
import glob
import hashlib
import os
import platform
import re
import site
import subprocess
import sys

script_dir = os.getcwd()
conda_env_path = os.path.join("../text-generation-webui", "installer_files", "env")
print("Conda environment path:", conda_env_path)
# Remove the '# ' from the following lines as needed for your AMD GPU on Linux
# os.environ["ROCM_PATH"] = '/opt/rocm'
# os.environ["HSA_OVERRIDE_GFX_VERSION"] = '10.3.0'
# os.environ["HCC_AMDGPU_TARGET"] = 'gfx1030'


def is_linux():
    return sys.platform.startswith("linux")


def is_windows():
    return sys.platform.startswith("win")


def is_macos():
    return sys.platform.startswith("darwin")


def is_x86_64():
    return platform.machine() == "x86_64"


def cpu_has_avx2():
    try:
        import cpuinfo

        info = cpuinfo.get_cpu_info()
        if 'avx2' in info['flags']:
            return True
        else:
            return False
    except:
        return True


def cpu_has_amx():
    try:
        import cpuinfo

        info = cpuinfo.get_cpu_info()
        if 'amx' in info['flags']:
            return True
        else:
            return False
    except:
        return True


def torch_version():
    site_packages_path = None
    for sitedir in site.getsitepackages():
        if "site-packages" in sitedir and conda_env_path in sitedir:
            site_packages_path = sitedir
            break

    if site_packages_path:
        torch_version_file = open(os.path.join(site_packages_path, 'torch', 'version.py')).read().splitlines()
        torver = [line for line in torch_version_file if '__version__' in line][0].split('__version__ = ')[1].strip("'")
    else:
        from torch import __version__ as torver
    return torver


def is_installed():
    site_packages_path = None
    for sitedir in site.getsitepackages():
        if "site-packages" in sitedir and conda_env_path in sitedir:
            site_packages_path = sitedir
            break

    if site_packages_path:
        return os.path.isfile(os.path.join(site_packages_path, 'torch', '__init__.py'))
    else:
        return os.path.isdir(conda_env_path)


def check_env():
    # If we have access to conda, we are probably in an environment
    conda_exist = run_cmd("conda", environment=True, capture_output=True).returncode == 0
    if not conda_exist:
        print("Conda is not installed. Exiting...")
        sys.exit(1)

    # Ensure this is a new environment and not the base environment
    if os.environ["CONDA_DEFAULT_ENV"] == "base":
        print("Create an environment for this project and activate it. Exiting...")
        sys.exit(1)


def clear_cache():
    run_cmd("conda clean -a -y", environment=True)
    run_cmd("python -m pip cache purge", environment=True)


def print_big_message(message):
    message = message.strip()
    lines = message.split('\n')
    print("\n\n*******************************************************************")
    for line in lines:
        if line.strip() != '':
            print("*", line)

    print("*******************************************************************\n\n")


def calculate_file_hash(file_path):
    p = os.path.join(script_dir, file_path)
    if os.path.isfile(p):
        with open(p, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    else:
        return ''


def run_cmd(cmd, assert_success=False, environment=False, capture_output=False, env=None):
    # Use the conda environment
    if environment:
        if is_windows():
            conda_bat_path = os.path.join(script_dir, "installer_files", "conda", "condabin", "conda.bat")
            cmd = "\"" + conda_bat_path + "\" activate \"" + conda_env_path + "\" >nul && " + cmd
        else:
            conda_sh_path = os.path.join(script_dir, "installer_files", "conda", "etc", "profile.d", "conda.sh")
            cmd = ". \"" + conda_sh_path + "\" && conda activate \"" + conda_env_path + "\" && " + cmd

    # Run shell commands
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, env=env)

    # Assert the command ran successfully
    if assert_success and result.returncode != 0:
        print("Command '" + cmd + "' failed with exit status code '" + str(result.returncode) + "'.\n\nExiting now.\nTry running the start/update script again.")
        sys.exit(1)

    return result


def update_requirements(initial_installation=False):
    # Create .git directory if missing
    if not os.path.isdir(os.path.join(script_dir, ".git")):
        git_creation_cmd = 'git init -b main && git remote add origin https://github.com/oobabooga/text-generation-webui && git fetch && git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/main && git reset --hard origin/main && git branch --set-upstream-to=origin/main'
        run_cmd(git_creation_cmd, environment=True, assert_success=True)

    files_to_check = [
        'start_linux.sh', 'start_macos.sh', 'start_windows.bat', 'start_wsl.bat',
        'update_linux.sh', 'update_macos.sh', 'update_windows.bat', 'update_wsl.bat',
        'one_click.py'
    ]

    before_pull_hashes = {file_name: calculate_file_hash(file_name) for file_name in files_to_check}
    run_cmd("git pull --autostash", assert_success=True, environment=True)
    after_pull_hashes = {file_name: calculate_file_hash(file_name) for file_name in files_to_check}

    # Check for differences in installation file hashes
    for file_name in files_to_check:
        if before_pull_hashes[file_name] != after_pull_hashes[file_name]:
            print_big_message(f"File '{file_name}' was updated during 'git pull'. Please run the script again.")
            exit(1)

    # Extensions requirements are installed only during the initial install by default.
    # That can be changed with the INSTALL_EXTENSIONS environment variable.
    install = initial_installation
    if "INSTALL_EXTENSIONS" in os.environ:
        install = os.environ["INSTALL_EXTENSIONS"].lower() in ("yes", "y", "true", "1", "t", "on")

    if install:
        print_big_message("Installing extensions requirements.")
        extensions = next(os.walk("extensions"))[1]
        for extension in extensions:
            if extension in ['superbooga', 'superboogav2']:  # No wheels available for requirements
                continue

            extension_req_path = os.path.join("extensions", extension, "requirements.txt")
            if os.path.exists(extension_req_path):
                run_cmd("python -m pip install -r " + extension_req_path + " --upgrade", assert_success=True, environment=True)
    elif initial_installation:
        print_big_message("Will not install extensions due to INSTALL_EXTENSIONS environment variable.")

    # Detect the Python and PyTorch versions
    torver = torch_version()
    print(f"TORCH: {torver}")
    is_cuda = '+cu' in torver
    is_cuda118 = '+cu118' in torver  # 2.1.0+cu118
    is_cuda117 = '+cu117' in torver  # 2.0.1+cu117
    is_rocm = '+rocm' in torver  # 2.0.1+rocm5.4.2
    is_intel = '+cxx11' in torver  # 2.0.1a0+cxx11.abi
    is_cpu = '+cpu' in torver  # 2.0.1+cpu

    if is_rocm:
        if cpu_has_avx2():
            requirements_file = "requirements_amd.txt"
        else:
            requirements_file = "requirements_amd_noavx2.txt"
    elif is_cpu:
        if cpu_has_avx2():
            requirements_file = "requirements_cpu_only.txt"
        else:
            requirements_file = "requirements_cpu_only_noavx2.txt"
    elif is_macos():
        if is_x86_64():
            requirements_file = "requirements_apple_intel.txt"
        else:
            requirements_file = "requirements_apple_silicon.txt"
    else:
        if cpu_has_avx2():
            requirements_file = "requirements.txt"
        else:
            requirements_file = "requirements_noavx2.txt"

    # Prepare the requirements file
    print_big_message(f"Installing webui requirements from file: {requirements_file}")
    textgen_requirements = open(requirements_file).read().splitlines()
    if is_cuda117:
        textgen_requirements = [req.replace('+cu121', '+cu117').replace('+cu122', '+cu117').replace('torch2.1', 'torch2.0') for req in textgen_requirements]
    elif is_cuda118:
        textgen_requirements = [req.replace('+cu121', '+cu118').replace('+cu122', '+cu118') for req in textgen_requirements]
    if is_windows() and (is_cuda117 or is_cuda118):  # No flash-attention on Windows for CUDA 11
        textgen_requirements = [req for req in textgen_requirements if 'bdashore3/flash-attention' not in req]

    with open('temp_requirements.txt', 'w') as file:
        file.write('\n'.join(textgen_requirements))

    # Workaround for git+ packages not updating properly.
    git_requirements = [req for req in textgen_requirements if req.startswith("git+")]
    for req in git_requirements:
        url = req.replace("git+", "")
        package_name = url.split("/")[-1].split("@")[0].rstrip(".git")
        run_cmd("python -m pip uninstall -y " + package_name, environment=True)
        print(f"Uninstalled {package_name}")

    # Make sure that API requirements are installed (temporary)
    extension_req_path = os.path.join("extensions", "openai", "requirements.txt")
    if os.path.exists(extension_req_path):
        run_cmd("python -m pip install -r " + extension_req_path + " --upgrade", environment=True)

    # Install/update the project requirements
    run_cmd("python -m pip install -r temp_requirements.txt --upgrade", assert_success=True, environment=True)
    os.remove('temp_requirements.txt')

    # Check for '+cu' or '+rocm' in version string to determine if torch uses CUDA or ROCm. Check for pytorch-cuda as well for backwards compatibility
    if not any((is_cuda, is_rocm)) and run_cmd("conda list -f pytorch-cuda | grep pytorch-cuda", environment=True, capture_output=True).returncode == 1:
        clear_cache()
        return

    if not os.path.exists("repositories/"):
        os.mkdir("repositories")

    os.chdir("repositories")

    # Install or update ExLlama as needed
    if not os.path.exists("exllama/"):
        run_cmd("git clone https://github.com/turboderp/exllama.git", environment=True)
    else:
        os.chdir("exllama")
        run_cmd("git pull", environment=True)
        os.chdir("..")

    if is_linux():
        # Fix JIT compile issue with ExLlama in Linux/WSL
        if not os.path.exists(f"{conda_env_path}/lib64"):
            run_cmd(f'ln -s "{conda_env_path}/lib" "{conda_env_path}/lib64"', environment=True)

        # On some Linux distributions, g++ may not exist or be the wrong version to compile GPTQ-for-LLaMa
        gxx_output = run_cmd("g++ -dumpfullversion -dumpversion", environment=True, capture_output=True)
        if gxx_output.returncode != 0 or int(gxx_output.stdout.strip().split(b".")[0]) > 11:
            # Install the correct version of g++
            run_cmd("conda install -y -k conda-forge::gxx_linux-64=11.2.0", environment=True)

    clear_cache()


if __name__ == "__main__":
    # Verifies we are in a conda environment
    check_env()

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--update', action='store_true', help='Update the web UI.')
    args, _ = parser.parse_known_args()

    if args.update:
        update_requirements()
    else:

        if os.environ.get("LAUNCH_AFTER_INSTALL", "").lower() in ("no", "n", "false", "0", "f", "off"):
            print_big_message("Install finished successfully and will now exit due to LAUNCH_AFTER_INSTALL.")
            sys.exit()

        # Workaround for llama-cpp-python loading paths in CUDA env vars even if they do not exist
        conda_path_bin = os.path.join(conda_env_path, "bin")
        if not os.path.exists(conda_path_bin):
            os.mkdir(conda_path_bin)
