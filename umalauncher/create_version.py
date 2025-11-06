import pyinstaller_versionfile
import version

def generate():
    pyinstaller_versionfile.create_versionfile(
        output_file="version.rc",
        version=version.VERSION,
        file_description="Uma Launcher",
        internal_name="Uma Launcher",
        original_filename="UmaLauncher.exe",
        product_name="Uma Launcher"
    )
    # Global release
    pyinstaller_versionfile.create_versionfile(
        output_file="version_global.rc",
        version=version.VERSION,
        file_description="Uma Launcher (Global)",
        internal_name="Uma Launcher (Global)",
        original_filename="UmaLauncher (Global).exe",
        product_name="Uma Launcher (Global)"
    )
    # Steam JP release
    pyinstaller_versionfile.create_versionfile(
        output_file="version_jp_steam.rc",
        version=version.VERSION,
        file_description="Uma Launcher (Steam)",
        internal_name="Uma Launcher (Steam)",
        original_filename="UmaLauncher (Steam).exe",
        product_name="Uma Launcher (Steam)"
    )

if __name__ == "__main__":
    generate()
