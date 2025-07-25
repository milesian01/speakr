from pathlib import Path
import subprocess

class AudioConversionError(Exception):
    """Raised when an audio conversion operation fails."""
    pass

def convert_to_flac(input_path):
    """Convert an audio file to FLAC format.

    Parameters
    ----------
    input_path : str or Path
        Path to the source audio file.

    Returns
    -------
    Path
        Path to the converted FLAC file.
    """
    path = Path(input_path)
    base = path.with_suffix('')
    temp_path = base.with_suffix('.temp.flac')
    final_path = base.with_suffix('.flac')

    try:
        subprocess.run(
            [
                'ffmpeg', '-i', str(path), '-y',
                '-acodec', 'flac', '-ar', '16000', '-ac', '1',
                str(temp_path)
            ],
            check=True, capture_output=True, text=True
        )
    except FileNotFoundError as exc:
        raise AudioConversionError('ffmpeg command not found.') from exc
    except subprocess.CalledProcessError as exc:
        raise AudioConversionError(f"ffmpeg conversion failed: {exc.stderr}") from exc

    if str(path).lower() != str(final_path).lower():
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    temp_path.rename(final_path)
    return final_path
